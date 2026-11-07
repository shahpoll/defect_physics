# Exercise 1: charge-state stability

- **Question:** why does the favored charge state change with Fermi level?
- **Calculation:** checked Python reconstruction; published crossings, not new DFT. Included charges: q = 0, −1, −2 only.
- **Source:** [Gali-Maze, arXiv v2](https://arxiv.org/pdf/1310.2137v2), Sec. II, Eqs. (3)-(4), PDF p. 2; Sec. III B / Fig. 4, PDF p. 4. HSE06 band gap: Sec. II.

## Inputs → lines

\[
F_q(E_F)=A_q+qE_F.
\]

- VBM = Fermi-level zero.
- F, A: energies in eV; A_q collects the Fermi-independent terms.
- E_F: electron chemical potential, eV above VBM.
- q: integer charge in units of positive elementary charge; negative q = added electrons.
- Published crossings: 1.43 eV and 2.14 eV; calculated HSE06 gap: 5.34 eV.
- **Arbitrary offset:** A_0 = 0; equality at the crossings fixes the other intercepts:

\[
A_{-1}=1.43\;\mathrm{eV},\qquad
A_{-2}=1.43+2.14=3.57\;\mathrm{eV}.
\]

- Derived relative intercepts; not published absolute formation energies.
- **Missing input:** numerical positive-charge crossing absent from the source text. Positive-charge line omitted; near-VBM q = 0 preference applies only to the included states.
- Evaluation: 1001 equally spaced Fermi points + two reported crossings → 1003 distinct rows.
- Envelope: analytic intervals from every pairwise intersection; retain only crossings that change the minimum.

## Result

| Fermi interval above VBM | Lowest relative energy among included states |
|---|---|
| 0 to 1.43 eV | q = 0 |
| 1.43 to 2.14 eV | q = -1 |
| 2.14 to 5.34 eV | q = -2 |

- Table: interval interiors. Adjacent states degenerate at each boundary.
- Floating-point representation: 2.1400000000000006 may appear for 2.14 eV.

![Relative formation-energy lines and their lower envelope](../runs/first_study/charge_states/relative_formation_energies.png)

- q = 0 / −2 crossing: **1.785 eV**; q = −1 lower by **0.355 eV** there → inactive crossing, not an envelope boundary.
- Increasing E_F favors added electrons → more negative q gives a more negative slope.
- Envelope = thermodynamic minimum among included states.
- **Limit:** no charge fractions, optical pumping dynamics, conversion rates, or laser-induced populations.

## Checks

- Largest adjacent-crossing residual: ≈ 2.2 × 10⁻¹⁶ eV.
- Slopes = q; common intercept shift leaves stability unchanged.
- Nonadjacent crossing correctly inactive.
- Mathematical checks of the reconstruction; no new experimental validation.

## Missing inputs / next question

- Actual populations: finite temperature, charge neutrality, specified reservoir required.
- Question: how do those inputs turn the three energy lines into charge populations?

## Files / rerun

- Input: [charge_states.json](../data/charge_states.json).
- Results: [intervals](../runs/first_study/charge_states/stable_charge_intervals.csv), [full curves](../runs/first_study/charge_states/relative_formation_energies.csv), [checks](../runs/first_study/charge_states/metrics.json).
- Input/code snapshots + result hashes: [public provenance](../references/public_provenance.md) ([JSON](../references/public_provenance.json)). Original execution records local and unchanged; public record omits machine paths and commands.
- Commands: [README](../README.md#reproduce-the-calculations).
