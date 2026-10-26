# Keeping useful evidence without filling the disk

The public `first_study/` folder is the small reference package. Each exercise contains:

- `provenance/input.json`: the exact input bytes used;
- `provenance/code/`: the package source at execution;
- numerical CSV tables and labeled PNG figures;
- `metrics.json`: derived values and mathematical checks;
- The [public provenance view](../references/public_provenance.md) and [JSON record](../references/public_provenance.json) locate the retained files and record original status, versions, timestamps, and hashes.

Original top-level and per-exercise manifests and logs remain unchanged in the local evidence package. They contain machine paths and commands and are excluded from the public checkout. The public derivative retains their exact hashes and explicitly names the withheld fields; its relative file paths are portable locators, not rewritten original commands. Maintainers can regenerate it with the [exporter](../tools/export_public_provenance.py) using the untouched local evidence as input.

A per-exercise `COMPLETE` status means that this teaching calculation completed its checks. It does not certify DFT convergence, agreement with experiment, or the adequacy of a physical model. Public readers can verify retained artifact hashes; hashes of withheld original records alone do not provide access to those records or an independent execution attestation.

Every new local attempt needs a new folder. Its local `manifest.json` and `execution.log` record completion or typed failure. Do not replace failed results with a later successful result. Forced termination can leave `RUNNING`; preserve it as incomplete. If input validation fails, the attempted input and typed error remain in that run. If the output directory already exists, the command refuses before changing it.

The package uses a temporary, non-global Matplotlib font-cache location. Temporary test fixtures are disposable; actual scientific run evidence is kept.

Before later QE work, assign a fresh run ID, preserve inputs and pseudopotential hashes, choose the executable explicitly, and set a disk budget. Keep large restart/wavefunction files in a named scratch area with a documented retention decision. Never discard the input, log, error diagnosis, or small result tables just because scratch data are removed later. Do not start a long run when its estimated scratch requirement plus an agreed free-space reserve exceeds available space.

Additional runs are ignored by Git by default. This controls future version history, not local retention: ignored files still occupy disk. Review outputs before deliberately including selected small runs or removing scratch data.
