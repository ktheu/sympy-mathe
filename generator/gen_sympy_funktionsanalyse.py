# Erzeugt ../content/sympy_funktionsanalyse.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_funktionsanalyse.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_funktionsanalyse.py
#
# Bildungsplan BW 2016, Kursstufe (Basis- und Leistungsfach), Leitidee Funktionaler Zusammenhang:
# Untersuchung von Funktionen mit e-Funktion und Sinus (Nullstellen, Grenzverhalten, Extrem- und Wendepunkte), Modellieren
# mit Sinusfunktionen, Extremwertprobleme, Bestimmen von Funktionen aus Eigenschaften (Steckbriefaufgaben, LGS),
# Funktionen mit Parametern (Funktionenscharen), Ortskurven (Zusatz), Umkehrfunktion und ihre Ableitung (Leistungsfach).
# Baut auf sympy_ableitungen (Klasse 10, Kurvendiskussion ganzrationaler Funktionen) und sympy_ableitungsregeln auf.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = ("from sympy import *\ninit_printing()\nimport matplotlib.pyplot as plt\nx, y = symbols('x y', real=True)\n"
         "a, b, c, d = symbols('a b c d', real=True)")

INTRO = '''In diesem Notebook untersuchst du Funktionen mit **e-Funktion** und **Sinus** vollständig, löst **Extremwertprobleme**,
bestimmst Funktionen aus vorgegebenen Eigenschaften (**Steckbriefaufgaben**) und untersuchst **Funktionenscharen**, also Funktionen
mit einem Parameter. Im Leistungsfach kommen **Umkehrfunktionen** dazu.

Die Denkarbeit bleibt bei dir: Welche Bedingung gehört zu welcher Eigenschaft? Was bedeutet das Ergebnis? sympy übernimmt das Rechnen.

Vorausgesetzt werden die Notebooks *Ableitungen* (Klasse 10) und *Ableitungsregeln*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy und matplotlib, schaltet die Formel-Ausgabe ein
und legt die reellen Variablen `x`, `y` und die Parameter `a`, `b`, `c`, `d` an.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Funktionen mit der e-Funktion untersuchen')
expl("""#### Die Schritte

1. **Nullstellen:** f(x) = 0. Da eˣ nie 0 ist, bleibt bei f(x) = g(x) · eˣ nur g(x) = 0 (**Satz vom Nullprodukt**).
2. **Grenzverhalten** für x → ±∞ mit `limit`.
3. **Extrempunkte:** f'(x) = 0 und Vorzeichen von f''.
4. **Wendepunkte:** f''(x) = 0 (und f''' ≠ 0).
5. **Graph** zeichnen.

`factor()` klammert die e-Funktion aus, dann sieht man die Nullstellen der Ableitungen direkt.""",
     """f = (x - 1) * exp(x)
display(solve(f, x))
display(limit(f, x, oo), limit(f, x, -oo))
f1, f2 = factor(diff(f, x)), factor(diff(f, x, 2))
display(f1, f2)
for xe in solve(f1, x):
    art = 'Hochpunkt' if f2.subs(x, xe) < 0 else 'Tiefpunkt'
    print(art)
    display((xe, f.subs(x, xe)))
