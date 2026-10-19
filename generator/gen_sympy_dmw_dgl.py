# Erzeugt ../content/sympy_dmw_dgl.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_dmw_dgl.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_dmw_dgl.py
#
# Wahlfach Digitale Mathematische Werkzeuge (BW 2016, Klassen 11/12), 3.1.5 Differentialgleichungen:
# Lösung grafisch mit dem Richtungsfeld deuten, prüfen, ob eine Funktion Lösung ist (Beispiele des Bildungsplans: y' = y/x, y' = k·y,
# y' = 2y/x, y' = n·y/x, y' = (y + y²)/x), Differentialgleichungen in einfachen Fällen untersuchen und deuten (logistisches Wachstum,
# Schwingungen), explizites und implizites Euler-Verfahren, Güte der Näherung (Schrittweite, Verfahren).
# Steigungsterme mit dem Symbol y; für dsolve/checkodesol die Funktion Y = Function('y') (Hilfsfunktion dgl() in der Setup-Zelle).
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = '''from sympy import *
init_printing()
import matplotlib.pyplot as plt
x, y = symbols('x y', real=True)
k, n, G = symbols('k n G', positive=True)
C1, C2 = symbols('C1 C2')
Y = Function('y')

def dgl(steigung):
    """Die Differentialgleichung y' = steigung für dsolve und checkodesol."""
    return Eq(Y(x).diff(x), steigung.subs(y, Y(x)))

def richtungsfeld(steigung, xb=(-3, 3), yb=(-3, 3), schritt=0.5):
    """Zeichnet das Richtungsfeld von y' = steigung (Term in x und y) als gleich lange Striche."""
    f = lambdify((x, y), steigung, 'math')
    xs, ys, us, vs = [], [], [], []
    for i in range(round((xb[1] - xb[0]) / schritt) + 1):
        for j in range(round((yb[1] - yb[0]) / schritt) + 1):
            a, b = xb[0] + i * schritt, yb[0] + j * schritt
            try:
                m = f(a, b)
            except (ZeroDivisionError, ValueError):
                continue
            xs.append(a)
            ys.append(b)
            us.append(1 / (1 + m**2)**0.5)
            vs.append(m / (1 + m**2)**0.5)
    plt.quiver(xs, ys, us, vs, angles='xy', pivot='mid', headwidth=1, headlength=0, headaxislength=0)
    plt.xlim(xb)
    plt.ylim(yb)'''

INTRO = '''Dieses Notebook gehört zum Wahlfach **Digitale Mathematische Werkzeuge**. Viele Vorgänge beschreibt man am einfachsten über ihre
**Änderungsrate**: Eine Population wächst umso schneller, je größer sie ist; eine Feder zieht umso stärker zurück, je weiter sie ausgelenkt ist.
Solche Gesetze sind **Differentialgleichungen**: Gleichungen, in denen eine unbekannte Funktion und ihre Ableitungen vorkommen.

Du siehst Lösungen im **Richtungsfeld**, prüfst, ob eine Funktion eine Lösung ist, untersuchst logistisches Wachstum und Schwingungen
und berechnest Näherungslösungen mit dem **Euler-Verfahren**, so wie es Computer tun, wenn es keine Formel für die Lösung gibt.

Vorausgesetzt werden die Notebooks *Wachstum* (`dsolve`, `checkodesol`) und *Integrale*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy und matplotlib, schaltet die Formel-Ausgabe ein und legt an:
- die reellen Variablen `x`, `y`, die positiven Parameter `k`, `n`, `G` und die Konstanten `C1`, `C2`,
- `Y`: die gesuchte Funktion y(x) für `dsolve` und `checkodesol`,
- `dgl(steigung)`: macht aus einem Steigungsterm in x und y die Differentialgleichung y' = steigung, z. B. `dgl(x * y)` für y' = x·y,
- `richtungsfeld(steigung, xb, yb, schritt)`: zeichnet das Richtungsfeld von y' = steigung im Bereich xb × yb (danach `plt.show()`).''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Richtungsfelder')
expl('''#### Die Steigung in jedem Punkt

Eine Differentialgleichung y' = f(x, y) sagt in jedem Punkt (x | y), welche **Steigung** eine Lösungskurve dort hat. Zeichnet man an vielen Punkten kleine
Striche mit dieser Steigung, erhält man das **Richtungsfeld**. Lösungskurven verlaufen überall in Richtung der Striche; durch jeden Punkt geht genau eine.

