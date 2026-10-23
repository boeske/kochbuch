#!/usr/bin/env python3
"""Build individual recipe .tex files and a combined cookbook .tex/PDF."""
from pathlib import Path
import re, subprocess, shutil, sys

ROOT = Path(__file__).resolve().parents[1]
RECIPES = ROOT / "rezepte"
BUILD = ROOT / "build"
OUT_RECIPES = BUILD / "rezepte"
CLASS_DIR = ROOT / "latex"
ORDER_FILE = ROOT / "config" / "reihenfolge.md"

def read_recipe(path):
    text = path.read_text(encoding="utf-8")
    meta = {}
    if text.startswith("---"):
        _, front, text = text.split("---", 2)
        for line in front.strip().splitlines():
            m = re.match(r'^([A-Za-z_]+):\s*(.*?)\s*$', line)
            if m:
                val = m.group(2)
                if len(val) >= 2 and val[0] == val[-1] and val[0] in "\"'":
                    val = val[1:-1]
                meta[m.group(1)] = val
    sections = {"Zutaten": [], "Zubereitung": []}
    current = None
    for line in text.splitlines():
        if line.startswith("# "):
            heading = line[2:].strip().lower()
            current = "Zutaten" if heading in ("zutaten", "ingredients") else (
                "Zubereitung" if heading in ("zubereitung", "zubereitungsschritte", "method", "methods") else None)
            continue
        if current and line.strip():
            m = re.match(r'^\s*[-*]\s+(.*)$', line)
            n = re.match(r'^\s*\d+[.)]\s+(.*)$', line)
            if m: sections[current].append(m.group(1).strip())
            elif n: sections[current].append(n.group(1).strip())
            else: sections[current].append(line.strip())
    if not meta.get("title"):
        raise ValueError(f"{path.name}: Metadatum 'title' fehlt.")
    if not sections["Zutaten"] or not sections["Zubereitung"]:
        raise ValueError(f"{path.name}: Bitte Abschnitte '# Zutaten' und '# Zubereitung' befüllen.")
    return meta, sections

def tex_escape(s):
    # Escape LaTeX special characters, but keep Markdown emphasis markers handled separately.
    s = s.replace("\\", r"\textbackslash{}")
    for char, repl in [("&", r"\&"), ("%", r"\%"), ("$", r"\$"), ("#", r"\#"),
                       ("_", r"\_"), ("{", r"\{"), ("}", r"\}"), ("~", r"\textasciitilde{}"),
                       ("^", r"\textasciicircum{}")]:
        s = s.replace(char, repl)
    s = re.sub(r"\*(.+?)\*", r"\\textit{\1}", s)
    return s

def cmd(name, value):
    return f"\\{name}{{{tex_escape(value or '')}}}"

def recipe_body(path, meta, sections, toc=False):
    # The class uses self-redefining commands for recipe metadata. Group each recipe
    # so those definitions are local and do not leak into the next recipe.
    lines = [r"\begingroup"]
    for key, macro in [("title","recipetitle"), ("subtitle","recipesubtitle"), ("heading","heading"),
                       ("description","recipedescription"), ("serves","recipeserves"),
                       ("prep_time","recipepreptime"), ("cooking_time","recipecookingtime"),
                       ("difficulty","recipedifficulty"), ("extra_info","extramethodinfo")]:
        lines.append(cmd(macro, meta.get(key, "")))
    # Page break first: the TOC entry and the hyperref anchor must belong to the
    # new recipe page. Otherwise both point at the end of the previous recipe.
    lines.append(r"\clearpage")
    if toc:
        # Recipes are listed below their chapter in the table of contents.
        lines += [r"\phantomsection",
                  r"\addcontentsline{toc}{subsection}{" + tex_escape(meta["title"]) + "}"]
    lines += [r"\outputrecipeheader", r"\outputrecipedescription", r"\seprule",
              r"\vspace*{0.015\textheight}", r"\columnratio{0.4, 0.6}", r"\begin{paracol}{2}",
              r"\begin{recipeingredients}"]
    lines += [r"\ingredient{" + tex_escape(x) + "}" for x in sections["Zutaten"]]
    lines += [r"\end{recipeingredients}", r"\switchcolumn", r"\begin{recipemethods}"]
    lines += [r"\method{" + tex_escape(x) + "}" for x in sections["Zubereitung"]]
    lines += [r"\end{recipemethods}", r"\end{paracol}", r"\vspace*{0.006\textheight}", r"\seprule"]
    lines.append(r"\endgroup")
    return "\n".join(lines)

def chapter_page(title, first=False):
    """Output a chapter divider page. Recipes of the chapter start on the next page."""
    lines = [r"\clearpage"]
    if first:
        # Front matter (title page + TOC) stays unnumbered; the book starts at 1.
        lines += [r"\pagenumbering{arabic}", r"\pagestyle{plain}"]
    lines += [r"\phantomsection",
              r"\addcontentsline{toc}{section}{" + tex_escape(title) + "}",
              r"\begin{center}",
              r"\vspace*{0.2\textheight}",
              r"{\fontsize{34pt}{34pt}\selectfont\latoblack{" + tex_escape(title) + r"}\par}",
              r"\vspace*{0.02\textheight}",
              r"{\color{myred}\rule{0.45\textwidth}{0.5pt}}",
              r"\end{center}"]
    return "\n".join(lines)