xw = solve(f2, x)[0]
display((xw, f.subs(x, xw)))
plot(f, (x, -5, 1.5), ylim=(-1.5, 2));""")

F1 = 'f = x**2 * exp(-x)'
t('Gib für f(x) = x² · e⁻ˣ die Nullstellen und die Grenzwerte für x → ∞ und x → −∞ aus.', F1,
  'display(solve(f, x))\ndisplay(limit(f, x, oo))\nlimit(f, x, -oo)')
t('Gib für f(x) = x² · e⁻ˣ die ausgeklammerte erste Ableitung und die Extrempunkte (Art und Punkt wie im Beispiel) aus.', F1,
  "f1, f2 = factor(diff(f, x)), diff(f, x, 2)\ndisplay(f1)\nfor xe in solve(f1, x):\n    art = 'Hochpunkt' if f2.subs(x, xe) < 0 else 'Tiefpunkt'\n    print(art)\n    display((xe, f.subs(x, xe)))")
t('Gib für f(x) = x² · e⁻ˣ die Wendestellen genau und mit 4 Ziffern aus.', F1,
  'l = solve(diff(f, x, 2), x)\ndisplay(l)\n[N(w, 4) for w in l]')
t('Zeichne den Graphen von f(x) = x² · e⁻ˣ für −1 ≤ x ≤ 8.', F1, 'plot(f, (x, -1, 8));')
t('''Untersuche f(x) = (2 − x) · eˣ: Gib Nullstelle, Grenzwerte für x → ±∞, Extrempunkt und Wendepunkt (als Tupel) aus.''',
  body="f = (2 - x) * exp(x)\ndisplay(solve(f, x))\ndisplay(limit(f, x, oo), limit(f, x, -oo))\nxe = solve(diff(f, x), x)[0]\ndisplay((xe, f.subs(x, xe)))\nxw = solve(diff(f, x, 2), x)[0]\n(xw, f.subs(x, xw))")
t('''Untersuche f(x) = x · e^(−x²/2): Gib die Symmetrie (`simplify(f.subs(x, -x) + f) == 0` bedeutet punktsymmetrisch), die Extrempunkte
und die Wendestellen aus.''',
  body="f = x * exp(-x**2 / 2)\ndisplay(simplify(f.subs(x, -x) + f) == 0)\ndisplay([(w, f.subs(x, w)) for w in solve(diff(f, x), x)])\nsolve(diff(f, x, 2), x)")
t('''Untersuche f(x) = eˣ − x: Gib den Extrempunkt und den kleinsten Wert von f auf ganz ℝ aus (`minimum(f, x, S.Reals)`).
Ist er positiv, hat f keine Nullstelle.''',
  body="f = exp(x) - x\nxe = solve(diff(f, x), x)[0]\ndisplay((xe, f.subs(x, xe)))\nminimum(f, x, S.Reals)")
t('''Bestimme, wo f(x) = x · e⁻ˣ streng monoton steigt (Lösungsmenge von f'(x) > 0) und wo der Graph linksgekrümmt ist (f''(x) > 0).''',
  body="f = x * exp(-x)\ndisplay(solveset(diff(f, x) > 0, x, S.Reals))\nsolveset(diff(f, x, 2) > 0, x, S.Reals)")
t('''Untersuche f(x) = 4/(1 + e⁻ˣ) (eine **logistische Funktion**): Gib die Grenzwerte für x → ±∞ (waagrechte Asymptoten) und den Wendepunkt aus.''',
  body="f = 4 / (1 + exp(-x))\ndisplay(limit(f, x, oo), limit(f, x, -oo))\nxw = solve(diff(f, x, 2), x)[0]\n(xw, f.subs(x, xw))")
predict("""f = 3 * exp(-x)
display(solve(f, x))
display(solve(diff(f, x), x))
limit(f, x, oo)""")

# ---------------------------------------------------------------- 2
sec('Sinusfunktionen untersuchen und modellieren')
expl('''#### Hoch-, Tief- und Wendepunkte im Intervall

Sinusfunktionen haben unendlich viele Extrem- und Wendepunkte. Man sucht sie deshalb in einem Intervall:
`solveset(diff(f, x), x, domain=Interval(0, 2*pi))`. Die Hochpunkte der Funktion f(x) = a · sin(b(x − c)) + d liegen bei y = d + |a|, die Tiefpunkte bei y = d − |a|.

`maximum(f, x, Interval(...))` und `minimum(...)` geben den größten und kleinsten Wert auf dem Intervall.''',
     """f = 2 * sin(x) + 1
display(solveset(diff(f, x), x, domain=Interval(0, 2*pi)))
display(maximum(f, x, Interval(0, 2*pi)), minimum(f, x, Interval(0, 2*pi)))
solveset(diff(f, x, 2), x, domain=Interval(0, 2*pi))""")
expl('''#### Sinusfunktion aus Eigenschaften bestimmen

Für ein **Modell** f(t) = a · sin(b(t − c)) + d liest man aus den Daten ab:
- d = (Maximum + Minimum) / 2 (Mittellinie), a = (Maximum − Minimum) / 2 (Amplitude)
- b = 2π / Periode
- c: Stelle, an der der Graph die Mittellinie **steigend** schneidet.

Beispiel: Die Temperatur schwankt im Lauf eines Tages (Periode 24 h) zwischen 8 °C und 20 °C. Das Minimum ist um 4 Uhr, das Maximum um 16 Uhr,
also wird die Mittellinie um 10 Uhr steigend erreicht.''',
     """t = symbols('t', real=True)
