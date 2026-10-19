# Erzeugt ../content/sympy_gleichungen.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_gleichungen.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_gleichungen.py
#
# Bildungsplan BW 2016, Leitidee Zahl – Variable – Operation: Klassen 7/8 (lineare Gleichungen mit Äquivalenzumformungen,
# LGS mit zwei Variablen, quadratische Gleichungen mit Formel, Satz vom Nullprodukt, Gleichung zu vorgegebenen Lösungen,
# Bruchgleichungen, Lösbarkeit, Ungleichungen), 9/10 (Wurzel-, Potenz-, Exponentialgleichungen, Logarithmus, Substitution,
# Nullstellen näherungsweise mit digitalen Hilfsmitteln).
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = "from sympy import *\ninit_printing()\nx, y, z, a, b, c = symbols('x y z a b c')"

INTRO = '''In diesem Notebook löst du **Gleichungen, Gleichungssysteme und Ungleichungen** mit sympy: lineare und quadratische Gleichungen,
Bruch- und Wurzelgleichungen, Potenz- und Exponentialgleichungen mit dem Logarithmus und lineare Gleichungssysteme.

sympy kann fast jede dieser Gleichungen sofort lösen. Wichtiger als das Ergebnis ist deshalb oft der Weg: Mache die **Probe**,
prüfe deine eigenen Umformungen und finde **Scheinlösungen**, die beim Quadrieren oder Multiplizieren mit dem Nenner entstehen.

Vorausgesetzt werden die Notebooks *Zahlen exakt* und *Terme*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy, schaltet die Formel-Ausgabe ein
und legt die Variablen `x`, `y`, `z`, `a`, `b` und `c` an.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Gleichungen lösen mit solve()')
expl('''#### `Eq()` und `solve()`

`Eq(links, rechts)` ist die Gleichung links = rechts. `solve(gleichung, x)` löst sie nach `x` auf und gibt eine **Liste** der Lösungen zurück.

- Gibt man statt einer Gleichung nur einen Term an, löst sympy `term = 0`: `solve(x**2 - 4, x)`.
- Die leere Liste `[]` bedeutet: keine Lösung.
- Die **Probe** macht man mit `subs()`: Setzt man die Lösung ein, müssen beide Seiten gleich sein.''',
     """gleichung = Eq(3*x + 5, 20)
display(gleichung)
loesungen = solve(gleichung, x)
display(loesungen)
display(gleichung.lhs.subs(x, loesungen[0]), gleichung.rhs)
gleichung.subs(x, loesungen[0])""")
expl('''#### Lösungsmengen mit `solveset()`

`solveset(gleichung, x, domain=S.Reals)` gibt die **Lösungsmenge** in der Grundmenge der reellen Zahlen zurück.
Daran sieht man auch die Sonderfälle: `EmptySet` (∅) für keine Lösung und `Reals` (ℝ), wenn jede Zahl eine Lösung ist.
`solve()` gibt in beiden Fällen nur die leere Liste `[]` zurück, weil sympy eine allgemeingültige Gleichung wie `x + 1 = x + 1` sofort zu `True` vereinfacht.