Man sieht oft schon am Richtungsfeld, wie sich Lösungen verhalten (wachsen, fallen, sich einer Geraden nähern), ohne eine Formel zu kennen.''',
     """richtungsfeld(x - y)
loes = dsolve(dgl(x - y), Y(x), ics={Y(0): 1})
display(loes)
fl = lambdify(x, loes.rhs)
xs = [-3 + i / 20 for i in range(121)]
plt.plot(xs, [fl(w) for w in xs], 'r')
plt.show()""")

t('Zeichne das Richtungsfeld von y\' = y für −3 ≤ x, y ≤ 3.', body="richtungsfeld(y)\nplt.show()")
t('Zeichne das Richtungsfeld von y\' = −x/y (die Punkte mit y = 0 lässt die Funktion weg). Die Lösungen sind Kreise.', body="richtungsfeld(-x / y)\nplt.gca().set_aspect('equal')\nplt.show()")
t('Zeichne das Richtungsfeld von y\' = y/x für −3 ≤ x, y ≤ 3 mit der Schrittweite 0,4.', body="richtungsfeld(y / x, schritt=0.4)\nplt.show()")
t('''Zeichne das Richtungsfeld von y' = x² − y für −2 ≤ x ≤ 3, −1 ≤ y ≤ 5 und dazu die Lösung durch (0 | 0) (mit `dsolve` und `lambdify` wie im Beispiel).''',
  body="richtungsfeld(x**2 - y, xb=(-2, 3), yb=(-1, 5))\nloes = dsolve(dgl(x**2 - y), Y(x), ics={Y(0): 0})\nfl = lambdify(x, loes.rhs)\nxs = [-2 + i / 20 for i in range(101)]\nplt.plot(xs, [fl(w) for w in xs], 'r')\nplt.show()")
t('''An welchen Punkten hat jede Lösung von y' = x − y eine waagrechte Tangente? Löse x − y = 0 nach y auf (das ist die **Isokline** zur Steigung 0).''',
  body="solve(Eq(x - y, 0), y)")

# ---------------------------------------------------------------- 2
sec('Lösungen prüfen')
expl('''#### Einsetzen und vergleichen

Ob eine Funktion y = g(x) Lösung von y' = f(x, y) ist, prüft man durch Einsetzen: g'(x) − f(x, g(x)) muss für alle x null sein.
`checkodesol(dgl(...), Eq(Y(x), g))` macht das und gibt `(True, 0)` bei einer Lösung aus.

Eine Lösung mit einer Konstanten C1 heißt **allgemeine Lösung**; jedes C1 gibt eine Kurve im Richtungsfeld.''',
     """g = C1 * x
display(simplify(diff(g, x) - (y / x).subs(y, g)))
display(checkodesol(dgl(y / x), Eq(Y(x), g)))
checkodesol(dgl(y / x), Eq(Y(x), x**2))""")

t('Prüfe von Hand (Ableitung minus rechte Seite, vereinfacht), ob y = C1 · e^(kx) die Gleichung y\' = k·y löst.', body="g = C1 * exp(k*x)\nsimplify(diff(g, x) - k * g)")
t('Prüfe mit `checkodesol`, ob y = C1 · x² die Gleichung y\' = 2y/x löst.', body="checkodesol(dgl(2*y / x), Eq(Y(x), C1 * x**2))")
t('Prüfe mit `checkodesol`, ob y = C1 · xⁿ die Gleichung y\' = n·y/x löst.', body="checkodesol(dgl(n*y / x), Eq(Y(x), C1 * x**n))")
t('''Prüfe, ob y = C1·x/(1 − C1·x) die Gleichung y' = (y + y²)/x löst (mit `checkodesol`), und ob y = x/(1 − x) eine spezielle Lösung ist.''',
  body="display(checkodesol(dgl((y + y**2) / x), Eq(Y(x), C1 * x / (1 - C1 * x))))\ncheckodesol(dgl((y + y**2) / x), Eq(Y(x), x / (1 - x)))")
t('''Welche der Funktionen x³, 2x³, x² + 1 und 3x lösen y' = 3y/x? (Liste der Wahrheitswerte: erstes Element von `checkodesol`)''',
  body="[checkodesol(dgl(3*y / x), Eq(Y(x), g))[0] for g in [x**3, 2*x**3, x**2 + 1, 3*x]]")
