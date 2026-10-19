# Erzeugt ../content/sympy_dmw_flaechen.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_dmw_flaechen.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_dmw_flaechen.py
#
# Wahlfach Digitale Mathematische Werkzeuge (BW 2016, Klassen 11/12), 3.1.3 3D-Flächen:
# Funktionen zweier Variablen definieren und darstellen (plot3d, Höhenlinien), ebene Schnitte parallel zur x-z- und y-z-Ebene
# (Beispiele f = 0,1·(x² − y²) und f = x·y), partielle Ableitungen und ihre Deutung, Gradient als Richtung des stärksten Anstiegs
# (durch Ausprobieren verschiedener Richtungen entdecken), lokale Extrema über die waagrechte Tangentialebene (Gradient = 0),
# Einordnung mit der Hesse-Matrix als Zusatz.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = ("from sympy import *\nfrom sympy.plotting import plot3d, plot_contour\ninit_printing()\nimport matplotlib.pyplot as plt\n"
         "x, y, z, s, phi = symbols('x y z s phi', real=True)")

INTRO = '''Dieses Notebook gehört zum Wahlfach **Digitale Mathematische Werkzeuge**. Bisher hatten Funktionen eine Eingabe x und eine Ausgabe f(x);
ihr Graph ist eine Kurve. Jetzt hängt der Funktionswert von **zwei** Variablen ab: z = f(x, y). Der Graph ist eine **Fläche** im Raum,
z. B. ein Gelände, bei dem jeder Punkt (x | y) auf der Karte eine Höhe z hat.

Vieles kennst du schon in neuer Form: Statt einer Ableitung gibt es **zwei partielle Ableitungen**, statt der Tangente eine **Tangentialebene**,
und Hoch- und Tiefpunkte findest du dort, wo die Tangentialebene waagrecht ist.

Vorausgesetzt werden die Notebooks *Ableitungen* (Klasse 10) und *Ebenen*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy mit den Zeichenbefehlen `plot3d` (Fläche) und
`plot_contour` (Höhenlinien) und matplotlib, schaltet die Formel-Ausgabe ein und legt die reellen Variablen `x`, `y`, `z`, `s` und `phi` an.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Funktionen zweier Variablen')
expl('''#### z = f(x, y)

Eine Funktion zweier Variablen ordnet jedem Punkt (x | y) eine Zahl z zu. In sympy ist das einfach ein Term mit x und y; Werte berechnet man mit
`f.subs({x: 1, y: 2})`.

- `plot3d(f, (x, a, b), (y, c, d))` zeichnet die **Fläche**.
- `plot_contour(f, (x, a, b), (y, c, d))` zeichnet **Höhenlinien** wie auf einer Wanderkarte: Linien, auf denen f denselben Wert hat.''',
     """f = Rational(1, 10) * (x**2 - y**2)
display(f.subs({x: 2, y: 1}))
plot3d(f, (x, -3, 3), (y, -3, 3));
plot_contour(f, (x, -3, 3), (y, -3, 3));""")

t('Berechne für f(x, y) = x² + 2y² die Werte f(1, 1), f(−2, 3) und f(0, 0) als Liste.', body="f = x**2 + 2*y**2\n[f.subs({x: a, y: b}) for a, b in [(1, 1), (-2, 3), (0, 0)]]")
t('Zeichne die Fläche f(x, y) = x² + y² (ein **Paraboloid**) für −2 ≤ x, y ≤ 2.', body="plot3d(x**2 + y**2, (x, -2, 2), (y, -2, 2));")
t('Zeichne die Fläche f(x, y) = x · y (**Sattelfläche**) für −2 ≤ x, y ≤ 2.', body="plot3d(x * y, (x, -2, 2), (y, -2, 2));")
t('Zeichne die Höhenlinien von f(x, y) = x² + y² für −2 ≤ x, y ≤ 2.', body="plot_contour(x**2 + y**2, (x, -2, 2), (y, -2, 2));")
t('''Zeichne den „Hügel“ f(x, y) = 4 · e^(−(x² + y²)/4) für −4 ≤ x, y ≤ 4 als Fläche.''', body="plot3d(4 * exp(-(x**2 + y**2) / 4), (x, -4, 4), (y, -4, 4));")
t('''Die Höhenlinie f(x, y) = c ist die Lösungsmenge einer Gleichung. Löse x² + 2y² = 8 nach y auf (die Höhenlinie zur Höhe 8 von f = x² + 2y²).''',
  body="solve(Eq(x**2 + 2*y**2, 8), y)")
t('''Der Definitionsbereich von f(x, y) = √(9 − x² − y²) ist eine Kreisscheibe. Gib f(0, 0), f(2, 2) und f(3, 0) aus und zeichne die Fläche für −2 ≤ x, y ≤ 2 (eine Halbkugel).''',
  body="f = sqrt(9 - x**2 - y**2)\ndisplay([f.subs({x: a, y: b}) for a, b in [(0, 0), (2, 2), (3, 0)]])\nplot3d(f, (x, -2, 2), (y, -2, 2));")

# ---------------------------------------------------------------- 2
sec('Ebene Schnitte')
expl('''#### Schnittkurven parallel zu den Koordinatenebenen