`solve()` rechnet ohne Angabe auch mit **komplexen** Zahlen. Dann erscheinen bei x² = −1 die Lösungen ±i (`I`).
Mit `solveset(..., domain=S.Reals)` bekommt man nur die reellen Lösungen.''',
     """display(solveset(Eq(2*x + 1, 2*x + 3), x, domain=S.Reals))
display(solveset(Eq(2*(x + 1), 2*x + 2), x, domain=S.Reals))
display(solve(x**2 + 1, x))
solveset(x**2 + 1, x, domain=S.Reals)""")

t('Löse `5x − 7 = 18`.', body='solve(Eq(5*x - 7, 18), x)')
t('Löse `3(x − 2) = 2x + 4`.', body='solve(Eq(3*(x - 2), 2*x + 4), x)')
t('Löse `x/4 + 3 = x/2 − 1`.', body='solve(Eq(x/4 + 3, x/2 - 1), x)')
t('Löse `0,5x − 1,2 = 0,3x + 0,4`. Verwende `Rational`, damit das Ergebnis exakt ist.',
  body="solve(Eq(Rational('0.5')*x - Rational('1.2'), Rational('0.3')*x + Rational('0.4')), x)")
t('Löse `7 − 2(x + 3) = 4x − 5` und mache die Probe: Setze die Lösung in die Gleichung ein.',
  body='gl = Eq(7 - 2*(x + 3), 4*x - 5)\nl = solve(gl, x)\ndisplay(l)\ngl.subs(x, l[0])')
t('Gib die Lösungsmenge von `3x + 2 = 3(x + 1)` mit `solveset()` aus.', body='solveset(Eq(3*x + 2, 3*(x + 1)), x, domain=S.Reals)')
t('Gib die Lösungsmenge von `4(x − 1) + 2 = 4x − 2` aus.', body='solveset(Eq(4*(x - 1) + 2, 4*x - 2), x, domain=S.Reals)')
t('''**Zahlenrätsel:** Wenn man zum Dreifachen einer Zahl 7 addiert, erhält man dasselbe wie wenn man vom Fünffachen der Zahl 9 subtrahiert.
Stelle die Gleichung auf und löse sie.''', body='solve(Eq(3*x + 7, 5*x - 9), x)')
t('''**Alter:** Eine Mutter ist heute 4-mal so alt wie ihr Sohn. In 20 Jahren ist sie doppelt so alt. Sei `x` das Alter des Sohnes.
Stelle die Gleichung `4x + 20 = 2(x + 20)` auf und löse sie.''', body='solve(Eq(4*x + 20, 2*(x + 20)), x)')
t('''Löse die Gleichung `a·x + b = c` nach `x` auf (allgemein, mit den Variablen a, b, c).''', body='solve(Eq(a*x + b, c), x)')
predict("""display(solve(Eq(x + 1, x + 1), x))
display(solve(Eq(x + 1, x + 2), x))
display(solveset(Eq(x + 1, x + 1), x, domain=S.Reals))
solve(2*x - 1, x)""")

# ---------------------------------------------------------------- 2
sec('Quadratische Gleichungen')
expl('''#### Lösungsformel

Eine quadratische Gleichung a·x² + b·x + c = 0 hat die Lösungen

x = (−b ± √(b² − 4ac)) / (2a)

Der Term unter der Wurzel heißt **Diskriminante** D = b² − 4ac. Ist D > 0, gibt es zwei Lösungen, bei D = 0 eine, bei D < 0 keine (reelle).
`solve()` liefert die Lösungen direkt, auch mit Wurzeln.''',
     """display(solve(x**2 - 5*x + 6, x))
display(solve(x**2 - 2*x - 1, x))
display(solve(Eq(2*x**2 + 3, 5*x), x))
display(solve(x**2 + 2*x + 5, x))
solveset(x**2 + 2*x + 5, x, domain=S.Reals)""")
expl('''#### Satz vom Nullprodukt

