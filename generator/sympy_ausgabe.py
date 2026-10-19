"""Führt Notebook-Zellen so aus wie Jupyter mit sympy und liefert die Ausgabe als Markdown für die erwartete Ausgabe.

- Text von print() erscheint als Codeblock.
- Der Wert des letzten Ausdrucks einer Zelle und alles, was mit display() ausgegeben wird, erscheint als Formel:
  $\\displaystyle ...$ als eigener Absatz (linksbündig; $$...$$ würde JupyterLab zentrieren).
  So sieht es auch im Notebook aus, wenn vorher init_printing() aufgerufen wurde (dann auch Listen und Tupel als Formel).
- Jede Zelle bekommt einen frischen Namensraum, in dem vorher der Code der Setup-Zelle ausgeführt wurde
  (z. B. from sympy import * und init_printing()), so wie im Notebook nach Ausführen der Setup-Zelle.

Dieses Modul läuft auch in Pyodide (pyodide_check), es darf deshalb nur die Standardbibliothek und sympy verwenden.
"""
import ast
import contextlib
import io
import warnings

# sympy 1.14 ruft in mpmath 1.4.1 (beide wie in Pyodide 314.0.6) die veraltete Funktion bitcount auf.
# Mit "-W error" würde daraus ein Fehler; im Notebook sieht man die Warnung nicht (sie entsteht in der Bibliothek).
warnings.filterwarnings('ignore', message='bitcount function is deprecated', category=DeprecationWarning)


def _als_formel(o):
    """Wie sympy.interactive.printing._can_print bei init_printing(): Zeigt Jupyter o als Formel (LaTeX) an?"""
    from sympy.core.basic import Printable
    if isinstance(o, (list, tuple, set, frozenset)):
        return all(_als_formel(i) for i in o)
    if isinstance(o, dict):
        return all(_als_formel(k) and _als_formel(v) for k, v in o.items())
    if isinstance(o, bool):
        return False
    if isinstance(o, Printable):
        return True
    if any(hasattr(o, h) for h in ('_latex', '_sympy_', '_repr_latex_')):
        return True
    return isinstance(o, (int, float))


def _markdown(teile):
    from sympy import latex
    md = []
    for art, inhalt in teile:
        if art == 'text':
            md.append('```\n' + inhalt.rstrip('\n') + '\n```')
        elif _als_formel(inhalt):
            md.append('$\\displaystyle ' + latex(inhalt) + '$')
        else:  # z. B. True, Texte: Jupyter zeigt die Python-Darstellung
            md.append('```\n' + repr(inhalt) + '\n```')
    return '\n\n'.join(md) + ('\n' if md else '')


def ausfuehren(code, namensraum):
    """Führt code im namensraum aus. Gibt (markdown, fehler) zurück."""
    teile = []

    class Schreiber(io.TextIOBase):
        def write(self, s):
            if teile and teile[-1][0] == 'text':
                teile[-1] = ('text', teile[-1][1] + s)
            else:
                teile.append(('text', s))
            return len(s)

    def display(*objekte):
        for o in objekte:
            teile.append(('formel', o))

    namensraum['display'] = display
    baum = ast.parse(code)
    letzter = None
    if baum.body and isinstance(baum.body[-1], ast.Expr):
        letzter = ast.Expression(baum.body.pop().value)
    fehler = None
    with contextlib.redirect_stdout(Schreiber()):
        try:
            exec(compile(baum, '<zelle>', 'exec'), namensraum)
            if letzter is not None:
                wert = eval(compile(letzter, '<zelle>', 'eval'), namensraum)
                if wert is not None:
                    teile.append(('formel', wert))
        except Exception as e:  # noqa
            fehler = e
    return _markdown(teile), fehler


def sympy_ausfuehrung(setup_code):
    """Ausführungsfunktion für nbgen.generate(..., sprache='sympy', ausfuehren=...): code -> (markdown, fehler, bilder)."""
    def ausf(code):
        namensraum = {}
        if code != setup_code:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(setup_code, namensraum)
        md, fehler = ausfuehren(code, namensraum)
        return md, fehler, []

    ausf.pyodide = {'setup': setup_code}  # für pyodide_check: dieselbe Ausführung in Pyodide wiederholen
    return ausf
