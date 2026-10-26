"""Axial-tensor reanalysis of Table I; no electronic-structure calculation."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


METHODS = ("experiment", "lda_no_core", "hse06_core")
ISOTOPES = ("13C", "29Si")
METHOD_LABELS = {
    "experiment": "Experiment",
    "lda_no_core": "LDA, no core polarization",
    "hse06_core": "HSE06, with core polarization",
}


def _finite(value: object, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite number, not bool")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def axial_tensor(
    a_parallel: float, a_perp: float, theta_deg: float = 0.0, phi_deg: float = 0.0
) -> np.ndarray:
    """Place an axial tensor in a chosen frame whose z axis is defect [111].

    theta is the polar angle of its parallel axis. phi is a coordinate choice,
    not an azimuth measured or inferred from the paper's Table I.
    """
    parallel = _finite(a_parallel, "parallel constant")
    perpendicular = _finite(a_perp, "perpendicular constant")
    theta = _finite(theta_deg, "theta")
    phi = _finite(phi_deg, "phi")
    if not 0.0 <= theta <= 180.0 or not 0.0 <= phi < 360.0:
        raise ValueError("Need 0 <= theta <= 180 and 0 <= phi < 360 degrees")
    t, p = np.deg2rad([theta, phi])
    axis = np.array([np.sin(t) * np.cos(p), np.sin(t) * np.sin(p), np.cos(t)])
    tensor = perpendicular * np.eye(3) + (parallel - perpendicular) * np.outer(axis, axis)
    if not np.all(np.isfinite(tensor)):
        raise ValueError("Tensor calculation overflowed")
    return tensor


def decompose_tensor(tensor: np.ndarray) -> tuple[float, np.ndarray]:
    """Return the isotropic scalar and symmetric traceless anisotropic part."""
    matrix = np.asarray(tensor, dtype=float)
    if matrix.shape != (3, 3) or not np.all(np.isfinite(matrix)):
        raise ValueError("Tensor must be a finite 3 by 3 array")
    if not np.allclose(matrix, matrix.T, rtol=0.0, atol=1e-12):
        raise ValueError("This exercise expects a real symmetric hyperfine tensor")
    isotropic = float(np.trace(matrix) / 3.0)
    return isotropic, matrix - isotropic * np.eye(3)


def tensor_metrics(tensor: np.ndarray) -> dict:
    isotropic, anisotropic = decompose_tensor(tensor)
    eigenvalues = np.linalg.eigvalsh(np.asarray(tensor, dtype=float))
    return {
        "a_iso_MHz": isotropic,
        "anisotropic_frobenius_norm_MHz": float(np.linalg.norm(anisotropic, ord="fro")),
        "anisotropic_trace_MHz": float(np.trace(anisotropic)),
        "principal_values_MHz": eigenvalues.tolist(),
        "principal_span_MHz": float(eigenvalues[-1] - eigenvalues[0]),
    }


def compute(config: dict, out_dir: Path) -> dict:
    convention = config["coordinate_convention"]
    phi = _finite(convention["phi_deg"], "illustrative phi")
    if phi != 0.0:
        raise ValueError("This configured illustration fixes phi = 0 degrees; it is not measured")
    inputs = config["rows"]
    if not isinstance(inputs, list) or len(inputs) != 6:
        raise ValueError("Supply the six Table I isotope/method rows")
    rows = {}
    for item in inputs:
        key = (item["isotope"], item["method"])
        if key[0] not in ISOTOPES or key[1] not in METHODS or key in rows:
            raise ValueError("Require unique rows for 13C and 29Si, each with experiment/LDA/HSE06")
        parallel = _finite(item["a_parallel_MHz"], "parallel constant")
        perpendicular = _finite(item["a_perp_MHz"], "perpendicular constant")
        theta = _finite(item["theta_deg"], "theta")
        tensor = axial_tensor(parallel, perpendicular, theta, phi)
        rows[key] = {
            "isotope": key[0], "method": key[1],
            "a_parallel_MHz": parallel, "a_perp_MHz": perpendicular,
            "theta_deg": theta, "phi_deg": phi,
            "tensor": tensor, **tensor_metrics(tensor),
        }
    expected = {(isotope, method) for isotope in ISOTOPES for method in METHODS}
    if set(rows) != expected:
        raise ValueError("Missing isotope/method combinations")

    rotation_angle = 0.371
    cosine, sine = math.cos(rotation_angle), math.sin(rotation_angle)
    rotation = np.array([[cosine, -sine, 0.0], [sine, cosine, 0.0], [0.0, 0.0, 1.0]])
    eigenvalue_errors, scalar_errors, anisotropic_traces = [], [], []
    rotation_eigenvalue_errors, rotation_trace_errors, rotation_norm_errors = [], [], []
    comparisons = {}
    output_rows = []
    tensor_rows = []
    for isotope in ISOTOPES:
        reference = rows[(isotope, "experiment")]
        reference_values = [reference["a_parallel_MHz"], reference["a_perp_MHz"], reference["a_iso_MHz"]]
        if any(value == 0.0 for value in reference_values):
            raise ValueError("Experimental constants and isotropic scalar must be nonzero for percentage errors")
        comparisons[isotope] = {}
        for method in METHODS:
            row = rows[(isotope, method)]
            tensor = row["tensor"]
            expected_eigenvalues = np.sort([row["a_parallel_MHz"], row["a_perp_MHz"], row["a_perp_MHz"]])
            eigenvalue_errors.append(float(np.max(np.abs(np.asarray(row["principal_values_MHz"]) - expected_eigenvalues))))
            scalar_errors.append(abs(row["a_iso_MHz"] - (row["a_parallel_MHz"] + 2.0 * row["a_perp_MHz"]) / 3.0))
            anisotropic_traces.append(abs(row["anisotropic_trace_MHz"]))
            rotated = tensor_metrics(rotation @ tensor @ rotation.T)
            rotation_eigenvalue_errors.append(float(np.max(np.abs(np.asarray(rotated["principal_values_MHz"]) - np.asarray(row["principal_values_MHz"])))))
            rotation_trace_errors.append(abs(rotated["a_iso_MHz"] - row["a_iso_MHz"]))
            rotation_norm_errors.append(abs(rotated["anisotropic_frobenius_norm_MHz"] - row["anisotropic_frobenius_norm_MHz"]))
            errors = {
                "parallel_signed_error_MHz": row["a_parallel_MHz"] - reference["a_parallel_MHz"],
                "perp_signed_error_MHz": row["a_perp_MHz"] - reference["a_perp_MHz"],
                "iso_signed_error_MHz": row["a_iso_MHz"] - reference["a_iso_MHz"],
                "theta_signed_error_deg": row["theta_deg"] - reference["theta_deg"],
            }
            errors["parallel_relative_error_percent"] = 100.0 * errors["parallel_signed_error_MHz"] / reference["a_parallel_MHz"]
            errors["perp_relative_error_percent"] = 100.0 * errors["perp_signed_error_MHz"] / reference["a_perp_MHz"]
            errors["iso_relative_error_percent"] = 100.0 * errors["iso_signed_error_MHz"] / reference["a_iso_MHz"]
            errors["principal_value_mae_MHz"] = (abs(errors["parallel_signed_error_MHz"]) + 2.0 * abs(errors["perp_signed_error_MHz"])) / 3.0
            scalar_output = {key: value for key, value in row.items() if key not in {"tensor", "principal_values_MHz"}}
            output_rows.append({**scalar_output, **errors})
            comparisons[isotope][method] = {
                "a_parallel_MHz": row["a_parallel_MHz"], "a_perp_MHz": row["a_perp_MHz"],
                "a_iso_MHz": row["a_iso_MHz"],
                "anisotropic_frobenius_norm_MHz": row["anisotropic_frobenius_norm_MHz"],
                "principal_values_MHz": row["principal_values_MHz"], **errors,
            }
            for i in range(3):
                for j in range(3):
                    tensor_rows.append({"isotope": isotope, "method": method,
                                        "row_xyz": "xyz"[i], "column_xyz": "xyz"[j],
                                        "tensor_element_MHz": float(tensor[i, j])})
    checks = {
        "principal_values_recovered": max(eigenvalue_errors) < 1e-10,
        "isotropic_scalar_matches_principal_value_average": max(scalar_errors) < 1e-10,
        "anisotropic_part_is_traceless": max(anisotropic_traces) < 1e-10,
        "rotation_preserves_principal_values": max(rotation_eigenvalue_errors) < 1e-10,
        "rotation_preserves_isotropic_scalar": max(rotation_trace_errors) < 1e-10,
        "rotation_preserves_anisotropic_norm": max(rotation_norm_errors) < 1e-10,
    }
    if not all(checks.values()):
        raise ArithmeticError(f"Hyperfine reanalysis checks failed: {checks}")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "hyperfine_derived_quantities.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)
    with (out_dir / "illustrative_tensor_elements.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(tensor_rows[0]))
        writer.writeheader()
        writer.writerows(tensor_rows)

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 2, figsize=(10.8, 7.2), layout="constrained")
    categories = np.arange(3)
    labels = ["A parallel", "A perpendicular", "A isotropic"]
    colors = ["#555555", "#4c78a8", "#e45756"]
    try:
        for column, isotope in enumerate(ISOTOPES):
            for index, method in enumerate(METHODS):
                row = comparisons[isotope][method]
                values = [row["a_parallel_MHz"], row["a_perp_MHz"], row["a_iso_MHz"]]
                axes[0, column].bar(categories + (index - 1) * 0.23, values, width=0.23,
                                    color=colors[index], label=METHOD_LABELS[method])
            for index, method in enumerate(METHODS[1:]):
                row = comparisons[isotope][method]
                errors = [row["parallel_signed_error_MHz"], row["perp_signed_error_MHz"], row["iso_signed_error_MHz"]]
                axes[1, column].bar(categories + (index - 0.5) * 0.3, errors, width=0.3,
                                    color=colors[index + 1], label=METHOD_LABELS[method])
            axes[0, column].set(title=f"{isotope}: reported constants and derived average", ylabel="Hyperfine constant (MHz)")
            axes[1, column].set(title=f"{isotope}: signed differences from experiment", ylabel="Theory minus experiment (MHz)")
            axes[1, column].axhline(0.0, color="black", linewidth=0.8)
            for row_index in range(2):
                axes[row_index, column].set_xticks(categories, labels)
                axes[row_index, column].grid(axis="y", alpha=0.2)
        axes[0, 0].legend(fontsize=7.5)
        axes[1, 0].legend(fontsize=7.5)
        fig.suptitle("Gali & Maze (2013), Table I: reported hyperfine constants\nReanalysis; functional, cell size and core treatment change together", fontsize=11)
        fig.savefig(out_dir / "hyperfine_comparison.png", dpi=180)
    finally:
        plt.close(fig)
    closest = {
        isotope: min(METHODS[1:], key=lambda method: comparisons[isotope][method]["principal_value_mae_MHz"])
        for isotope in ISOTOPES
    }
    return {
        "exercise_type": "reanalysis_of_reported_hyperfine_tensors",
        "coordinate_assumption": "z along defect [111]; illustrative phi=0, not a measured azimuth",
        "isolated_core_polarization_effect_identified": False,
        "comparisons": comparisons,
        "closer_method_by_principal_value_mae": closest,
        "mae_definition": "(|parallel error| + 2 |perpendicular error|) / 3, accounting for axial eigenvalue multiplicity",
        "max_principal_value_error_MHz": float(max(eigenvalue_errors)),
        "max_scalar_average_error_MHz": float(max(scalar_errors)),
        "max_anisotropic_trace_MHz": float(max(anisotropic_traces)),
        "max_rotation_eigenvalue_error_MHz": float(max(rotation_eigenvalue_errors)),
        "max_rotation_isotropic_error_MHz": float(max(rotation_trace_errors)),
        "max_rotation_anisotropic_norm_error_MHz": float(max(rotation_norm_errors)),
        "checks": checks,
        "all_checks_passed": all(checks.values()),
    }


def main() -> int:
    from .run_support import run_cli

    return run_cli("hyperfine", compute)


if __name__ == "__main__":
    raise SystemExit(main())