Ein Produkt ist genau dann 0, wenn einer der Faktoren 0 ist. Ist ein quadratischer Term in Linearfaktoren zerlegt, liest man
die Lösungen direkt ab: (x − 2)(x + 7) = 0 ⇔ x = 2 oder x = −7. `factor()` liefert die Zerlegung.''',
     """term = x**2 + 5*x - 14
display(factor(term))
solve(term, x)""")

t('Löse `x² − 7x + 12 = 0`.', body='solve(x**2 - 7*x + 12, x)')
t('Löse `x² = 2x + 15`.', body='solve(Eq(x**2, 2*x + 15), x)')
t('Löse `2x² − 3x − 2 = 0`.', body='solve(2*x**2 - 3*x - 2, x)')
t('Löse `x² − 6x + 7 = 0` exakt und gib die Lösungen danach als Dezimalzahlen mit 5 Ziffern aus.',
  body='l = solve(x**2 - 6*x + 7, x)\ndisplay(l)\n[N(w, 5) for w in l]')
t('Löse `x² + 4x + 4 = 0`.', body='solve(x**2 + 4*x + 4, x)')
t('Gib die reelle Lösungsmenge von `x² + x + 1 = 0` aus.', body='solveset(x**2 + x + 1, x, domain=S.Reals)')
t('Löse `3x² = 12x` mit dem Satz vom Nullprodukt: Gib zuerst `3x² − 12x` faktorisiert aus und dann die Lösungen.',
  body='display(factor(3*x**2 - 12*x))\nsolve(Eq(3*x**2, 12*x), x)')
t('Berechne die Diskriminante von `2x² − 4x + 5` und gib danach die reelle Lösungsmenge aus.',
  body='a1, b1, c1 = 2, -4, 5\ndisplay(b1**2 - 4*a1*c1)\nsolveset(2*x**2 - 4*x + 5, x, domain=S.Reals)')
t('''Programmiere die Lösungsformel: Berechne für `a1, b1, c1 = 1, -2, -3` die beiden Lösungen mit `sqrt()` und gib sie als Liste aus.
Vergleiche mit `solve()`.''',
  given='a1, b1, c1 = 1, -2, -3',
  body='D = b1**2 - 4*a1*c1\ndisplay([(-b1 - sqrt(D)) / (2*a1), (-b1 + sqrt(D)) / (2*a1)])\nsolve(a1*x**2 + b1*x + c1, x)')
t('Bestimme eine quadratische Gleichung `x² + px + q = 0` mit den Lösungen 3 und −5: Multipliziere `(x − 3)(x + 5)` aus.',
  body='expand((x - 3) * (x + 5))')
t('''Löse `x² − c = 0` allgemein nach `x` auf. Lege `c` dazu positiv an.''',
  given="c = symbols('c', positive=True)", body='solve(x**2 - c, x)')
t('''Für welche Werte von `k` hat `x² + kx + 9 = 0` genau eine Lösung? Löse dazu die Gleichung „Diskriminante = 0“ nach `k`.''',
  given="k = symbols('k')", body='solve(Eq(k**2 - 4*9, 0), k)')
t('''Ein Rechteck hat den Flächeninhalt 60 cm² und ist 7 cm länger als breit. Löse `x(x + 7) = 60` und gib nur die positive Lösung aus
(mit `solveset(..., domain=Interval(0, oo))`).''', body='solveset(Eq(x * (x + 7), 60), x, domain=Interval(0, oo))')
predict("""display(solve(x**2, x))
display(solve(x**2 - 2, x))
display(solve((x - 1)*(x - 4), x))
solveset(x**2 + 4, x, domain=S.Reals)""")

# ---------------------------------------------------------------- 3
sec('Bruchgleichungen')
expl('''#### Definitionsmenge und Scheinlösungen

Bei einer **Bruchgleichung** steht die Variable im Nenner. Für Werte, bei denen ein Nenner 0 wird, ist die Gleichung nicht definiert.
Diese Werte gehören nicht zur **Definitionsmenge**.