T = (20 - 8) / Integer(2) * sin(2*pi/24 * (t - 10)) + (20 + 8) / Integer(2)
display(T)
display(T.subs(t, 16), T.subs(t, 4))
plot(T, (t, 0, 24));""")

t('Gib die Extremstellen von f(x) = 3 · sin(2x) im Intervall [0, π] aus und die zugehörigen Funktionswerte.',
  body="f = 3 * sin(2*x)\nl = solveset(diff(f, x), x, domain=Interval(0, pi))\ndisplay(l)\n[f.subs(x, w) for w in l]")
t('Gib die Wendestellen von f(x) = cos(x) − 2 im Intervall [0, 2π] aus.', body="solveset(diff(cos(x) - 2, x, 2), x, domain=Interval(0, 2*pi))")
t('Gib den größten und den kleinsten Wert von f(x) = −2 · cos(πx/4) + 5 auf [0, 8] aus.',
  body="f = -2 * cos(pi * x / 4) + 5\ndisplay(maximum(f, x, Interval(0, 8)))\nminimum(f, x, Interval(0, 8))")
t('Gib die Extrempunkte von f(x) = sin(x) + x/2 im Intervall [0, 2π] als Liste von Tupeln aus.',
  body="f = sin(x) + x / 2\n[(w, f.subs(x, w)) for w in solveset(diff(f, x), x, domain=Interval(0, 2*pi))]")
t('''Wie groß ist die größte Steigung von f(x) = 2 · sin(3x)? Gib den größten Wert von f' auf [0, 2π] aus.''',
  body="maximum(diff(2 * sin(3*x), x), x, Interval(0, 2*pi))")
t('''**Riesenrad:** Eine Gondel hat nach t Minuten die Höhe h(t) = −20 · cos(πt/5) + 22 (in m). Gib die Periode, die größte und die kleinste Höhe
und die Zeitpunkte in [0, 10] aus, zu denen die Gondel 32 m hoch ist.''',
  given="t = symbols('t', real=True)",
  body="h = -20 * cos(pi * t / 5) + 22\ndisplay(periodicity(h, t))\ndisplay(maximum(h, t, Interval(0, 10)), minimum(h, t, Interval(0, 10)))\nsolveset(Eq(h, 32), t, domain=Interval(0, 10))")
t('''**Ebbe und Flut:** Der Wasserstand schwankt zwischen 1 m und 5 m, die Periode ist 12 Stunden, Hochwasser ist um 3 Uhr.
Stelle f(t) = a · sin(b(t − c)) + d auf (die Mittellinie wird 3 Stunden vor dem Hochwasser steigend erreicht) und gib f, f(3) und f(9) aus.''',
  given="t = symbols('t', real=True)",
  body="f = (5 - 1) / Integer(2) * sin(2*pi/12 * t) + (5 + 1) / Integer(2)\ndisplay(f)\ndisplay(f.subs(t, 3))\nf.subs(t, 9)")
t('''Prüfe, dass das Modell der vorigen Aufgabe stimmt: Gib die Stellen mit waagrechter Tangente in [0, 12] aus und die Werte dort.''',
  given="t = symbols('t', real=True)\nf = 2 * sin(pi * t / 6) + 3",
  body="l = solveset(diff(f, t), t, domain=Interval(0, 12))\ndisplay(l)\n[f.subs(t, w) for w in l]")
t('''**Tageslänge (Modell):** In einer Stadt ist der längste Tag 16 Stunden (Tag 172), der kürzeste 8,4 Stunden. Stelle das Modell L(t) mit Periode 365 auf
(Mittellinie steigend 365/4 Tage vor dem längsten Tag; Zahlen als `Rational`) und gib L(t) und L(1) mit 3 Ziffern aus.''',
  given="t = symbols('t', real=True)",
  body="amp = (16 - Rational(42, 5)) / 2\nmitte = (16 + Rational(42, 5)) / 2\nL = amp * sin(2*pi/365 * (t - (172 - Rational(365, 4)))) + mitte\ndisplay(L)\nN(L.subs(t, 1), 3)")

# ---------------------------------------------------------------- 3
sec('Extremwertprobleme')
expl('''#### Vorgehen

1. **Zielgröße** aufschreiben (was soll maximal oder minimal werden?), oft mit zwei Variablen.
2. Mit der **Nebenbedingung** eine Variable ersetzen, sodass die Zielfunktion nur noch von einer Variablen abhängt.
3. **Definitionsbereich** festlegen.
4. Extremstelle mit der Ableitung bestimmen und die **Ränder** des Definitionsbereichs prüfen.

Beispiel: Unter dem Graphen von f(x) = e⁻ˣ liegt ein Rechteck mit einer Ecke im Ursprung und der gegenüberliegenden Ecke P(u | f(u)) auf dem Graphen (u > 0).
Für welches u ist der Flächeninhalt maximal?''',
     """u = symbols('u', positive=True)
