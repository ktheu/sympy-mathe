# Erzeugt ../content/sympy_funktionen.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_funktionen.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_funktionen.py
#
# Bildungsplan BW 2016, Leitidee Funktionaler Zusammenhang: Klassen 7/8 (lineare Funktionen, Gerade durch zwei Punkte,
# Lagebeziehung, quadratische Funktionen, Scheitelform, Linearfaktoren, Parameter, Extremwerte), 9/10 (Potenz-, Wurzel-,
# Exponential-, ganzrationale und Sinusfunktionen, Parameter, Nullstellen mit Vielfachheit, Symmetrie, Verhalten für x → ±∞,
# Definitions- und Wertemenge, Wachstum, Halbwertszeit).
# Die Setup-Zelle importiert matplotlib, damit Pyodide es lädt (sonst zeichnet sympy.plot nur einen Text-Plot).
# Diagramme: plot(...); mit Semikolon, die Bilder sammelt sympy_ausgabe.py ein.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = "from sympy import *\ninit_printing()\nimport matplotlib.pyplot as plt\nx, y, a, b, c = symbols('x y a b c')"

INTRO = '''In diesem Notebook untersuchst du **Funktionen** mit sympy: Funktionswerte und Wertetabellen, Graphen, lineare und quadratische
Funktionen, Potenz-, Wurzel- und Exponentialfunktionen, ganzrationale Funktionen und die Sinusfunktion. Du bestimmst Nullstellen,
Scheitelpunkte, Schnittpunkte, Symmetrie und das Verhalten für große x.

Vorausgesetzt werden die Notebooks *Zahlen exakt*, *Terme* und *Gleichungen*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**, bei Graphen als Bild.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy, schaltet die Formel-Ausgabe ein,
lädt matplotlib für die Graphen und legt die Variablen `x`, `y`, `a`, `b` und `c` an.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Funktionen und Funktionswerte')
expl('''#### Eine Funktion als Python-Funktion

Eine Funktion wie f(x) = x² − 3x schreibt man in Python mit `def`:

```python
def f(x):
    return x**2 - 3*x
```

Dann ist `f(2)` der Funktionswert an der Stelle 2 und `f(x)` der Funktionsterm. Mit `f(a + 1)` setzt man auch Terme ein.
Steht im Term eine **Division**, setze Zahlen als `Integer(...)` oder `Rational(...)` ein, sonst rechnet Python mit Kommazahlen:
Für f(x) = 1/x ist `f(2)` die Kommazahl 0.5, `f(Integer(2))` der Bruch 1/2.
Eine **Wertetabelle** erstellt man mit einer List Comprehension.''',
     """def f(x):
    return x**2 - 3*x

display(f(2))
display(f(Rational(1, 2)))
display(f(x))
display(expand(f(a + 1)))
[(k, f(k)) for k in range(-1, 5)]""")

t('Definiere `f(x) = 2x² − 5` und gib `f(3)` und `f(−1/2)` aus.',
  body='def f(x):\n    return 2*x**2 - 5\n\ndisplay(f(3))\nf(Rational(-1, 2))')
t('Erstelle für `g(x) = x³ − 2x` eine Wertetabelle als Liste von Paaren für die ganzen Zahlen von −2 bis 2.',
  body='def g(x):\n    return x**3 - 2*x\n\n[(k, g(k)) for k in range(-2, 3)]')
t('Definiere `h(x) = (x + 1)/(x − 2)` und gib `h(0)` und `h(3)` exakt (mit `Integer`) sowie `h(√2)` (mit `radsimp()`) aus.',
  body='def h(x):\n    return (x + 1) / (x - 2)\n\ndisplay(h(Integer(0)), h(Integer(3)))\nradsimp(h(sqrt(2)))')
t('Für `f(x) = x² + 1`: Gib `f(a + b)` ausmultipliziert aus.', body='def f(x):\n    return x**2 + 1\n\nexpand(f(a + b))')
t('Für `f(x) = 3x − 4`: Gib `f(f(x))` vereinfacht aus.', body='def f(x):\n    return 3*x - 4\n\nexpand(f(f(x)))')
t('Für `f(x) = x²`: Gib den Differenzenquotienten `(f(x + h) − f(x))/h` vereinfacht aus.',
  given="h = symbols('h')", body='def f(x):\n    return x**2\n\nsimplify((f(x + h) - f(x)) / h)')

# ---------------------------------------------------------------- 2
sec('Graphen zeichnen')
expl('''#### `plot()`