Beim Lösen von Hand multipliziert man mit dem Nenner. Dabei kann eine **Scheinlösung** entstehen, die nicht in der Definitionsmenge liegt.
`solve()` prüft das selbst und lässt solche Werte weg.''',
     """gl = Eq(x / (x - 1), 1 / (x - 1) + 2)
display(gl)
display(solve(x - 1, x))
display(solve(Eq(x, 1 + 2*(x - 1)), x))
solve(gl, x)""")

t('Löse `6/x = 2`.', body='solve(Eq(6 / x, 2), x)')
t('Löse `3/(x − 2) = 1`.', body='solve(Eq(3 / (x - 2), 1), x)')
t('Löse `(x + 1)/(x − 1) = 3`.', body='solve(Eq((x + 1) / (x - 1), 3), x)')
t('Löse `1/x + 1/(2x) = 3`.', body='solve(Eq(1/x + 1/(2*x), 3), x)')
t('Löse `x/(x + 2) = 2/(x + 2)`.', body='solve(Eq(x / (x + 2), 2 / (x + 2)), x)')
t('Bestimme die Werte, die nicht zur Definitionsmenge von `5/(x² − 9) = 1` gehören (Nenner gleich 0 setzen), und danach die Lösungen.',
  body='display(solve(x**2 - 9, x))\nsolve(Eq(5 / (x**2 - 9), 1), x)')
t('''Ein Schüler multipliziert `x²/(x − 3) = 9/(x − 3)` mit `(x − 3)` und löst `x² = 9`. Gib seine Lösungen aus und darunter die richtigen.''',
  body='display(solve(Eq(x**2, 9), x))\nsolve(Eq(x**2 / (x - 3), 9 / (x - 3)), x)')
t('''**Arbeit:** Ein Rohr füllt ein Becken in 6 Stunden, ein zweites in 3 Stunden. Wie lange dauert es mit beiden? Löse `1/6 + 1/3 = 1/x`.
Schreibe die Brüche mit `Rational`, sonst rechnet Python `1/6` als Kommazahl und das Ergebnis wird `2.0`.''',
  body='solve(Eq(Rational(1, 6) + Rational(1, 3), 1 / x), x)')

# ---------------------------------------------------------------- 4
sec('Lineare Gleichungssysteme')
expl('''#### Mehrere Gleichungen mit mehreren Variablen

`solve([gleichung1, gleichung2], [x, y])` löst ein Gleichungssystem und gibt ein **Dictionary** {x: ..., y: ...} zurück.
Mit `loesung[x]` bekommt man den Wert für x.

`linsolve([gl1, gl2], [x, y])` gibt die Lösungsmenge zurück. Hat das System keine Lösung, ist sie leer (∅).
Hat es unendlich viele, enthält sie die Lösungen mit einem Parameter (z. B. alle Paare (x, 3 − x)).''',
     """gl1 = Eq(2*x + y, 7)
gl2 = Eq(x - y, -1)
l = solve([gl1, gl2], [x, y])
display(l)
display(l[x])
display(linsolve([Eq(x + y, 1), Eq(x + y, 2)], [x, y]))
linsolve([Eq(x + y, 3), Eq(2*x + 2*y, 6)], [x, y])""")

t('Löse das System `x + y = 10`, `x − y = 4`.', body='solve([Eq(x + y, 10), Eq(x - y, 4)], [x, y])')
t('Löse das System `3x + 2y = 12`, `x = 2y`.', body='solve([Eq(3*x + 2*y, 12), Eq(x, 2*y)], [x, y])')
t('Löse das System `2x − 3y = 1`, `4x + y = 9`.', body='solve([Eq(2*x - 3*y, 1), Eq(4*x + y, 9)], [x, y])')
t('Gib die Lösungsmenge von `x + 2y = 4`, `2x + 4y = 5` mit `linsolve()` aus.', body='linsolve([Eq(x + 2*y, 4), Eq(2*x + 4*y, 5)], [x, y])')
t('Gib die Lösungsmenge von `x − y = 1`, `3x − 3y = 3` mit `linsolve()` aus.', body='linsolve([Eq(x - y, 1), Eq(3*x - 3*y, 3)], [x, y])')
t('Löse das System mit drei Gleichungen: `x + y + z = 6`, `x − y + z = 2`, `2x + y − z = 1`.',
  body='solve([Eq(x + y + z, 6), Eq(x - y + z, 2), Eq(2*x + y - z, 1)], [x, y, z])')
t('''**Einsetzungsverfahren von Hand:** Löse `y = 2x − 1` und `3x + y = 9`. Setze dazu den Term für y in die zweite Gleichung ein
(`subs()`), löse nach x und berechne dann y. Gib x und y aus.''',
  body='x_wert = solve(Eq(3*x + (2*x - 1), 9), x)[0]\ndisplay(x_wert)\n(2*x - 1).subs(x, x_wert)')
t('''**Kino:** Für 3 Erwachsene und 2 Kinder zahlt man 41 €, für 2 Erwachsene und 4 Kinder 38 €. Was kostet eine Karte für Erwachsene (x)
und für Kinder (y)?''', body='solve([Eq(3*x + 2*y, 41), Eq(2*x + 4*y, 38)], [x, y])')
t('''**Mischung:** Aus Tee für 12 €/kg und Tee für 20 €/kg sollen 10 kg Mischung für 15 €/kg entstehen. Wie viel kg braucht man von jeder Sorte?''',
  body='solve([Eq(x + y, 10), Eq(12*x + 20*y, 15 * 10)], [x, y])')
t('''Bestimme die Gerade `y = m·x + n` durch die Punkte (1, 3) und (4, 9): Löse das System für `m` und `n`.''',
  given="m, n = symbols('m n')", body='solve([Eq(3, m*1 + n), Eq(9, m*4 + n)], [m, n])')
t('''Bestimme die Parabel `y = ax² + bx + c` durch die Punkte (0, 1), (1, 0) und (2, 3).''',
  body='solve([Eq(1, c), Eq(0, a + b + c), Eq(3, 4*a + 2*b + c)], [a, b, c])')
predict("""display(solve([Eq(x + y, 2), Eq(x - y, 0)], [x, y]))
display(linsolve([Eq(x, 1), Eq(x, 2)], [x, y]))
linsolve([Eq(x + y, 5)], [x, y])""")

# ---------------------------------------------------------------- 5
sec('Ungleichungen')
expl('''#### Ungleichungen lösen