Hält man y fest (y = c), erhält man die Funktion x ↦ f(x, c): Das ist die **Schnittkurve** der Fläche mit der Ebene y = c (parallel zur x-z-Ebene).
Entsprechend liefert x = c eine Schnittkurve parallel zur y-z-Ebene. Schnittkurven sind gewöhnliche Funktionen einer Variablen; man kann sie zeichnen
und mit den bekannten Methoden untersuchen.

Bei der **Sattelfläche** f = 0,1·(x² − y²) sind die Schnitte y = c nach oben offene Parabeln, die Schnitte x = c nach unten offene.''',
     """f = Rational(1, 10) * (x**2 - y**2)
display([f.subs(y, c) for c in [-2, 0, 2]])
plot(*[f.subs(y, c) for c in [-2, 0, 2]], (x, -3, 3), legend=True);
plot(*[f.subs(x, c) for c in [-2, 0, 2]], (y, -3, 3), legend=True);""")

t('Gib für f(x, y) = x · y die Schnittkurven für y = −1, 0, 1, 2 als Liste aus (es sind Geraden durch den Ursprung).',
  body="f = x * y\n[f.subs(y, c) for c in [-1, 0, 1, 2]]")
t('Zeichne die Schnittkurven von f(x, y) = x · y für y = −1, 0, 1, 2 in ein Diagramm (−3 ≤ x ≤ 3, mit Legende).',
  body="plot(*[(x * y).subs(y, c) for c in [-1, 0, 1, 2]], (x, -3, 3), legend=True);")
t('Gib für f(x, y) = x² + y² die Schnitte x = 0 und x = 1 aus und den Tiefpunkt der Schnittkurve x = 1.',
  body="f = x**2 + y**2\ndisplay(f.subs(x, 0), f.subs(x, 1))\nsolve(diff(f.subs(x, 1), y), y)")
t('''Für welches c ist die Schnittkurve y = c von f(x, y) = x² − 4x + c·y eine Parabel mit dem Scheitel (2 | 0)? Gib den Scheitel der Schnittkurve in Abhängigkeit von c aus
und löse.''',
  given="c = symbols('c', real=True)",
  body="g = (x**2 - 4*x + c*y).subs(y, c)\nxs = solve(diff(g, x), x)[0]\ndisplay((xs, g.subs(x, xs)))\nsolve(Eq(g.subs(x, xs), 0), c)")
t('''Untersuche den Hügel f(x, y) = 4 · e^(−(x² + y²)/4): Gib die Schnittkurve y = 0 aus, ihre Wendestellen und zeichne die Schnitte y = 0, 1, 2.''',
  body="f = 4 * exp(-(x**2 + y**2) / 4)\ng = f.subs(y, 0)\ndisplay(g)\ndisplay(solve(diff(g, x, 2), x))\nplot(*[f.subs(y, c) for c in [0, 1, 2]], (x, -5, 5), legend=True);")
t('''Ein **diagonaler** Schnitt: Setze y = x in f(x, y) = 0,1·(x² − y²) ein. Was kommt heraus? Gib auch den Schnitt y = −x und y = 2x aus.''',
  body="f = Rational(1, 10) * (x**2 - y**2)\n[f.subs(y, w) for w in [x, -x, 2*x]]")

# ---------------------------------------------------------------- 3
sec('Partielle Ableitungen')
expl('''#### ∂f/∂x und ∂f/∂y