`plot(term, (x, von, bis))` zeichnet den Graphen. Schreibe ein **Semikolon** `;` ans Ende der Zeile, sonst gibt Jupyter unter dem Bild
noch eine unschöne Textzeile aus.

- Mehrere Graphen: `plot(term1, term2, (x, -3, 3))`, mit `legend=True` erscheint eine Legende.
- `ylim=(-5, 5)` legt den Bereich der y-Achse fest, `title='...'` setzt eine Überschrift.
- Die Achsen schneiden sich wie im Heft im Ursprung.''',
     """plot(x**2 - 2, (x, -3, 3));""")
expl('''#### Mehrere Graphen''',
     """plot(x**2, 2*x**2, x**2 / 2, (x, -2, 2), legend=True, title='Parabeln');""")

t('Zeichne den Graphen von `f(x) = x² − 4x + 3` für x von −1 bis 5.', body='plot(x**2 - 4*x + 3, (x, -1, 5));')
t('Zeichne die Graphen von `2x − 1` und `−x + 5` für x von −2 bis 4 mit Legende.', body='plot(2*x - 1, -x + 5, (x, -2, 4), legend=True);')
t('Zeichne den Graphen von `1/x` für x von −4 bis 4 mit der y-Achse von −5 bis 5.', body='plot(1 / x, (x, -4, 4), ylim=(-5, 5));')
t('Zeichne `x³ − 3x` für x von −2,5 bis 2,5 mit der Überschrift `f(x) = x³ − 3x`.',
  body="plot(x**3 - 3*x, (x, -2.5, 2.5), title='f(x) = x³ − 3x');")
predict("""plot(x, x**2, x**3, (x, -1.5, 1.5), legend=True);""")

# ---------------------------------------------------------------- 3
sec('Lineare Funktionen')
expl('''#### Steigung, Gerade durch zwei Punkte, Schnittpunkt

Eine lineare Funktion hat die Gleichung f(x) = m·x + c mit der **Steigung** m und dem **y-Achsenabschnitt** c.

- Durch die Punkte (x₁, y₁) und (x₂, y₂): m = (y₂ − y₁)/(x₂ − x₁), danach c aus y₁ = m·x₁ + c.
- **Nullstelle:** `solve(m*x + c, x)`
- **Schnittpunkt** zweier Geraden: Funktionsterme gleichsetzen.
- Zwei Geraden sind **parallel**, wenn sie dieselbe Steigung haben.''',
     """m = Rational(7 - 1, 4 - 1)
c0 = 1 - m * 1
display(m, c0)
g = m*x + c0
display(g)
display(solve(g, x))
solve(Eq(g, -x + 7), x)""")

t('Bestimme die Steigung der Geraden durch die Punkte (2, 3) und (6, 11).', body='Rational(11 - 3, 6 - 2)')
t('Bestimme die Gleichung der Geraden durch (−1, 4) und (3, −4). Gib den Term `m·x + c` aus.',
  body='m = Rational(-4 - 4, 3 - (-1))\nc0 = 4 - m * (-1)\nm*x + c0')
t('Bestimme die Nullstelle von `f(x) = 3x − 7`.', body='solve(3*x - 7, x)')
t('Bestimme den Schnittpunkt der Geraden `y = 2x + 1` und `y = −x + 7`: Gib die x-Koordinate und den Punkt als Tupel aus.',
  body='xs = solve(Eq(2*x + 1, -x + 7), x)[0]\ndisplay(xs)\n(xs, 2*xs + 1)')
t('Prüfe, ob die Geraden `y = 3x − 2` und `y = 3x + 5` einen Schnittpunkt haben: Gib die Lösungsmenge der Gleichung aus.',
  body='solveset(Eq(3*x - 2, 3*x + 5), x, domain=S.Reals)')
t('Bestimme die Gleichung der Geraden, die parallel zu `y = −2x + 1` ist und durch den Punkt (3, 4) geht.',
  body='c0 = 4 - (-2) * 3\n-2*x + c0')
