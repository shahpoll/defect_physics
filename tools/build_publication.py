#!/usr/bin/env python3
"""Build the reading site and PDFs from canonical Markdown, without Node or network."""
from __future__ import annotations

import argparse
import copy
import hashlib
import html
from html.parser import HTMLParser
import importlib.metadata
import json
import os
from pathlib import Path
import re
import shutil
import string
import subprocess
import sys
import tempfile
from urllib.parse import quote, unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
READER = "markdown+pipe_tables+tex_math_single_backslash"


class BuildError(RuntimeError):
    """A missing or unresolved publication input, or an unsuccessful engine."""


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def table_rows(table: dict) -> tuple[list, list]:
    """Read the unmerged pipe-table cells in Pandoc's table AST."""
    content = table["c"]
    head = content[3][1]
    if len(head) != 1 or content[5][1]:
        raise BuildError("Print-entry tables require one header row and no footer rows.")
    rows = []
    for body in content[4]:
        rows.extend(body[2])
        rows.extend(body[3])
    cells = [head[0][1]] + [row[1] for row in rows]
    if any(cell[2:4] != [1, 1] for row in cells for cell in row):
        raise BuildError("Merged table cells need an explicit print-layout treatment.")
    return cells[0], cells[1:]


def cell_inlines(cell: list) -> list:
    """The source tables use inline cells; retain the full inline structures."""
    inlines = []
    for index, block in enumerate(cell[4]):
        if block["t"] not in {"Plain", "Para"}:
            raise BuildError("A print-entry label must contain inline text.")
        if index:
            inlines.append({"t": "Space"})
        inlines.extend(copy.deepcopy(block["c"]))
    return inlines


def labeled_cell(label: list, cell: list) -> list[dict]:
    blocks = copy.deepcopy(cell[4])
    prefix = [{"t": "Strong", "c": cell_inlines(label)}, {"t": "Str", "c": ":"}, {"t": "Space"}]
    if blocks and blocks[0]["t"] in {"Plain", "Para"}:
        blocks[0] = {"t": "Para", "c": prefix + blocks[0]["c"]}
    else:
        blocks.insert(0, {"t": "Para", "c": prefix})
    return blocks


def print_entries(ast: dict, section_id: str) -> dict:
    """Reflow reference tables for print without another content source.

    Every source body cell and its links survive; column headings become labels.
    Numerical comparison tables elsewhere remain real tables.
    """
    if section_id not in {"glossary", "questions"}:
        return ast
    blocks = []
    for block in ast["blocks"]:
        if block["t"] != "Table":
            blocks.append(block)
            continue
        labels, rows = table_rows(block)
        if section_id == "glossary":
            definitions = []
            for row in rows:
                description = []
                for label, cell in zip(labels[1:], row[1:]):
                    description.extend(labeled_cell(label, cell))
                definitions.append([cell_inlines(row[0]), [description]])
            blocks.append({"t": "DefinitionList", "c": definitions})
        else:
            for number, row in enumerate(rows, start=1):
                blocks.append({"t": "Header", "c": [2, [f"questions--entry-{number}", [], []], cell_inlines(row[0])]})
                for label, cell in zip(labels[1:], row[1:]):
                    blocks.extend(labeled_cell(label, cell))
    ast["blocks"] = blocks
    return ast


def command(argv: list[str], *, stdin: str | None = None, cwd: Path = ROOT) -> str:
    result = subprocess.run(argv, input=stdin, text=True, capture_output=True, cwd=cwd)
    if result.returncode:
        raise BuildError(f"{Path(argv[0]).name} failed:\n{result.stderr.strip()}")
    return result.stdout


def pandoc_path() -> str:
    try:
        import pypandoc
        return pypandoc.get_pandoc_path()
    except (ImportError, OSError) as exc:
        raise BuildError("Install the pinned publication requirements in .venv first.") from exc


class Document:
    def __init__(self, path: Path, pandoc: str):
        self.path = path
        self.ast = json.loads(command([pandoc, "--from", READER, "--to", "json"], stdin=path.read_text()))
        self.anchors = {node["c"][1][0] for node in walk(self.ast) if node.get("t") == "Header"}


