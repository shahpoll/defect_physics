# Reading notes

Source: Adam Gali & Jeronimo R. Maze, [PRB 88, 235205 (2013)](https://doi.org/10.1103/PhysRevB.88.235205). Reading copy: [arXiv:1310.2137v2](https://arxiv.org/pdf/1310.2137v2), 14 October 2013, 8 PDF pages. Page refs below: arXiv v2, 1-based; published layout: 7 pages.

DC - direct calculation, not experimental proof. IS - indirect support. PR - proposed mechanism/assignment. MU - understanding to check.

## 1. Questions behind the paper

- Which SiV electronic states explain the optical and magnetic signals?
  - Historical competing assignments of the Si-related optical center.
  - 1.68 eV line → negative SiV?
  - 1.31 eV line → neutral SiV?
  - KUL1 EPR signal → neutral SiV?
  - Origin of dark/shelving states?
  - [Sec. I, p. 1; Sec. III opening, p. 3.]
- Needed connection: atomic structure → electron count → spin/symmetry → measured transition. One optical line alone is insufficient.
- Keep two questions separate:
  1. Which assignment has support?
  2. Which microscopic mechanism was actually calculated?
- Evidence strength varies across the conclusions; neutral optical assignment needs particular care (§9).

## 2. Split-vacancy picture

- DC: substitutional Si beside a C vacancy → relaxed Si near the midpoint of two vacant C sites.
  - Six neighboring C atoms; axis along diamond ⟨111⟩.
  - Ideal symmetry: D3d, with inversion.
  - [Sec. III A, p. 3; Fig. 1, p. 2.]
- Sketch: remove two adjacent C atoms; put Si between their old sites.
  - Not a normal substitutional Si plus only one missing site in the final geometry.
  - **To learn:** sketch the structure and mark its inversion center.
- Six C dangling bonds → defect-molecule basis.
  - Symmetry selects combinations that can mix with Si orbitals.
  - eg combinations: C dangling-bond character; other symmetry channels can include Si.
  - A Si-related defect orbital need not be concentrated on Si.
  - [Sec. III A, p. 3; Figs. 2-3, pp. 3-4.]

## 3. Electron counting

- Neutral reduced basis: 6 dangling-bond electrons + 4 from Si = 10 electrons.
- Low-energy occupation:

\[
a_{1g}^{2}a_{2u}^{2}e_u^{4}e_g^{2}.
\]

- Exponent = electron count, not number of orbital functions.
- An e level: 2 spatial functions × 2 spins → capacity 4 electrons.
- Neutral eg² ground configuration: triplet favored; added electrons fill the same manifold.
- [Sec. III A, p. 3; Secs. III C-D, pp. 4-6.]

| Charge state | Electrons in this defect basis | Active occupation | Spin in the paper's ground-state description |
|---|---:|---|---|
| SiV0 | 10 | eu4 eg2 | S = 1 |
| SiV− | 11 | eu4 eg3 | S = 1/2 |
| SiV2− | 12 | eu4 eg4 | S = 0, closed shell |

- Counts apply to this reduced basis, not all supercell electrons.
- Negative charge = added electron.
  - Hole picture: full e manifold → no holes; eg³ → one hole.
  - State which picture is being used.
- **To learn:** draw occupations. Counting alone gives no formation energy, stability proof, or optical wavelength.

## 4. Orbital labels vs many-electron terms

- Lowercase eg: 2-dimensional one-electron orbital representation; two orbital components.
- Term superscript, e.g. 2Eg: spin multiplicity 2S + 1; 2 → S = 1/2.
- Uppercase A/E: many-electron spatial symmetry.
  - A → orbital singlet; E → orbital doublet.
- g/u: even/odd inversion parity; not ground/upper.
- Examples in ideal D3d:
  - Neutral 3A2g: spin triplet, orbital singlet.
  - Negative 2Eg: spin doublet, orbitally degenerate.
  - Occupancy diagram ≠ many-electron term diagram.
  - [Sec. III A, p. 3; Sec. III C, pp. 4-5; Sec. III D, p. 6.]
- **To learn:** construct allowed terms from antisymmetrized electron states.
  - Hund's rule: first guide to spin ordering; full symmetry construction and energy calculation still needed.

## 5. Four different energies

| Quantity | What changes? | What it tells me |
|---|---|---|
| One-electron orbital energy | An eigenvalue in a specified electronic calculation | Location/character of an orbital relative to a chosen reference |
| Many-electron excitation energy | Electronic state, with the same overall charge | Cost of an excitation under specified geometric conditions |
| Optical ZPL energy | Ground and excited electronic states at their relaxed minima | An electronic transition energy, with vibrational qualifications |
| Thermal charge-transition level | Charge state and electron exchange with a reservoir | Fermi level where relaxed defect formation energies cross |

- Optical excitation: electron rearrangement; total defect charge need not change.
- Charge conversion: charge exchange with a reservoir/host.
  - Photon-triggered conversion is possible; optical excitation energy ≠ thermal charge-transition level.
- Configuration-coordinate sketch:
  - Qg/Qe: ground-/excited-state equilibrium geometries.
  - Eg(Q)/Ee(Q): ground-/excited-state energy surfaces at geometry Q.
  - Vertical absorption: Ee(Qg) − Eg(Qg).
  - Vertical emission: Ee(Qe) − Eg(Qe).
  - Relaxed minima: Ee(Qe) − Eg(Qg), electronic approximation to ZPL.
  - **Missing input for a fuller ZPL:** zero-point vibrational corrections.
  - **To learn:** draw both surfaces and mark the relaxation energies.
- Paper method:
  - Constrained DFT → excited-state energies and nuclear relaxation.
  - Relaxed total energies + charged-cell corrections → charge-transition levels.
  - Not read from orbital eigenvalues.
  - [Sec. II, p. 2, Eqs. (3)-(4); Sec. III B, p. 4.]
- Neutral occupied eg: near VBM + 0.3 eV; eu: resonant below VBM.
  - Subtracting these orbital positions does not establish the observed ZPL.
  - [Sec. III A, p. 3.]
- Calculation/plot requirement: label energy type, units, charge state, and reference.

## 6. Valence-band resonance

- Defect character can survive energetic overlap with host bands.
  - “Resonant with valence band” ≠ irrelevant or fully delocalized.
- DC: eu defect resonance in valence band; localized eg gap state.
  - Defect also perturbs the valence-band edge → symmetry-resolved states involved in excitations.
  - [Sec. III A, p. 3; Figs. 2-3, pp. 3-4.]
- Check energies **and spatial character**:
  - DOS peak alone → insufficient evidence for localization.
  - Localized orbital alone → insufficient evidence for optical transition.
  - **Needed in future calculations:** orbital plots, projections, charge state, occupancy.

## 7. Bright SiV− transition

- DC: eu → eg promotion; bright 2Eu excited state above 2Eg ground state.
  - Relaxed optical energy: ≈1.72 eV.
  - Assigned experimental line: 1.68 eV.
  - Excitation-related relaxation energy: ≈0.03 eV.
  - [Sec. III C, p. 5; Fig. 5(a,c), p. 5.]
- Support: appropriate symmetry + total-energy difference + experimental comparison.
  - Stronger than matching an orbital eigenvalue to a line.
  - Agreement here supplies no universal error bar for other calculations.
- Author interpretation:
  - Similar charge distributions → small structural relaxation, weak vibrational sideband.
  - Different Si orbital contributions → qualitative explanation of ground-/excited-state fine-structure splitting differences.
  - **Paper limit:** no complete spin-orbit/vibronic spectrum.
  - [Sec. III C, p. 5.]

## 8. Shelving states and parity

- Shelving state: population outside the main bright optical cycle.
  - “Dark” need not mean different spin multiplicity.
- DC: excitations involving perturbed valence-band-edge states → additional same-spin states.
  - PR: shelving channels for SiV−.
  - Same parity as ground state in ideal inversion symmetry → electric-dipole emission to ground state forbidden.
  - [Sec. III C, pp. 5-6; Fig. 5(b,c), p. 5.]
- MU: electric-dipole operator is inversion-odd.
  - ⟨f|r|i⟩: two even states × odd operator → odd integrand → zero integral in inversion symmetry.
  - Opposite parity: necessary, not sufficient.
  - Full representation, polarization, spin, matrix element still matter.
  - Higher-order, phonon-assisted, and symmetry-breaking processes need separate treatment.
- PR: weak NIR feature ↔ possible distorted shelving-state transition.
  - **Missing input:** measured matrix element / calculated lifetime for this assignment.
  - [Sec. III C, p. 6.]
- Distortion caveat:
  - Homogeneous strain r → F r preserves r/−r pairing about the transformed center; F = deformation matrix.
  - Rotational symmetry can decrease while inversion survives.
  - Parity mixing requires inversion breaking; not every strain field qualifies.
  - Toy model tests this condition; **missing microscopic input** for a real SiV strain coefficient.
  - [Parity calculation](reports/parity_mixing.md).

## 9. Neutral SiV: indirect optical assignment

- DC: 3A2g ground state; calculated hyperfine pattern supports KUL1 comparison.
- IS: proposed 3A1u → 3A2g assignment for the 1.31 eV line.
  - **Paper limit:** relevant 3A1u state not directly representable by the single-determinant constrained-DFT treatment.
  - Accessible 3Eu excitation: ≈1.63 eV, well above 1.31 eV.
  - Exclusion of that alternative + experimental polarization reasoning → support for 3A1u.
  - Conditional on candidate-state picture and experimental interpretation.
  - Not a direct reproduction of the neutral 1.31 eV ZPL.
  - [Sec. III D, p. 6.]
- **Question:** which calculation directly tests the missing state, beyond excluding an alternative?
- PR: neutral metastable state near 1.27 eV; symmetry breaking and charge conversion.
  - Mechanisms to investigate; no complete predictive kinetic model.
  - [Sec. III D, pp. 6-7.]

## 10. Hyperfine: agreement and mismatch

- Hyperfine tensor: coupling of electronic and nuclear spins.
  - Isotropic part = trace/3; anisotropic part = traceless remainder.
  - Contact/dipolar contributions probe different aspects of spin density.
  - Appreciable contact coupling possible even if simple orbital picture places most unpaired density elsewhere.
  - [Sec. II, p. 2, Eqs. (1)-(2); Sec. III D, p. 6.]
- Table I, p. 6; pairs below = Aparallel/Aperpendicular, MHz:
  - 13C: experiment 66.2/30.2; LDA-nocp 51/12; HSE06-cp 68/28 → newer column closer.
  - 29Si: experiment 76.3/78.9; LDA-nocp 78/82; HSE06-cp 92/97 → newer column worse.
  - No uniform improvement.
- Isotope discrepancy:
  - Introduction/methods: 28Si; Table I/discussion: 29Si.
  - Likely label typo: 28Si has I = 0; no ordinary spin hyperfine splitting of this kind. 29Si has I = 1/2.
  - [NIST spin column](https://physics.nist.gov/PhysRefData/Handbook/Tables/silicontable1_a.htm).
  - Retain discrepancy; no silent source correction.
  - [Sec. I, p. 1; Sec. II, p. 2; Sec. III D and Table I, p. 6.]
- Core polarization emphasized for C; comparison also changes functional and supercell size.
  - **Missing matched comparison:** same settings, core contribution on/off.
  - Table does not isolate core polarization as sole cause.
- [Our hyperfine comparison](reports/hyperfine.md): table analysis, no new hyperfine DFT.

## 11. Method settings and limits

- Paper settings below; not a ready-made Mac/QE input. [Sec. II, pp. 2-3.]

| Method ingredient | What the paper uses | What I should remember |
|---|---|---|
| Code and core treatment | VASP 5.3.2, PAW; projectors supplied with version 5.2 | This is distinct from choosing a QE pseudopotential. |
| Main functional | HSE06, 25% mixing, screening 0.2 Å−1 | PBE is also used in establishing bulk settings; it is a different approximation. |
| Defect-cell sampling | The paper's “512-atom supercell” scale, Γ only | Treat this as the nominal host-supercell scale, not a claim that every defect configuration literally has 512 nuclei after removal/insertion. |
| Bulk primitive-cell sampling | 8 × 8 × 8; PBE total-energy check at 12 × 12 × 12 | The bulk check is separate from defect Γ sampling and is not a convergence proof for every defect observable. |
| Standard cutoffs | 370 / 740 eV for wavefunctions / charge density | VASP dataset/code-dependent choices; not transferable QE cutoffs. |
| Hyperfine cutoffs | 500 / 1000 eV | The hyperfine observable uses a stricter basis setting. |
| Geometry relaxation | Constant volume; forces below 0.01 eV/Å | Geometry convergence is distinct from electronic, cell-size, and excitation convergence. |
| Charged cells | Potential alignment and Lany-Zunger charge-correction scheme, paper Ref. 33 | Keep the correction convention with the total energies and reference. |
| Excitations | Constrained DFT | Check whether the desired term can be represented by the chosen determinant. |

- Future QE work needs compatible pseudopotentials and observable-specific convergence checks.
- **Paper limit:** static distortions allowed; dynamic vibration-electronic coupling absent.
  - Lower-symmetry relaxed geometry does not establish full dynamic Jahn-Teller behavior or optical fine structure.
  - [Sec. III C, pp. 4-5.]
- Keep separate:
  - **To learn:** my concept gaps.
  - **Paper limit:** this 2013 method's boundary.
  - **Possible research question:** needs later-literature check.
  - Dynamic Jahn-Teller: limitation here; subsequent work exists. Check later work before any novelty claim.
- Further boundaries:
  - Formation-energy diagram → equilibrium thermodynamics; no optical pumping dynamics.
  - Proposed shelving pathway → no transition rates.
  - Large cell → reduced, not proven absent, finite-size error.
  - QE/PBE → different model from HSE06/VASP, not exact reproduction.

## 12. What to use for discussion

- Three small calculations; reports retain executed-run evidence, checks, limits:
  1. [Charge states](reports/charge_states.md): reconstruct crossing lines from published transition levels.
  2. [Parity mixing](reports/parity_mixing.md): deliberately simplified Hamiltonian.
  3. [Hyperfine](reports/hyperfine.md): quantify Table I agreement/mismatch.
- **To learn:** underlying derivations; executed scripts do not establish mastery.
- Discussion chain: question → assumptions → calculation/paper evidence → result → limits → next question.
  - Traceable disagreement is useful.
  - Illustrative model ≠ new physics; plot quality cannot supply a missing physical ingredient.
- Next reading: [glossary](notes/glossary.md), [question log](notes/questions.md).
- Meeting entry: [supervisor brief](reports/supervisor_brief.md).
- Status: present understanding, open to correction.
