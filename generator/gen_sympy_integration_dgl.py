# Erzeugt ../content/sympy_integration_dgl.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_integration_dgl.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_integration_dgl.py
#
# Vertiefungskurs Mathematik BW: weiterführende Integralrechnung (partielle Integration, Substitution, Partialbruchzerlegung als Zusatz)
# und Differentialgleichungen (Begriff, Richtungsfeld, Trennung der Variablen, lineare DGL 1. Ordnung, Schwingungsgleichung
# 2. Ordnung, Anfangswertprobleme). Baut auf sympy_integrale und sympy_wachstum (dsolve, Function, checkodesol) auf.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = ("from sympy import *\ninit_printing()\nimport matplotlib.pyplot as plt\nx, u = symbols('x u', real=True)\n"
         "C1, C2 = symbols('C1 C2')\ny = Function('y')")

INTRO = '''In diesem Notebook (Vertiefungskurs) geht es um **Integrationstechniken** und **Differentialgleichungen**.
Mit **partieller Integration** und **Substitution** findest du Stammfunktionen, die man nicht einfach „ablesen“ kann.
Danach löst du Differentialgleichungen: mit **Trennung der Variablen**, als **lineare** Gleichungen und als **Schwingungsgleichung**;
das **Richtungsfeld** zeigt, wie die Lösungen verlaufen.

`integrate()` und `dsolve()` liefern das Ergebnis sofort. Hier geht es aber um den **Rechenweg**: Du führst die Schritte einzeln mit sympy aus
und vergleichst am Ende mit dem fertigen Ergebnis.

Vorausgesetzt werden die Notebooks *Integrale* und *Wachstum* (`dsolve`).

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy und matplotlib, schaltet die Formel-Ausgabe ein
und legt die reellen Variablen `x`, `u`, die Konstanten `C1`, `C2` und das Funktionssymbol `y` (für Differentialgleichungen) an.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Partielle Integration')
expl('''#### ∫ u · v' dx = u · v − ∫ u' · v dx

Die **partielle Integration** kommt aus der Produktregel. Man zerlegt den Integranden in einen Faktor u, der beim Ableiten einfacher wird,
und einen Faktor v', den man integrieren kann.

Beispiel ∫ x · eˣ dx: u = x (u' = 1), v' = eˣ (v = eˣ). Dann ist ∫ x · eˣ dx = x · eˣ − ∫ 1 · eˣ dx = (x − 1) · eˣ.''',
     """uu = x
vs = exp(x)
v = integrate(vs, x)
F = uu * v - integrate(diff(uu, x) * v, x)
display(factor(F))
display(integrate(x * exp(x), x))
simplify(diff(F, x) - x * exp(x))""")

PI = "F = uu * v - integrate(diff(uu, x) * v, x)\n"
t('Berechne ∫ x · sin(x) dx mit partieller Integration (u = x, v\' = sin x) wie im Beispiel und vergleiche mit `integrate`.',
  body="uu, vs = x, sin(x)\nv = integrate(vs, x)\n" + PI + "display(F)\nintegrate(x * sin(x), x)")
t('Berechne ∫ x · e^(−x) dx mit partieller Integration.', body="uu, vs = x, exp(-x)\nv = integrate(vs, x)\n" + PI + "factor(F)")
t('''Berechne ∫ ln(x) dx mit dem Trick ln(x) = 1 · ln(x): u = ln(x), v' = 1.''', body="uu, vs = log(x), 1\nv = integrate(vs, x)\n" + PI + "F")
t('''Berechne ∫ x · ln(x) dx (u = ln x, v' = x).''', body="uu, vs = log(x), x\nv = integrate(vs, x)\n" + PI + "expand(F)")
t('''∫ x² · eˣ dx braucht **zweimal** partielle Integration. Gib zuerst u · v − ∫ u'·v **ohne** das letzte Integral auszurechnen aus
(`Integral(...)` statt `integrate`), dann das Endergebnis mit `integrate` (ausgeklammert).''',
  body="display(x**2 * exp(x) - Integral(2*x * exp(x), x))\nfactor(integrate(x**2 * exp(x), x))")
