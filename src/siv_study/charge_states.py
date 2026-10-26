"""Relative formation-energy reconstruction from reported charge crossings."""

from __future__ import annotations

import csv
import math
from collections.abc import Mapping
from pathlib import Path

import numpy as np


def _finite(value: object, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite number, not bool")
    try:
        result = float(value)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def derive_intercepts(
    level_zero_minus: float,
    level_minus_double: float,
    neutral_offset: float = 0.0,
) -> dict[int, float]:
    """Choose the shared zero, then impose the two adjacent crossings."""
    first = _finite(level_zero_minus, "zero/minus crossing")
    second = _finite(level_minus_double, "minus/double-minus crossing")
    offset = _finite(neutral_offset, "neutral offset")
    if not 0.0 < first < second:
        raise ValueError("Crossings must satisfy 0 < zero/minus < minus/double-minus")
    return {0: offset, -1: offset + first, -2: offset + first + second}


def formation_energy(
    fermi_eV: float | np.ndarray, charge: int, intercept: float
) -> float | np.ndarray:
    """Evaluate the relative line A_q + q E_F (E_F measured above VBM)."""
    if isinstance(charge, bool) or not isinstance(charge, (int, np.integer)):
        raise ValueError("Charge must be an integer")
    origin = _finite(intercept, "intercept")
    fermi = np.asarray(fermi_eV, dtype=float)
    if not np.all(np.isfinite(fermi)):
        raise ValueError("Fermi levels must be finite")
    result = origin + int(charge) * fermi
    if not np.all(np.isfinite(result)):
        raise ValueError("Formation energies overflowed")
    return float(result) if result.ndim == 0 else result


def stable_intervals(
    intercepts: Mapping[int, float], minimum: float = 0.0, maximum: float = 5.34
) -> list[dict[str, float | int]]:
    """Find the exact lower-envelope intervals, discarding inactive crossings.

    Interval endpoints can be degenerate; the returned charge is the unique
    minimum in the open interior. No population or kinetic meaning is implied.
    """
    lo = _finite(minimum, "minimum Fermi level")
    hi = _finite(maximum, "maximum Fermi level")
    if lo >= hi or not intercepts:
        raise ValueError("Need at least one line and minimum < maximum")
    lines: dict[int, float] = {}
    for charge, offset in intercepts.items():
        if isinstance(charge, bool) or not isinstance(charge, (int, np.integer)):
            raise ValueError("Charge keys must be integers")
        lines[int(charge)] = _finite(offset, "line intercept")
    points = [lo, hi]
    charges = sorted(lines, reverse=True)
    for index, first in enumerate(charges):
        for second in charges[index + 1 :]:
            crossing = (lines[second] - lines[first]) / (first - second)
            if lo < crossing < hi:
                points.append(crossing)
    edges = sorted(set(points))
    intervals: list[dict[str, float | int]] = []
    for left, right in zip(edges[:-1], edges[1:]):
        middle = 0.5 * (left + right)
        charge = min(charges, key=lambda q: lines[q] + q * middle)
        if intervals and intervals[-1]["charge"] == charge:
            intervals[-1]["fermi_max_eV"] = right
        else:
            intervals.append(
                {"charge": charge, "fermi_min_eV": left, "fermi_max_eV": right}
            )
    return intervals


def compute(config: dict, out_dir: Path) -> dict:
    reported = config["reported"]
    transition = reported["transition_levels_eV"]
    model = config["model"]
    first = _finite(transition["zero_to_minus_one"], "zero/minus crossing")
    second = _finite(transition["minus_one_to_minus_two"], "minus/double-minus crossing")
    gap = _finite(reported["band_gap_eV"], "band gap")
    offset = _finite(model["neutral_energy_offset_eV"], "neutral offset")
    if not 0.0 < first < second < gap:
        raise ValueError("Need 0 < first crossing < second crossing < band gap")
    charges = model["charge_states"]
    if (
        not isinstance(charges, list)
        or len(charges) != 3
        or any(isinstance(q, bool) or not isinstance(q, int) for q in charges)
        or set(charges) != {0, -1, -2}
    ):
        raise ValueError("This reconstruction covers exactly charge states 0, -1, -2")
    count = model["fermi_grid_points"]
    if isinstance(count, bool) or not isinstance(count, int) or not 3 <= count <= 100001:
        raise ValueError("fermi_grid_points must be an integer from 3 to 100001")
    intercepts = derive_intercepts(first, second, offset)
    intervals = stable_intervals(intercepts, 0.0, gap)
    expected = [(0, 0.0, first), (-1, first, second), (-2, second, gap)]
    if len(intervals) != len(expected) or any(
        item["charge"] != charge
        or abs(float(item["fermi_min_eV"]) - left) > 1e-12
        or abs(float(item["fermi_max_eV"]) - right) > 1e-12
        for item, (charge, left, right) in zip(intervals, expected)
    ):
        raise ArithmeticError("The lower envelope did not recover adjacent charge intervals")
    crossing_residuals = [
        abs(formation_energy(first, 0, intercepts[0]) - formation_energy(first, -1, intercepts[-1])),
        abs(formation_energy(second, -1, intercepts[-1]) - formation_energy(second, -2, intercepts[-2])),
    ]
    slope_error = max(
        abs((formation_energy(gap, q, intercepts[q]) - formation_energy(0.0, q, intercepts[q])) / gap - q)
        for q in charges
    )
    inactive_crossing = (intercepts[-2] - intercepts[0]) / 2.0
    inactive_margin = formation_energy(inactive_crossing, 0, intercepts[0]) - formation_energy(
        inactive_crossing, -1, intercepts[-1]
    )
    shifted = stable_intervals({q: value + 7.0 for q, value in intercepts.items()}, 0.0, gap)
    offset_invariance_error = max(
        max(abs(float(a[k]) - float(b[k])) for k in ("fermi_min_eV", "fermi_max_eV"))
        for a, b in zip(intervals, shifted)
    )
    checks = {
        "adjacent_crossing_equalities": max(crossing_residuals) < 1e-12,
        "slopes_equal_charges": slope_error < 1e-12,
        "nonadjacent_crossing_is_inactive": inactive_margin > 0.0,
        "common_offset_leaves_intervals_unchanged": offset_invariance_error < 1e-12
        and [a["charge"] for a in intervals] == [b["charge"] for b in shifted],
        "known_stability_order": True,
    }
    if not all(checks.values()):
        raise ArithmeticError(f"Charge reconstruction checks failed: {checks}")
    fermi = np.unique(np.concatenate((np.linspace(0.0, gap, count), [first, second])))
    ordered = [0, -1, -2]
    energies = np.vstack([formation_energy(fermi, q, intercepts[q]) for q in ordered])
    envelope = np.min(energies, axis=0)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "relative_formation_energies.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow([
            "fermi_above_vbm_eV", "relative_q0_eV", "relative_qminus1_eV",
            "relative_qminus2_eV", "lower_envelope_relative_eV", "co_minimal_charges"
        ])
        for index, x in enumerate(fermi):
            co_minima = "|".join(
                str(q) for row, q in enumerate(ordered)
                if abs(float(energies[row, index] - envelope[index])) < 1e-10
            )
            writer.writerow([float(x), *energies[:, index].tolist(), float(envelope[index]), co_minima])
    with (out_dir / "stable_charge_intervals.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["charge", "fermi_min_eV", "fermi_max_eV"])
        writer.writeheader()
        writer.writerows(intervals)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8.2, 5.0), layout="constrained")
    try:
        for row, charge in enumerate(ordered):
            ax.plot(fermi, energies[row], linewidth=1.5, label=f"q = {charge}")
        ax.plot(fermi, envelope, color="black", linewidth=3, alpha=0.65, label="Lower envelope")
        for crossing in (first, second):
            ax.axvline(crossing, color="0.5", linestyle=":", linewidth=1)
            ax.annotate(f"{crossing:.2f} eV", (crossing, 1.0), xycoords=("data", "axes fraction"),
                        xytext=(5, -6), textcoords="offset points", va="top", fontsize=9)
        ax.set(xlabel="Fermi level above VBM (eV)", ylabel="Relative formation energy (eV)",
               title="SiV charge states: reconstruction from reported crossings\nGali & Maze (2013), Sec. III B / Fig. 4; gap from Sec. II", xlim=(0.0, gap))
        ax.text(0.01, 0.02, "Arbitrary common energy zero; only q = 0, -1, -2 included",
                transform=ax.transAxes, fontsize=8, bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "none"})
        ax.legend(loc="upper right")
        ax.grid(alpha=0.2)
        fig.savefig(out_dir / "relative_formation_energies.png", dpi=180)
    finally:
        plt.close(fig)
    return {
        "exercise_type": "reconstruction_from_reported_values",
        "energy_zero": "arbitrary common offset; no absolute formation energies",
        "band_gap_eV": gap,
        "reported_transition_levels_eV": [first, second],
        "derived_intercepts_eV": {str(q): value for q, value in intercepts.items()},
        "stable_intervals": intervals,
        "nonadjacent_zero_minus_two_crossing_eV": inactive_crossing,
        "nonadjacent_crossing_is_stability_boundary": False,
        "minus_one_energy_advantage_at_nonadjacent_crossing_eV": float(inactive_margin),
        "max_crossing_residual_eV": float(max(crossing_residuals)),
        "max_slope_error": float(slope_error),
        "offset_invariance_error_eV": float(offset_invariance_error),
        "grid_rows": int(fermi.size),
        "checks": checks,
        "all_checks_passed": all(checks.values()),
    }


def main() -> int:
    from .run_support import run_cli

    return run_cli("charge_states", compute)


if __name__ == "__main__":
    raise SystemExit(main())
