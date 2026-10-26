# First discussion: what I currently understand about SiV

Prepared 26 October 2026. **Draft study notes plus three executed Python exercises.** My understanding is for discussion and correction; this package does not certify that I can yet derive every step unaided.

## What we studied

Gali and Maze, [Physical Review B 88, 235205 (2013)](https://doi.org/10.1103/PhysRevB.88.235205), using the [eight-page arXiv v2](https://arxiv.org/pdf/1310.2137v2) reading copy.

The question is how structure, charge, spin, symmetry, and computed energies connect the silicon-vacancy center to optical and magnetic observations. My main conceptual checkpoint is to distinguish an orbital energy, a many-electron state, an optical excitation, and a thermal charge-transition level.

The [main notes](../Rudimentary_Notes_Gali_n_Maze.md) connect claims to sections/figures and explain the background. Two conclusions need particularly careful wording: the neutral 1.31 eV optical assignment is supported indirectly rather than directly calculated by the stated method; and the hyperfine table's improved carbon agreement coexists with a larger silicon mismatch. The paper's dynamic Jahn-Teller limitation is followed by a [selected later-reading guide](literature_followup.md), including a relevant erratum.

## What we ran and what it means

| Exercise | Result | What I can claim |
|---|---|---|
| [Charge-state reconstruction](charge_states.md) | Restricted lowest-energy sequence 0, -1, -2, switching at the input crossings 1.43 and 2.14 eV. The 0/-2 crossing at 1.785 eV is inactive. | I can explain relative formation-energy slopes and the lower envelope. The crossing values are source inputs, not fresh predictions. |
| [Parity and mixing](parity_mixing.md) | Same-parity electric-dipole matrix elements vanish in the symmetric model. A chosen odd coupling produces quadratic borrowed dipole strength at weak mixing. | I can demonstrate one symmetry condition and a simple mixing mechanism. No physical strain coefficient, rate, or lifetime is calculated. |
| [Hyperfine reanalysis](hyperfine.md) | Principal-value MAE changes from 17.20 to 2.07 MHz for carbon, but from 2.63 to 17.30 MHz for silicon, comparing the old/new theoretical columns. | I can quantify both agreement and disagreement in Table I. The comparison cannot isolate the cause as core polarization alone. |

The public reference runs contain their exact inputs, code snapshots, CSV results, figures, and completion checks. See [the curated public provenance](../references/public_provenance.md), its [JSON hash record](../references/public_provenance.json), and [the historical 29-test record](verification.txt). Original manifests and logs remain unchanged locally; the public derivative omits machine paths and commands and identifies those redactions. Numerical and analytic checks establish that these small calculations work as specified; they do not independently validate the paper's electronic-structure model.

## Questions I want to bring to the meeting

1. Can I explain the four energy concepts at the board and draw the relevant geometries/occupancies?
2. What would directly calculate the neutral state that the paper's single-determinant treatment cannot represent?
3. Which perturbations actually break inversion in a proposed experimental geometry?
4. What matched calculation or additional evidence would help diagnose the silicon hyperfine discrepancy?
5. Should our next effort deepen the symmetry/vibronic derivation, or begin the [small bulk-diamond QE benchmark](qe_next_step.md)?

The [full question log](../notes/questions.md) separates learning gaps, paper-specific limitations, and candidate follow-ups. Candidate follow-ups have not been established as current research gaps.

## Practical next step

Discuss and annotate the draft before expanding the project. Python has supplied a small, reproducible first package on the M4 Mac mini. QE remains proposed; bulk convergence, measured resource use, and storage must be checked before choosing a defect supercell. The original study milestone included no QE simulation; the public repository presents that earlier work with its limits and questions intact.
