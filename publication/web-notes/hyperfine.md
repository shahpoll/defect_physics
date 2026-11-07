# Exercise 3: hyperfine-table comparison

- **Questions:** isotropic vs anisotropic agreement? Does the newer theory improve both isotopes?
- **Calculation:** checked reanalysis of published principal constants; no new electron spin density or EPR spectrum simulation.
- **Source:** [Gali-Maze, arXiv v2](https://arxiv.org/pdf/1310.2137v2), Sec. II, Eqs. (1)-(2), PDF p. 2; Sec. III D / Table I, PDF p. 6.
- Table I: experimental values from paper Ref. 15; older LDA values from Ref. 35. Transcription only; no independent measurement or recomputation.

## Tensor assumptions

- Axial, real symmetric tensor; unit vector u along parallel principal axis:

\[
A=A_\perp\mathbf1+(A_\parallel-A_\perp)uu^T,
\quad A_{\mathrm{iso}}=\frac{\operatorname{tr}A}{3}
=\frac{A_\parallel+2A_\perp}{3},
\quad T=A-A_{\mathrm{iso}}\mathbf1.
\]

- A, T: MHz; traceless anisotropic part: tr T = 0.
- Illustrative Cartesian matrices: z along defect [111]; table's polar angle θ; chosen azimuth φ = 0.
- **Missing orientation input:** Table I gives no unique 3D orientation for every tensor. φ = 0 is a coordinate choice; principal values and A_iso unchanged.
- Theory labels retained: LDA-nocp, HSE06-cp.
- Tabulated signs retained; no additional claim about independently measured signs.
- Silicon label: **29Si**, following Table I + discussion. Apparent 28Si wording discrepancy elsewhere preserved in main notes.

## Result

- A_parallel, A_perpendicular: transcribed; A_isotropic: calculated here.

| Isotope | Source method | A parallel (MHz) | A perpendicular (MHz) | A isotropic (MHz) |
|---|---|---:|---:|---:|
| 13C | Experiment | 66.2 | 30.2 | 42.2000 |
| 13C | LDA-nocp | 51.0 | 12.0 | 25.0000 |
| 13C | HSE06-cp | 68.0 | 28.0 | 41.3333 |
| 29Si | Experiment | 76.3 | 78.9 | 78.0333 |
| 29Si | LDA-nocp | 78.0 | 82.0 | 80.6667 |
| 29Si | HSE06-cp | 92.0 | 97.0 | 95.3333 |

- Experimental principal-value span: **13C 36.0 MHz**; **29Si 2.6 MHz** → carbon more anisotropic in this comparison.
- Close A_iso alone ≠ complete tensor agreement.

![Reported hyperfine constants, derived averages, and differences from experiment](../runs/first_study/hyperfine/hyperfine_comparison.png)

- Principal-value mean absolute error; repeated perpendicular eigenvalue counted twice:

\[
\mathrm{MAE}=\frac{|\delta A_\parallel|+2|\delta A_\perp|}{3}.
\]

- δA = theory − experiment, in MHz.

| Isotope | LDA-nocp MAE (MHz) | HSE06-cp MAE (MHz) |
|---|---:|---:|
| 13C | 17.2000 | 2.0667 |
| 29Si | 2.6333 | 17.3000 |

- HSE06-cp signed component errors, parallel / perpendicular:
  - 13C: **+1.8 / −2.2 MHz**.
  - 29Si: **+15.7 / +18.1 MHz**.
- Better carbon agreement; worse silicon agreement.
- Hyperfine comparison: evidence for an electronic-structure assignment + visible quantitative mismatch.

## Checks

- Reconstructed tensors recover principal eigenvalues + isotropic averages; anisotropic traces zero to floating-point precision.
- Independent rotation preserves principal values, isotropic parts, anisotropic norms.
- Maximum checked invariant discrepancies: < 3 × 10⁻¹⁴ MHz.

## Missing inputs / next question

- Source emphasizes core polarization, but theory columns also change functional + supercell size.
- **Missing controlled comparison:** otherwise matched calculations with/without core term; table cannot assign improvement/deterioration to core polarization alone.
- **Missing uncertainty:** no error bars for a statistical-significance claim.
- Next question: core-term contribution for each isotope? Requires additional electronic-structure calculations + suitable hyperfine implementation; table manipulation insufficient.

## Files / rerun

- Transcription + coordinate choice: [hyperfine.json](../data/hyperfine.json).
- Results: [derived quantities and errors](../runs/first_study/hyperfine/hyperfine_derived_quantities.csv), [illustrative tensors](../runs/first_study/hyperfine/illustrative_tensor_elements.csv), [checks](../runs/first_study/hyperfine/metrics.json).
- Input/code snapshots + result hashes: [public provenance](../references/public_provenance.md) ([JSON](../references/public_provenance.json)). Original execution records local and unchanged; public record omits machine paths and commands.
- Commands: [README](../README.md#reproduce-the-calculations).
