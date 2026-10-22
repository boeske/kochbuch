# Kochbuch-Pipeline (Testprojekt)

## Aufbau

- `rezepte/*.md`: Je Rezept eine Markdown-Datei.
- `config/reihenfolge.md`: Legt die Reihenfolge der Rezepte fest.
- `latex/CSMorganaRecipe.cls`: Bestehendes Layout.
- `scripts/kochbuch_builder.py`: Erzeugt einzelne `.tex`-Dateien und das Gesamtkochbuch.
- `build/`: Generierte Dateien und PDF.

## Reihenfolge festlegen

In `config/reihenfolge.md` stehen die Dateinamen aus `rezepte/` ohne `.md`, jeweils eine Zeile. Nummerierte Listen oder einfache Listen funktionieren:

```markdown
# Reihenfolge des Kochbuchs

1. fischli-nudeln
2. fischli-nudeln2
```

Alle Rezeptdateien müssen genau einmal in dieser Datei stehen. Das Skript meldet fehlende oder doppelte Einträge.

## Bauen

Im Projektordner ausführen:

```bash
python scripts/kochbuch_builder.py
```

Benötigt Python 3 sowie eine LaTeX-Installation mit `latexmk`, `lualatex` oder `pdflatex`. Das PDF wird unter `build/kochbuch.pdf` erstellt.