t('''**Taxi:** Ein Taxi kostet 4 € Grundgebühr und 2,20 € pro km. Gib den Funktionsterm für die Kosten aus, berechne die Kosten für 12 km
und die Strecke, die man für 30 € fahren kann.''',
  body="k = 4 + Rational('2.2')*x\ndisplay(k)\ndisplay(k.subs(x, 12))\nsolve(Eq(k, 30), x)")
t('Zeichne die Geraden `y = 0,5x + 1` und `y = −2x + 6` für x von −1 bis 4 mit Legende und gib ihren Schnittpunkt als Tupel aus.',
  body="g1 = Rational(1, 2)*x + 1\ng2 = -2*x + 6\nplot(g1, g2, (x, -1, 4), legend=True)\nxs = solve(Eq(g1, g2), x)[0]\n(xs, g1.subs(x, xs))")
predict("""m = Rational(2, 4)
display(m * 6)
solve(Eq(m*x + 1, 0), x)""")

# ---------------------------------------------------------------- 4
sec('Quadratische Funktionen')
expl('''#### Scheitelpunkt und Scheitelform

f(x) = a·x² + b·x + c hat den **Scheitelpunkt** S(xₛ | yₛ) mit xₛ = −b/(2a) und yₛ = f(xₛ).
Die **Scheitelform** ist f(x) = a(x − xₛ)² + yₛ. Ob man richtig umgeformt hat, prüft man mit `expand()`.

Die **Nullstellen** liefert `solve()`, die **Linearfaktorform** a(x − x₁)(x − x₂) liefert `factor()`.''',
     """def f(x):
    return 2*x**2 - 8*x + 6

xs = Rational(8, 2 * 2)
display(xs, f(xs))
scheitelform = 2*(x - xs)**2 + f(xs)
display(scheitelform)
display(expand(scheitelform) == f(x))
display(solve(f(x), x))
factor(f(x))""")
expl('''#### Die Parameter der Scheitelform

In f(x) = a(x − d)² + e verschiebt d den Graphen nach rechts, e nach oben. a streckt ihn (|a| > 1), staucht ihn (|a| < 1)
oder spiegelt ihn an der x-Achse (a < 0).''',
     """plot(x**2, (x - 2)**2 + 1, -Rational(1, 2)*(x + 1)**2 + 3, (x, -4, 4), ylim=(-3, 8), legend=True);""")

t('Bestimme den Scheitelpunkt von `f(x) = x² − 6x + 5` als Tupel.', body='xs = Rational(6, 2)\n(xs, (x**2 - 6*x + 5).subs(x, xs))')
t('Bestimme den Scheitelpunkt von `f(x) = −2x² + 4x + 1` als Tupel.', body='xs = Rational(-4, 2 * -2)\n(xs, (-2*x**2 + 4*x + 1).subs(x, xs))')
t('Prüfe, dass `(x − 3)² − 4` die Scheitelform von `x² − 6x + 5` ist.', body='expand((x - 3)**2 - 4) == x**2 - 6*x + 5')
t('Bestimme die Nullstellen von `f(x) = x² − 6x + 5` und gib die Linearfaktorform aus.', body='display(solve(x**2 - 6*x + 5, x))\nfactor(x**2 - 6*x + 5)')
t('Gib die Normalform der Parabel mit dem Scheitel S(−1 | 4) und a = −1 aus.', body='expand(-(x + 1)**2 + 4)')
t('Gib die Normalform der Parabel mit den Nullstellen −2 und 3 aus, die durch den Punkt (0, 12) geht. Tipp: a(x + 2)(x − 3), a aus dem Punkt bestimmen.',
  body='a_wert = solve(Eq(a * (0 + 2) * (0 - 3), 12), a)[0]\nexpand(a_wert * (x + 2) * (x - 3))')
t('Zeichne `x² − 6x + 5` und seine Scheitelform `(x − 3)² − 4` für x von 0 bis 6 (die Graphen liegen übereinander).',
  body='plot(x**2 - 6*x + 5, (x - 3)**2 - 4, (x, 0, 6));')
t('Zeichne die Parabeln `(x − d)²` für d = −2, 0, 2 für x von −5 bis 5 mit Legende.',
  body='plot((x + 2)**2, x**2, (x - 2)**2, (x, -5, 5), ylim=(-1, 10), legend=True);')
