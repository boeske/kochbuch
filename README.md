# Kochbuch-Pipeline (Testprojekt)

## Aufbau

- `rezepte/*.md`: Je Rezept eine Markdown-Datei.
- `config/reihenfolge.md`: Legt die Reihenfolge der Rezepte fest.
- `latex/CSMorganaRecipe.cls`: Bestehendes Layout.
- `scripts/kochbuch_builder.py`: Erzeugt einzelne `.tex`-Dateien und das Gesamtkochbuch.
- `build/`: Generierte Dateien und PDF.

## Kapitel und Reihenfolge festlegen

In `config/reihenfolge.md` stehen die Dateinamen aus `rezepte/` ohne `.md`. Kapitel beginnen mit einer Überschrift der zweiten Ebene (`##`); darunter stehen die Rezepte als nummerierte oder einfache Liste:

```markdown
# Reihenfolge des Kochbuchs

## Nudelgerichte

1. fischli-nudeln
2. thunfisch-zucchini-nudeln

## Ofengerichte

1. gnocci-auflauf
```

Jedes Kapitel erscheint als eigene Kapitelseite und als Eintrag im Inhaltsverzeichnis; die Rezepte sind darunter eingerückt. Rezepte, die in `reihenfolge.md` fehlen, aber in `rezepte/` liegen, werden automatisch im letzten Kapitel **Unsortiert** ausgegeben. Doppelte oder unbekannte Rezeptnamen meldet das Skript als Fehler. Die `# ...`-Überschrift am Dateianfang ist nur der Titel der Datei und kein Kapitel.

## Bauen

Im Projektordner ausführen:

```bash
python scripts/kochbuch_builder.py
```

Benötigt Python 3 sowie eine LaTeX-Installation mit `latexmk`, `lualatex` oder `pdflatex`. Das PDF wird unter `build/kochbuch.pdf` erstellt.