t('''Bestimme C1 so, dass die Lösung y = C1 · x² von y' = 2y/x durch den Punkt (2 | 6) geht.''', body="solve(Eq(C1 * 2**2, 6), C1)")
t('''Löse y' = y/x und y' = n·y/x mit `dsolve` allgemein.''', body="display(dsolve(dgl(y / x), Y(x)))\ndsolve(dgl(n*y / x), Y(x))")
predict("""display(checkodesol(dgl(y), Eq(Y(x), exp(x))))
display(checkodesol(dgl(y), Eq(Y(x), 5 * exp(x))))
checkodesol(dgl(y), Eq(Y(x), exp(x) + 1))[0]""")

# ---------------------------------------------------------------- 3
sec('Logistisches Wachstum')
expl('''#### y' = k · y · (G − y)

Beim **logistischen Wachstum** ist die Wachstumsrate proportional zum Bestand y **und** zum Abstand zur Grenze G. Am Anfang wächst der Bestand fast
exponentiell, später bremst er ab und nähert sich G. Lösungen sind

y(x) = G / (1 + a·e^(−k·G·x))  mit a = G/y(0) − 1.

Ohne die Lösung zu kennen, liest man aus der DGL ab: Für 0 < y < G ist y' > 0; y' ist am größten bei y = G/2 (dort ist der **Wendepunkt**).''',
     """steig = k * y * (G - y)
display(solve(diff(steig, y), y))
loes = G / (1 + C1 * exp(-k * G * x))
display(checkodesol(dgl(steig), Eq(Y(x), loes)))
f = Rational(1, 50) * y * (10 - y)
richtungsfeld(f, xb=(0, 40), yb=(0, 12), schritt=2)
g = 10 / (1 + 9 * exp(-Rational(1, 5) * x))
xs = list(range(41))
plt.plot(xs, [float(g.subs(x, w)) for w in xs], 'r')
plt.show()""")

t('''Für welchen Bestand y ist das Wachstum y' = 0,02·y·(10 − y) am größten, und wie groß ist es dann?''', body="steig = Rational(2, 100) * y * (10 - y)\nym = solve(diff(steig, y), y)[0]\n(ym, steig.subs(y, ym))")
t('''Prüfe, dass y = 10/(1 + 9·e^(−0,2x)) die Gleichung y' = 0,02·y·(10 − y) mit y(0) = 1 löst (`checkodesol` und y(0)).''',
  body="g = 10 / (1 + 9 * exp(-Rational(1, 5) * x))\ndisplay(checkodesol(dgl(Rational(2, 100) * y * (10 - y)), Eq(Y(x), g)))\ng.subs(x, 0)")
t('''Bestimme für die Lösung der vorigen Aufgabe die Wendestelle (genau und mit 4 Ziffern) und den Grenzwert für x → ∞.''',
  body="g = 10 / (1 + 9 * exp(-Rational(1, 5) * x))\nxw = solve(diff(g, x, 2), x)[0]\ndisplay(expand_log(xw, force=True), N(xw, 4))\nlimit(g, x, oo)")
t('''**Gerücht:** In einer Schule mit 600 Schülern kennen anfangs 6 ein Gerücht; es breitet sich nach y' = 0,001·y·(600 − y) aus (x in Stunden). Stelle die Lösung nach der Formel
G/(1 + a·e^(−kGx)) auf und gib aus, wann die Hälfte der Schüler das Gerücht kennt (4 Ziffern).''',
  body="a = Rational(600, 6) - 1\ng = 600 / (1 + a * exp(-Rational(1, 1000) * 600 * x))\ndisplay(g)\nN(solve(Eq(g, 300), x)[0], 4)")
t('''Was passiert bei y(0) > G? Zeichne das Richtungsfeld von y' = 0,02·y·(10 − y) für 0 ≤ x ≤ 40, 0 ≤ y ≤ 16 (Schritt 2) und dazu die Lösung mit y(0) = 15:
10/(1 − (1/3)·e^(−0,2x)).''',
  body="richtungsfeld(Rational(2, 100) * y * (10 - y), xb=(0, 40), yb=(0, 16), schritt=2)\ng = 10 / (1 - Rational(1, 3) * exp(-Rational(1, 5) * x))\nxs = list(range(41))\nplt.plot(xs, [float(g.subs(x, w)) for w in xs], 'r')\nplt.show()")

