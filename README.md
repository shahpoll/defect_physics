# Defect physics: an open study notebook

[![Build and publish](https://github.com/shahpoll/defect_physics/actions/workflows/publication.yml/badge.svg)](https://github.com/shahpoll/defect_physics/actions/workflows/publication.yml)

Paper-reading notes, questions, and small reproducible calculations while learning point-defect physics. The first study is **Gali and Maze (2013), on the silicon-vacancy center in diamond**. This is an evolving student notebook for discussion and correction, rather than a finished paper or a claim of new first-principles results.

**[Read the scrolling website](https://shahpoll.github.io/defect_physics/)** · **[Printable notes](https://shahpoll.github.io/defect_physics/downloads/study-notes.pdf)** · **[Full printable study pack](https://shahpoll.github.io/defect_physics/downloads/study-pack.pdf)**

## Start here

- [Main reading notes](Rudimentary_Notes_Gali_n_Maze.md): the paper's question, background physics, evidence, and limitations, in a working-study voice.
- [Supervisor brief](reports/supervisor_brief.md): a short entry point to the study and its results.
- [Glossary](notes/glossary.md), [reading map](notes/reading_map.md), and [questions](notes/questions.md): what I need to understand next.
- [Sources and versions](references/sources.md), [bibliography](references/bibliography.bib), and [selected follow-up reading](reports/literature_followup.md).

The source is [Gali and Maze, Physical Review B 88, 235205 (2013)](https://doi.org/10.1103/PhysRevB.88.235205). Page references use the [eight-page arXiv v2 manuscript](https://arxiv.org/pdf/1310.2137v2), not the journal layout. Draft first-person wording is a study aid, not evidence that every derivation has been mastered.

## What has been calculated

| Exercise | Purpose | Boundary |
|---|---|---|
| [Charge-state stability](reports/charge_states.md) | Reconstruct relative formation-energy lines and their lower envelope | Uses published crossings; no new DFT or absolute formation energies |
| [Parity and mixing](reports/parity_mixing.md) | Test a symmetry condition and diagonalize a small teaching Hamiltonian | Dimensionless model; no physical strain, rate, or lifetime prediction |
| [Hyperfine comparison](reports/hyperfine.md) | Decompose reported tensors and quantify agreement with experiment | Reanalysis of Table I; no new spin-density calculation |

The carbon/silicon comparison retains a useful mismatch: the newer theoretical column is closer for carbon but farther from experiment for silicon. The reports make both visible. Scientific claims, author proposals, explanatory models, and student questions are distinguishable.

Selected results live in `runs/first_study/`: figures, CSV tables, metrics, and exact input/code snapshots. [Public provenance](references/public_provenance.md) records their hashes and explains which local details were withheld. [The original test record](reports/verification.txt) documents the first study; subsequent checks run in GitHub Actions.

## Reproduce the calculations

Use **Python 3.13**. Create an isolated environment and install the pinned dependencies:

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt -r requirements-publication.txt
make test
.venv/bin/python run_study.py
```

The last command creates a new dated run folder. Existing run folders are refused, preserving previous attempts. For a single exercise:

```sh
PYTHONPATH=src .venv/bin/python -m siv_study.charge_states --input data/charge_states.json --output runs/my_charge_trial
```

Replace `charge_states` and its input name with `parity_mixing` or `hyperfine` for the others. See [the run policy](runs/README.md). Testing new inputs does not silently replace the published baseline; update the relevant report and select a new dated reference deliberately.

## Print after a reading session

Install the **Typst CLI 0.14.2** once if unavailable. It is already installed on the study's Mac. Pandoc is included in the publication dependency above; no separate Pandoc install is needed.

After editing the Markdown:

```sh
make pdf
```

Open `build/pdf/study-notes.pdf` for the notes and glossary, or `build/pdf/study-pack.pdf` for the notes, exercise reports, and supporting material. Both are A4 documents built from the Markdown, with typeset equations and the existing Python figures. There is no separate PDF source to edit.

Build the website and PDFs together:

```sh
make all
```

Preview the website:

```sh
make preview
```

Visit `http://localhost:8000`; stop the preview with Control-C. The reader uses native MathML, local styling, and no remote math renderer or web-font service.

## What goes into GitHub

**Track sources and small reference evidence.** Markdown is the content source. Figures are stored once, beside the Python reference results; site/PDF builds read those files. Generated HTML, PDFs, caches, and build-time asset copies stay under ignored `build/`.

After a push to `main`, GitHub Actions tests the project, builds the reader and PDFs, and deploys them to GitHub Pages. The PDF links above provide compiled copies without repeatedly committing binary PDFs. Selected milestone PDFs can later be attached to tagged GitHub Releases; ordinary reading sessions do not need releases.

Local machine records, original private execution logs, large future simulation outputs, and publisher PDFs are excluded. The original local evidence is unchanged. The publication export documents omissions instead of presenting rewritten commands as original execution records.

## Next study step

Discuss the notes and question log, then choose deeper symmetry/vibronic reading or [a small bulk-diamond QE benchmark](reports/qe_next_step.md). The first study ran Python only. A successful small model does not establish the accuracy or feasibility of a later defect-supercell calculation.
