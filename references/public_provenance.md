# Public provenance for the first study

This is a **curated derivative of local execution evidence**, not a new execution or a rewritten original manifest. Original manifests and logs remain unchanged locally. Their machine paths and commands are not published.

The [public JSON record](public_provenance.json) contains exact original-manifest hashes, original timestamps/status, version information, retained input/code snapshots, and hashes for the published results. Relative paths in that record locate public files; they do not claim to be the original invocation paths.

Source study: **first_study**, status **COMPLETE**, finished `2026-10-26T17:30:57.036995+00:00`.

| Exercise | Status | Retained run artifacts |
|---|---|---:|
| [charge_states](../runs/first_study/charge_states/metrics.json) | COMPLETE | 10 |
| [parity_mixing](../runs/first_study/parity_mixing/metrics.json) | COMPLETE | 11 |
| [hyperfine](../runs/first_study/hyperfine/metrics.json) | COMPLETE | 10 |

## What can be checked from this repository

The published CSVs, figures, metrics, and input/code snapshots can be checked against `published_files_sha256` in the JSON record. The exporter rejects modified public artifacts or source snapshots that do not match their recorded hashes. The original study runner and public input configurations also match the execution evidence.

## What is withheld

Original commands, working directories, executable locations, requested local input/output paths, installation records and uncurated logs are local-only. Withheld run artifacts are named as relative identifiers with hashes and an explicit withholding reason, rather than linked as available downloads.

A hash of an unpublished original is an identity commitment, not a way for a public reader to inspect that original or independently attest execution. The published view makes its redactions explicit and preserves the distinction between original evidence and a portable presentation.

## Interpretation

A COMPLETE teaching exercise passed its specified mathematical checks. It does not establish a new electronic-structure calculation, experimental measurement, converged DFT result, or independent validation of the paper. The original local manifests were not edited to make this public view.