t('''Berechne das bestimmte Integral ∫₀^π x · sin(x) dx: [u · v]₀^π − ∫₀^π u' · v dx.''',
  body="uu, vs = x, sin(x)\nv = integrate(vs, x)\n(uu * v).subs(x, pi) - (uu * v).subs(x, 0) - integrate(diff(uu, x) * v, (x, 0, pi))")
t('''**Phönix-Trick:** Bei I = ∫ eˣ · sin(x) dx kommt nach zweimaliger partieller Integration I wieder vor: I = eˣ sin x − eˣ cos x − I. Löse diese Gleichung nach I
(mit `solve(..., simplify=False)`, sonst schreibt sympy das Ergebnis mit einem verschobenen Kosinus) und vergleiche mit `integrate`.''',
  given="I_ = symbols('I_')",
  body="display(solve(Eq(I_, exp(x) * sin(x) - exp(x) * cos(x) - I_), I_, simplify=False))\nintegrate(exp(x) * sin(x), x)")
t('''Prüfe das Ergebnis von ∫ x² · cos(x) dx durch Ableiten (`simplify` der Differenz).''',
  body="F = integrate(x**2 * cos(x), x)\ndisplay(F)\nsimplify(diff(F, x) - x**2 * cos(x))")

# ---------------------------------------------------------------- 2
sec('Integration durch Substitution')
expl('''#### ∫ f(g(x)) · g'(x) dx = F(g(x))

Steht im Integranden eine verkettete Funktion **und** die Ableitung der inneren Funktion, ersetzt man die innere Funktion durch u = g(x).
Dann ist du = g'(x) dx, und das Integral wird einfacher.

Beispiel ∫ 2x · cos(x²) dx: u = x², du = 2x dx, also ∫ cos(u) du = sin(u) = sin(x²).

Mit sympy: Integrand durch g'(x) teilen, g(x) durch u ersetzen (`subs`), nach u integrieren, dann u = g(x) zurücksetzen.''',
     """g = x**2
integrand = 2*x * cos(x**2)
in_u = simplify(integrand / diff(g, x)).subs(g, u)
display(in_u)
Fu = integrate(in_u, u)
display(Fu.subs(u, g))
integrate(integrand, x)""")

t('Berechne ∫ 3x² · e^(x³) dx mit der Substitution u = x³ wie im Beispiel.',
  body="g = x**3\nin_u = simplify(3*x**2 * exp(x**3) / diff(g, x)).subs(g, u)\ndisplay(in_u)\nintegrate(in_u, u).subs(u, g)")
t('Berechne ∫ x · (x² + 1)⁵ dx mit u = x² + 1 (hier bleibt ein Faktor 1/2).',
  body="g = x**2 + 1\nin_u = simplify(x * (x**2 + 1)**5 / diff(g, x)).subs(g, u)\ndisplay(in_u)\nintegrate(in_u, u).subs(u, g)")
t('Berechne ∫ cos(x) · sin³(x) dx mit u = sin(x).',
  body="g = sin(x)\nin_u = simplify(cos(x) * sin(x)**3 / diff(g, x)).subs(g, u)\ndisplay(in_u)\nintegrate(in_u, u).subs(u, g)")
t('''Berechne ∫ x/(x² + 4) dx mit u = x² + 4 (ein Logarithmus entsteht).''',
  body="g = x**2 + 4\nin_u = simplify(x / (x**2 + 4) / diff(g, x)).subs(g, u)\ndisplay(in_u)\nintegrate(in_u, u).subs(u, g)")
t('''**Logarithmische Integration:** ∫ g'(x)/g(x) dx = ln|g(x)|. Berechne ∫ (2x + 3)/(x² + 3x + 1) dx und ∫ tan(x) dx = ∫ sin(x)/cos(x) dx mit `integrate`.''',
  body="display(integrate((2*x + 3) / (x**2 + 3*x + 1), x))\nintegrate(sin(x) / cos(x), x)")
