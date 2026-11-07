# HTML reading drafts

- `content.json`: `site_path` selects these six compact working-note sources for HTML.
- `path`: earlier Markdown, retained separately for a later manual print revision.
- Links and figures resolve relative to the original `path`; keep those targets.
- Figures still come from `runs/first_study/`; no additional figure sources.
- Rebuild HTML: `make site`. Preview: `make preview` → <http://localhost:8000>.
- `site_enabled: false`: section omitted from HTML; print inclusion stays separate.
- Three supporting HTML drafts are archived locally, excluded from Git and publication.
- `site_downloads_enabled: false`: no cached PDFs copied or linked by the HTML build.
- GitHub Actions tests and publishes HTML only; it does not generate PDFs or new study runs.
- Read via the [website](https://shahpoll.github.io/defect_physics/). GitHub's Markdown view uses a different relative-link base from this pipeline.