# ---------------------------------------------------------------- 4
sec('Schwingungen')
expl('''#### y'' = −ω² · y

Bei einer Feder ist die Beschleunigung der Auslenkung entgegengesetzt und proportional zu ihr: y'' = −ω²·y (**harmonische Schwingung**).
Die Lösungen sind y = C1·sin(ωx) + C2·cos(ωx) mit der Periode 2π/ω. Für eine eindeutige Lösung braucht man **zwei** Anfangswerte: Auslenkung y(0) und
Geschwindigkeit y'(0). In sympy: `ics={Y(0): 1, Y(x).diff(x).subs(x, 0): 0}`.

Mit Reibung kommt ein Term mit y' dazu (**gedämpfte Schwingung**), z. B. y'' + 0,5·y' + 4y = 0; die Amplitude nimmt dann exponentiell ab.''',
     """sw = Eq(Y(x).diff(x, 2), -4 * Y(x))
display(dsolve(sw, Y(x)))
l = dsolve(sw, Y(x), ics={Y(0): 1, Y(x).diff(x).subs(x, 0): 0})
display(l)
d = dsolve(Eq(Y(x).diff(x, 2) + Rational(1, 2) * Y(x).diff(x) + 4 * Y(x), 0), Y(x), ics={Y(0): 1, Y(x).diff(x).subs(x, 0): 0})
plot(l.rhs, d.rhs, (x, 0, 10), legend=True);""")

t('Löse y\'\' = −9y allgemein und gib die Periode der Lösungen aus.', body="display(dsolve(Eq(Y(x).diff(x, 2), -9 * Y(x)), Y(x)))\n2 * pi / 3")
t('Löse y\'\' = −9y mit y(0) = 0 und y\'(0) = 6.', body="dsolve(Eq(Y(x).diff(x, 2), -9 * Y(x)), Y(x), ics={Y(0): 0, Y(x).diff(x).subs(x, 0): 6})")
t('Prüfe mit `checkodesol`, dass y = 3·cos(2x) + sin(2x) die Gleichung y\'\' + 4y = 0 löst.',
  body="checkodesol(Eq(Y(x).diff(x, 2) + 4 * Y(x), 0), Eq(Y(x), 3 * cos(2*x) + sin(2*x)))")
t('Löse die gedämpfte Schwingung y\'\' + 2y\' + 5y = 0 mit y(0) = 1, y\'(0) = −1.',
  body="dsolve(Eq(Y(x).diff(x, 2) + 2 * Y(x).diff(x) + 5 * Y(x), 0), Y(x), ics={Y(0): 1, Y(x).diff(x).subs(x, 0): -1})")
t('''**Federpendel:** Eine Masse m = 0,5 kg hängt an einer Feder mit D = 8 N/m. Es gilt m·y'' = −D·y. Wie groß ist ω (ω² = D/m), und wie lange dauert eine Schwingung (4 Ziffern)?''',
  body="w = sqrt(Rational(8) / Rational(1, 2))\ndisplay(w)\nN(2 * pi / w, 4)")
t('''Zeichne die Lösung von y'' + 0,3·y' + y = 0 mit y(0) = 2, y'(0) = 0 für 0 ≤ x ≤ 30 (0,3 als `Rational`).''',
  body="l = dsolve(Eq(Y(x).diff(x, 2) + Rational(3, 10) * Y(x).diff(x) + Y(x), 0), Y(x), ics={Y(0): 2, Y(x).diff(x).subs(x, 0): 0})\nplot(l.rhs, (x, 0, 30));")

# ---------------------------------------------------------------- 5
sec('Das explizite Euler-Verfahren')
expl('''#### Schritt für Schritt entlang der Tangente

Wenn man keine Formel für die Lösung findet, rechnet man **numerisch**. Beim **expliziten Euler-Verfahren** geht man vom Anfangspunkt (x₀ | y₀) mit der
Schrittweite h jeweils ein Stück entlang der Steigung, die die DGL im **aktuellen** Punkt vorgibt:

xₖ₊₁ = xₖ + h,  yₖ₊₁ = yₖ + h · f(xₖ, yₖ)

Beispiel y' = y, y(0) = 1 (genaue Lösung eˣ), h = 0,1. Gerechnet wird mit Kommazahlen; `round(w, 4)` rundet auf 4 Nachkommastellen.''',
     """f = lambdify((x, y), y)
h = 0.1
xs, ys = [0.0], [1.0]
for i in range(10):
    ys.append(ys[-1] + h * f(xs[-1], ys[-1]))
    xs.append(xs[-1] + h)
display([round(w, 4) for w in ys])
display(round(ys[-1], 4), N(E, 5))
plt.plot(xs, ys, 'o-', label='Euler')
plt.plot(xs, [float(exp(w)) for w in xs], label='e^x')
plt.legend()
plt.show()""")