t('''Berechne ∫₀² x · e^(x²) dx mit Substitution: Die Grenzen werden mit u = x² zu 0 und 4. Rechne ∫₀⁴ (1/2) eᵘ du und vergleiche mit `integrate`.''',
  body="display(integrate(exp(u) / 2, (u, 0, 4)))\nintegrate(x * exp(x**2), (x, 0, 2))")
t('''Prüfe durch Ableiten, dass F(x) = −(1/3)·(1 − x²)^(3/2) eine Stammfunktion von x · √(1 − x²) ist.''',
  body="F = -Rational(1, 3) * (1 - x**2)**Rational(3, 2)\nsimplify(diff(F, x) - x * sqrt(1 - x**2))")
t('''**Fläche des Einheitskreises:** Berechne 4 · ∫₀¹ √(1 − x²) dx (Viertelkreis). Von Hand mit x = sin(u); hier mit `integrate`.''',
  body="4 * integrate(sqrt(1 - x**2), (x, 0, 1))")
predict("""display(integrate(2*x * exp(x**2), x))
display(integrate(cos(3*x), x))
integrate(1 / (2*x + 1), x)""")

# ---------------------------------------------------------------- 3
sec('Partialbruchzerlegung (Zusatz)')
expl('''#### Brüche zerlegen, dann integrieren

Gebrochenrationale Funktionen zerlegt man in eine Summe einfacher Brüche (**Partialbrüche**), die man einzeln integrieren kann.
`apart(term, x)` zerlegt, z. B. (3x + 1)/(x² − 1) = 2/(x − 1) + 1/(x + 1).

Von Hand: Ansatz A/(x − 1) + B/(x + 1), mit dem Nenner (x − 1)(x + 1) multiplizieren: 3x + 1 = A(x + 1) + B(x − 1).
Setzt man die Nullstellen x = 1 und x = −1 ein, erhält man A und B.''',
     """display(apart((3*x + 1) / (x**2 - 1), x))
A_, B_ = symbols('A_ B_')
gl = Eq(3*x + 1, A_ * (x + 1) + B_ * (x - 1))
display(solve([gl.subs(x, 1), gl.subs(x, -1)], [A_, B_]))
integrate((3*x + 1) / (x**2 - 1), x)""")

t('Zerlege 1/(x² − 4) in Partialbrüche und integriere.', body="display(apart(1 / (x**2 - 4), x))\nintegrate(1 / (x**2 - 4), x)")
t('Zerlege (x + 5)/(x² + x − 2) in Partialbrüche und integriere.', body="display(apart((x + 5) / (x**2 + x - 2), x))\nintegrate((x + 5) / (x**2 + x - 2), x)")
t('Zerlege x²/(x² − 1) (erst Polynomdivision, `apart` macht beides).', body="apart(x**2 / (x**2 - 1), x)")
t('Berechne ∫₂³ 1/(x² − 1) dx genau und fasse die Logarithmen mit `logcombine` zusammen.', body="logcombine(integrate(1 / (x**2 - 1), (x, 2, 3)), force=True)")

