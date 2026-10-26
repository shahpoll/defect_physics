# Glossary I can keep expanding

Working definitions, written to support the [main reading notes](../Rudimentary_Notes_Gali_n_Maze.md). “I can say the words” and “I can derive/use the idea” are different checkpoints. Paper-specific locators use the 8-page [arXiv v2 PDF](https://arxiv.org/pdf/1310.2137v2).

| Term | My working meaning | Check I should be able to do |
|---|---|---|
| Defect | A departure from the perfect crystal, such as a missing atom or impurity. | Draw the host and specify what was removed/added. |
| Split vacancy | Here, Si near the midpoint of two adjacent vacant C sites, with six neighboring C atoms. | Locate the inversion center. Paper Sec. III A, p. 3; Fig. 1, p. 2. |
| Dangling bond | A locally unsatisfied bonding orbital after a neighbor is removed. It is a basis idea, not automatically an independent eigenstate. | Form combinations that respect the defect symmetry. |
| D3d | The point group of the ideal split-vacancy model, including inversion. | Distinguish lowering rotational symmetry from removing inversion. |
| Irreducible representation | A basic symmetry transformation pattern used to label orbitals or states. | Explain what transforms, rather than treating the label as an energy. |
| a / e orbital | One-/two-dimensional spatial orbital representation in this notation. | Count capacities: a holds up to 2 electrons, e up to 4 including spin. |
| A / E term | One-/two-dimensional spatial symmetry of a many-electron term. | Avoid equating uppercase terms with single-particle orbitals. |
| g / u | Even / odd under inversion. | Apply inversion twice and recover the original state. |
| Spin S | Total electronic angular momentum from spin in the model. | Calculate multiplicity 2S + 1. |
| Spin singlet/doublet/triplet | S = 0, 1/2, 1 respectively. | Explain why 3A2g is spin triplet but orbital singlet. |
| Orbital degeneracy | Several independent spatial states share an energy in a specified symmetric model. | Say what symmetry or approximation protects the equality. |
| Kramers degeneracy | Time-reversal-related degeneracy for half-integer total angular momentum under its assumptions. | Do not confuse it with an e orbital's two components. |
| Electronic configuration | Occupancy of selected orbitals, such as eu4 eg3. | State the omitted filled orbitals and electron/hole convention. |
| Slater determinant | An antisymmetrized product of spin orbitals. Some many-electron states require combinations of determinants. | Explain the representability limit in neutral SiV; Sec. III D, p. 6. |
| Hund's rule | A guide to favorable spin arrangements in degenerate shells; full ordering depends on interactions. | Draw neutral eg2 high-spin occupancy without claiming a quantitative splitting. |
| Valence-band maximum (VBM) | The highest valence-band edge of the stated host/reference calculation. | Label energy zero consistently. |
| Conduction-band minimum | The lowest conduction-band edge in the specified model. | Distinguish a band edge from a defect level. |
| Band gap | Difference between valence- and conduction-band edges, with the theory/measurement specified. | Separate Kohn–Sham and measured fundamental/optical gaps. |
| Resonant defect state | Defect-related electronic character overlaps host-band energies and can mix with the band. | Inspect localization as well as energy. Paper Sec. III A, p. 3; Fig. 3, p. 4. |
| DFT | A ground-state density-based electronic-structure framework with an approximate exchange-correlation functional in practical use. | Name the functional and observable before assessing accuracy. |
| PBE / HSE06 | A semilocal / screened hybrid functional used at different stages or in different models. | Avoid calling a PBE result a reproduction of an HSE06 number. |
| Constrained DFT | Here, an imposed electronic occupancy used to access a selected excited-state description and relaxation. | Check whether the target term can be represented by that construction. |
| Supercell | A repeated simulation cell containing a defect and its periodic replicas. | Ask whether replicas affect the property being discussed. |
| Γ-point approximation | Sampling the supercell Brillouin zone at Γ only. | Test suitability rather than assume large cells make every observable converged. |
| Charged-cell correction | Treatment of artifacts from a periodically repeated charged defect and compensating background/reference. | Keep correction and potential alignment with total-energy data. Paper Sec. II, pp. 2–3. |
| Formation energy | Energy cost relative to specified atom/electron reservoirs, not an optical transition energy. | State chemical potentials and the Fermi-level reference. |
| Thermal charge-transition level | Fermi level where relaxed formation energies of two charge states are equal. | Find a line crossing and its slope difference. Paper Eq. (4), p. 2. |
| Fermi level | Electron chemical potential; in formation-energy plots it is a reservoir parameter. | Explain why more positive EF can favor negative charge. |
| PL | Photoluminescence: light emitted following excitation. | Separate emitted photon energy from the pump energy. |
| ZPL | Zero-phonon line: the transition without net vibrational quanta in the optical event; theory requires clear vibrational conventions. | Draw relaxed minima and distinguish vertical transitions. |
| Stokes shift | Difference between absorption and emission energies under a defined comparison. | Do not equate it automatically with one relaxation-energy component. |
| Vibronic state | A state with coupled electronic and vibrational character. | Identify when a purely electronic diagram omits essential dynamics. |
| Jahn–Teller effect | Coupling of an electronically degenerate state to distortions that can lower energy. | Distinguish a static minimum from motion among equivalent distortions. |
| Dynamic Jahn–Teller effect | A coupled vibronic problem not exhausted by optimizing one static geometry. | Consult later work before declaring it an open problem. |
| Spin–orbit coupling | Coupling between spin and orbital degrees of freedom. | Explain why a spin-free term scheme is not a full fine-structure spectrum. |
| Electric-dipole selection rule | A symmetry condition for a dipole matrix element; opposite parity is necessary for ideal centrosymmetric electronic states. | Explain why opposite parity is not by itself sufficient. |
| Shelving / metastable state | A state outside the bright cycle that can retain population; an actual lifetime/rate needs more evidence. | Avoid treating an energy diagram as a kinetic prediction. |
| Charge conversion | Change in defect charge through exchange with carriers or reservoirs, possibly induced by illumination. | Track where the electron or hole goes. |
| EPR | Electron paramagnetic resonance, probing electronic spin structure and interactions under appropriate conditions. | Keep optical and magnetic evidence distinct. |
| Hyperfine tensor | Coupling between electronic and nuclear spin; units and sign convention must be stated. | Compute isotropic trace/3 and the traceless remainder. |
| Fermi contact term | Isotropic hyperfine contribution associated with spin density at the nucleus, including applicable core effects. | Avoid inferring it solely from an orbital cartoon. |
| Dipolar hyperfine term | Anisotropic magnetic coupling sensitive to spatial spin-density distribution. | Recover the traceless form under an axial model. |
| Core polarization | Spin polarization of core electrons contributing to hyperfine contact coupling. | Demand an otherwise matched on/off comparison for a causal attribution. |
| Nuclear isotope | Same element, different neutron number; nuclear spin and mass may differ. | Use 29Si, I = 1/2, for ordinary Si hyperfine splitting; 28Si has I = 0. |
| Illustrative model | A model built to expose a mechanism under chosen assumptions. | State which parameters are schematic and which are sourced. |
| Reproduction | A defined attempt to recover a prior result under documented conditions. | State what was matched and what changed. |
| Convergence | Stability of a stated observable against a stated numerical refinement. | Never substitute successful completion for convergence. |

For isotope data and primary paper records see [the source register](../references/sources.md). The table supplies learning definitions; it does not certify that every concept has been independently derived or every calculation completed.