`solve(ungleichung, x)` löst eine Ungleichung und gibt die Bedingung für x zurück, z. B. `x < 4`.
Das Zeichen ∧ bedeutet „und“, ∨ bedeutet „oder“.

`solveset(ungleichung, x, domain=S.Reals)` gibt die Lösungsmenge als **Intervall** zurück: (−2, 2) ist das offene Intervall
von −2 bis 2 (ohne die Grenzen), [−2, 2] mit den Grenzen. ∪ verbindet zwei Intervalle.

Achtung bei Ungleichungen: Multipliziert man mit einer negativen Zahl, dreht sich das Zeichen um.''',
     """display(solve(3*x - 5 < 7, x))
display(solve(-2*x > 6, x))
display(solve(x**2 - 4 < 0, x))
display(solveset(x**2 - 4 < 0, x, domain=S.Reals))
solveset(x**2 - 4 >= 0, x, domain=S.Reals)""")

t('Löse `4x + 3 > 11`.', body='solve(4*x + 3 > 11, x)')
t('Löse `5 − 2x ≤ 1`.', body='solve(5 - 2*x <= 1, x)')
t('Gib die Lösungsmenge von `3(x − 1) ≥ 2x + 4` als Intervall aus.', body='solveset(3*(x - 1) >= 2*x + 4, x, domain=S.Reals)')
t('Gib die Lösungsmenge von `x² < 9` als Intervall aus.', body='solveset(x**2 < 9, x, domain=S.Reals)')
t('Gib die Lösungsmenge von `x² − 5x + 6 > 0` aus.', body='solveset(x**2 - 5*x + 6 > 0, x, domain=S.Reals)')
t('Gib die Lösungsmenge von `(x − 1)(x + 3) ≤ 0` aus.', body='solveset((x - 1) * (x + 3) <= 0, x, domain=S.Reals)')
t('Gib die Lösungsmenge von `x² + 1 > 0` aus.', body='solveset(x**2 + 1 > 0, x, domain=S.Reals)')
t('''**Handytarif:** Tarif A kostet 5 € plus 0,09 € pro Minute, Tarif B 15 € plus 0,04 € pro Minute. Ab wie vielen Minuten ist B günstiger?
Löse `15 + 0,04x < 5 + 0,09x` (mit `Rational`).''',
  body="solve(15 + Rational('0.04')*x < 5 + Rational('0.09')*x, x)")
predict("""display(solve(x > 3, x))
display(solve(-x > 3, x))
solveset(x**2 <= 0, x, domain=S.Reals)""")

# ---------------------------------------------------------------- 6
sec('Wurzelgleichungen')
expl('''#### Quadrieren und Probe