Die **partielle Ableitung nach x** erhält man, indem man y wie eine Konstante behandelt und nach x ableitet: fₓ = ∂f/∂x = `diff(f, x)`.
Sie ist die Steigung der Schnittkurve in x-Richtung. Entsprechend ist f_y = ∂f/∂y = `diff(f, y)` die Steigung in y-Richtung.

Auch höhere partielle Ableitungen gibt es: fₓₓ = `diff(f, x, 2)`, fₓᵧ = `diff(f, x, y)` usw.''',
     """f = x**2 * y + 3*y**2
display(diff(f, x), diff(f, y))
display(diff(f, x).subs({x: 1, y: 2}), diff(f, y).subs({x: 1, y: 2}))
schnitt = f.subs(y, 2)
display(diff(schnitt, x).subs(x, 1))
display(diff(f, x, 2), diff(f, x, y), diff(f, y, x))""")

t('Berechne die partiellen Ableitungen von f(x, y) = 3x²y − 2xy³ + 5.', body="f = 3*x**2*y - 2*x*y**3 + 5\ndisplay(diff(f, x))\ndiff(f, y)")
t('Berechne die partiellen Ableitungen von f(x, y) = e^(x·y).', body="f = exp(x*y)\ndisplay(diff(f, x))\ndiff(f, y)")
t('Berechne die partiellen Ableitungen von f(x, y) = sin(x) · cos(y) an der Stelle (π/2 | π/4).',
  body="f = sin(x) * cos(y)\n(diff(f, x).subs({x: pi/2, y: pi/4}), diff(f, y).subs({x: pi/2, y: pi/4}))")
t('''Prüfe die Deutung: Für f(x, y) = x · y ist fₓ(2, 3) die Steigung der Schnittkurve y = 3 an der Stelle x = 2. Berechne beides.''',
  body="f = x * y\ndisplay(diff(f, x).subs({x: 2, y: 3}))\ndiff(f.subs(y, 3), x).subs(x, 2)")
t('''Berechne alle zweiten partiellen Ableitungen fₓₓ, fₓᵧ, fᵧₓ, fᵧᵧ von f(x, y) = x³y² + sin(xy) als Liste und prüfe, ob fₓᵧ = fᵧₓ (Satz von Schwarz).''',
  body="f = x**3*y**2 + sin(x*y)\nl = [diff(f, x, 2), diff(f, x, y), diff(f, y, x), diff(f, y, 2)]\ndisplay(l)\nsimplify(l[1] - l[2]) == 0")
t('''Ein Gelände hat die Höhe h(x, y) = 100 − x² − 2y² (in m, x und y in 10 m). Wie steil ist es im Punkt (3 | 2) in x-Richtung und in y-Richtung?''',
  body="h = 100 - x**2 - 2*y**2\n(diff(h, x).subs({x: 3, y: 2}), diff(h, y).subs({x: 3, y: 2}))")
predict("""f = 5*x + 2*y
display(diff(f, x))
display(diff(f, y))
diff(x**2 * y**2, x, y)""")

# ---------------------------------------------------------------- 4
sec('Der Gradient')
expl('''#### Richtung des stärksten Anstiegs

Der **Gradient** fasst die partiellen Ableitungen zu einem Vektor zusammen: grad f = (fₓ | f_y). In sympy: `Matrix([diff(f, x), diff(f, y)])`.