# ---------------------------------------------------------------- 4
sec('Differentialgleichungen und Richtungsfelder')
expl('''#### y' = f(x, y)

Eine **Differentialgleichung 1. Ordnung** y' = f(x, y) gibt in jedem Punkt (x | y) die **Steigung** der Lösungskurve an.
Zeichnet man in vielen Punkten kleine Striche mit dieser Steigung, erhält man das **Richtungsfeld**; Lösungskurven folgen den Strichen.

Für das Zeichnen: Aus dem sympy-Term macht `lambdify((x, yy), term)` eine Python-Funktion mit zwei Eingaben. `plt.quiver(xs, ys, dx, dy)` zeichnet Pfeile
mit den Richtungen (dx, dy); für Striche mit gleicher Länge teilt man (1, m) durch √(1 + m²).

**Probe:** `checkodesol(dgl, loesung)` prüft eine Lösung, `dsolve(dgl, y(x))` löst die Gleichung.''',
     """yy = symbols('yy', real=True)
steigung = lambdify((x, yy), x - yy)
xs, ys, dxs, dys = [], [], [], []
for i in range(-4, 5):
    for j in range(-4, 5):
        m = steigung(i / 2, j / 2)
        xs.append(i / 2)
        ys.append(j / 2)
        dxs.append(1 / (1 + m**2)**0.5)
        dys.append(m / (1 + m**2)**0.5)
plt.quiver(xs, ys, dxs, dys, angles='xy', pivot='mid')
loes = dsolve(Eq(y(x).diff(x), x - y(x)), y(x), ics={y(0): 1})
display(loes)
fl = lambdify(x, loes.rhs)
xx = [-2 + i / 20 for i in range(81)]
plt.plot(xx, [fl(w) for w in xx], 'r')
plt.ylim(-2, 2)
plt.show()""")

t('''Prüfe mit `checkodesol`, ob y = C1 · e^(x²/2) die Differentialgleichung y' = x · y löst.''',
  body="checkodesol(Eq(y(x).diff(x), x * y(x)), Eq(y(x), C1 * exp(x**2 / 2)))")
t('''Prüfe, welche der Funktionen y = x² + C1, y = 2x, y = x² die Differentialgleichung y' = 2x lösen (Liste der Ergebnisse von `checkodesol`).''',
  body="dgl = Eq(y(x).diff(x), 2*x)\n[checkodesol(dgl, Eq(y(x), w)) for w in [x**2 + C1, 2*x, x**2]]")
t('''Löse y' = x · y allgemein und mit y(0) = 2.''', body="dgl = Eq(y(x).diff(x), x * y(x))\ndisplay(dsolve(dgl, y(x)))\ndsolve(dgl, y(x), ics={y(0): 2})")
t('''Zeichne das Richtungsfeld von y' = −x/y für −2 ≤ x, y ≤ 2 (Gitter mit Schritt 0,5, ohne die Punkte mit y = 0) wie im Beispiel.''',
  body="yy = symbols('yy', real=True)\nsteigung = lambdify((x, yy), -x / yy)\nxs, ys, dxs, dys = [], [], [], []\nfor i in range(-4, 5):\n    for j in range(-4, 5):\n        if j != 0:\n            m = steigung(i / 2, j / 2)\n            xs.append(i / 2)\n            ys.append(j / 2)\n            dxs.append(1 / (1 + m**2)**0.5)\n            dys.append(m / (1 + m**2)**0.5)\nplt.quiver(xs, ys, dxs, dys, angles='xy', pivot='mid')\nplt.gca().set_aspect('equal')\nplt.show()")
predict("""dgl = Eq(y(x).diff(x), 3)
display(dsolve(dgl, y(x)))
dsolve(dgl, y(x), ics={y(0): 5})""")

# ---------------------------------------------------------------- 5
sec('Trennung der Variablen')
expl('''#### y' = g(x) · h(y)

Lässt sich die rechte Seite als Produkt g(x) · h(y) schreiben, trennt man die Variablen:

dy / h(y) = g(x) dx, also ∫ 1/h(y) dy = ∫ g(x) dx + C

Dann löst man nach y auf. Beispiel y' = x · y: ∫ 1/y dy = ∫ x dx ⟹ ln|y| = x²/2 + C ⟹ y = C1 · e^(x²/2).''',
     """yv = symbols('yv', positive=True)
links = integrate(1 / yv, yv)
rechts = integrate(x, x) + C1
display(Eq(links, rechts))
display(solve(Eq(links, rechts), yv))
dsolve(Eq(y(x).diff(x), x * y(x)), y(x))""")

