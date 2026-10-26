// Pandoc template. The body is generated from the canonical Markdown files.
#let horizontalrule = line(length: 100%, stroke: 0.5pt + rgb("d7ddd6"))
#set document(title: [$title$], author: "Defect physics study notebook")
#set page(paper: "a4", margin: (x: 22mm, y: 22mm), numbering: "1", number-align: center)
#set text(font: "Libertinus Serif", size: 12pt, fill: rgb("242b2a"), lang: "en")
#set par(justify: false, leading: 0.45em, spacing: 0.55em)
#set heading(numbering: none)
#show heading.where(level: 1): it => block(sticky: true, above: 1.4em, below: 0.7em)[#text(size: 20pt, weight: "bold")[#it.body]]
#show heading.where(level: 2): it => block(sticky: true, above: 1em, below: 0.5em)[#text(size: 14pt, weight: "bold")[#it.body]]
#show heading.where(level: 3): it => block(sticky: true, above: 0.8em, below: 0.4em)[#text(size: 12pt, weight: "bold")[#it.body]]
#show link: set text(fill: rgb("255b51"))
#set table(inset: (x: 4pt, y: 5pt), stroke: none)
#show table.cell.where(y: 0): set text(weight: "bold")
#show figure.where(kind: table): set text(size: 10.5pt)
#show figure.where(kind: table): set block(breakable: true)
#show figure.where(kind: table): set figure.caption(position: top)
#show figure.where(kind: image): set image(width: 100%)
#show figure.caption: set text(size: 9pt, fill: rgb("606965"))
#show raw: set text(font: "DejaVu Sans Mono", size: 10.5pt)
#show terms.item: it => block(breakable: false, above: 0.7em, below: 0.3em)[
  #strong(it.term)
  #parbreak()
  #it.description
]
$if(highlighting-definitions)$
$highlighting-definitions$
$endif$
#text(size: 9pt, fill: rgb("255b51"), tracking: 1pt)[STUDY NOTEBOOK / SILICON-VACANCY CENTER]
#v(8pt)
#text(size: 26pt, weight: "bold")[$title$]
#v(7pt)
#text(size: 12pt, fill: rgb("606965"))[$subtitle$]
#v(10pt)
#text(size: 10pt)[$description$]
#v(10pt)
#horizontalrule
#v(8pt)
$body$