Geht man vom Punkt (x₀ | y₀) in eine Richtung u = (cos φ | sin φ) (Einheitsvektor), dann ist die Steigung in dieser Richtung
(**Richtungsableitung**) gleich grad f · u. Probiert man viele Richtungen aus, sieht man: Am größten ist die Steigung in Richtung
des Gradienten, und sie ist dann gleich seiner Länge |grad f|. Senkrecht zum Gradienten ist die Steigung 0 (Richtung der Höhenlinie).

`atan2(gy, gx)` gibt den Winkel des Vektors (gx | gy) gegen die x-Achse (im Bogenmaß, richtig für alle vier Quadranten).
Zum Zeichnen mit matplotlib macht `lambdify((x, y), term)` aus einem sympy-Term eine Python-Funktion mit zwei Eingaben.''',
     """f = x**2 + 3*y**2
g = Matrix([diff(f, x), diff(f, y)]).subs({x: 1, y: 1})
display(g, g.norm())
steigungen = [(w, N(g.dot(Matrix([cos(w * pi / 180), sin(w * pi / 180)])), 4)) for w in range(0, 360, 30)]
display(steigungen)
N(deg(atan2(g[1], g[0])), 4)""")

t('Berechne den Gradienten von f(x, y) = x²y + y³ allgemein und im Punkt (1 | 2).',
  body="f = x**2*y + y**3\ngr = Matrix([diff(f, x), diff(f, y)])\ndisplay(gr)\ngr.subs({x: 1, y: 2})")
t('''Berechne für f(x, y) = x² + 3y² im Punkt (1 | 1) die Steigung in die Richtungen 0°, 45°, 90° und 180° (Einheitsvektoren (cos φ | sin φ)).''',
  body="g = Matrix([2, 6])\n[simplify(g.dot(Matrix([cos(w), sin(w)]))) for w in [0, pi/4, pi/2, pi]]")
t('''Bestimme für f(x, y) = x² + 3y² im Punkt (1 | 1) die Richtung φ mit der größten Steigung **mit Analysis**: Die Steigung ist s(φ) = 2 cos φ + 6 sin φ.
Gib die Stellen mit s'(φ) = 0 in [0, 2π) aus, die größte Steigung und die Länge des Gradienten.''',
  body="st = 2*cos(phi) + 6*sin(phi)\nl = solveset(diff(st, phi), phi, Interval.Ropen(0, 2*pi))\ndisplay(l)\ndisplay(maximum(st, phi, Interval(0, 2*pi)))\nMatrix([2, 6]).norm()")
t('''In welche Richtung (Winkel in Grad, 4 Ziffern) muss man im Gelände h(x, y) = 100 − x² − 2y² vom Punkt (3 | 2) aus gehen, um am steilsten aufzusteigen? Wie groß ist die Steigung dort?''',
  body="h = 100 - x**2 - 2*y**2\ng = Matrix([diff(h, x), diff(h, y)]).subs({x: 3, y: 2})\ndisplay(g)\ndisplay(N(deg(atan2(g[1], g[0])), 4))\ng.norm()")
t('''Prüfe, dass der Gradient senkrecht auf der Höhenlinie steht: Für f(x, y) = x² + y² ist die Höhenlinie durch (3 | 4) der Kreis mit Radius 5, ihr Tangentenvektor dort (−4 | 3).
Berechne das Skalarprodukt mit dem Gradienten.''',
  body="f = x**2 + y**2\ng = Matrix([diff(f, x), diff(f, y)]).subs({x: 3, y: 4})\ng.dot(Matrix([-4, 3]))")