A = u * exp(-u)
ue = solve(diff(A, u), u)
display(ue)
display(diff(A, u, 2).subs(u, ue[0]) < 0)
display(A.subs(u, ue[0]))
display(limit(A, u, 0), limit(A, u, oo))""")

t('''Ein Rechteck hat eine Ecke im Ursprung, die gegenüberliegende Ecke P(u | f(u)) liegt auf dem Graphen von f(x) = 4 − x² (0 < u < 2).
Bestimme u so, dass der Flächeninhalt maximal ist, und gib den maximalen Flächeninhalt aus.''',
  given="u = symbols('u', positive=True)",
  body="A = u * (4 - u**2)\nue = solve(diff(A, u), u)[0]\ndisplay(ue)\nA.subs(u, ue)")
t('''Wie die vorige Aufgabe, aber mit f(x) = 3 · e^(−x/2) (u > 0). Gib u und den maximalen Flächeninhalt aus.''',
  given="u = symbols('u', positive=True)",
  body="A = u * 3 * exp(-u / 2)\nue = solve(diff(A, u), u)[0]\ndisplay(ue)\nA.subs(u, ue)")
t('''Ein Dreieck hat die Ecken O(0 | 0), Q(u | 0) und P(u | f(u)) mit f(x) = x · e⁻ˣ (u > 0). Für welches u ist der Flächeninhalt maximal?
Gib u, den Flächeninhalt genau und mit 4 Ziffern aus.''',
  given="u = symbols('u', positive=True)",
  body="A = u * u * exp(-u) / 2\nue = solve(diff(A, u), u)[0]\ndisplay(ue)\ndisplay(A.subs(u, ue))\nN(A.subs(u, ue), 4)")
t('''**Abstand:** Welcher Punkt auf dem Graphen von f(x) = √x hat vom Punkt (3 | 0) den kleinsten Abstand? Minimiere das Quadrat des Abstands
d(x)² = (x − 3)² + f(x)² und gib den Punkt und den kleinsten Abstand aus.''',
  body="d2 = (x - 3)**2 + sqrt(x)**2\nxe = solve(diff(d2, x), x)[0]\ndisplay((xe, sqrt(xe)))\nsqrt(d2.subs(x, xe))")
t('''Wo ist der senkrechte Abstand der Graphen von f(x) = eˣ und g(x) = x + 2 auf dem Intervall [−1, 1] am kleinsten bzw. größten?
Die Differenz ist d(x) = x + 2 − eˣ. Gib die Extremstelle von d und die Werte von d an der Extremstelle und an den Rändern −1 und 1 mit 4 Ziffern aus.''',
  body="dx = x + 2 - exp(x)\nxe = solve(diff(dx, x), x)[0]\ndisplay(xe)\n[N(dx.subs(x, w), 4) for w in [-1, xe, 1]]")
t('''**Zylinderdose:** Eine Dose (Zylinder) soll 1 Liter = 1000 cm³ fassen. Für welchen Radius r ist die Oberfläche O = 2πr² + 2πrh minimal?
Ersetze h mit der Nebenbedingung πr²h = 1000. Gib r und h mit 4 Ziffern aus.''',
  given="r, h = symbols('r h', positive=True)",
  body="h_r = solve(Eq(pi * r**2 * h, 1000), h)[0]\nO = 2*pi*r**2 + 2*pi*r*h_r\nre = solve(diff(O, r), r)[0]\ndisplay(N(re, 4))\nN(h_r.subs(r, re), 4)")
t('''**Rinne:** Aus einem 30 cm breiten Blech wird eine Rinne gebogen: Boden 10 cm, die beiden 10 cm breiten Seiten stehen im Winkel φ schräg nach außen.
Der Querschnitt ist A(φ) = 100 · sin(φ) + 100 · sin(φ) · cos(φ). Bestimme φ in (0, π/2) mit größtem Querschnitt (in Grad) und den Querschnitt mit 4 Ziffern.''',
  given="phi = symbols('phi', real=True)",
  body="A = 100 * sin(phi) + 100 * sin(phi) * cos(phi)\nl = solveset(diff(A, phi), phi, domain=Interval.open(0, pi/2))\ndisplay([deg(w) for w in l])\n[N(A.subs(phi, w), 4) for w in l]")

# ---------------------------------------------------------------- 4
sec('Funktionen aus Eigenschaften bestimmen')
expl('''#### Steckbriefaufgaben

Gesucht ist eine Funktion mit vorgegebenen Eigenschaften. Man setzt die Funktion mit unbekannten Koeffizienten an, übersetzt jede
Eigenschaft in eine Gleichung und löst das **lineare Gleichungssystem** mit `linsolve()` oder `solve()`.

| Eigenschaft | Gleichung |
|---|---|
| Punkt P(2 \\| 3) liegt auf dem Graphen | f(2) = 3 |
| Extremstelle bei x = 1 | f'(1) = 0 |
| Wendestelle bei x = 0 | f''(0) = 0 |
| Steigung 4 an der Stelle 1 | f'(1) = 4 |
| Graph symmetrisch zur y-Achse | nur gerade Potenzen ansetzen |

Beispiel: Eine ganzrationale Funktion 3. Grades hat bei x = 0 einen Wendepunkt, geht durch (0 | 1) und hat in T(2 | −3) einen Tiefpunkt.
`solve` liefert ein Dictionary; mit `f.subs(loesung)` setzt man alle Koeffizienten auf einmal ein.''',
     """f = a*x**3 + b*x**2 + c*x + d