t('''**Extremwertaufgabe:** Ein Rechteck hat den Umfang 24 cm. Seine Breite ist x, die Länge 12 − x. Gib den Term für den Flächeninhalt aus,
bestimme die Breite mit dem größten Flächeninhalt (Scheitelstelle) und den größten Flächeninhalt.''',
  body='A = expand(x * (12 - x))\ndisplay(A)\nxs = Rational(-12, 2 * -1)\ndisplay(xs)\nA.subs(x, xs)')
t('''Ein Ball wird geworfen. Seine Höhe ist `h(t) = −5t² + 20t + 1,5` (t in s, h in m). Gib die größte Höhe aus und den Zeitpunkt, an dem er auf dem
Boden aufkommt (positive Nullstelle, mit `N()` auf 3 Ziffern).''',
  given="t = symbols('t')",
  body="h = -5*t**2 + 20*t + Rational('1.5')\ntm = Rational(-20, 2 * -5)\ndisplay(h.subs(t, tm))\nN(max(solve(h, t)), 3)")
t('Bestimme mit `maximum()` den größten Wert von `−x² + 4x + 1` auf den reellen Zahlen. Vergleiche mit der Scheitelpunktberechnung.',
  body='maximum(-x**2 + 4*x + 1, x, S.Reals)')
predict("""display(factor(x**2 - 4*x + 4))
display(solve(x**2 - 4*x + 4, x))
minimum(x**2 - 4*x + 4, x, S.Reals)""")

# ---------------------------------------------------------------- 5
sec('Potenz- und Wurzelfunktionen')
expl('''#### Potenzfunktionen, Symmetrie, Definitions- und Wertemenge

f(x) = xⁿ: Bei **geradem** n ist der Graph **achsensymmetrisch** zur y-Achse (f(−x) = f(x)), bei **ungeradem** n **punktsymmetrisch**
zum Ursprung (f(−x) = −f(x)). Das prüft man mit `simplify(f(-x) - f(x)) == 0` bzw. `simplify(f(-x) + f(x)) == 0`.

Die **Definitionsmenge** (für welche x ist f definiert?) und die **Wertemenge** (welche y kommen vor?) bestimmen
`continuous_domain()` und `function_range()`. Sie müssen extra importiert werden.''',
     """from sympy.calculus.util import continuous_domain, function_range
plot(x**2, x**3, x**4, (x, -1.5, 1.5), ylim=(-3, 3), legend=True)
f = x**3
display(simplify(f.subs(x, -x) + f) == 0)
display(continuous_domain(sqrt(x), x, S.Reals))
display(function_range(x**2, x, S.Reals))
function_range(1 / x, x, S.Reals)""")

t('Zeichne die Graphen von `x⁻¹` und `x⁻²` für x von −3 bis 3 mit der y-Achse von −5 bis 5 und Legende.',
  body='plot(x**-1, x**-2, (x, -3, 3), ylim=(-5, 5), legend=True);')
t('Prüfe, ob `f(x) = x⁴ − 3x²` achsensymmetrisch zur y-Achse ist.', body='f = x**4 - 3*x**2\nsimplify(f.subs(x, -x) - f) == 0')
t('Prüfe, ob `f(x) = x³ − 2x` punktsymmetrisch zum Ursprung ist.', body='f = x**3 - 2*x\nsimplify(f.subs(x, -x) + f) == 0')
t('Prüfe, ob `f(x) = x³ + x²` achsensymmetrisch oder punktsymmetrisch ist. Gib beide Prüfungen aus.',
  body='f = x**3 + x**2\ndisplay(simplify(f.subs(x, -x) - f) == 0)\nsimplify(f.subs(x, -x) + f) == 0')
t('Bestimme die Definitionsmenge von `√(x − 3)`.', given='from sympy.calculus.util import continuous_domain',
  body='continuous_domain(sqrt(x - 3), x, S.Reals)')
t('Bestimme die Definitionsmenge von `1/(x² − 4)`.', given='from sympy.calculus.util import continuous_domain',
  body='continuous_domain(1 / (x**2 - 4), x, S.Reals)')
t('Bestimme die Wertemenge von `x² − 4x + 1`.', given='from sympy.calculus.util import function_range',
  body='function_range(x**2 - 4*x + 1, x, S.Reals)')
t('Bestimme die Wertemenge von `√x + 2`.', given='from sympy.calculus.util import function_range',
  body='function_range(sqrt(x) + 2, x, S.Reals)')