Eine **Wurzelgleichung** löst man von Hand, indem man die Wurzel allein auf eine Seite bringt und beide Seiten **quadriert**.
Quadrieren ist aber keine Äquivalenzumformung: Es können **Scheinlösungen** entstehen. Deshalb ist die Probe Pflicht.

`solve()` macht die Probe selbst und gibt nur die echten Lösungen zurück.''',
     """gl = Eq(sqrt(x + 2), x)
display(gl)
display(solve(Eq(x + 2, x**2), x))
display(solve(gl, x))
[gl.subs(x, w) for w in [-1, 2]]""")

t('Löse `√x = 5`.', body='solve(Eq(sqrt(x), 5), x)')
t('Löse `√(2x + 3) = 7`.', body='solve(Eq(sqrt(2*x + 3), 7), x)')
t('Löse `√(x + 6) = x`.', body='solve(Eq(sqrt(x + 6), x), x)')
t('''Löse `√(x + 6) = x` von Hand: Quadriere beide Seiten und löse `x + 6 = x²`. Gib diese Lösungen aus und darunter für jede die Probe
(`Eq(sqrt(x + 6), x).subs(x, ...)`) als Liste.''',
  body='l = solve(Eq(x + 6, x**2), x)\ndisplay(l)\n[Eq(sqrt(x + 6), x).subs(x, w) for w in l]')
t('Löse `√(x − 1) + 3 = x`.', body='solve(Eq(sqrt(x - 1) + 3, x), x)')
t('Gib die reelle Lösungsmenge von `√x = −2` aus.', body='solveset(Eq(sqrt(x), -2), x, domain=S.Reals)')
t('''Ein Quadrat hat die Diagonale `d = √2 · a`. Wie lang ist die Seite `a`, wenn die Diagonale 10 cm lang ist?''',
  body='solve(Eq(sqrt(2) * x, 10), x)')

# ---------------------------------------------------------------- 7
sec('Potenz- und Exponentialgleichungen')
expl('''#### Potenzgleichungen

Eine **Potenzgleichung** xⁿ = a löst man mit der n-ten Wurzel. Bei geradem n gibt es für a > 0 zwei reelle Lösungen (±).
Weil `solve()` auch komplexe Lösungen findet, verwendet man hier besser `solveset(..., domain=S.Reals)`.''',
     """display(solve(x**3 - 8, x))
display(solveset(x**3 - 8, x, domain=S.Reals))
solveset(x**4 - 16, x, domain=S.Reals)""")
expl('''#### Exponentialgleichungen und Logarithmus

Bei einer **Exponentialgleichung** steht die Variable im Exponenten, z. B. 2ˣ = 32. Die Lösung ist der **Logarithmus**:
x = log₂(32) = 5, denn 2⁵ = 32. In sympy ist `log(32, 2)` der Logarithmus zur Basis 2, `log(x)` ohne Basis der natürliche Logarithmus (Basis e).

