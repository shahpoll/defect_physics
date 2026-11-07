# Defect physics: working notes

[![Build and publish](https://github.com/shahpoll/defect_physics/actions/workflows/publication.yml/badge.svg)](https://github.com/shahpoll/defect_physics/actions/workflows/publication.yml)

Reading notes, questions, and three small Python exercises while learning point-defect physics. First paper: **Gali and Maze (2013), silicon-vacancy center in diamond**. Work in progress; present understanding, assumptions, and gaps kept visible.

**[Open the reading website](https://shahpoll.github.io/defect_physics/)**

## Reading

- [Reading notes](https://shahpoll.github.io/defect_physics/#study-notes)
- [Exercise 1: charge states](https://shahpoll.github.io/defect_physics/#charge-states)
- [Exercise 2: parity and mixing](https://shahpoll.github.io/defect_physics/#parity-mixing)
- [Exercise 3: hyperfine comparison](https://shahpoll.github.io/defect_physics/#hyperfine)
- [Working glossary](https://shahpoll.github.io/defect_physics/#glossary)
- [Questions for discussion](https://shahpoll.github.io/defect_physics/#questions)

Source: [Gali and Maze, Physical Review B 88, 235205 (2013)](https://doi.org/10.1103/PhysRevB.88.235205). Page references use the [8-page arXiv v2 manuscript](https://arxiv.org/pdf/1310.2137v2).

## Calculations already in the notebook

| Exercise | Calculation | Limit |
|---|---|---|
| Charge states | Relative formation-energy lines and lower envelope | Published crossings; arbitrary common offset; no new DFT or absolute formation energies |
| Parity and mixing | Parity test and two-state diagonalization | Dimensionless teaching model; no physical strain coefficient, rate, or lifetime |
| Hyperfine | Table I tensor decomposition and component comparison | Published constants; no new spin-density or EPR calculation |

- Carbon: newer theory column closer to experiment. Silicon: worse agreement. Both retained.
- Reference figures, CSVs, metrics, and exact input/code snapshots: [runs/first_study](runs/first_study/).
- Evidence hashes and local-record omissions: [public provenance](references/public_provenance.md).
- Original mathematical checks: [test record](reports/verification.txt). Current checks run in GitHub Actions.

## Edit and preview HTML

Use **Python 3.13** with the pinned requirements:

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt -r requirements-publication.txt
make test
make preview
```

Open <http://localhost:8000>. Stop with Control-C. After editing, rebuild with `make site` and reload; the preview does not watch files.

- Edit the six Markdown drafts in [publication/web-notes](publication/web-notes/).
- Section selection: [publication/content.json](publication/content.json), using `site_path`.
- Layout: [publication/site.html](publication/site.html) and [publication/study.css](publication/study.css).
- Links and figures in each draft resolve from its original `path` in the config. Read the result in the website; GitHub's Markdown view uses a different relative-link base.
- Figures come from the existing Python reference outputs. No duplicate figure source.
- Native MathML; local styles; no external math renderer or web fonts.

The earlier root/report Markdown sources remain separate from these HTML drafts. Three supporting HTML drafts are archived locally and excluded from Git. They are omitted from the website.

## Reproduce the calculations

After setup, create a new study run:

```sh
.venv/bin/python run_study.py
```

Existing output folders are refused. To run one exercise:

```sh
PYTHONPATH=src .venv/bin/python -m siv_study.charge_states --input data/charge_states.json --output runs/my_charge_trial
```

Replace `charge_states` and its input with `parity_mixing` or `hyperfine` as needed. See [run policy](runs/README.md). New trials do not replace the selected reference evidence.

## Publication and printing

- Push to `main`: tests, reference-hash verification, HTML build, GitHub Pages deployment.
- This presentation revision does not create new study runs or compile/publish PDFs in CI.
- PDF downloads are disabled, including cached copies. Print wording will be revised separately.
- The manual `make pdf` pipeline is retained for a later print build; it uses the earlier Markdown sources and requires Typst CLI **0.14.2**. It does not yet reflect the current HTML wording.
- Generated HTML/PDFs, environments, caches, private local records, publisher PDFs, and large simulation outputs stay excluded from Git.

## Next study step

Discuss the notes and questions, then choose more symmetry/vibronic reading or [a bulk-diamond QE benchmark](reports/qe_next_step.md). The first study uses Python. Defect-cell cost and accuracy need separate checks.