EULER = ("def euler(steigung, x0, y0, h, schritte):\n    f = lambdify((x, y), steigung)\n    xs, ys = [x0], [y0]\n"
         "    for i in range(schritte):\n        ys.append(ys[-1] + h * f(xs[-1], ys[-1]))\n        xs.append(xs[-1] + h)\n    return xs, ys\n")
t('''Schreibe eine Funktion `euler(steigung, x0, y0, h, schritte)`, die die Listen xs und ys zurückgibt. Teste mit y' = y, y(0) = 1, h = 0,1, 10 Schritte
und gib den letzten y-Wert auf 4 Stellen gerundet aus.''',
  body=EULER + "\nxs, ys = euler(y, 0.0, 1.0, 0.1, 10)\nround(ys[-1], 4)")
t('''Berechne mit dem expliziten Euler-Verfahren y(1) für y' = y, y(0) = 1 mit h = 0,1, 0,01 und 0,001 (auf 5 Stellen gerundet).''', EULER,
  "[round(euler(y, 0.0, 1.0, h, round(1 / h))[1][-1], 5) for h in [0.1, 0.01, 0.001]]")
t('''Löse y' = x − y, y(0) = 1 mit Euler (h = 0,2, 10 Schritte) und gib die y-Werte auf 3 Stellen gerundet aus. Vergleiche y(2) mit der genauen Lösung (4 Ziffern).''', EULER,
  "xs, ys = euler(x - y, 0.0, 1.0, 0.2, 10)\ndisplay([round(w, 3) for w in ys])\nloes = dsolve(dgl(x - y), Y(x), ics={Y(0): 1})\nN(loes.rhs.subs(x, 2), 4)")
t('''Logistisches Wachstum mit Euler: y' = 0,02·y·(10 − y), y(0) = 1, h = 1, 40 Schritte. Gib y nach 10, 20, 30, 40 Schritten auf 3 Stellen gerundet aus.''', EULER,
  "xs, ys = euler(0.02 * y * (10 - y), 0.0, 1.0, 1.0, 40)\n[round(ys[i], 3) for i in [10, 20, 30, 40]]")
t('''Zeichne die Euler-Näherung (h = 1) und die genaue Lösung 10/(1 + 9·e^(−0,2x)) der vorigen Aufgabe in ein Diagramm (mit Legende).''', EULER,
  "xs, ys = euler(0.02 * y * (10 - y), 0.0, 1.0, 1.0, 40)\nplt.plot(xs, ys, 'o', label='Euler')\nplt.plot(xs, [float(10 / (1 + 9 * exp(-w / 5))) for w in xs], label='genau')\nplt.legend()\nplt.show()")
expl('''#### Schwingungen mit Euler

Eine DGL 2. Ordnung wie y'' = −ω²·y schreibt man als zwei Gleichungen 1. Ordnung mit der Geschwindigkeit v = y':
y' = v, v' = −ω²·y. Euler rechnet beide gleichzeitig weiter (mit den **alten** Werten):

yₖ₊₁ = yₖ + h·vₖ,  vₖ₊₁ = vₖ − h·ω²·yₖ

Für ω = 1 ist die genaue Lösung y = cos x, v = −sin x, also immer y² + v² = 1 (die Energie bleibt gleich). An y² + v² sieht man den Fehler des Verfahrens.''',
     """h, om = 0.1, 1.0
ys, vs = [1.0], [0.0]
for i in range(100):
    ys.append(ys[-1] + h * vs[-1])
    vs.append(vs[-1] - h * om**2 * ys[-2])
ts = [i * h for i in range(101)]
plt.plot(ts, ys, label='Euler')
plt.plot(ts, [float(cos(w)) for w in ts], label='cos')
plt.legend()
plt.show()
round(ys[-1]**2 + vs[-1]**2, 3)""")
t('''Rechne die Schwingung y'' = −y, y(0) = 1, y'(0) = 0 mit Euler und h = 0,05 für 200 Schritte (bis x = 10). Gib y² + v² am Ende auf 3 Stellen gerundet aus.
(Genau wäre es 1; das explizite Verfahren lässt die Schwingung immer größer werden.)''',
  body="h = 0.05\nys, vs = [1.0], [0.0]\nfor i in range(200):\n    ys.append(ys[-1] + h * vs[-1])\n    vs.append(vs[-1] - h * ys[-2])\nround(ys[-1]**2 + vs[-1]**2, 3)")

