"""Reader/rendering contracts: real source math, tables, links and canonical figures."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from collections import Counter
import copy

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_publication", ROOT / "tools/build_publication.py")
builder = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(builder)


class PublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.publication = builder.Publication()

    def test_real_sources_parse_as_math_and_tables(self):
        for section_id in ("study-notes", "charge-states", "parity-mixing", "hyperfine"):
            path = ROOT / self.publication.by_id[section_id]["path"]
            nodes = list(builder.walk(self.publication.document(path).ast))
            self.assertTrue(any(n.get("t") == "Math" for n in nodes), section_id)
            self.assertTrue(any(n.get("t") == "Table" for n in nodes), section_id)
        parity_ast = self.publication.document(ROOT / "reports/parity_mixing.md").ast
        math = [n["c"][1] for n in builder.walk(parity_ast) if n.get("t") == "Math"]
        self.assertTrue(any("pmatrix" in equation for equation in math))

    def test_figures_resolve_to_three_canonical_run_assets(self):
        images = self.publication.images
        self.assertEqual(len(images), 3)
        self.assertTrue(all(path.is_relative_to(ROOT / "runs/first_study") for path in images))
        self.assertTrue(all(path.suffix == ".png" for path in images))

    def test_site_drafts_retain_scientific_tables_equations_and_figure_targets(self):
        scientific = {"study-notes", "charge-states", "parity-mixing", "hyperfine"}
        for section in self.publication.sections:
            if section["id"] not in scientific:
                continue
            original = self.publication.document(ROOT / section["path"]).ast
            draft = self.publication.document(self.publication.site_paths[section["id"]]).ast
            for kind in ("Table", "Math"):
                def elements(ast):
                    return Counter(json.dumps(n, sort_keys=True, ensure_ascii=False).replace("\u2013", "-").replace("\u2014", "-")
                                   for n in builder.walk(ast) if n.get("t") == kind)
                self.assertFalse(elements(original) - elements(draft), (section["id"], kind))
            def figures(ast):
                return Counter(n["c"][2][0] for n in builder.walk(ast) if n.get("t") == "Image")
            self.assertEqual(figures(original), figures(draft), section["id"])

    def test_editing_html_draft_does_not_change_print_ast(self):
        publication = self.publication
        included = set(publication.by_id)
        section_id = "study-notes"
        typst_dir = ROOT / "build/pdf/typst"
        before = publication.section_ast(section_id, included, "pdf", typst_dir=typst_dir)
        draft = publication.document(publication.site_paths[section_id])
        saved = copy.deepcopy(draft.ast)
        marker = "HTML_ONLY_DRAFT_SENTINEL"
        try:
            draft.ast["blocks"].append({"t": "Para", "c": [{"t": "Str", "c": marker}]})
            web = publication.section_ast(section_id, included, "site")
            after = publication.section_ast(section_id, included, "pdf", typst_dir=typst_dir)
            self.assertIn(marker, json.dumps(web))
            self.assertNotIn(marker, json.dumps(after))
            self.assertEqual(before, after)
        finally:
            draft.ast = saved

    def test_site_links_use_sections_assets_or_public_sources(self):
        included = {s["id"] for s in self.publication.site_sections}
        image_targets = []
        for section_id in included:
            ast = self.publication.section_ast(section_id, included, "site")
            for node in builder.walk(ast):
                if node.get("t") == "Link":
                    target = node["c"][2][0]
                    self.assertTrue(target.startswith(("#", "https://", "http://", "mailto:")), target)
                elif node.get("t") == "Image":
                    image_targets.append(node["c"][2][0])
        self.assertEqual(len(set(image_targets)), 3)
        self.assertTrue(all(t.startswith("assets/figures/runs/first_study/") for t in image_targets))

    def test_archived_sections_remain_available_for_print_without_private_inputs(self):
        visible = {s["id"] for s in self.publication.site_sections}
        for ident in ("reading-map", "later-reading", "sources"):
            self.assertNotIn(ident, visible)
            self.assertIn(ident, self.publication.by_id)
        self.assertFalse(any(p.is_relative_to(ROOT / "personal") for p in self.publication.input_files))

    def test_print_subset_links_do_not_target_absent_sections(self):
        included = {"study-notes", "glossary"}
        ast = self.publication.section_ast("study-notes", included, "pdf", typst_dir=ROOT / "build/pdf/typst")
        targets = [n["c"][2][0] for n in builder.walk(ast) if n.get("t") == "Link"]
        self.assertIn("#glossary", targets)
        self.assertIn("https://github.com/shahpoll/defect_physics/blob/main/reports/charge_states.md", targets)

    def test_native_mathml_and_tables_render_offline(self):
        ast = self.publication.section_ast("parity-mixing", set(self.publication.by_id), "site")
        output = builder.command([self.publication.pandoc, "--from", "json", "--to", "html5", "--mathml"], stdin=json.dumps(ast))
        self.assertIn("<math", output)
        self.assertIn("<mtable", output)
        self.assertIn("<table", output)
        self.assertNotIn("<script", output)
        self.assertNotIn("cdn", output)

    def test_validator_rejects_missing_assets_and_anchors(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "index.html"
            for content in ('<a href="#missing">Link</a>', '<img src="missing.png">', '<p id="same"></p><p id="same"></p>'):
                path.write_text(content)
                with self.assertRaises(builder.BuildError):
                    builder.validate_html(path)
            path.write_text('<p id="good"></p><a href="#good">Link</a>')
            builder.validate_html(path)

    def test_manifest_input_names_are_project_relative(self):
        inputs, digest = self.publication.fingerprint()
        self.assertEqual(len(digest), 64)
        self.assertTrue(all(not Path(name).is_absolute() for name in inputs))
        self.assertIn("Rudimentary_Notes_Gali_n_Maze.md", inputs)

    def test_print_reference_entries_preserve_all_source_cells_and_links(self):
        for section_id, filename in (("glossary", "notes/glossary.md"), ("questions", "notes/questions.md")):
            original = self.publication.document(ROOT / filename).ast
            table = next(n for n in builder.walk(original) if n.get("t") == "Table")
            _, rows = builder.table_rows(table)
            transformed = self.publication.section_ast(section_id, set(self.publication.by_id), "pdf", typst_dir=ROOT / "build/pdf/typst")
            self.assertFalse(any(n.get("t") == "Table" for n in builder.walk(transformed)))
            if section_id == "glossary":
                entries = next(n for n in builder.walk(transformed) if n.get("t") == "DefinitionList")["c"]
                self.assertEqual(len(entries), len(rows))
            else:
                entries = [n for n in builder.walk(transformed) if n.get("t") == "Header" and n["c"][1][0].startswith("questions--entry-")]
                self.assertEqual(len(entries), len(rows))
            # Compare every complete source cell with the plain-text print view,
            # so long definitions/questions cannot silently lose a clause.
            output = builder.command([self.publication.pandoc, "--from", "json", "--to", "plain", "--wrap=none"], stdin=json.dumps(transformed))
            normalized = " ".join(output.split())
            for row in rows:
                for cell in row:
                    cell_ast = {**original, "blocks": cell[4]}
                    cell_text = builder.command([self.publication.pandoc, "--from", "json", "--to", "plain", "--wrap=none"], stdin=json.dumps(cell_ast))
                    self.assertIn(" ".join(cell_text.split()), normalized)
            expected_labels = Counter(json.dumps(n["c"][1], sort_keys=True) for n in builder.walk(table) if n.get("t") == "Link")
            actual_labels = Counter(json.dumps(n["c"][1], sort_keys=True) for n in builder.walk(transformed) if n.get("t") == "Link")
            self.assertFalse(expected_labels - actual_labels)

    def test_print_keeps_numerical_tables_and_resolves_all_internal_links(self):
        included = set(self.publication.config["pdfs"]["study-pack"]["sections"])
        asts = [self.publication.section_ast(section_id, included, "pdf", typst_dir=ROOT / "build/pdf/typst") for section_id in included]
        anchors = {n["c"][1][0] for ast in asts for n in builder.walk(ast) if n.get("t") == "Header"}
        for ast in asts:
            for node in builder.walk(ast):
                if node.get("t") == "Link" and node["c"][2][0].startswith("#"):
                    self.assertIn(node["c"][2][0][1:], anchors)
        for section_id in ("charge-states", "parity-mixing", "hyperfine"):
            ast = self.publication.section_ast(section_id, included, "pdf", typst_dir=ROOT / "build/pdf/typst")
            self.assertTrue(any(n.get("t") == "Table" for n in builder.walk(ast)))


if __name__ == "__main__":
    unittest.main()