gl = [Eq(f.subs(x, 0), 1), Eq(f.subs(x, 2), -3),
      Eq(diff(f, x).subs(x, 2), 0), Eq(diff(f, x, 2).subs(x, 0), 0)]
loesung = solve(gl, [a, b, c, d])
display(loesung)
f.subs(loesung)""")

t('''Eine Parabel f(x) = ax² + bx + c geht durch die Punkte (0 | 1), (1 | 4) und (−1 | 0). Bestimme f.''',
  body="f = a*x**2 + b*x + c\nf.subs(solve([Eq(f.subs(x, 0), 1), Eq(f.subs(x, 1), 4), Eq(f.subs(x, -1), 0)], [a, b, c]))")
t('''Eine Parabel hat den Scheitel S(2 | −1) und geht durch (0 | 3). Bestimme f(x) = ax² + bx + c (Scheitel: f(2) = −1 und f'(2) = 0).''',
  body="f = a*x**2 + b*x + c\nf.subs(solve([Eq(f.subs(x, 2), -1), Eq(diff(f, x).subs(x, 2), 0), Eq(f.subs(x, 0), 3)], [a, b, c]))")
t('''Eine ganzrationale Funktion 3. Grades hat in H(−1 | 4) einen Hochpunkt und in T(1 | 0) einen Tiefpunkt. Bestimme sie.''',
  body="f = a*x**3 + b*x**2 + c*x + d\ngl = [Eq(f.subs(x, -1), 4), Eq(diff(f, x).subs(x, -1), 0), Eq(f.subs(x, 1), 0), Eq(diff(f, x).subs(x, 1), 0)]\nf.subs(solve(gl, [a, b, c, d]))")
t('''Ein zur y-Achse symmetrischer Graph 4. Grades (f(x) = ax⁴ + bx² + c) hat den Tiefpunkt T(0 | 0) und den Hochpunkt H(2 | 4). Bestimme f.''',
  body="f = a*x**4 + b*x**2 + c\ngl = [Eq(f.subs(x, 0), 0), Eq(f.subs(x, 2), 4), Eq(diff(f, x).subs(x, 2), 0)]\nf.subs(solve(gl, [a, b, c]))")
t('''Eine ganzrationale Funktion 3. Grades geht durch den Ursprung, hat dort die Steigung 2 und in W(1 | 3) einen Wendepunkt. Bestimme sie.''',
  body="f = a*x**3 + b*x**2 + c*x + d\ngl = [Eq(f.subs(x, 0), 0), Eq(diff(f, x).subs(x, 0), 2), Eq(f.subs(x, 1), 3), Eq(diff(f, x, 2).subs(x, 1), 0)]\nf.subs(solve(gl, [a, b, c, d]))")
t("""Prüfe das Ergebnis der vorigen Aufgabe: Gib für f(x) = −x³/2 + 3x²/2 + 2x die Werte f(0), f'(0), f(1), f''(1) und f'''(1) als Liste aus.""",
  given="f = -x**3 / 2 + 3*x**2 / 2 + 2*x",
  body="[f.subs(x, 0), diff(f, x).subs(x, 0), f.subs(x, 1), diff(f, x, 2).subs(x, 1), diff(f, x, 3).subs(x, 1)]")
t('''Gibt es eine Parabel durch (0 | 0), (1 | 1), (2 | 2) und (3 | 5)? Gib das Ergebnis von `linsolve` für die vier Gleichungen aus
(leere Menge = keine Lösung).''',
  body="f = a*x**2 + b*x + c\nlinsolve([Eq(f.subs(x, 0), 0), Eq(f.subs(x, 1), 1), Eq(f.subs(x, 2), 2), Eq(f.subs(x, 3), 5)], [a, b, c])")
t('''**Straßenbau:** Eine Straße verläuft für x ≤ 0 auf der x-Achse und für x ≥ 4 auf der Geraden y = 2 (Einheit 100 m). Dazwischen soll ein
Übergangsbogen f (3. Grades) ohne Knick anschließen: f(0) = 0, f'(0) = 0, f(4) = 2, f'(4) = 0. Bestimme f und gib die größte Steigung des Bogens aus.''',
  body="f = a*x**3 + b*x**2 + c*x + d\ngl = [Eq(f.subs(x, 0), 0), Eq(diff(f, x).subs(x, 0), 0), Eq(f.subs(x, 4), 2), Eq(diff(f, x).subs(x, 4), 0)]\nf = f.subs(solve(gl, [a, b, c, d]))\ndisplay(f)\nmaximum(diff(f, x), x, Interval(0, 4))")
t('''Eine Funktion f(x) = a · e^(bx) geht durch die Punkte (0 | 3) und (2 | 12). Bestimme a und b (die Gleichungen sind nicht linear, nimm `solve`).''',
  given="a, b = symbols('a b', positive=True)",
  body="f = a * exp(b*x)\nl = solve([Eq(f.subs(x, 0), 3), Eq(f.subs(x, 2), 12)], [a, b], dict=True)\ndisplay(l)\nf.subs(l[0])")

# ---------------------------------------------------------------- 5
sec('Funktionenscharen')
expl('''#### Funktionen mit einem Parameter

Eine **Funktionenschar** enthält einen Parameter, z. B. fₐ(x) = x · e^(−a·x). Für jeden Wert von a ergibt sich eine Funktion.
Man untersucht die Schar allgemein: Die Ergebnisse (Nullstellen, Extrempunkte, ...) hängen von a ab.

Oft muss man wissen, ob der Parameter positiv ist. Dann legt man ihn mit `positive=True` an. Mit einer Liste von Funktionen
zeichnet `plot` mehrere Graphen der Schar in ein Diagramm.''',
     """a = symbols('a', positive=True)