t('Zeichne `√x` und `x²` für x von 0 bis 2 und gib die Schnittstellen aus (`solve(Eq(sqrt(x), x**2), x)`).',
  body='plot(sqrt(x), x**2, (x, 0, 2), legend=True)\nsolve(Eq(sqrt(x), x**2), x)')

# ---------------------------------------------------------------- 6
sec('Exponentialfunktionen und Wachstum')
expl('''#### f(x) = c · aˣ + d

- Für a > 1 wächst der Graph (**exponentielles Wachstum**), für 0 < a < 1 fällt er (**exponentielle Abnahme**).
- c ist der Funktionswert bei x = 0 (ohne d), d verschiebt den Graphen nach oben. Die Gerade y = d ist eine **Asymptote**.
- Das Verhalten für sehr große bzw. sehr kleine x bestimmt man mit dem **Grenzwert** `limit(f, x, oo)` bzw. `limit(f, x, -oo)`.
  `oo` (zwei kleine o) steht in sympy für ∞.''',
     """f = 3 * Rational(1, 2)**x + 1
plot(2**x, f, (x, -3, 4), ylim=(-1, 10), legend=True)
display(limit(f, x, oo))
limit(2**x, x, -oo)""")

t('Zeichne `2ˣ`, `3ˣ` und `0,5ˣ` für x von −3 bis 3 mit der y-Achse von 0 bis 10 und Legende.',
  body='plot(2**x, 3**x, Rational(1, 2)**x, (x, -3, 3), ylim=(0, 10), legend=True);')
t('Bestimme die Grenzwerte von `f(x) = 5 · 0,8ˣ + 2` für x → ∞ und x → −∞.',
  body="f = 5 * Rational('0.8')**x + 2\ndisplay(limit(f, x, oo))\nlimit(f, x, -oo)")
t('''Eine Population hat 200 Tiere und wächst um 15 % pro Jahr. Gib den Funktionsterm aus, die Größe nach 10 Jahren (ganzzahlig gerundet mit `round(N(...))`)
und die Verdopplungszeit mit 4 Ziffern.''',
  body="P = 200 * Rational('1.15')**x\ndisplay(P)\ndisplay(round(N(P.subs(x, 10))))\nN(solve(Eq(Rational('1.15')**x, 2), x)[0], 4)")
t('''Ein Medikament wird abgebaut: Von 400 mg sind nach jeder Stunde nur noch 80 % vorhanden. Gib die Halbwertszeit mit 4 Ziffern aus
und zeichne den Verlauf für die ersten 12 Stunden.''',
  body="M = 400 * Rational('0.8')**x\nplot(M, (x, 0, 12))\nN(solve(Eq(Rational('0.8')**x, Rational(1, 2)), x)[0], 4)")
t('''Bestimme `c` und `a` für eine Exponentialfunktion `f(x) = c · aˣ` durch die Punkte (0, 3) und (2, 12). Lege `a` positiv an.''',
  given="a = symbols('a', positive=True)", body='c0 = 3\na_wert = solve(Eq(c0 * a**2, 12), a)[0]\nc0 * a_wert**x')
t('''Ein Tee kühlt ab: `T(x) = 20 + 70 · 0,9ˣ` (x in Minuten). Gib die Temperatur, der sich der Tee annähert (Grenzwert für x → ∞), und den Zeitpunkt aus,
an dem er 40 °C hat (mit 4 Ziffern).''',
  body="T = 20 + 70 * Rational('0.9')**x\ndisplay(limit(T, x, oo))\nN(solve(Eq(T, 40), x)[0], 4)")
predict("""display(limit(2**(-x), x, oo))
display(limit(1 / x, x, oo))
limit(x**2, x, -oo)""")

