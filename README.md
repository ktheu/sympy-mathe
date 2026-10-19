# Mathematik mit sympy

Übungsnotebooks zum Selbststudium: Mathematik mit dem Computer-Algebra-Paket [sympy](https://www.sympy.org/de/) in Python,
passend zum Bildungsplan Mathematik des Gymnasiums in Baden-Württemberg. Die Notebooks laufen direkt im Browser mit
[JupyterLite](https://jupyterlite.readthedocs.io/), ohne Installation und ohne Anmeldung.

| Thema | Notebook öffnen |
|---|---|
| Zahlen exakt: Brüche, Primzahlen, Potenzen und Wurzeln | [sympy_zahlen.ipynb](https://ktheu.github.io/sympy-mathe/notebooks/index.html?path=sympy_zahlen.ipynb) |
| Terme: Einsetzen, Ausmultiplizieren, Faktorisieren, Formeln umstellen | [sympy_terme.ipynb](https://ktheu.github.io/sympy-mathe/notebooks/index.html?path=sympy_terme.ipynb) |
| Gleichungen, Gleichungssysteme und Ungleichungen | [sympy_gleichungen.ipynb](https://ktheu.github.io/sympy-mathe/notebooks/index.html?path=sympy_gleichungen.ipynb) |
| Funktionen: Graphen, Nullstellen, Scheitel, Wachstum, Sinus | [sympy_funktionen.ipynb](https://ktheu.github.io/sympy-mathe/notebooks/index.html?path=sympy_funktionen.ipynb) |
| Ableitungen: Änderungsrate, Tangente, Extrem- und Wendepunkte | [sympy_ableitungen.ipynb](https://ktheu.github.io/sympy-mathe/notebooks/index.html?path=sympy_ableitungen.ipynb) |

Alle Notebooks auf einmal: [JupyterLab](https://ktheu.github.io/sympy-mathe/lab/index.html)

Python-Grundlagen (Listen, Funktionen, numpy, matplotlib, ...): [Python-Übungen](https://ktheu.github.io/python-uebungen/)

## Hinweise

- Beim ersten Ausführen einer Zelle wird Python in den Browser geladen, beim ersten `import sympy` zusätzlich sympy. Das dauert ein paar Sekunden.
- Deine Änderungen werden **im Browser** gespeichert. Auf einem anderen Gerät oder nach dem Löschen der Browserdaten sind sie weg.
  Wer seine Lösungen behalten will, lädt das Notebook herunter (*File → Download*).
- Unter jeder Aufgabe kann man die Lösung aufklappen. Erst selbst probieren!

## Für Lehrkräfte

Die Notebooks in `content/` werden von den Skripten in `generator/` erzeugt (`generator/nbgen.py`, ein Skript pro Notebook).
Dabei wird jede Musterlösung ausgeführt; die erwarteten Ausgaben stammen aus diesen Läufen.