f = x * exp(-a*x)
xe = solve(diff(f, x), x)
display(xe)
display(f.subs(x, xe[0]))
plot(*[f.subs(a, w) for w in [Rational(1, 2), 1, 2]], (x, 0, 6), legend=True);""")

t('''Gegeben ist fₐ(x) = x² − 2ax (a reell). Gib die Nullstellen und den Scheitelpunkt (als Tupel) in Abhängigkeit von a aus.''',
  body="f = x**2 - 2*a*x\ndisplay(solve(f, x))\nxe = solve(diff(f, x), x)[0]\n(xe, f.subs(x, xe))")
t('''Gegeben ist fₐ(x) = (x − a) · eˣ. Gib die Nullstelle und den Extrempunkt (als Tupel) in Abhängigkeit von a aus.''',
  body="f = (x - a) * exp(x)\ndisplay(solve(f, x))\nxe = solve(diff(f, x), x)[0]\n(xe, f.subs(x, xe))")
t('''Gegeben ist fₖ(x) = x³ − kx (k > 0). Gib die Extremstellen in Abhängigkeit von k aus. Für welches k liegt eine Extremstelle bei x = 2?''',
  given="k = symbols('k', positive=True)",
  body="f = x**3 - k*x\ndisplay(solve(diff(f, x), x))\nsolve(Eq(diff(f, x).subs(x, 2), 0), k)")
t('''Zeichne die Graphen von fₐ(x) = a · x · e⁻ˣ für a = 1, 2, 3 in ein Diagramm für 0 ≤ x ≤ 5 (mit Legende).''',
  body="f = a * x * exp(-x)\nplot(*[f.subs(a, w) for w in [1, 2, 3]], (x, 0, 5), legend=True);")
t('''Gegeben ist fₐ(x) = a · x² + 1 − a. Alle Graphen der Schar gehen durch zwei gemeinsame Punkte. Bestimme sie: Setze f für a = 1 und a = 2 gleich
und löse nach x; gib die Punkte als Liste von Tupeln aus.''',
  body="f = a*x**2 + 1 - a\nxs = solve(Eq(f.subs(a, 1), f.subs(a, 2)), x)\n[(w, f.subs(x, w)) for w in xs]")
t('''Prüfe für die Schar der vorigen Aufgabe, dass die Punkte für **jedes** a auf dem Graphen liegen: Gib fₐ(−1) und fₐ(1) aus.''',
  given="f = a*x**2 + 1 - a", body="display(f.subs(x, -1))\nf.subs(x, 1)")
t('''Für welchen Wert von a hat fₐ(x) = x² + a·x + 4 genau eine Nullstelle? (Die Diskriminante ist dann 0; oder: der Tiefpunkt liegt auf der x-Achse.)
Gib die Werte von a aus.''',
  body="f = x**2 + a*x + 4\nxe = solve(diff(f, x), x)[0]\nsolve(f.subs(x, xe), a)")
t('''Gegeben ist fₜ(x) = −x² + t (t > 0). Die Nullstellen und der Scheitel bilden ein Dreieck. Für welches t hat es den Flächeninhalt 8?''',
  given="t = symbols('t', positive=True)",
  body="f = -x**2 + t\nns = solve(f, x)\nA = (ns[1] - ns[0]) * t / 2\nsolve(Eq(A, 8), t)")
expl('''#### Ortskurven (Zusatz)

Die Extrempunkte einer Schar liegen auf einer Kurve, der **Ortskurve**. Man bestimmt sie so: Extrempunkt E(x(a) | y(a)) bestimmen,
x = x(a) nach a auflösen und in y(a) einsetzen. Das Ergebnis hängt nur noch von x ab.''',
     """a = symbols('a', positive=True)