t('''Zeichne für f(x, y) = x² + 3y² an den Gitterpunkten (a | b) mit a, b ∈ {−2, −1, 0, 1, 2} die Gradienten als Pfeile mit `plt.quiver(xs, ys, us, vs)`
(Startpunkte xs, ys und Pfeilrichtungen us, vs als Listen; mit `angles='xy', scale_units='xy', scale=10` werden alle Pfeile maßstabsgerecht auf ein Zehntel
verkürzt). Zeichne dazu die Höhenlinie x² + 3y² = 3 als Ellipse (√3·cos w | sin w) mit `plt.plot`.
Die Pfeile stehen senkrecht auf der Höhenlinie.''',
  body="f = x**2 + 3*y**2\nfx, fy = lambdify((x, y), diff(f, x)), lambdify((x, y), diff(f, y))\npunkte = [(a, b) for a in range(-2, 3) for b in range(-2, 3)]\nplt.quiver([a for a, b in punkte], [b for a, b in punkte], [fx(a, b) for a, b in punkte], [fy(a, b) for a, b in punkte], angles='xy', scale_units='xy', scale=10)\nws = [float(2 * pi * i / 100) for i in range(101)]\nplt.plot([float(sqrt(3) * cos(w)) for w in ws], [float(sin(w)) for w in ws])\nplt.gca().set_aspect('equal')\nplt.show()")

# ---------------------------------------------------------------- 5
sec('Tangentialebene und lokale Extrema')
expl('''#### Waagrechte Tangentialebene

Die **Tangentialebene** an die Fläche im Punkt (x₀ | y₀ | f(x₀, y₀)) ist

z = f(x₀, y₀) + fₓ(x₀, y₀)·(x − x₀) + f_y(x₀, y₀)·(y − y₀)

An einem Hoch- oder Tiefpunkt ist sie **waagrecht**, also fₓ = 0 **und** f_y = 0 (Gradient = Nullvektor). Solche Punkte heißen **kritische Punkte**.
Nicht jeder kritische Punkt ist ein Extremum: Bei der Sattelfläche ist (0 | 0) ein **Sattelpunkt**, in x-Richtung ein Tiefpunkt, in y-Richtung ein Hochpunkt.

Einordnen kann man einen kritischen Punkt, indem man die Funktionswerte in der Umgebung betrachtet oder die Schnittkurven untersucht.''',
     """f = x**3 - 3*x + y**2
kritisch = solve([diff(f, x), diff(f, y)], [x, y])
display(kritisch)
for px, py in kritisch:
    umgebung = [f.subs({x: px + a, y: py + b}) - f.subs({x: px, y: py}) for a, b in [(Rational(1, 10), 0), (-Rational(1, 10), 0), (0, Rational(1, 10)), (0, -Rational(1, 10))]]
    print((px, py), umgebung)
x0, y0 = 1, 1
expand(f.subs({x: x0, y: y0}) + diff(f, x).subs({x: x0, y: y0}) * (x - x0) + diff(f, y).subs({x: x0, y: y0}) * (y - y0))""")
expl('''#### Zusatz: Die Hesse-Matrix

Wie bei f'' im Eindimensionalen entscheiden die zweiten Ableitungen. Die **Hesse-Matrix** H = [[fₓₓ, fₓᵧ], [fᵧₓ, fᵧᵧ]] (`hessian(f, (x, y))`) an einem kritischen Punkt:
- det H > 0 und fₓₓ > 0: Tiefpunkt; det H > 0 und fₓₓ < 0: Hochpunkt
- det H < 0: Sattelpunkt; det H = 0: keine Entscheidung''',
     """f = x**3 - 3*x + y**2
H = hessian(f, (x, y))
display(H)
[(p, H.subs({x: p[0], y: p[1]}).det(), H.subs({x: p[0], y: p[1]})[0, 0]) for p in solve([diff(f, x), diff(f, y)], [x, y])]""")

t('Gib die Tangentialebene an f(x, y) = x² + y² im Punkt (1 | 2) aus (ausmultipliziert).',
  body="f = x**2 + y**2\nexpand(f.subs({x: 1, y: 2}) + diff(f, x).subs({x: 1, y: 2}) * (x - 1) + diff(f, y).subs({x: 1, y: 2}) * (y - 2))")
t('Bestimme die kritischen Punkte von f(x, y) = x² + y² − 4x + 6y.', body="f = x**2 + y**2 - 4*x + 6*y\nsolve([diff(f, x), diff(f, y)], [x, y])")
t('''Bestimme die kritischen Punkte von f(x, y) = x · y und ordne sie ein: Gib die Funktionswerte an den Stellen (0,1 | 0,1) und (0,1 | −0,1) aus.''',
  body="f = x * y\ndisplay(solve([diff(f, x), diff(f, y)], [x, y]))\n[f.subs({x: Rational(1, 10), y: Rational(1, 10)}), f.subs({x: Rational(1, 10), y: -Rational(1, 10)})]")