class Publication:
    def __init__(self, root: Path = ROOT, pandoc: str | None = None):
        self.root = root.resolve()
        self.pandoc = pandoc or pandoc_path()
        self.config_path = self.root / "publication/content.json"
        self.config = json.loads(self.config_path.read_text())
        self.sections = self.config["sections"]
        self.by_id = {section["id"]: section for section in self.sections}
        self.by_path = {self.local_path(section["path"]): section for section in self.sections}
        if len(self.by_id) != len(self.sections) or len(self.by_path) != len(self.sections):
            raise BuildError("Section IDs and source paths must be unique.")
        if not re.fullmatch(r"https://github\.com/[^/]+/[^/]+/blob/[^/]+/", self.config["source_base_url"]):
            raise BuildError("source_base_url must be a GitHub blob URL ending with a branch and slash.")
        self.documents: dict[Path, Document] = {}
        self.input_files: set[Path] = {
            self.config_path, self.root / "publication/site.html", self.root / "publication/study.css",
            self.root / "publication/study.typ", self.root / "tools/build_publication.py",
        }
        self.images: set[Path] = set()
        for path in self.by_path:
            self.document(path)
        self._validate_inputs()

    def local_path(self, relative: str, source: Path | None = None) -> Path:
        path = ((source.parent if source else self.root) / unquote(relative)).resolve()
        if not path.is_relative_to(self.root):
            raise BuildError(f"Local target escapes the project: {relative}")
        if not path.exists():
            origin = source.relative_to(self.root) if source else "publication config"
            raise BuildError(f"Missing local target {relative!r} in {origin}")
        return path

    def document(self, path: Path) -> Document:
        if path not in self.documents:
            self.documents[path] = Document(path, self.pandoc)
        return self.documents[path]

    def _local_target(self, target: str, source: Path) -> tuple[Path, str] | None:
        url = urlsplit(target)
        if url.scheme or url.netloc:
            if url.scheme == "file":
                raise BuildError(f"Use project-relative links, not file URLs, in {source.relative_to(self.root)}")
            return None
        path = self.local_path(url.path, source) if url.path else source
        fragment = unquote(url.fragment)
        if fragment and path.suffix.lower() == ".md" and fragment not in self.document(path).anchors:
            raise BuildError(f"Missing Markdown anchor #{fragment} in {path.relative_to(self.root)}")
        return path, fragment

    def _validate_inputs(self):
        for source in self.by_path:
            self.input_files.add(source)
            for node in walk(self.document(source).ast):
                if node.get("t") not in ("Link", "Image"):
                    continue
                target = node["c"][2][0]
                resolved = self._local_target(target, source)
                if node["t"] == "Image":
                    if resolved is None:
                        raise BuildError("Publication figures must be local canonical assets for offline reading.")
                    path, fragment = resolved
                    if fragment or path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".svg"}:
                        raise BuildError(f"Unsupported figure target: {target}")
                    self.images.add(path)
                    self.input_files.add(path)

    def fingerprint(self) -> tuple[dict, str]:
        inputs = {str(path.relative_to(self.root)): sha256(path) for path in sorted(self.input_files)}
        digest = hashlib.sha256(json.dumps(inputs, sort_keys=True).encode()).hexdigest()
        return inputs, digest

    def github_url(self, path: Path, fragment: str = "") -> str:
        base = self.config["source_base_url"]
        if path.is_dir():
            base = base.replace("/blob/", "/tree/")
        target = base + quote(path.relative_to(self.root).as_posix(), safe="/")
        return target + ("#" + quote(fragment) if fragment else "")

    def section_ast(self, section_id: str, included: set[str], mode: str, *, typst_dir: Path | None = None) -> dict:
        section = self.by_id[section_id]
        source = self.local_path(section["path"])
        ast = copy.deepcopy(self.document(source).ast)
        first_heading = True
        for node in walk(ast):
            if node.get("t") == "Header":
                original = node["c"][1][0]
                node["c"][1][0] = section_id if first_heading else f"{section_id}--{original}"
                node["c"][0] = min(node["c"][0] + (1 if mode == "site" else 0), 6)
                if first_heading:
                    node["c"][2] = [{"t": "Str", "c": section["title"]}]
                    first_heading = False
            if node.get("t") not in ("Link", "Image"):
                continue
            resolved = self._local_target(node["c"][2][0], source)
            if resolved is None:
                continue
            path, fragment = resolved
            if node["t"] == "Image":
                if mode == "site":
                    target = "assets/figures/" + path.relative_to(self.root).as_posix()
                else:
                    target = Path(os.path.relpath(path, typst_dir)).as_posix()
            elif path in self.by_path and self.by_path[path]["id"] in included:
                destination_id = self.by_path[path]["id"]
                first_id = next((n["c"][1][0] for n in walk(self.document(path).ast) if n.get("t") == "Header"), "")
                target = "#" + (f"{destination_id}--{fragment}" if fragment and fragment != first_id else destination_id)
            else:
                target = self.github_url(path, fragment)
            node["c"][2][0] = target
        return print_entries(ast, section_id) if mode == "pdf" else ast

    def versions(self, include_typst: bool = False) -> dict:
        versions = {"python": sys.version.split()[0], "pandoc": command([self.pandoc, "--version"]).splitlines()[0]}
        try:
            versions["pypandoc_binary"] = importlib.metadata.version("pypandoc_binary")
        except importlib.metadata.PackageNotFoundError:
            versions["pypandoc_binary"] = "not installed as a binary distribution"
        if include_typst:
            versions["typst"] = command(["typst", "--version"]).strip()
        return versions

    def manifest(self, directory: Path, format_name: str, versions: dict):
        inputs, digest = self.fingerprint()
        outputs = {p.relative_to(directory).as_posix(): sha256(p) for p in sorted(directory.rglob("*")) if p.is_file()}
        (directory / "publication-manifest.json").write_text(json.dumps({
            "schema": 1, "format": format_name, "input_sha256": inputs,
            "input_digest": digest, "build_versions": versions, "output_sha256": outputs,
        }, indent=2, sort_keys=True) + "\n")

    def _replace_output(self, stage: Path, target: Path):
        if target.exists():
            shutil.rmtree(target)
        stage.rename(target)

    def build_site(self) -> Path:
        build = self.root / "build"
        build.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".site-", dir=build) as temporary:
            stage = Path(temporary) / "site"
            stage.mkdir()
            (stage / "assets").mkdir()
            shutil.copyfile(self.root / "publication/study.css", stage / "assets/study.css")
            for path in self.images:
                destination = stage / "assets/figures" / path.relative_to(self.root)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, destination)
            included = set(self.by_id)
            rendered = []
            for section in self.sections:
                ast = self.section_ast(section["id"], included, "site")
                # The wrapper owns each section's anchor. Avoid duplicate IDs.
                first = next((n for n in walk(ast) if n.get("t") == "Header"), None)
                if first is not None:
                    if section.get("optional"):
                        ast["blocks"].remove(first)
                    else:
                        first["c"][1][0] = section["id"] + "--title"
                body = command([self.pandoc, "--from", "json", "--to", "html5", "--mathml", "--wrap=none"], stdin=json.dumps(ast))
                body = re.sub(r"(<table(?:\s[^>]*)?>.*?</table>)", r'<div class="table-scroll" tabindex="0">\1</div>', body, flags=re.S)
                ident, title = html.escape(section["id"]), html.escape(section["title"])
                if section.get("optional"):
                    rendered.append(f'<details id="{ident}" class="optional-section"><summary>{title}</summary>\n{body}\n</details>')
                else:
                    rendered.append(f'<section id="{ident}" class="study-section">\n{body}\n</section>')
            download_links = []
            pdf_dir = build / "pdf"
            pdf_manifest = pdf_dir / "publication-manifest.json"
            if pdf_manifest.exists() and json.loads(pdf_manifest.read_text()).get("input_digest") == self.fingerprint()[1]:
                (stage / "downloads").mkdir()
                for name, label in (("study-notes", "Notes PDF"), ("study-pack", "Full study pack PDF")):
                    pdf = pdf_dir / f"{name}.pdf"
                    if not pdf.exists():
                        raise BuildError("PDF manifest exists but a PDF is missing; rebuild --format all.")
                    shutil.copyfile(pdf, stage / "downloads" / pdf.name)
                    download_links.append(f'<a class="download-link" href="downloads/{pdf.name}">{label}</a>')
            navigation = "<ul>" + "".join(f'<li><a href="#{html.escape(s["id"])}">{html.escape(s["title"])}</a></li>' for s in self.sections) + "</ul>"
            repository = self.config["source_base_url"].split("/blob/", 1)[0]
            substitutions = {key: html.escape(self.config[key]) for key in ("title", "subtitle", "description", "kicker")}
            substitutions.update(body="\n".join(rendered), navigation=navigation, downloads="".join(download_links), repository_url=html.escape(repository))
            template = string.Template((self.root / "publication/site.html").read_text())
            page = template.substitute(substitutions).replace('<body>', '<body id="top">', 1)
            (stage / "index.html").write_text(page)
            validate_html(stage / "index.html")
            self.manifest(stage, "site", self.versions())
            self._replace_output(stage, build / "site")
        return build / "site/index.html"

    def build_pdfs(self) -> list[Path]:
        if shutil.which("typst") is None:
            raise BuildError("Typst is required for PDF output; install the documented CLI first.")
        build = self.root / "build"
        build.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".pdf-", dir=build) as temporary:
            # Keep the same depth as build/pdf so retained Typst image paths
            # remain valid after the completed directory is moved into place.
            stage = Path(temporary)
            (stage / "typst").mkdir(parents=True)
            for name, spec in self.config["pdfs"].items():
                included = set(spec["sections"])
                merged = None
                for section_id in spec["sections"]:
                    ast = self.section_ast(section_id, included, "pdf", typst_dir=stage / "typst")
                    if merged is None:
                        merged = ast
                    else:
                        merged["blocks"].extend(ast["blocks"])
                for key, value in {"title": self.config["title"], "subtitle": spec["subtitle"], "description": self.config["description"]}.items():
                    merged["meta"][key] = {"t": "MetaString", "c": value}
                typst_source = command([
                    self.pandoc, "--from", "json", "--to", "typst", "--standalone", "--wrap=none",
                    "--template", str(self.root / "publication/study.typ"),
                ], stdin=json.dumps(merged))
                source_path = stage / "typst" / f"{name}.typ"
                source_path.write_text(typst_source)
                command(["typst", "compile", "--root", str(self.root), str(source_path), str(stage / f"{name}.pdf")])
            self.manifest(stage, "pdf", self.versions(include_typst=True))
            self._replace_output(stage, build / "pdf")
        return [build / "pdf" / f"{name}.pdf" for name in self.config["pdfs"]]


class LocalHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids: list[str] = []
        self.targets: list[str] = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.append(attributes["id"])
        for key in ("href", "src"):
            if key in attributes:
                self.targets.append(attributes[key])


def validate_html(index: Path):
    page = LocalHTML()
    page.feed(index.read_text())
    if len(page.ids) != len(set(page.ids)):
        raise BuildError("Generated HTML has duplicate IDs.")
    for target in page.targets:
        url = urlsplit(target)
        if url.scheme or url.netloc:
            continue
        if url.path:
            destination = (index.parent / unquote(url.path)).resolve()
            if not destination.is_relative_to(index.parent.resolve()) or not destination.is_file():
                raise BuildError(f"Broken generated local asset/link: {target}")
        elif url.fragment and unquote(url.fragment) not in page.ids:
            raise BuildError(f"Broken generated section anchor: {target}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("all", "pdf", "site"), default="all")
    args = parser.parse_args(argv)
    try:
        publication = Publication()
        outputs = []
        if args.format in ("all", "pdf"):
            outputs.extend(publication.build_pdfs())
        if args.format in ("all", "site"):
            outputs.append(publication.build_site())
        for output in outputs:
            print(output.relative_to(ROOT).as_posix())
        return 0
    except (BuildError, OSError, ValueError) as exc:
        print(f"Publication build failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