def preamble():
    return r"""\documentclass[a4paper,10pt]{CSMorganaRecipe}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{hyperref}
\pagestyle{plain}
\begin{document}
"""

def read_order(available_files):
    """Read chapters and recipe stems from config/reihenfolge.md.

    Chapters are introduced by '## Kapitelname'. Recipes without a chapter entry
    are collected in a final chapter named 'Unsortiert'.
    """
    if not ORDER_FILE.exists():
        raise SystemExit(f"Reihenfolge-Datei fehlt: {ORDER_FILE}")
    available = {path.stem: path for path in available_files}
    chapters = []  # [ [chapter_name, [recipe_stem, ...]], ... ]
    current = None
    seen = set()
    for line in ORDER_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("<!--"):
            continue
        if line.startswith("## "):
            name = line[3:].strip()
            if not name:
                raise SystemExit("Kapitelüberschrift ohne Namen in reihenfolge.md.")
            current = [name, []]
            chapters.append(current)
            continue
        if line.startswith("#"):
            # '# ...' ist die Überschrift der Datei, kein Kapitel.
            continue
        line = re.sub(r"^[-*]\s+", "", line)
        line = re.sub(r"^\d+[.)]\s+", "", line).strip()
        if not line:
            continue
        name = Path(line).stem
        if name in seen:
            raise SystemExit(f"Rezept doppelt in reihenfolge.md: {name}")
        if name not in available:
            raise SystemExit(f"Rezept '{name}' aus reihenfolge.md nicht gefunden in rezepte/.")
        seen.add(name)
        if current is None:
            current = ["Ohne Kapitel", []]
            chapters.append(current)
        current[1].append(name)

    missing = sorted(set(available) - seen)
    result = []
    unsorted = []
    for name, stems in chapters:
        if name.casefold() == "unsortiert":
            unsorted.extend(stems)
        elif stems:
            result.append((name, [available[stem] for stem in stems]))
    # Everything not listed in reihenfolge.md goes into the final chapter.
    unsorted.extend(missing)
    if unsorted:
        result.append(("Unsortiert", [available[stem] for stem in unsorted]))
    if not result:
        raise SystemExit(f"Keine Rezepte in {ORDER_FILE} eingetragen.")
    return result

def main():
    BUILD.mkdir(exist_ok=True)
    OUT_RECIPES.mkdir(parents=True, exist_ok=True)
    discovered = sorted(RECIPES.glob("*.md"))
    if not discovered:
        raise SystemExit("Keine Rezept-Markdown-Dateien in rezepte/ gefunden.")
    chapters = read_order(discovered)
    parsed = {}
    for _chapter, paths in chapters:
        for path in paths:
            meta, sections = read_recipe(path)
            parsed[path] = (meta, sections)
            individual = preamble() + recipe_body(path, meta, sections) + "\n\\end{document}\n"
            (OUT_RECIPES / f"{path.stem}.tex").write_text(individual, encoding="utf-8")
    master = [preamble(), r"\pagestyle{empty}",
              r"\begin{center}{\Huge\bfseries Kochbuch}\end{center}", r"\tableofcontents"]
    first = True
    for chapter, paths in chapters:
        master.append(chapter_page(chapter, first=first))
        first = False
        for path in paths:
            meta, sections = parsed[path]
            master.append(recipe_body(path, meta, sections, toc=True))
    master.append(r"\end{document}")
    master_tex = BUILD / "kochbuch.tex"
    master_tex.write_text("\n\n".join(master) + "\n", encoding="utf-8")
    # Keep the class beside generated TeX so LaTeX finds it.
    shutil.copy2(CLASS_DIR / "CSMorganaRecipe.cls", BUILD / "CSMorganaRecipe.cls")
    shutil.copy2(CLASS_DIR / "CSMorganaRecipe.cls", OUT_RECIPES / "CSMorganaRecipe.cls")
    compiler = shutil.which("pdflatex") or shutil.which("lualatex") or shutil.which("latexmk")
    if not compiler:
        print("LaTeX-Quelldateien erstellt. Kein LaTeX-Compiler gefunden; PDF wurde nicht gebaut.")
        print(f"Masterdatei: {master_tex}")
        return
    if Path(compiler).name == "latexmk":
        cmdline = [compiler, "-pdf", "-interaction=nonstopmode", "-halt-on-error", "kochbuch.tex"]
    else:
        cmdline = [compiler, "-interaction=nonstopmode", "-halt-on-error", "kochbuch.tex"]
    # Run twice for table of contents references.
    for _ in range(2):
        result = subprocess.run(cmdline, cwd=BUILD, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, errors="replace")
        if result.returncode:
            (BUILD / "latex-build.log").write_text(result.stdout, encoding="utf-8")
            raise SystemExit("LaTeX-Kompilierung fehlgeschlagen. Details: build/latex-build.log")
    print(f"Erstellt: {BUILD / 'kochbuch.pdf'}")

if __name__ == "__main__":
    main()
