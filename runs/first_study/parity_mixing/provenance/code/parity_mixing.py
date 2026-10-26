"""Necessary inversion-parity rule and an explicitly illustrative mixing model."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np


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


def parity_permits(initial: str, final: str, operator: str = "u") -> bool:
    """Return whether parity alone does NOT force a matrix element to vanish.

    True is a necessary-condition result, not the full optical selection rule.
    In particular it does not check spin, polarization, or the full D3d irreps.
    """
    signs = {"g": 1, "u": -1}
    if any(value not in signs for value in (initial, final, operator)):
        raise ValueError("Parity labels must be 'g' (even) or 'u' (odd)")
    return signs[initial] * signs[operator] * signs[final] == 1


def borrowed_intensity_analytic(strength: float) -> float:
    """Bright weight of the lower eigenstate of [[0, lambda],[lambda,1]].

    This cancellation-resistant expression equals (1-1/sqrt(1+4 lambda^2))/2.
    It assumes a fixed even ground state, unit bright dipole, and zero dark
    dipole, chosen for teaching. This normalized squared matrix element omits
    transition-frequency and state-population factors in radiative intensities.
    """
    coupling = _finite(strength, "dimensionless coupling")
    if abs(coupling) > 1.0:
        raise ValueError("This teaching exercise supports |lambda| <= 1")
    radius = math.sqrt(1.0 + 4.0 * coupling * coupling)
    return 2.0 * coupling * coupling / (radius * (radius + 1.0))


def mixing_solution(strength: float) -> dict[str, float]:
    """Diagonalize the dimensionless Hamiltonian in its dark, bright basis."""
    coupling = _finite(strength, "dimensionless coupling")
    if abs(coupling) > 1.0:
        raise ValueError("This teaching exercise supports |lambda| <= 1")
    hamiltonian = np.array([[0.0, coupling], [coupling, 1.0]])
    energies, vectors = np.linalg.eigh(hamiltonian)
    residual = np.max(np.abs(hamiltonian @ vectors - vectors * energies[np.newaxis, :]))
    orthogonality = np.max(np.abs(vectors.T @ vectors - np.eye(2)))
    return {
        "lower_energy_over_Delta": float(energies[0]),
        "upper_energy_over_Delta": float(energies[1]),
        "lower_borrowed_intensity": float(vectors[1, 0] ** 2),
        "upper_bright_intensity": float(vectors[1, 1] ** 2),
        "max_eigenvector_residual": float(residual),
        "max_orthogonality_error": float(orthogonality),
    }


def compute(config: dict, out_dir: Path) -> dict:
    model = config["model"]
    operator = model["operator_parity"]
    if operator != "u":
        raise ValueError("The electric-dipole exercise requires odd operator parity 'u'")
    transitions = config["parity_transitions"]
    if not isinstance(transitions, list) or len(transitions) != 4:
        raise ValueError("Supply all four initial/final parity combinations")
    combinations = set()
    parity_rows = []
    for transition in transitions:
        initial = transition["initial_parity"]
        final = transition["final_parity"]
        permitted = parity_permits(initial, final, operator)
        combinations.add((initial, final))
        parity_rows.append({
            "initial_parity": initial,
            "final_parity": final,
            "operator_parity": operator,
            "not_forbidden_by_parity": permitted,
            "interpretation": "Necessary condition only" if permitted else "Forbidden by inversion parity in the ideal symmetric model",
            "example": str(transition.get("example", "")),
        })
    if combinations != {("g", "g"), ("g", "u"), ("u", "g"), ("u", "u")}:
        raise ValueError("Parity combinations must be unique and cover g/g, g/u, u/g, u/u")
    lower = _finite(model["mixing_strength_min"], "minimum coupling")
    upper = _finite(model["mixing_strength_max"], "maximum coupling")
    if not -1.0 <= lower < 0.0 < upper <= 1.0 or not math.isclose(lower, -upper, abs_tol=1e-12):
        raise ValueError("Use symmetric finite coupling limits about zero within [-1, 1]")
    count = model["mixing_grid_points"]
    if isinstance(count, bool) or not isinstance(count, int) or not 3 <= count <= 100001:
        raise ValueError("mixing_grid_points must be an integer from 3 to 100001")
    weak_inputs = model["weak_limit_strengths"]
    if not isinstance(weak_inputs, list) or len(weak_inputs) < 2:
        raise ValueError("Provide at least two distinct positive weak-limit couplings")
    weak = sorted((_finite(value, "weak-limit coupling") for value in weak_inputs), reverse=True)
    if len(set(weak)) != len(weak) or not all(1e-8 <= value <= 0.01 for value in weak):
        raise ValueError("Weak-limit couplings must be distinct and lie between 1e-8 and 0.01")
    coupling = np.unique(np.concatenate((np.linspace(lower, upper, count), [0.0])))
    results = [mixing_solution(float(value)) for value in coupling]
    numerical = np.array([row["lower_borrowed_intensity"] for row in results])
    analytic = np.array([borrowed_intensity_analytic(float(value)) for value in coupling])
    weak_rows = []
    for value in weak:
        intensity = mixing_solution(value)["lower_borrowed_intensity"]
        ratio = intensity / (value * value)
        weak_rows.append({
            "lambda": value, "lower_borrowed_intensity": intensity,
            "lambda_squared": value * value, "intensity_over_lambda_squared": ratio,
            "relative_departure_from_quadratic_limit": abs(ratio - 1.0),
        })
    max_analytic_error = float(np.max(np.abs(numerical - analytic)))
    max_parity_error = max(
        abs(mixing_solution(float(value))["lower_borrowed_intensity"]
            - mixing_solution(float(-value))["lower_borrowed_intensity"])
        for value in coupling
    )
    max_residual = max(row["max_eigenvector_residual"] for row in results)
    max_orthogonality = max(row["max_orthogonality_error"] for row in results)
    max_trace_error = max(
        abs(row["lower_energy_over_Delta"] + row["upper_energy_over_Delta"] - 1.0)
        for row in results
    )
    max_strength_error = max(
        abs(row["lower_borrowed_intensity"] + row["upper_bright_intensity"] - 1.0)
        for row in results
    )
    weak_errors = [row["relative_departure_from_quadratic_limit"] for row in weak_rows]
    checks = {
        "same_parity_is_forbidden_for_odd_dipole": not parity_permits("g", "g") and not parity_permits("u", "u"),
        "opposite_parity_passes_necessary_condition": parity_permits("g", "u") and parity_permits("u", "g"),
        "zero_mixing_gives_zero_dark_intensity": mixing_solution(0.0)["lower_borrowed_intensity"] == 0.0,
        "eigenvectors_solve_hamiltonian": max_residual < 1e-12,
        "eigenvectors_are_orthonormal": max_orthogonality < 1e-12,
        "eigenenergy_sum_matches_trace": max_trace_error < 1e-12,
        "total_normalized_bright_weight_is_conserved": max_strength_error < 1e-12,
        "numerical_intensity_matches_analytic_solution": max_analytic_error < 1e-12,
        "intensity_is_even_in_coupling": max_parity_error < 1e-12,
        "quadratic_limit_is_approached": max(weak_errors) < 4.0 * weak[0] ** 2
        and all(later <= earlier + 1e-13 for earlier, later in zip(weak_errors[:-1], weak_errors[1:])),
    }
    if not all(checks.values()):
        raise ArithmeticError(f"Parity/mixing checks failed: {checks}")
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "parity_necessary_condition.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(parity_rows[0]))
        writer.writeheader()
        writer.writerows(parity_rows)
    with (out_dir / "dimensionless_mixing_sweep.csv").open("w", newline="") as stream:
        names = ["lambda", *results[0], "analytic_lower_borrowed_intensity"]
        writer = csv.DictWriter(stream, fieldnames=names)
        writer.writeheader()
        for value, result, prediction in zip(coupling, results, analytic):
            writer.writerow({"lambda": float(value), **result, "analytic_lower_borrowed_intensity": float(prediction)})
    with (out_dir / "weak_mixing_limit.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(weak_rows[0]))
        writer.writeheader()
        writer.writerows(weak_rows)

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(10.3, 4.6), layout="constrained")
    try:
        axes[0].plot(coupling, [row["lower_energy_over_Delta"] for row in results], label="Lower (dark at zero mixing)")
        axes[0].plot(coupling, [row["upper_energy_over_Delta"] for row in results], label="Upper (bright at zero mixing)")
        axes[0].set(xlabel="Dimensionless odd-parity coupling, lambda = V / Delta",
                    ylabel="Energy / Delta", title="Two-state eigenenergies")
        axes[0].legend(fontsize=8)
        axes[1].plot(coupling, numerical, linewidth=2, label="Numerical lower-state bright weight")
        axes[1].plot(coupling, analytic, linestyle="--", linewidth=1.2, color="black", label="Analytic solution")
        axes[1].set(xlabel="Dimensionless odd-parity coupling, lambda = V / Delta",
                    ylabel="Normalized borrowed dipole strength (bright weight)",
                    title="Dark-state brightening in a teaching model", ylim=(0.0, max(0.01, float(np.max(numerical)) * 1.1)))
        axes[1].legend(fontsize=8)
        for ax in axes:
            ax.grid(alpha=0.2)
        fig.suptitle("Parity motivated by Gali & Maze (2013), Sec. III C / Fig. 5\nIllustrative model: no conversion to strain, rates, or lifetimes", fontsize=11)
        fig.savefig(out_dir / "dimensionless_parity_mixing.png", dpi=180)
    finally:
        plt.close(fig)
    return {
        "exercise_type": "parity_necessary_condition_and_dimensionless_teaching_model",
        "selection_rule_scope": "Parity is necessary, not sufficient; full D3d, spin and polarization rules are not implemented",
        "intensity_definition": "Normalized squared dipole strength with a fixed even ground state; frequency and population factors omitted",
        "physical_strain_or_rate_prediction": False,
        "coupling_range": [lower, upper],
        "grid_rows": int(coupling.size),
        "zero_coupling_borrowed_intensity": mixing_solution(0.0)["lower_borrowed_intensity"],
        "edge_borrowed_intensity": mixing_solution(upper)["lower_borrowed_intensity"],
        "max_analytic_intensity_error": max_analytic_error,
        "max_coupling_reversal_error": float(max_parity_error),
        "max_eigenvector_residual": float(max_residual),
        "max_orthogonality_error": float(max_orthogonality),
        "max_bright_weight_sum_error": float(max_strength_error),
        "weak_limit": weak_rows,
        "checks": checks,
        "all_checks_passed": all(checks.values()),
    }


def main() -> int:
    from .run_support import run_cli

    return run_cli("parity_mixing", compute)


if __name__ == "__main__":
    raise SystemExit(main())