f = x**2 - 2*a*x
xe = solve(diff(f, x), x)[0]
ye = f.subs(x, xe)
display((xe, ye))
a_von_x = solve(Eq(x, xe), a)[0]
ye.subs(a, a_von_x)""")
t('''Bestimme die Ortskurve der Tiefpunkte von fₐ(x) = x² − 4ax + a (a > 0).''',
  given="a = symbols('a', positive=True)",
  body="f = x**2 - 4*a*x + a\nxe = solve(diff(f, x), x)[0]\nye = f.subs(x, xe)\nexpand(ye.subs(a, solve(Eq(x, xe), a)[0]))")
t('''Bestimme die Ortskurve der Hochpunkte von fₐ(x) = x · e^(−a·x) (a > 0).''',
  given="a = symbols('a', positive=True)",
  body="f = x * exp(-a*x)\nxe = solve(diff(f, x), x)[0]\nye = f.subs(x, xe)\nye.subs(a, solve(Eq(x, xe), a)[0])")

# ---------------------------------------------------------------- 6
sec('Umkehrfunktionen (Leistungsfach)')
expl('''#### f⁻¹ bestimmen

Eine Funktion ist **umkehrbar**, wenn jeder y-Wert nur einmal vorkommt (z. B. wenn f streng monoton ist). Die **Umkehrfunktion** f⁻¹ macht f rückgängig.
Man löst y = f(x) nach x auf und vertauscht dann x und y. Der Graph von f⁻¹ ist der an der Geraden y = x gespiegelte Graph von f.

Für die **Ableitung der Umkehrfunktion** gilt: (f⁻¹)'(y₀) = 1 / f'(x₀), wenn y₀ = f(x₀).''',
     """f = exp(x) + 1
