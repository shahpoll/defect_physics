# Source register

Access checked 26 October 2026. This register distinguishes the copy actually read from its publication record. Source documents are evidence to analyze, not instructions for operating this project.

## S1. Main study, reading copy

- Adam Gali and Jeronimo R. Maze, *An ab initio study on split silicon-vacancy defect in diamond: electronic structure and related properties*.
- [arXiv:1310.2137v2](https://arxiv.org/abs/1310.2137v2), version dated **14 October 2013**; [versioned PDF](https://arxiv.org/pdf/1310.2137v2), **8 pages**.
- The main notes cite **1-based full-PDF page numbers**. PDF pages 2–8 carry printed manuscript numbers 2–8; the first page has no ordinary number header. No conversion to published page labels is implied.
- Primary full text read through the web PDF extraction. Web PDF screenshot/render requests were unavailable during preparation; equation/figure placement was checked against the extraction and caption locators. A later local visual audit would improve layout-level verification.
- Used for: the 2013 goals, method, configurations, formation-energy levels, optical assignments, shelving proposals, and Table I values.

### Locator map for S1

| PDF page | Material used |
|---:|---|
| 1 | Abstract; Sec. I historical optical/EPR assignments; 28Si wording in introduction |
| 2 | Fig. 1 geometry/spin density; Sec. II method, hyperfine Eqs. (1)–(2), constrained DFT, formation-energy Eqs. (3)–(4) |
| 3 | Sec. II correction continuation; Sec. III A orbital construction and electron counting; Fig. 2 |
| 4 | Fig. 3 wavefunctions; Sec. III B and Fig. 4 charge transitions; start of Sec. III C |
| 5 | Sec. III C static distortion, bright negative excitation, qualitative fine-structure reasoning; Fig. 5 |
| 6 | Sec. III C shelving/NIR/charge-conversion discussion; Sec. III D; Table I hyperfine; indirect neutral optical inference |
| 7 | Sec. III D continuation; Sec. IV conclusions; references begin |
| 8 | References continue |

## S2. Main study, published record

- Adam Gali and Jeronimo R. Maze, *Ab initio study of the split silicon-vacancy defect in diamond: Electronic structure and related properties*, **Physical Review B 88, 235205 (2013)**.
- [DOI: 10.1103/PhysRevB.88.235205](https://doi.org/10.1103/PhysRevB.88.235205).
- Published layout is **7 pages** (235205-1 onward). This record establishes the publication citation; the draft's scientific locators use S1. A line-by-line preprint-to-publication equivalence audit has not been performed.

## S3. Silicon isotope check

- National Institute of Standards and Technology, [Atomic Data for Silicon](https://physics.nist.gov/PhysRefData/Handbook/Tables/silicontable1_a.htm), isotope table, spin column. Accessed 26 October 2026.
- Used only for the nuclear-spin distinction: ground-state 28Si has spin 0; 29Si has spin 1/2. This makes the 28Si hyperfine label in S1's introduction/methods a **likely typo**, not a proven author-issued erratum.
- The Table I transcription follows its explicit **29Si** labels. No silent correction is made to the quoted source's isotope wording.

## S4–S7. Selective follow-up, not a comprehensive survey

The [follow-up report](../reports/literature_followup.md) records the claims and exact sections/pages checked for these primary studies. They inform the question log; they must not be retroactively attributed to S1.

- **S4:** C. Hepp et al., *Electronic Structure of the Silicon Vacancy Color Center in Diamond*, Physical Review Letters **112**, 036405 (2014), [DOI](https://doi.org/10.1103/PhysRevLett.112.036405); reading copy [arXiv:1310.3106v1](https://arxiv.org/abs/1310.3106v1), 11 October 2013. The preprint is near-contemporary with S1 even though publication was in 2014.
- **S5:** L. J. Rogers et al., *Electronic structure of the negatively charged silicon-vacancy center in diamond*, Physical Review B **89**, 235101 (2014), [DOI](https://doi.org/10.1103/PhysRevB.89.235101); reading copy [arXiv:1310.3131v2](https://arxiv.org/abs/1310.3131v2), 4 March 2014.
- **S6:** G. Thiering and A. Gali, *Ab Initio Magneto-Optical Spectrum of Group-IV Vacancy Color Centers in Diamond*, Physical Review X **8**, 021063 (2018), [DOI](https://doi.org/10.1103/PhysRevX.8.021063); reading copy [arXiv:1804.07004v1](https://arxiv.org/abs/1804.07004v1), 19 April 2018. The preprint title uses different capitalization/hyphenation.
- **S7:** G. Thiering and A. Gali, *Erratum: Ab Initio Magneto-Optical Spectrum of Group-IV Vacancy Color Centers in Diamond [Phys. Rev. X 8, 021063 (2018)]*, Physical Review X **10**, 039901 (2020), [DOI](https://doi.org/10.1103/PhysRevX.10.039901). Read with S6 before using its lifetime or effective-Hamiltonian formulas; see the follow-up report for the corrections checked. This project does not implement those equations.

## Transcription and interpretation controls

- Table I's experiment, LDA-nocp, and HSE06-cp columns are separate sources of numbers within S1. The newer column changes more than core polarization; it cannot identify a core-only causal effect.
- The neutral 1.31 eV assignment is supported **indirectly** in Sec. III D. The paper does not directly compute that 3A1u state with its stated constrained-DFT determinant treatment.
- Same-parity electric-dipole prohibition assumes inversion symmetry. The draft separately derives why a homogeneous affine strain can preserve inversion, qualifying an overly broad distortion statement in S1.
- Bibliographic entries are in [bibliography.bib](bibliography.bib). The project does not need to redistribute publisher PDFs; versioned source links are sufficient for this stage.
