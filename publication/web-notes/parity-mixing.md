# Exercise 2: same spin, dark transition?

- **Questions:** what makes the optical matrix element vanish? What changes under an inversion-breaking coupling?
- **Calculation:** checked parity test + dimensionless teaching model; not a fitted SiV Hamiltonian or a parameter extraction.
- **Source:** [Gali-Maze, arXiv v2](https://arxiv.org/pdf/1310.2137v2), Sec. III C / Fig. 5, PDF pp. 5-6: shelving-state parity argument.

## Parity test

- Exact inversion eigenstates: g = even (+1); u = odd (−1).
- Electric-dipole operator: odd.
- Product of final-state, operator, and initial-state parities odd → matrix element zero.

| Initial | Final | Electric-dipole parity test |
|---|---|---|
| g | g | Forbidden by inversion parity |
| g | u | Not forbidden by parity |
| u | g | Not forbidden by parity |
| u | u | Forbidden by inversion parity |

- Opposite parity: necessary, not sufficient.
- **Missing checks:** full D3d representation products, polarization, spin selection, actual orbital matrix elements.

## Two-state model

- Fixed even ground state.
- Excited basis: D = even, dark; B = odd, bright.
- Bare dipoles: ground → D = 0; ground → B = 1.
- Δ > 0: unperturbed separation; V: real, inversion-odd coupling; λ = V/Δ, dimensionless.

\[
\frac{H}{\Delta}=\begin{pmatrix}0&\lambda\\\lambda&1\end{pmatrix},
\qquad \lambda=V/\Delta.
\]

- Energy zero: unperturbed dark excited state; physical ground-state energy absent from matrix.
- Negative lower eigenvalue relative to this zero ≠ negative physical optical excitation energy.
- Coupling, energy scale, normalization: teaching choices; no measured field/strain mapping.

## Diagonalization → borrowed dipole strength

- Sweep: 401 points, λ = −0.5 to +0.5.
- Dimensionless eigenenergies:

\[
\epsilon_\pm=\frac{1\pm\sqrt{1+4\lambda^2}}{2}.
\]

- Lower eigenstate's squared bright coefficient:

\[
I_{\mathrm{borrowed}}=\frac12\left(1-\frac{1}{\sqrt{1+4\lambda^2}}\right)
\simeq\lambda^2\quad (|\lambda|\ll1).
\]

- I: normalized squared dipole matrix element, fixed-ground assumption.
- **Omitted factors:** transition frequency, populations → no complete oscillator strength, emission intensity, radiative rate, or lifetime.

## Result

- λ = 0: lower state exactly dark.
- λ = ±0.5: bright weight **0.1464466094**.
- Coupling sign reversal: mixing phase changes; squared strength unchanged.

| lambda | Borrowed strength | Strength / lambda squared |
|---:|---:|---:|
| 0.01 | 9.997001e-5 | 0.9997001000 |
| 0.001 | 9.999970e-7 | 0.9999970000 |
| 0.0001 | 9.9999997e-9 | 0.9999999700 |

![Dimensionless eigenenergies and borrowed dipole strength](../runs/first_study/parity_mixing/dimensionless_parity_mixing.png)

- Exact symmetry can suppress a matrix element without changing spin.
- Inversion-odd perturbation → parity mixing → borrowed dipole amplitude in this model.
- **Limit:** homogeneous affine strain can preserve inversion while changing other symmetries; “all strain brightens a dark state” does not follow.

## Checks

- Numerical vs analytic strengths: agreement ≈ 5.6 × 10⁻¹⁷ across sweep.
- Eigenvector residuals + normalization errors: < 5 × 10⁻¹⁶.
- Zero coupling, sign reversal, conserved total bright weight, quadratic weak limit: passed.

## Missing inputs / next question

- Real SiV coupling V: microscopic perturbation, geometry, symmetry argument needed.
- Possible changes outside model: ground state, other excited states, phonons, populations.
- Question: which physical perturbation supplies V, and what else does it change? No quantitative answer from this curve alone.

## Files / rerun

- Input + model choices: [parity_mixing.json](../data/parity_mixing.json).
- Results: [parity table](../runs/first_study/parity_mixing/parity_necessary_condition.csv), [sweep](../runs/first_study/parity_mixing/dimensionless_mixing_sweep.csv), [weak limit](../runs/first_study/parity_mixing/weak_mixing_limit.csv), [checks](../runs/first_study/parity_mixing/metrics.json).
- Input/code snapshots + result hashes: [public provenance](../references/public_provenance.md) ([JSON](../references/public_provenance.json)). Original execution records local and unchanged; public record omits machine paths and commands.
- Commands: [README](../README.md#reproduce-the-calculations).