umk = solve(Eq(y, f), x)
display(umk)
g = umk[0].subs(y, x)
display(g)
display(simplify(f.subs(x, g)))
plot(f, g, x, (x, -3, 4), xlim=(-3, 4), ylim=(-3, 4), aspect_ratio=(1, 1), legend=True);""")

t('Bestimme die Umkehrfunktion von f(x) = 2x − 6 (in x geschrieben).', body="solve(Eq(y, 2*x - 6), x)[0].subs(y, x)")
t('Bestimme die Umkehrfunktion von f(x) = e^(2x) (in x geschrieben).', body="solve(Eq(y, exp(2*x)), x)[0].subs(y, x)")
t('Bestimme die Umkehrfunktion von f(x) = ln(x − 1) + 3 (x > 1, in x geschrieben).', body="solve(Eq(y, log(x - 1) + 3), x)[0].subs(y, x)")
t('''f(x) = x² ist nur für x ≥ 0 umkehrbar. Lege dafür `xp = symbols('xp', positive=True)` an (für x > 0), löse y = xp² nach xp und gib die Umkehrfunktion in x aus.''',
  given="xp = symbols('xp', positive=True)", body="solve(Eq(y, xp**2), xp)[0].subs(y, x)")
t('''Prüfe, dass g(x) = (x − 3)/2 die Umkehrfunktion von f(x) = 2x + 3 ist: Gib `f(g(x))` und `g(f(x))` vereinfacht aus.''',
  body="f = 2*x + 3\ng = (x - 3) / 2\ndisplay(simplify(f.subs(x, g)))\nsimplify(g.subs(x, f))")
t('''Berechne die Steigung der Umkehrfunktion von f(x) = x³ + x an der Stelle y₀ = 2 (es ist f(1) = 2) mit (f⁻¹)'(2) = 1/f'(1).''',
  body="f = x**3 + x\n1 / diff(f, x).subs(x, 1)")
t('''Leite die Ableitung von ln(x) her: ln ist die Umkehrfunktion von eˣ. Berechne 1 / f'(ln(x)) für f(x) = eˣ und vereinfache.''',
  body="1 / diff(exp(x), x).subs(x, log(x))")
t('''Zeichne f(x) = eˣ, ihre Umkehrfunktion ln(x) und die Gerade y = x für −3 ≤ x ≤ 4 (wie im Beispiel mit `aspect_ratio=(1, 1)` und gleichen Achsenbereichen).''',
  body="plot(exp(x), log(x), x, (x, -3, 4), xlim=(-3, 4), ylim=(-3, 4), aspect_ratio=(1, 1), legend=True);")

# ---------------------------------------------------------------- 7
sec('Gemischte Übungen')
t('''**Medikament:** Die Wirkstoffmenge im Blut ist m(t) = 50 · (e^(−0,2t) − e^(−t)) (mg, t in Stunden; Zahlen als `Rational`). Wann ist die Menge am größten
(genau und mit 4 Ziffern)? Wie groß ist sie dann (4 Ziffern)? Wann nimmt sie am stärksten ab (Wendestelle, 4 Ziffern)?''',
  given="t = symbols('t', positive=True)",
  body="m = 50 * (exp(-Rational(1, 5) * t) - exp(-t))\nte = solve(diff(m, t), t)[0]\ndisplay(te, N(te, 4))\ndisplay(N(m.subs(t, te), 4))\nN(solve(diff(m, t, 2), t)[0], 4)")
t('''Bestimme a > 0 so, dass der Hochpunkt von fₐ(x) = a · x · e⁻ˣ auf der Geraden y = 2 liegt.''',
  given="a = symbols('a', positive=True)",
  body="f = a * x * exp(-x)\nxe = solve(diff(f, x), x)[0]\nsolve(Eq(f.subs(x, xe), 2), a)")
t('''Eine ganzrationale Funktion 3. Grades hat bei x = 0 eine doppelte Nullstelle und in (3 | 0) eine weitere Nullstelle; ihr Graph geht durch (1 | 4).
Setze f(x) = a · x² · (x − 3) an und bestimme a.''',
  body="f = a * x**2 * (x - 3)\nexpand(f.subs(a, solve(Eq(f.subs(x, 1), 4), a)[0]))")
t('''Gib für f(x) = sin(x) · e^(−x/5) die ersten drei Hochstellen x > 0 mit 4 Ziffern aus (`solveset` im Intervall [0, 20], dann nur die mit f'' < 0).''',
  body="f = sin(x) * exp(-x / 5)\nl = solveset(diff(f, x), x, domain=Interval(0, 20))\n[N(w, 4) for w in l if diff(f, x, 2).subs(x, w) < 0][:3]")
t('''Zeichne die Funktion der vorigen Aufgabe zusammen mit den Hüllkurven e^(−x/5) und −e^(−x/5) für 0 ≤ x ≤ 20.''',
  body="plot(sin(x) * exp(-x / 5), exp(-x / 5), -exp(-x / 5), (x, 0, 20));")

generate('sympy_funktionsanalyse', 'Funktionsanalyse: Kurvendiskussion, Extremwertprobleme, Steckbriefe, Scharen', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