t('''Bestimme die kritischen Punkte von f(x, y) = x³ + y³ − 3xy und ordne sie mit der Hesse-Matrix ein (Liste von (Punkt, det H, fₓₓ)). **(Zusatz)**''',
  body="f = x**3 + y**3 - 3*x*y\nH = hessian(f, (x, y))\n[(p, H.subs({x: p[0], y: p[1]}).det(), H.subs({x: p[0], y: p[1]})[0, 0]) for p in solve([diff(f, x), diff(f, y)], [x, y])]")
t('''Bestimme den Hochpunkt des Hügels f(x, y) = 4 · e^(−(x² + y²)/4) und die Tangentialebene dort.''',
  body="f = 4 * exp(-(x**2 + y**2) / 4)\nk = solve([diff(f, x), diff(f, y)], [x, y])\ndisplay(k)\nf.subs({x: 0, y: 0}) + diff(f, x).subs({x: 0, y: 0}) * x + diff(f, y).subs({x: 0, y: 0}) * y")
t('''Bestimme die kritischen Punkte von f(x, y) = x · e^(−x² − y²) (Liste) und die Funktionswerte dort.''',
  body="f = x * exp(-x**2 - y**2)\nk = solve([diff(f, x), diff(f, y)], [x, y])\ndisplay(k)\n[f.subs({x: a, y: b}) for a, b in k]")
t('''Zeichne die Fläche f(x, y) = x · e^(−x² − y²) für −2 ≤ x, y ≤ 2 und erkenne Hoch- und Tiefpunkt.''', body="plot3d(x * exp(-x**2 - y**2), (x, -2, 2), (y, -2, 2));")

# ---------------------------------------------------------------- 6
sec('Anwendungen')
t('''**Kiste ohne Deckel:** Eine Kiste mit der rechteckigen Grundfläche x · y und der Höhe h soll 32 Liter fassen (x·y·h = 32, in dm). Die Oberfläche ohne Deckel ist
O = x·y + 2·x·h + 2·y·h. Ersetze h = 32/(x·y) und bestimme die kritischen Punkte für x, y > 0 sowie die Maße der Kiste.''',
  given="a, b = symbols('a b', positive=True)",
  body="O = a*b + 2*a*32/(a*b) + 2*b*32/(a*b)\nk = solve([diff(O, a), diff(O, b)], [a, b], dict=True)\ndisplay(k)\n(k[0][a], k[0][b], 32 / (k[0][a] * k[0][b]))")
t('''**Gewinn:** Eine Firma stellt zwei Produkte in den Mengen x und y her. Der Gewinn ist G(x, y) = 40x + 60y − x² − xy − 2y². Bei welchen Mengen ist er maximal, und wie groß ist er?''',
  body="G = 40*x + 60*y - x**2 - x*y - 2*y**2\nk = solve([diff(G, x), diff(G, y)], [x, y])\ndisplay(k)\nG.subs(k)")
t('''**Methode der kleinsten Quadrate:** Durch die Punkte (1 | 2), (2 | 3), (3 | 5), (4 | 6) soll eine Gerade y = m·x + b gelegt werden, sodass die Summe der Abweichungsquadrate
S(m, b) = Σ (m·xᵢ + b − yᵢ)² minimal ist. Stelle S auf und bestimme m und b über den Gradienten.''',
  given="m, b = symbols('m b', real=True)",
  body="punkte = [(1, 2), (2, 3), (3, 5), (4, 6)]\nS = sum([(m * px + b - py)**2 for px, py in punkte])\nsolve([diff(S, m), diff(S, b)], [m, b])")

generate('sympy_dmw_flaechen', 'DMW: Flächen im Raum, partielle Ableitungen und Gradient', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
