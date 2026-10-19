# Läuft in Pyodide (von check.mjs gestartet). Erwartet die Variable zellen_json und setzt die Variable ergebnis.
# Bei sympy-Notebooks enthält zellen_json zusätzlich den Quelltext von sympy_ausgabe.py und den Setup-Code:
# dann wird jede Zelle genauso wie beim Generieren ausgeführt (Formeln als Markdown) und das Ergebnis verglichen.
import contextlib
import io
import json
import os
import sys
import tempfile

os.environ['MPLBACKEND'] = 'Agg'  # in Node gibt es kein Browserfenster; Diagramme werden nur gezeichnet, nicht angezeigt

daten = json.loads(zellen_json)
zellen = daten['zellen']
sympy_info = daten.get('sympy')
sympy_modul = {}
if sympy_info:
    exec(sympy_info['quelle'], sympy_modul)
os.chdir(tempfile.mkdtemp())

ERWARTET = {'beispiel', 'free', 'predict'}  # dort steht keine erwartete Ausgabe im Notebook (z. B. Zufall ohne Seed)
echt = []
andere = []
for z in zellen:
    plt = None
    if 'matplotlib' in z['code']:
        import matplotlib
        import matplotlib.pyplot as plt
        plt.close('all')
        matplotlib.rcdefaults()
    fehler = None
    if sympy_info and z['art'] != 'setup':
        namensraum = {}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(sympy_info['setup'], namensraum)
        ausgabe, err = sympy_modul['ausfuehren'](z['code'], namensraum)
        fehler = type(err).__name__ if err else None
    else:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            try:
                exec(z['code'], {})
            except Exception as e:
                fehler = type(e).__name__
        ausgabe = buf.getvalue()
    if plt is not None:
        plt.close('all')
    if fehler != z.get('fehler'):
        erwartet = z.get('fehler') or 'kein Fehler'
        echt.append(f"{z['nr']} ({z['art']})\n--- Laufzeitfehler: {fehler or 'keiner'}, erwartet: {erwartet}\n")
    elif ausgabe != z['out']:
        text = f"{z['nr']} ({z['art']})\n--- lokal:\n{z['out']}--- pyodide:\n{ausgabe}"
        (andere if z['art'] in ERWARTET else echt).append(text)

versionen = f'Python {sys.version.split()[0]}'
for paket in ['sympy', 'numpy', 'matplotlib']:
    if paket in sys.modules:
        versionen += f', {paket} {sys.modules[paket].__version__}'
if 'numpy' in sys.modules:
    versionen += f' (Ganzzahltyp {sys.modules["numpy"].arange(1).dtype})'

zeilen = [f'{versionen}, {len(zellen)} Zellen',
          f'ECHTE FEHLER: {len(echt)} (Laufzeitfehler oder Aufgaben mit erwarteter Ausgabe, die in Pyodide anders herauskommen)',
          f'Andere Unterschiede: {len(andere)} (Beispiele, free und predict, z. B. Zufall ohne Seed; nur zur Info)']
if echt:
    zeilen += ['', '##### Echte Fehler'] + echt
if andere:
    zeilen += ['', '##### Andere Unterschiede: ' + ', '.join(t.split('\n')[0] for t in andere)]
ergebnis = '\n'.join(zeilen)