# ---------------------------------------------------------------- 7
sec('Ganzrationale Funktionen')
expl('''#### Nullstellen mit Vielfachheit und Verhalten im Unendlichen

Eine **ganzrationale Funktion** (Polynomfunktion) ist eine Summe von Potenzen von x, z. B. f(x) = x³ − 3x + 2.

- `degree(f, x)` ist der **Grad** (höchste Potenz).
- `roots(f, x)` gibt die Nullstellen mit ihrer **Vielfachheit** als Dictionary zurück: {Nullstelle: Vielfachheit}.
  An einer **doppelten** Nullstelle berührt der Graph die x-Achse, an einer einfachen schneidet er sie.
- `factor(f)` zeigt die faktorisierte Form.
- Für x → ±∞ bestimmt der Summand mit der höchsten Potenz das Verhalten.''',
     """f = x**3 - 3*x + 2
display(degree(f, x))
display(roots(f, x))
display(factor(f))
display(limit(f, x, oo), limit(f, x, -oo))
plot(f, (x, -3, 2.5), ylim=(-5, 8));""")

t('Gib Grad, Nullstellen mit Vielfachheit und faktorisierte Form von `f(x) = x³ − x² − 4x + 4` aus.',
  body='f = x**3 - x**2 - 4*x + 4\ndisplay(degree(f, x))\ndisplay(roots(f, x))\nfactor(f)')
t('Gib die Nullstellen mit Vielfachheit von `f(x) = x⁴ − 2x³ + x²` aus.', body='roots(x**4 - 2*x**3 + x**2, x)')
t('Zeichne `f(x) = x⁴ − 2x³ + x²` für x von −0,7 bis 1,7 und achte auf die doppelten Nullstellen.', body='plot(x**4 - 2*x**3 + x**2, (x, -0.7, 1.7));')
t('Gib eine ganzrationale Funktion 3. Grades mit den Nullstellen −1, 2 und 4 und dem Faktor 1 ausmultipliziert aus.',
  body='expand((x + 1) * (x - 2) * (x - 4))')
t('Gib eine Funktion 4. Grades aus, die bei 0 eine doppelte Nullstelle und bei ±3 einfache Nullstellen hat (Faktor −1), ausmultipliziert.',
  body='expand(-x**2 * (x - 3) * (x + 3))')
t('Bestimme die Grenzwerte von `f(x) = −2x³ + 5x² + 1` für x → ∞ und x → −∞.', body='f = -2*x**3 + 5*x**2 + 1\ndisplay(limit(f, x, oo))\nlimit(f, x, -oo)')
t('Bestimme die reellen Nullstellen von `x³ − 2x − 1` exakt (`solveset`) und als Dezimalzahlen mit 4 Ziffern.',
  body='l = solveset(x**3 - 2*x - 1, x, domain=S.Reals)\ndisplay(l)\n[N(w, 4) for w in l]')
t('Bestimme die Nullstellen von `f(x) = x³ − 2x² − 5x + 6` und prüfe die Symmetrie (beide Prüfungen). Zeichne den Graphen für x von −3 bis 4.',
  body='f = x**3 - 2*x**2 - 5*x + 6\ndisplay(roots(f, x))\ndisplay(simplify(f.subs(x, -x) - f) == 0, simplify(f.subs(x, -x) + f) == 0)\nplot(f, (x, -3, 4));')
predict("""display(roots((x - 1)**2 * (x + 2), x))
display(degree(x**5 - x, x))
factor(x**3 - x**2)""")

# ---------------------------------------------------------------- 8
sec('Sinusfunktionen')
expl('''#### Bogenmaß und exakte Werte

In sympy rechnen `sin`, `cos` und `tan` im **Bogenmaß**: Der Vollwinkel 360° ist 2π. `rad(90)` rechnet 90° in Bogenmaß um (π/2),
`deg(pi)` umgekehrt. Für besondere Winkel kennt sympy **exakte** Werte: sin(π/6) = 1/2, sin(π/4) = √2/2.''',
     """display(rad(90), deg(pi / 3))
display(sin(pi / 6), sin(pi / 4), cos(pi / 3))
N(sin(1), 5)""")
expl('''#### f(x) = a · sin(b(x − c)) + d

- a ist die **Amplitude** (Streckung in y-Richtung),
- die **Periode** ist 2π/b (`periodicity(f, x)` berechnet sie),
- c verschiebt nach rechts, d nach oben.''',
     """display(periodicity(sin(3*x), x))
plot(sin(x), 2*sin(x), sin(2*x), (x, 0, 2*pi), legend=True);""")