Oft kommt kein glattes Ergebnis heraus. Dann gibt sympy einen Ausdruck mit `log` zurück, und `N()` liefert einen Näherungswert.''',
     """display(solve(Eq(2**x, 32), x))
display(log(32, 2))
l = solve(Eq(Rational(105, 100)**x, 2), x)
display(l)
N(l[0], 5)""")

t('Gib die reellen Lösungen von `x³ = 27` aus.', body='solveset(Eq(x**3, 27), x, domain=S.Reals)')
t('Gib die reellen Lösungen von `x⁴ = 81` aus.', body='solveset(Eq(x**4, 81), x, domain=S.Reals)')
t('Gib die reellen Lösungen von `2x⁵ = −64` aus.', body='solveset(Eq(2*x**5, -64), x, domain=S.Reals)')
t('Löse `3ˣ = 81`.', body='solve(Eq(3**x, 81), x)')
t('Berechne log₂(1024), log₁₀(0,001) und log₅(1/25).', body="display(log(1024, 2), log(Rational('0.001'), 10), log(Rational(1, 25), 5))")
t('Löse `2ˣ = 10` exakt und gib einen Näherungswert mit 4 Ziffern aus.', body='l = solve(Eq(2**x, 10), x)\ndisplay(l)\nN(l[0], 4)')
t('Löse `5 · 1,2ˣ = 30` und gib einen Näherungswert mit 4 Ziffern aus.', body="N(solve(Eq(5 * Rational('1.2')**x, 30), x)[0], 4)")
t('''**Verdopplungszeit:** Ein Kapital wächst mit 3 % Zinsen pro Jahr. Nach wie vielen Jahren hat es sich verdoppelt? Löse `1,03ˣ = 2`
und gib das Ergebnis mit 4 Ziffern aus.''', body="N(solve(Eq(Rational('1.03')**x, 2), x)[0], 4)")
t('''**Halbwertszeit:** Von einem radioaktiven Stoff zerfallen pro Jahr 5 %. Nach wie vielen Jahren ist nur noch die Hälfte da?
Löse `0,95ˣ = 0,5` und gib das Ergebnis mit 4 Ziffern aus.''', body="N(solve(Eq(Rational('0.95')**x, Rational('0.5')), x)[0], 4)")
t('''Eine Bakterienkultur hat 500 Bakterien und wächst um 20 % pro Stunde. Ab wann sind es mehr als 10000? Löse `500 · 1,2ˣ = 10000`
und gib das Ergebnis aufgerundet als ganze Stunde aus (`ceiling()`).''', body="ceiling(solve(Eq(500 * Rational('1.2')**x, 10000), x)[0])")
predict("""display(log(8, 2))
display(log(1, 10))
display(solve(Eq(10**x, 1000), x))
N(log(2, 10), 3)""")

# ---------------------------------------------------------------- 8
sec('Substitution und näherungsweises Lösen')
expl('''#### Substitution

Eine Gleichung wie x⁴ − 5x² + 4 = 0 löst man von Hand mit einer **Substitution**: Man ersetzt x² durch eine neue Variable u
und erhält die quadratische Gleichung u² − 5u + 4 = 0. Aus jeder Lösung für u bekommt man dann x = ±√u.''',
     """u = symbols('u')
display(solve(u**2 - 5*u + 4, u))
display([solveset(Eq(x**2, w), x, domain=S.Reals) for w in [1, 4]])
solveset(x**4 - 5*x**2 + 4, x, domain=S.Reals)""")
expl('''#### Näherungsweise lösen mit `nsolve()`

