# Erzeugt ../content/sympy_dmw_kruemmung.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_dmw_kruemmung.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_dmw_kruemmung.py
#
# Wahlfach Digitale Mathematische Werkzeuge (BW 2016, Klassen 11/12), 3.1.2 Krümmung und Bogenlänge:
# Bogenlänge von Kurven (Streckenzug → Integral, auch Parameterkurven als Zusatz), Krümmung quantitativ, Krümmungskreis als
# geometrischer Zugang (Kreis durch drei benachbarte Kurvenpunkte), Krümmungskreis als beste Approximation (gleiche Werte von
# f, f', f'' an der Stelle). Anwendung: Übergangsbögen im Straßen- und Schienenbau.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = "from sympy import *\ninit_printing()\nimport matplotlib.pyplot as plt\nx, h, s = symbols('x h s', real=True)\nt = symbols('t', real=True)"

INTRO = '''Dieses Notebook gehört zum Wahlfach **Digitale Mathematische Werkzeuge**. Es geht um zwei Größen, die man einem Graphen ansehen kann:
Wie **lang** ist ein Kurvenstück (**Bogenlänge**)? Und wie **stark gekrümmt** ist die Kurve an einer Stelle (**Krümmung**)?
Die Krümmung wird über den **Krümmungskreis** anschaulich: Er schmiegt sich an die Kurve an und hat an der Stelle dieselbe Krümmung.

Vorausgesetzt werden die Notebooks *Ableitungsregeln* und *Integrale*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy und matplotlib, schaltet die Formel-Ausgabe ein
und legt die reellen Variablen `x`, `h`, `s` und den Parameter `t` an.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Bogenlänge')
expl('''#### Vom Streckenzug zum Integral

Teilt man das Kurvenstück über [a, b] in n kleine Stücke und verbindet die Kurvenpunkte geradlinig, erhält man einen **Streckenzug**.
Seine Länge nähert die Bogenlänge an; mit wachsendem n wird die Näherung besser. Eine kleine Strecke hat nach Pythagoras die Länge
√(Δx² + Δy²) = √(1 + (Δy/Δx)²) · Δx. Im Grenzfall wird daraus das Integral für die **Bogenlänge**:

L = ∫ₐᵇ √(1 + f'(x)²) dx

Viele dieser Integrale kann man nicht genau ausrechnen. Dann schreibt man `Integral(...)` und berechnet mit `N()` einen Näherungswert.''',
     """f = x**2
n = 10
punkte = [Point(Rational(i, n), f.subs(x, Rational(i, n))) for i in range(n + 1)]
streckenzug = sum([punkte[i].distance(punkte[i + 1]) for i in range(n)])
display(N(streckenzug, 6))
L = integrate(sqrt(1 + diff(f, x)**2), (x, 0, 1))
display(L, N(L, 6))
N(Integral(sqrt(1 + diff(sin(x), x)**2), (x, 0, pi)), 6)""")

t('Berechne die Länge des Streckenzugs für f(x) = x² über [0, 1] mit n = 100 Teilstücken (6 Ziffern).',
  body="f = x**2\nn = 100\npunkte = [Point(Rational(i, n), f.subs(x, Rational(i, n))) for i in range(n + 1)]\nN(sum([punkte[i].distance(punkte[i + 1]) for i in range(n)]), 6)")
t('''Schreibe eine Funktion `streckenzug(f, a, b, n)` für die Länge des Streckenzugs mit n gleich langen Teilstücken. Gib für f(x) = sin(x) über [0, π]
die Werte für n = 2, 4, 8, 16 mit 6 Ziffern als Liste aus.''',
  body="def streckenzug(f, a, b, n):\n    xs = [a + (b - a) * Rational(i, n) for i in range(n + 1)]\n    punkte = [Point(w, f.subs(x, w)) for w in xs]\n    return sum([punkte[i].distance(punkte[i + 1]) for i in range(n)])\n\n[N(streckenzug(sin(x), 0, pi, m), 6) for m in [2, 4, 8, 16]]")
t('Berechne die Bogenlänge von f(x) = x^(3/2) über [0, 4] genau und mit 5 Ziffern.',
  body="f = x**Rational(3, 2)\nL = integrate(sqrt(1 + diff(f, x)**2), (x, 0, 4))\ndisplay(L)\nN(L, 5)")
t('''Berechne die Bogenlänge der **Kettenlinie** f(x) = cosh(x) über [0, 1]. Vereinfache dazu zuerst √(1 + f'²) mit `simplify` und integriere dann.''',
  body="w = simplify(sqrt(1 + diff(cosh(x), x)**2))\ndisplay(w)\nintegrate(w, (x, 0, 1))")
t('Berechne die Bogenlänge der Normalparabel f(x) = x² über [−2, 2] mit 5 Ziffern.', body="N(Integral(sqrt(1 + diff(x**2, x)**2), (x, -2, 2)), 5)")
t('''Prüfe die Formel am Halbkreis f(x) = √(1 − x²) über [−1, 1], die Bogenlänge muss π sein. Von Hand vereinfacht ist √(1 + f'²) = 1/√(1 − x²).
Prüfe diese Vereinfachung an der Stelle x = 1/2 und integriere dann 1/√(1 − x²) über [−1, 1].''',
  body="w = sqrt(1 + diff(sqrt(1 - x**2), x)**2)\ndisplay(simplify(w.subs(x, Rational(1, 2)) - 1 / sqrt(1 - Rational(1, 4))))\nintegrate(1 / sqrt(1 - x**2), (x, -1, 1))")
t('''Ein Seil hängt in Form von f(x) = 2 · cosh(x/2) (in m) zwischen x = −3 und x = 3. Wie lang ist es (4 Ziffern)?''',
  body="N(Integral(sqrt(1 + diff(2 * cosh(x / 2), x)**2), (x, -3, 3)), 4)")
t('''**(Zusatz) Parameterkurven:** Für eine Kurve (x(t) | y(t)) ist L = ∫ √(x'(t)² + y'(t)²) dt. Berechne den Umfang des Kreises (3 cos t | 3 sin t), 0 ≤ t ≤ 2π,
und die Länge eines Bogens der **Zykloide** (t − sin t | 1 − cos t), 0 ≤ t ≤ 2π (mit `simplify` vor dem Integrieren, dann `N` mit 5 Ziffern).''',
  body="display(integrate(simplify(sqrt(diff(3*cos(t), t)**2 + diff(3*sin(t), t)**2)), (t, 0, 2*pi)))\nN(Integral(sqrt(diff(t - sin(t), t)**2 + diff(1 - cos(t), t)**2), (t, 0, 2*pi)), 5)")

# ---------------------------------------------------------------- 2
sec('Krümmung')
expl('''#### κ = f''/(1 + f'²)^(3/2)

Die **Krümmung** κ gibt an, wie schnell sich die Richtung der Kurve ändert, gemessen pro Längeneinheit des Bogens.
Für den Graphen einer Funktion gilt

κ(x) = f''(x) / (1 + f'(x)²)^(3/2)

- κ > 0: Linkskurve, κ < 0: Rechtskurve, κ = 0: gerade (z. B. im Wendepunkt)
- Eine Gerade hat überall die Krümmung 0, ein Kreis mit Radius r überall den Betrag 1/r.

Die zweite Ableitung allein reicht nicht: Bei steilen Stellen wird sie durch den Nenner „gedämpft“.''',
     """def kruemmung(f):
    return diff(f, x, 2) / (1 + diff(f, x)**2)**Rational(3, 2)

k = kruemmung(x**2)
display(k)
display(k.subs(x, 0), k.subs(x, 1))
display(kruemmung(sqrt(4 - x**2)).subs(x, 1))
plot(x**2, k, (x, -2, 2), legend=True);""")

K = "def kruemmung(f):\n    return diff(f, x, 2) / (1 + diff(f, x)**2)**Rational(3, 2)\n"
t('Berechne die Krümmung von f(x) = x³ allgemein und an den Stellen −1, 0 und 1.', K,
  "k = kruemmung(x**3)\ndisplay(k)\n[k.subs(x, w) for w in [-1, 0, 1]]")
t('Zeige, dass der Kreis f(x) = √(9 − x²) überall die Krümmung −1/3 hat: Werte die Krümmung an den Stellen 0, 1, 2 aus (mit `simplify`).', K,
  "[simplify(kruemmung(sqrt(9 - x**2)).subs(x, w)) for w in [0, 1, 2]]")
t('Berechne die Krümmung von f(x) = eˣ an der Stelle 0 genau und mit 4 Ziffern.', K, "k0 = kruemmung(exp(x)).subs(x, 0)\ndisplay(k0)\nN(k0, 4)")
t('''Wo ist die Krümmung von f(x) = eˣ am größten? Löse κ'(x) = 0 und gib die Stelle genau und mit 4 Ziffern aus.''', K,
  "l = solve(diff(kruemmung(exp(x)), x), x)\ndisplay(l)\nN(l[0], 4)")
t('''Berechne die Krümmung der Parabel f(x) = a·x² im Scheitel in Abhängigkeit von a (a > 0).''',
  K + "a = symbols('a', positive=True)", "kruemmung(a * x**2).subs(x, 0)")
t('''Vergleiche f''(x) und κ(x) für f(x) = x² an den Stellen 0, 1, 2, 3 (Liste von Paaren mit 4 Ziffern). Die zweite Ableitung ist konstant, die Krümmung nicht.''', K,
  "f = x**2\n[(diff(f, x, 2).subs(x, w), N(kruemmung(f).subs(x, w), 4)) for w in [0, 1, 2, 3]]")
t('''Zeichne f(x) = sin(x) und seine Krümmung für 0 ≤ x ≤ 2π in ein Diagramm (mit Legende).''', K, "plot(sin(x), kruemmung(sin(x)), (x, 0, 2*pi), legend=True);")
predict("""def kruemmung(f):
    return diff(f, x, 2) / (1 + diff(f, x)**2)**Rational(3, 2)

display(kruemmung(3*x + 1))
display(kruemmung(x**2 / 2).subs(x, 0))
kruemmung(-x**2 / 2).subs(x, 0)""")

# ---------------------------------------------------------------- 3
sec('Der Krümmungskreis')
expl('''#### Kreis durch drei benachbarte Punkte

Durch drei Punkte, die nicht auf einer Geraden liegen, geht genau ein Kreis (`Circle(P1, P2, P3)` aus `sympy.geometry`).
Nimmt man die Kurvenpunkte an den Stellen x₀ − h, x₀ und x₀ + h und lässt h kleiner werden, nähern sich diese Kreise dem **Krümmungskreis**.
Sein Radius ist r = 1/|κ(x₀)|, sein Mittelpunkt M liegt auf der Normalen auf der Seite, zu der die Kurve gekrümmt ist:

M = (x₀ − f'·(1 + f'²)/f'' | f(x₀) + (1 + f'²)/f'')  (Ableitungen an der Stelle x₀)''',
     """f = x**3
x0 = 1
def P(a):
    return Point(a, f.subs(x, a))
for hh in [Rational(1, 2), Rational(1, 10), Rational(1, 100)]:
    C = Circle(P(x0 - hh), P(x0), P(x0 + hh))
    print(hh, N(C.center, 5), N(C.radius, 5))
f1, f2 = diff(f, x).subs(x, x0), diff(f, x, 2).subs(x, x0)
display((x0 - f1 * (1 + f1**2) / f2, f.subs(x, x0) + (1 + f1**2) / f2))
(1 + f1**2)**Rational(3, 2) / Abs(f2)""")
expl('''#### Zeichnen

Den Kreis zeichnet man als Parameterkurve (xₘ + r·cos t | yₘ + r·sin t) mit `plot_parametric`; zusammen mit dem Graphen
und gleich langen Achsen (`aspect_ratio=(1, 1)`) sieht man, wie er sich anschmiegt. Mit `p.extend(...)` fügt man einem sympy-Diagramm
weitere Kurven hinzu, `p.show()` zeigt es.''',
     """f = x**2
xm, ym, r = 0, Rational(1, 2), Rational(1, 2)
p = plot(f, (x, -1.5, 1.5), show=False, aspect_ratio=(1, 1), ylim=(-0.5, 2))
p.extend(plot_parametric(xm + r * cos(t), ym + r * sin(t), (t, 0, 2*pi), show=False))
p.show()""")

KK = ("def kreis(f, x0):\n    f1, f2 = diff(f, x).subs(x, x0), diff(f, x, 2).subs(x, x0)\n"
      "    M = (x0 - f1 * (1 + f1**2) / f2, f.subs(x, x0) + (1 + f1**2) / f2)\n"
      "    return M, (1 + f1**2)**Rational(3, 2) / Abs(f2)\n")
t('''Schreibe eine Funktion `kreis(f, x0)`, die Mittelpunkt (als Tupel) und Radius des Krümmungskreises zurückgibt. Teste mit f(x) = x² an der Stelle 0
und an der Stelle 1.''',
  body=KK + "\ndisplay(kreis(x**2, 0))\nkreis(x**2, 1)")
t('Bestimme den Krümmungskreis von f(x) = eˣ an der Stelle 0 (Mittelpunkt und Radius).', KK, "kreis(exp(x), 0)")
t('Bestimme den Krümmungskreis von f(x) = sin(x) an der Stelle π/2.', KK, "kreis(sin(x), pi/2)")
t('''Berechne die Kreise durch die Punkte von f(x) = x⁴ an den Stellen 1 − h, 1, 1 + h für h = 1/2, 1/10, 1/100 und gib jeweils den Radius mit 5 Ziffern aus.
Vergleiche mit dem Radius des Krümmungskreises an der Stelle 1 (mit `kreis` von oben, 5 Ziffern).''', KK,
  "def P(a):\n    return Point(a, a**4)\n\ndisplay([N(Circle(P(1 - hh), P(1), P(1 + hh)).radius, 5) for hh in [Rational(1, 2), Rational(1, 10), Rational(1, 100)]])\nN(kreis(x**4, 1)[1], 5)")
t('''Zeichne f(x) = x³ und seinen Krümmungskreis an der Stelle x₀ = 1 (Mittelpunkt (−4 | 8/3), Radius 5√10/3) wie im Beispiel (−9 ≤ x ≤ 2, y von −3 bis 9).''',
  body="p = plot(x**3, (x, -9, 2), show=False, aspect_ratio=(1, 1), ylim=(-3, 9))\nr = 5 * sqrt(10) / 3\np.extend(plot_parametric(-4 + r * cos(t), Rational(8, 3) + r * sin(t), (t, 0, 2*pi), show=False))\np.show()")
t('''**Ellipse:** Der obere Bogen der Ellipse x²/4 + y² = 1 ist f(x) = √(1 − x²/4). Berechne die Radien der Krümmungskreise am Scheitel (0 | 1) und nahe am Ende (x = 1,9),
mit 4 Ziffern.''', KK, "f = sqrt(1 - x**2 / 4)\n[N(kreis(f, w)[1], 4) for w in [0, Rational(19, 10)]]")

# ---------------------------------------------------------------- 4
sec('Der Krümmungskreis als beste Annäherung')
expl('''#### Gleiche Werte bis zur zweiten Ableitung

Die **Tangente** stimmt an der Stelle x₀ mit f im Funktionswert und in der ersten Ableitung überein (beste Gerade).
Der **Krümmungskreis** stimmt sogar im Funktionswert, in der ersten **und** in der zweiten Ableitung überein: Er ist der Kreis, der sich am besten anschmiegt.

Prüfen: Den unteren Halbkreis um M(xₘ | yₘ) mit Radius r beschreibt g(x) = yₘ − √(r² − (x − xₘ)²) (oberer: +).
Man vergleicht g, g', g'' an der Stelle x₀ mit f, f', f''.''',
     """f = x**2
xm, ym, r = 0, Rational(1, 2), Rational(1, 2)
g = ym - sqrt(r**2 - (x - xm)**2)
display([f.subs(x, 0), diff(f, x).subs(x, 0), diff(f, x, 2).subs(x, 0)])
[g.subs(x, 0), diff(g, x).subs(x, 0), diff(g, x, 2).subs(x, 0)]""")

t('''Prüfe für f(x) = eˣ an der Stelle 0: Der Krümmungskreis hat den Mittelpunkt (−2 | 3) und den Radius 2√2. Vergleiche f, f', f'' mit g, g', g'' des **unteren** Halbkreises.''',
  body="f = exp(x)\ng = 3 - sqrt(8 - (x + 2)**2)\ndisplay([f.subs(x, 0), diff(f, x).subs(x, 0), diff(f, x, 2).subs(x, 0)])\n[simplify(g.subs(x, 0)), simplify(diff(g, x).subs(x, 0)), simplify(diff(g, x, 2).subs(x, 0))]")
t('''Ein anderer Kreis durch (0 | 1) mit derselben Tangente: Mittelpunkt (−1 | 2), Radius √2. Vergleiche g'' an der Stelle 0 mit f''(0) = 1. (Er stimmt nur bis zur ersten Ableitung.)''',
  body="g = 2 - sqrt(2 - (x + 1)**2)\n[simplify(g.subs(x, 0)), simplify(diff(g, x).subs(x, 0)), simplify(diff(g, x, 2).subs(x, 0))]")
t('''Zeichne f(x) = eˣ, die Tangente y = x + 1 und den unteren Bogen des Krümmungskreises g(x) = 3 − √(8 − (x + 2)²) für −2 ≤ x ≤ 1 in ein Diagramm (mit Legende).''',
  body="plot(exp(x), x + 1, 3 - sqrt(8 - (x + 2)**2), (x, -2, 1), legend=True);")
t('''Wie gut nähern Tangente und Krümmungskreis f(x) = eˣ bei x = 0,2 an? Gib die Fehler |f − Tangente| und |f − g| mit 3 Ziffern aus.''',
  body="w = Rational(1, 5)\ndisplay(N(Abs(exp(w) - (w + 1)), 3))\nN(Abs(exp(w) - (3 - sqrt(8 - (w + 2)**2))), 3)")

# ---------------------------------------------------------------- 5
sec('Anwendung: Übergangsbögen')
expl('''#### Kein Krümmungssprung

Fährt ein Auto oder Zug von einer Geraden (κ = 0) direkt in einen Kreisbogen (κ = 1/r), springt die Krümmung. Man müsste das Lenkrad
schlagartig drehen, im Zug spürt man einen Ruck. Deshalb baut man **Übergangsbögen**, deren Krümmung stetig von 0 auf 1/r wächst.

Beispiel: Ein Bogen f(x) = a·x³ für x ≥ 0 schließt an die x-Achse (x ≤ 0) ohne Knick **und** ohne Krümmungssprung an:
f(0) = 0, f'(0) = 0, κ(0) = 0.''',
     """def kruemmung(f):
    return diff(f, x, 2) / (1 + diff(f, x)**2)**Rational(3, 2)

f = x**3 / 30
display([f.subs(x, 0), diff(f, x).subs(x, 0), kruemmung(f).subs(x, 0)])
display([N(kruemmung(f).subs(x, w), 3) for w in [1, 2, 3]])
g = x**2 / 2
[g.subs(x, 0), diff(g, x).subs(x, 0), kruemmung(g).subs(x, 0)]""")

t('''Prüfe, ob der Anschluss von f(x) = x²/10 (x ≥ 0) an die x-Achse (x ≤ 0) einen Krümmungssprung hat: Gib f(0), f'(0) und κ(0) aus.''', K,
  "f = x**2 / 10\n[f.subs(x, 0), diff(f, x).subs(x, 0), kruemmung(f).subs(x, 0)]")
t('''Bestimme a so, dass der Übergangsbogen f(x) = a·x³ an der Stelle x = 2 die Krümmung 1/10 hat (4 Ziffern). Es gibt zwei Lösungen; gesucht ist die kleine
(flacher Bogen). Mit einem Startwert findet `nsolve` hier die große. Suche deshalb im Intervall [0; 0,05] mit dem **Bisektionsverfahren**:
`nsolve(term, a, (0, 0.05), solver='bisect')`.''',
  K + "a = symbols('a', positive=True)", "N(nsolve(kruemmung(a * x**3).subs(x, 2) - Rational(1, 10), a, (0, 0.05), solver='bisect'), 4)")
t('''Zeichne die Krümmung des Übergangsbogens f(x) = x³/30 für 0 ≤ x ≤ 6.''', K, "plot(kruemmung(x**3 / 30), (x, 0, 6));")
t('''Eine Straße verläuft für x ≤ 0 auf der x-Achse. Ein Übergangsbogen f(x) = a·x³ + b·x⁴ soll an der Stelle x = 1 die Steigung 1/2 und die Krümmung 0 haben.
Bestimme a und b (zwei Gleichungen, `solve`) und gib zur Kontrolle κ(0) aus.''', K,
  "a, b = symbols('a b', real=True)\nf = a * x**3 + b * x**4\nl = solve([Eq(diff(f, x).subs(x, 1), Rational(1, 2)), Eq(diff(f, x, 2).subs(x, 1), 0)], [a, b])\ndisplay(l)\nkruemmung(f.subs(l)).subs(x, 0)")

generate('sympy_dmw_kruemmung', 'DMW: Bogenlänge und Krümmung', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