# ---------------------------------------------------------------- 6
sec('Das implizite Euler-Verfahren')
expl('''#### Die Steigung am neuen Punkt

Beim **impliziten Euler-Verfahren** nimmt man die Steigung am **neuen** Punkt:

yₖ₊₁ = yₖ + h · f(xₖ₊₁, yₖ₊₁)

Das unbekannte yₖ₊₁ steht auf beiden Seiten, man muss in jedem Schritt eine **Gleichung lösen**. Dafür ist ein CAS praktisch: `nsolve(gleichung, z, start)`
löst sie numerisch, als Startwert nimmt man yₖ.

Für y' = k·y kann man von Hand auflösen: yₖ₊₁ = yₖ + h·k·yₖ₊₁ ⟹ yₖ₊₁ = yₖ / (1 − h·k).''',
     """z = symbols('z')
f = y
h = 0.1
ys = [1.0]
for i in range(10):
    xneu = (i + 1) * h
    ys.append(float(nsolve(z - ys[-1] - h * f.subs({x: xneu, y: z}), z, ys[-1])))
display([round(w, 4) for w in ys])
display(round(1 / (1 - 0.1)**10, 4), N(E, 5))""")

IMPL = ("def euler_implizit(steigung, x0, y0, h, schritte):\n    z = symbols('z')\n    xs, ys = [x0], [y0]\n"
        "    for i in range(schritte):\n        xs.append(xs[-1] + h)\n        ys.append(float(nsolve(z - ys[-1] - h * steigung.subs({x: xs[-1], y: z}), z, ys[-1])))\n    return xs, ys\n")
t('''Schreibe eine Funktion `euler_implizit(steigung, x0, y0, h, schritte)` (wie im Beispiel mit `nsolve`). Teste mit y' = y, y(0) = 1, h = 0,1, 10 Schritte
(letzter Wert auf 4 Stellen gerundet).''',
  body=IMPL + "\nxs, ys = euler_implizit(y, 0.0, 1.0, 0.1, 10)\nround(ys[-1], 4)")
t('''Vergleiche für y' = y, y(0) = 1 die Werte y(1) des expliziten und des impliziten Verfahrens mit h = 0,1 mit e (alle auf 4 Stellen). Das explizite Verfahren liegt
darunter, das implizite darüber.''', EULER + IMPL,
  "[round(euler(y, 0.0, 1.0, 0.1, 10)[1][-1], 4), round(euler_implizit(y, 0.0, 1.0, 0.1, 10)[1][-1], 4), round(float(E), 4)]")
t('''Löse y' = x − y, y(0) = 1 mit dem impliziten Verfahren (h = 0,2, 10 Schritte) und gib y(2) auf 4 Stellen gerundet aus.''', IMPL,
  "round(euler_implizit(x - y, 0.0, 1.0, 0.2, 10)[1][-1], 4)")
t('''Logistisches Wachstum implizit: y' = 0,02·y·(10 − y), y(0) = 1, h = 1. Gib y nach 10, 20, 30, 40 Schritten auf 3 Stellen gerundet aus.''', IMPL,
  "xs, ys = euler_implizit(Rational(2, 100) * y * (10 - y), 0.0, 1.0, 1.0, 40)\n[round(ys[i], 3) for i in [10, 20, 30, 40]]")
t('''Implizit für die Schwingung: y' = v, v' = −y. Mit den neuen Werten gilt yₖ₊₁ = yₖ + h·vₖ₊₁, vₖ₊₁ = vₖ − h·yₖ₊₁. Löse dieses lineare System für einen Schritt allgemein
nach yₖ₊₁ und vₖ₊₁.''',
  given="yk, vk, h0, yn, vn = symbols('y_k v_k h y_{k+1} v_{k+1}')",
  body="solve([Eq(yn, yk + h0 * vn), Eq(vn, vk - h0 * yn)], [yn, vn])")
