# Reading map and checkpoints

This is a proposed learning sequence, not a completed-reading checklist. Start with [the main notes](../Rudimentary_Notes_Gali_n_Maze.md) and keep [questions](questions.md) open alongside them. All paper page numbers below use the 8-page [arXiv v2 PDF](https://arxiv.org/pdf/1310.2137v2), not the published article's pagination.

| Pass | Read | What I want to produce | A useful checkpoint |
|---|---|---|---|
| 1. The actual problem | Abstract + Sec. I, p. 1; Sec. IV, p. 7 | A short statement of the optical/magnetic identification problem | I can distinguish the authors' goal from a result they directly calculated. |
| 2. Geometry and counting | Fig. 1, p. 2; Sec. III A + Fig. 2, p. 3; Fig. 3, p. 4 | A split-vacancy sketch and neutral/negative/doubly-negative occupancies | I can explain 10/11/12 electrons in the defect basis and A versus E versus spin multiplicity. |
| 3. Method and energy references | Sec. II, pp. 2–3, especially Eqs. (1)–(4) | A one-page map of orbital, total, optical, and charge-transition energies | Every energy I write has a reference, charge, geometry, and method. |
| 4. Equilibrium charge | Sec. III B + Fig. 4, p. 4 | Annotated formation-energy crossing reconstruction | I can explain its arbitrary common offset and why it gives no pumping rate. |
| 5. Bright and dark negative states | Sec. III C, pp. 4–6; Fig. 5, p. 5 | A term diagram marked direct / proposed / symmetry argument | I can derive the parity rule and say why not all strain breaks inversion. |
| 6. Neutral assignment and hyperfine | Sec. III D + Table I, p. 6; continuation p. 7 | An evidence comparison with the indirect neutral inference and silicon mismatch visible | I can identify what the determinant method cannot calculate and what the table cannot causally isolate. |
| 7. Later context | [Selective follow-up](../reports/literature_followup.md) | A comparison of the 2013 model with specific subsequent measurements/theory | I do not present a 2013 limitation as an untouched problem today. |
| 8. Discussion | [Supervisor brief](../reports/supervisor_brief.md) + run reports | Explainable figures, source locators, and the next decision | Another person can see the assumptions, reproduce the small runs, and correct my reasoning. |

## The first calculation ladder

1. [Charge-state reconstruction](../reports/charge_states.md): mathematical illustration using paper transition levels; no DFT and no absolute formation-energy reproduction.
2. [Parity mixing](../reports/parity_mixing.md): deliberately reduced Hamiltonian; test the zero-coupling limit and state what microscopic parameters are absent.
3. [Hyperfine comparison](../reports/hyperfine.md): arithmetic on Table I, retaining isotope/source labels and the mismatch.
4. Optional next stage: verify the exact QE installation, then benchmark bulk diamond before deciding a defect-cell size and runtime budget. A QE/PBE pilot would not reproduce the paper's full VASP/HSE06 workflow.

## How I will keep the notes honest

- Attach a page/section/figure/table locator to paper-derived claims.
- Keep the paper's direct calculation, its experimental comparison, its proposed mechanism, and my explanatory derivation distinguishable.
- Update an earlier misunderstanding explicitly when discussion resolves it; do not pretend it was always understood.
- Record unsuccessful or inconclusive calculations alongside successful ones.
- Use a parameter taken from a paper as a sourced input, not a prediction of the model that imports it.
- Before using “open problem,” check newer primary sources and state the scope of that check.

The [source register](../references/sources.md) fixes versions and access dates. The glossary is a working aid, not an authoritative replacement for the original definitions.