t('Rechne 45°, 120° und 270° in Bogenmaß um.', body='display(rad(45), rad(120), rad(270))')
t('Gib die exakten Werte von `cos(π/6)`, `tan(π/4)` und `sin(2π/3)` aus.', body='display(cos(pi / 6), tan(pi / 4), sin(2*pi / 3))')
t('Gib `sin(37°)` mit 4 Ziffern aus.', body='N(sin(rad(37)), 4)')
t('Bestimme die Periode von `sin(4x)`, `cos(x/2)` und `3 sin(πx)`.', body='display(periodicity(sin(4*x), x), periodicity(cos(x / 2), x), periodicity(3*sin(pi*x), x))')
t('Zeichne `sin(x)` und `cos(x)` für x von −π bis 2π mit Legende.', body='plot(sin(x), cos(x), (x, -pi, 2*pi), legend=True);')
t('Zeichne `2 sin(x − π/2) + 1` für x von 0 bis 2π.', body='plot(2*sin(x - pi / 2) + 1, (x, 0, 2*pi));')
t('Prüfe, dass `sin(x + π/2) = cos(x)` gilt.', body='simplify(sin(x + pi / 2) - cos(x)) == 0')
t('Bestimme alle Lösungen von `sin(x) = 1/2` im Intervall [0, 2π].', body='solveset(Eq(sin(x), Rational(1, 2)), x, domain=Interval(0, 2*pi))')
t('''**Tageslänge:** In einer Stadt ist die Tageslänge (in Stunden) am Tag x des Jahres etwa `12 + 4,5 · sin(2π/365 · (x − 80))`.
Gib die Periode aus, zeichne den Verlauf für ein Jahr und gib die Tageslänge am Tag 172 (21. Juni) mit 3 Ziffern aus.''',
  body="L = 12 + Rational('4.5') * sin(2*pi / 365 * (x - 80))\ndisplay(periodicity(L, x))\nplot(L, (x, 0, 365))\nN(L.subs(x, 172), 3)")
predict("""display(sin(pi), cos(pi), sin(pi / 2))
display(periodicity(sin(x) + cos(x), x))
rad(180)""")

# ---------------------------------------------------------------- 9
sec('Gemischte Übungen')
t('''Bestimme die Schnittpunkte der Parabel `y = x² − 2` mit der Geraden `y = x` als Liste von Punkten und zeichne beide für x von −3 bis 3.''',
  body='plot(x**2 - 2, x, (x, -3, 3))\n[(w, w) for w in solve(Eq(x**2 - 2, x), x)]')
t('''Für welche Werte von `k` berührt die Gerade `y = k` die Parabel `y = x² − 4x + 7` genau in einem Punkt? Das ist der y-Wert des Scheitels.
Berechne ihn mit `minimum()`.''', body='minimum(x**2 - 4*x + 7, x, S.Reals)')
t('''Ein Sparkonto mit 1000 € wird mit 2 % verzinst, ein zweites mit 800 € mit 4 %. Ab welchem Jahr hat das zweite mehr Geld? Zeichne beide
Verläufe für 0 bis 20 Jahre und gib die Schnittstelle mit `nsolve()` (Startwert 10) aus.''',
  body="k1 = 1000 * Rational('1.02')**x\nk2 = 800 * Rational('1.04')**x\nplot(k1, k2, (x, 0, 20), legend=True)\nnsolve(Eq(k1, k2), x, 10)")
t('''Gib für `f(x) = x³ − 6x² + 9x` die Nullstellen mit Vielfachheit, das Verhalten für x → ±∞ und den Graphen für x von −0,5 bis 4,5 aus.''',
  body='f = x**3 - 6*x**2 + 9*x\ndisplay(roots(f, x))\ndisplay(limit(f, x, oo), limit(f, x, -oo))\nplot(f, (x, -0.5, 4.5));')
t('''Die Parabel `y = ax² + bx + c` geht durch die Punkte (−1, 6), (1, 2) und (2, 3). Bestimme a, b und c und gib den Scheitelpunkt als Tupel aus.''',
  body='l = solve([Eq(a - b + c, 6), Eq(a + b + c, 2), Eq(4*a + 2*b + c, 3)], [a, b, c])\nf = l[a]*x**2 + l[b]*x + l[c]\ndisplay(f)\nxs = -l[b] / (2 * l[a])\n(xs, f.subs(x, xs))')

generate('sympy_funktionen', 'Funktionen: Graphen, Nullstellen, Scheitel, Wachstum, Sinus', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