t('''Rechne damit die Schwingung y'' = −y, y(0) = 1, y'(0) = 0 implizit mit h = 0,05 für 200 Schritte und gib y² + v² am Ende
auf 3 Stellen gerundet aus. (Beim impliziten Verfahren wird die Schwingung immer kleiner.)''',
  body="h = 0.05\nys, vs = [1.0], [0.0]\nfor i in range(200):\n    yk, vk = ys[-1], vs[-1]\n    ys.append((yk + h * vk) / (1 + h**2))\n    vs.append((vk - h * yk) / (1 + h**2))\nround(ys[-1]**2 + vs[-1]**2, 3)")

# ---------------------------------------------------------------- 7
sec('Die Güte der Näherung')
expl('''#### Schrittweite und Verfahren

Der Fehler des Euler-Verfahrens hängt von der **Schrittweite** ab: Halbiert man h, halbiert sich der Fehler an einer festen Stelle ungefähr
(das Verfahren hat die **Ordnung 1**). Doppelte Genauigkeit kostet also doppelt so viele Schritte.

Bei manchen Gleichungen ist das explizite Verfahren bei zu großem h sogar **instabil**: Für y' = −10·y (genaue Lösung fällt schnell auf 0) springen
die Euler-Werte bei h = 0,25 hin und her und wachsen. Das implizite Verfahren bleibt stabil.''',
     """def euler(steigung, x0, y0, h, schritte):
    f = lambdify((x, y), steigung)
    xs, ys = [x0], [y0]
    for i in range(schritte):
        ys.append(ys[-1] + h * f(xs[-1], ys[-1]))
        xs.append(xs[-1] + h)
    return xs, ys

fehler = [(h, round(float(E) - euler(y, 0.0, 1.0, h, round(1 / h))[1][-1], 5)) for h in [0.1, 0.05, 0.025, 0.0125]]
display(fehler)
display([round(w, 2) for w in euler(-10 * y, 0.0, 1.0, 0.25, 8)[1]])
[round(1 / (1 + 10 * 0.25)**i, 4) for i in range(9)]""")

t('''Berechne für y' = y, y(0) = 1 die Fehler e − y(1) des expliziten Verfahrens für h = 0,1, 0,05, 0,025 und die Quotienten aufeinanderfolgender Fehler (auf 3 Stellen).''', EULER,
  "f = [float(E) - euler(y, 0.0, 1.0, h, round(1 / h))[1][-1] for h in [0.1, 0.05, 0.025]]\n[round(f[0] / f[1], 3), round(f[1] / f[2], 3)]")
t('''Wie viele Schritte braucht das explizite Verfahren für y' = y, y(0) = 1, damit y(1) auf 0,001 genau ist? Verdopple die Schrittzahl ab 10, bis |e − y(1)| < 0,001.''', EULER,
  "m = 10\nwhile abs(float(E) - euler(y, 0.0, 1.0, 1 / m, m)[1][-1]) >= 0.001:\n    m *= 2\nm")
t('''Untersuche die Stabilität für y' = −10·y, y(0) = 1: Gib die ersten 6 Werte des expliziten Verfahrens für h = 0,05 und h = 0,25 aus (auf 3 Stellen).''', EULER,
  "display([round(w, 3) for w in euler(-10 * y, 0.0, 1.0, 0.05, 5)[1]])\n[round(w, 3) for w in euler(-10 * y, 0.0, 1.0, 0.25, 5)[1]]")
t('''Das **Verfahren von Heun** (verbessertes Euler-Verfahren) nimmt den Mittelwert der Steigungen am alten und am vorläufigen neuen Punkt:
p = yₖ + h·f(xₖ, yₖ), yₖ₊₁ = yₖ + h/2·(f(xₖ, yₖ) + f(xₖ₊₁, p)). Berechne damit y(1) für y' = y, y(0) = 1, h = 0,1 und den Fehler (auf 5 Stellen). **(Zusatz)**''',
  body="f = lambdify((x, y), y)\nh = 0.1\nxk, yk = 0.0, 1.0\nfor i in range(10):\n    p = yk + h * f(xk, yk)\n    yk = yk + h / 2 * (f(xk, yk) + f(xk + h, p))\n    xk = xk + h\n(round(yk, 5), round(float(E) - yk, 5))")

generate('sympy_dmw_dgl', 'DMW: Differentialgleichungen, Richtungsfelder und Euler-Verfahren', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