YV = "yv = symbols('yv', positive=True)"
t('''Löse y' = y² · x mit Trennung der Variablen: Gib die Gleichung ∫ 1/y² dy = ∫ x dx + C1 und ihre Lösung nach y aus. Vergleiche mit `dsolve`.''', YV,
  "gl = Eq(integrate(1 / yv**2, yv), integrate(x, x) + C1)\ndisplay(gl)\ndisplay(solve(gl, yv))\ndsolve(Eq(y(x).diff(x), y(x)**2 * x), y(x))")
t('''Löse y' = e^(−y) · 2x mit Trennung der Variablen (∫ eʸ dy = ∫ 2x dx + C1) und gib y aus.''', YV,
  "gl = Eq(integrate(exp(yv), yv), integrate(2*x, x) + C1)\ndisplay(gl)\nsolve(gl, yv)")
t('''Löse das Anfangswertproblem y' = x/y, y(0) = 2 mit `dsolve`.''', body="dsolve(Eq(y(x).diff(x), x / y(x)), y(x), ics={y(0): 2})")
t('''Löse das Anfangswertproblem y' = (1 + y²) mit y(0) = 0 (Lösung mit Tangens).''', body="dsolve(Eq(y(x).diff(x), 1 + y(x)**2), y(x), ics={y(0): 0})")
t('''**Abkühlung (allgemein):** T' = −k · (T − 20). Löse mit `dsolve` für ein positives k und T(0) = 90.''',
  given="k = symbols('k', positive=True)",
  body="dsolve(Eq(y(x).diff(x), -k * (y(x) - 20)), y(x), ics={y(0): 90})")

# ---------------------------------------------------------------- 6
sec('Lineare Differentialgleichungen 1. Ordnung')
expl('''#### y' + a · y = b(x)

Eine **lineare** DGL hat die Form y' + a(x) · y = b(x). Ihre Lösung ist die allgemeine Lösung der **homogenen** Gleichung y' + a·y = 0
plus eine **spezielle** Lösung der ganzen Gleichung. Beispiel y' + y = x: homogen y = C1 · e⁻ˣ, speziell y = x − 1 (durch Einsetzen prüfen).''',
     """dgl = Eq(y(x).diff(x) + y(x), x)
display(dsolve(Eq(y(x).diff(x) + y(x), 0), y(x)))
display(checkodesol(dgl, Eq(y(x), x - 1)))
dsolve(dgl, y(x))""")

t('''Löse y' − 2y = 4 allgemein und mit y(0) = 1.''', body="dgl = Eq(y(x).diff(x) - 2 * y(x), 4)\ndisplay(dsolve(dgl, y(x)))\ndsolve(dgl, y(x), ics={y(0): 1})")
t('''Löse y' + y = eˣ und prüfe die spezielle Lösung y = eˣ/2 mit `checkodesol`.''',
  body="dgl = Eq(y(x).diff(x) + y(x), exp(x))\ndisplay(dsolve(dgl, y(x)))\ncheckodesol(dgl, Eq(y(x), exp(x) / 2))")
t('''Löse y' + 2y = sin(x) allgemein.''', body="dsolve(Eq(y(x).diff(x) + 2 * y(x), sin(x)), y(x))")
t('''**Fallschirm:** Die Geschwindigkeit v(t) beim Fall mit Luftwiderstand erfüllt v' = 9,81 − 0,2·v (Zahlen als `Rational`), v(0) = 0. Löse die DGL
(mit x als Zeit) und gib die Grenzgeschwindigkeit (x → ∞) aus.''',
  body="l = dsolve(Eq(y(x).diff(x), Rational(981, 100) - Rational(1, 5) * y(x)), y(x), ics={y(0): 0})\ndisplay(l)\nlimit(l.rhs, x, oo)")