Viele Gleichungen kann man nicht exakt lösen, z. B. x³ − 2x − 5 = 0 hat zwar eine Lösungsformel, die aber sehr unhandlich ist,
und cos(x) = x hat gar keine. `nsolve(gleichung, x, startwert)` sucht eine Lösung in der Nähe des Startwerts **numerisch**
(mit dem Newton-Verfahren). Einen guten Startwert findet man z. B. mit einer Wertetabelle.''',
     """display([(k, k**3 - 2*k - 5) for k in range(4)])
display(nsolve(x**3 - 2*x - 5, x, 2))
nsolve(Eq(cos(x), x), x, 1)""")

t('Löse `x⁴ − 13x² + 36 = 0` mit der Substitution u = x²: Gib zuerst die Lösungen für u aus, dann die reelle Lösungsmenge für x.',
  given="u = symbols('u')", body='display(solve(u**2 - 13*u + 36, u))\nsolveset(x**4 - 13*x**2 + 36, x, domain=S.Reals)')
t('Gib die reelle Lösungsmenge von `x⁴ − 3x² − 4 = 0` aus.', body='solveset(x**4 - 3*x**2 - 4, x, domain=S.Reals)')
t('Löse `(x² − 1)² − 5(x² − 1) + 6 = 0` mit `solveset()` über den reellen Zahlen.', body='solveset((x**2 - 1)**2 - 5*(x**2 - 1) + 6, x, domain=S.Reals)')
t('Löse `4ˣ − 6 · 2ˣ + 8 = 0` mit der Substitution u = 2ˣ: Löse zuerst nach u, dann `2ˣ = 2` und `2ˣ = 4`.',
  given="u = symbols('u')", body='display(solve(u**2 - 6*u + 8, u))\n[solve(Eq(2**x, w), x) for w in [2, 4]]')
t('Bestimme die Lösung von `x³ + x − 3 = 0` in der Nähe von 1 mit `nsolve()`.', body='nsolve(x**3 + x - 3, x, 1)')
t('Bestimme mit `nsolve()` die Lösung von `2ˣ = x + 3` in der Nähe von 2.', body='nsolve(Eq(2**x, x + 3), x, 2)')
t('''Die Gleichung `2ˣ = x + 3` hat auch eine negative Lösung. Erstelle eine Wertetabelle von `2**x - x - 3` für x von −4 bis 0 (als Liste von Paaren,
Werte mit `N()` auf 3 Ziffern) und bestimme dann die Lösung mit `nsolve()` und einem passenden Startwert.''',
  body='display([(k, N(Integer(2)**k - k - 3, 3)) for k in range(-4, 1)])\nnsolve(Eq(2**x, x + 3), x, -3)')
t('Bestimme die Lösung von `cos(x) = x/2` mit `nsolve()` und dem Startwert 1.', body='nsolve(Eq(cos(x), x / 2), x, 1)')

# ---------------------------------------------------------------- 9
sec('Gemischte Übungen')
t('''Ein Zug fährt um 8 Uhr mit 120 km/h in A ab, ein zweiter um 9 Uhr mit 160 km/h ebenfalls in A in dieselbe Richtung. Nach wie vielen Stunden
(ab 8 Uhr gerechnet) holt der zweite den ersten ein? Löse `120t = 160(t − 1)`.''',
  given="t = symbols('t')", body='solve(Eq(120*t, 160*(t - 1)), t)')
t('''Die Summe zweier Zahlen ist 50, ihr Produkt 600. Bestimme die Zahlen mit `solve()` für das Gleichungssystem.''',
  body='solve([Eq(x + y, 50), Eq(x * y, 600)], [x, y])')
t('''Ein Quader hat eine quadratische Grundfläche mit der Seite `x` und die Höhe 5. Sein Volumen beträgt 180. Bestimme `x` (nur positive Lösung).''',
  body='solveset(Eq(x**2 * 5, 180), x, domain=Interval(0, oo))')
t('''Für welche `x` ist der Term `(x − 2)/(x² − 1)` positiv? Gib die Lösungsmenge von `(x − 2)/(x² − 1) > 0` aus.''',
  body='solveset((x - 2) / (x**2 - 1) > 0, x, domain=S.Reals)')
t('''Ein Kapital von 2000 € soll durch Zinseszins in 10 Jahren auf 3000 € wachsen. Welcher Zinssatz ist nötig? Löse `2000 q¹⁰ = 3000`
für positives `q` und gib `(q − 1) · 100` mit 3 Ziffern aus.''',
  given="q = symbols('q', positive=True)", body='q_wert = solve(Eq(2000 * q**10, 3000), q)[0]\nN((q_wert - 1) * 100, 3)')
t('''Bestimme den Schnittpunkt der Geraden `y = 2x − 1` und `y = −x + 5`.''', body='solve([Eq(y, 2*x - 1), Eq(y, -x + 5)], [x, y])')
t('''Bestimme die Schnittpunkte der Parabel `y = x²` mit der Geraden `y = x + 2`.''', body='solve([Eq(y, x**2), Eq(y, x + 2)], [x, y])')

generate('sympy_gleichungen', 'Gleichungen, Gleichungssysteme und Ungleichungen', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