# ---------------------------------------------------------------- 7
sec('Schwingungen: Differentialgleichungen 2. Ordnung')
expl('''#### y'' = −ω² · y

Eine Feder (ohne Reibung) erfüllt y'' = −ω² · y: Die Beschleunigung ist der Auslenkung entgegengesetzt. Die Lösungen sind
**Schwingungen** y = C1 · sin(ωx) + C2 · cos(ωx). Für eine eindeutige Lösung braucht man **zwei** Anfangswerte: y(0) und y'(0).
In sympy: `ics={y(0): 1, y(x).diff(x).subs(x, 0): 0}`.

Mit Reibung (gedämpfte Schwingung) kommt ein Term mit y' dazu, z. B. y'' + 2y' + 5y = 0; die Lösungen enthalten dann e^(−x).''',
     """dgl = Eq(y(x).diff(x, 2), -4 * y(x))
display(dsolve(dgl, y(x)))
l = dsolve(dgl, y(x), ics={y(0): 1, y(x).diff(x).subs(x, 0): 0})
display(l)
d = dsolve(Eq(y(x).diff(x, 2) + Rational(1, 2) * y(x).diff(x) + 4 * y(x), 0), y(x), ics={y(0): 1, y(x).diff(x).subs(x, 0): 0})
plot(l.rhs, d.rhs, (x, 0, 10), legend=True);""")

t('''Löse y'' = −9y allgemein.''', body="dsolve(Eq(y(x).diff(x, 2), -9 * y(x)), y(x))")
t('''Löse y'' = −9y mit y(0) = 0 und y'(0) = 6.''', body="dsolve(Eq(y(x).diff(x, 2), -9 * y(x)), y(x), ics={y(0): 0, y(x).diff(x).subs(x, 0): 6})")
t('''Prüfe mit `checkodesol`, dass y = 3 · cos(2x) + sin(2x) die Gleichung y'' + 4y = 0 löst.''',
  body="checkodesol(Eq(y(x).diff(x, 2) + 4 * y(x), 0), Eq(y(x), 3 * cos(2*x) + sin(2*x)))")
t('''Löse die gedämpfte Schwingung y'' + 2y' + 5y = 0 mit y(0) = 1, y'(0) = −1.''',
  body="dsolve(Eq(y(x).diff(x, 2) + 2 * y(x).diff(x) + 5 * y(x), 0), y(x), ics={y(0): 1, y(x).diff(x).subs(x, 0): -1})")
t('''Löse y'' − y = 0 allgemein (keine Schwingung, sondern e-Funktionen).''', body="dsolve(Eq(y(x).diff(x, 2) - y(x), 0), y(x))")
t('''Zeichne die Lösung von y'' + 0,3·y' + y = 0 mit y(0) = 2, y'(0) = 0 für 0 ≤ x ≤ 30 (0,3 als `Rational`).''',
  body="l = dsolve(Eq(y(x).diff(x, 2) + Rational(3, 10) * y(x).diff(x) + y(x), 0), y(x), ics={y(0): 2, y(x).diff(x).subs(x, 0): 0})\nplot(l.rhs, (x, 0, 30));")

# ---------------------------------------------------------------- 8
sec('Gemischte Übungen')
t('''Berechne ∫ x³ · e^(x²) dx mit sympy und prüfe das Ergebnis durch Ableiten. (Von Hand: erst u = x², dann partiell.)''',
  body="F = integrate(x**3 * exp(x**2), x)\ndisplay(F)\nsimplify(diff(F, x) - x**3 * exp(x**2))")
t('''Berechne ∫₁^e x² · ln(x) dx genau.''', body="integrate(x**2 * log(x), (x, 1, E))")
t('''**Logistisches Wachstum:** Löse y' = y · (1 − y) mit y(0) = 1/2 mit `dsolve` und gib den Grenzwert für x → ∞ aus.''',
  body="l = dsolve(Eq(y(x).diff(x), y(x) * (1 - y(x))), y(x), ics={y(0): Rational(1, 2)})\ndisplay(l)\nlimit(l.rhs, x, oo)")
t('''Eine Kurve geht durch (0 | 1), und in jedem Punkt ist ihre Steigung gleich der Summe der Koordinaten (y' = x + y). Bestimme die Kurve.''',
  body="dsolve(Eq(y(x).diff(x), x + y(x)), y(x), ics={y(0): 1})")

generate('sympy_integration_dgl', 'Integrationstechniken und Differentialgleichungen', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
