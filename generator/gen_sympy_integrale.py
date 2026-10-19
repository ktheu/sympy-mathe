# Erzeugt ../content/sympy_integrale.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_integrale.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_integrale.py
#
# Bildungsplan BW 2016, Kursstufe (Basis- und Leistungsfach), Leitidee Funktionaler Zusammenhang / Messen:
# Stammfunktionen, bestimmtes Integral als orientierter Flächeninhalt und als Rekonstruktion eines Bestands aus der Änderungsrate,
# Hauptsatz der Differential- und Integralrechnung, Flächen zwischen Graph und x-Achse bzw. zwischen zwei Graphen,
# Integralfunktion, Mittelwert einer Funktion, Rotationskörper und uneigentliche Integrale (Leistungsfach).
# (Mittelwert und uneigentliche Integrale sind laut Facherlass 2025 nicht Gegenstand der schriftlichen Abiturprüfung, gehören aber zum Bildungsplan.)
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = ("from sympy import *\ninit_printing()\nimport matplotlib.pyplot as plt\nx, t = symbols('x t', real=True)\n"
         "a, b, k = symbols('a b k', real=True)")

INTRO = '''In diesem Notebook geht es um die **Integralrechnung**: Stammfunktionen, das bestimmte Integral, Flächen unter und zwischen Graphen,
die Rekonstruktion eines Bestands aus seiner Änderungsrate und (im Leistungsfach) Rotationskörper und uneigentliche Integrale.

sympy integriert mit `integrate()`. Bestimme Stammfunktionen trotzdem zuerst **von Hand** und prüfe sie mit `diff()` oder `integrate()`.
Beim Flächenberechnen ist die wichtigste Arbeit deine: Nullstellen finden, Intervalle richtig aufteilen, Vorzeichen beachten.

Vorausgesetzt werden die Notebooks *Ableitungsregeln* und *Funktionsanalyse*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy und matplotlib, schaltet die Formel-Ausgabe ein
und legt die reellen Variablen `x`, `t` und die Parameter `a`, `b`, `k` an.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Stammfunktionen')
expl('''#### F' = f

Eine Funktion F heißt **Stammfunktion** von f, wenn F'(x) = f(x). Mit F ist auch F + C eine Stammfunktion (C eine Konstante).

`integrate(f, x)` gibt **eine** Stammfunktion aus, **ohne** + C. Prüfen kannst du jede Stammfunktion durch Ableiten.

| f(x) | F(x) |
|---|---|
| xⁿ (n ≠ −1) | xⁿ⁺¹ / (n + 1) |
| e^(kx) | e^(kx) / k |
| sin(kx) | −cos(kx) / k |
| cos(kx) | sin(kx) / k |
| 1/x (Leistungsfach) | ln\\|x\\| (sympy schreibt nur `log(x)`, gemeint ist für x < 0 ln(−x)) |

Für eine **lineare Verkettung** f(ax + b) gilt: F(ax + b) / a.''',
     """display(integrate(x**3, x))
display(integrate(exp(2*x), x))
display(integrate(sin(x) + 4, x))
display(integrate((2*x + 1)**3, x))
F = x**4 / 4 + 7
diff(F, x)""")

t('Gib eine Stammfunktion von f(x) = 6x² − 4x + 1 aus.', body='integrate(6*x**2 - 4*x + 1, x)')
t('Gib eine Stammfunktion von f(x) = 1/x² aus.', body='integrate(1 / x**2, x)')
t('Gib eine Stammfunktion von f(x) = √x aus.', body='integrate(sqrt(x), x)')
t('Gib eine Stammfunktion von f(x) = 3 · e^(−x) aus.', body='integrate(3 * exp(-x), x)')
t('Gib eine Stammfunktion von f(x) = cos(2x) − sin(x) aus.', body='integrate(cos(2*x) - sin(x), x)')
t('''Gib eine Stammfunktion von f(x) = (3x − 1)⁵ aus (sympy multipliziert aus). Berechne dann mit `simplify` die Differenz zur Stammfunktion (3x − 1)⁶/18,
die man mit der Regel für lineare Verkettungen erhält. Ist die Differenz eine Konstante, sind beide Stammfunktionen.''',
  body='F = integrate((3*x - 1)**5, x)\ndisplay(F)\nsimplify(F - (3*x - 1)**6 / 18)')
t('Gib eine Stammfunktion von f(x) = e^(kx) aus (k ≠ 0, lege dafür ein Symbol `k` mit `nonzero=True` an).',
  given="k = symbols('k', real=True, nonzero=True)", body='integrate(exp(k*x), x)')
t('Gib eine Stammfunktion von f(x) = 2/x aus. **(Leistungsfach)**', body='integrate(2 / x, x)')
t('''Prüfe, ob F(x) = x · eˣ − eˣ eine Stammfunktion von f(x) = x · eˣ ist (`simplify(F' − f)`).''',
  body='F = x * exp(x) - exp(x)\nsimplify(diff(F, x) - x * exp(x))')
t('''Prüfe, ob F(x) = (x² + 1)³ eine Stammfunktion von f(x) = 6x · (x² + 1)² ist.''',
  body='F = (x**2 + 1)**3\nsimplify(diff(F, x) - 6*x * (x**2 + 1)**2)')
t('''Bestimme die Stammfunktion von f(x) = 2x − 3, deren Graph durch P(1 | 4) geht: Setze F(x) = (Stammfunktion) + C an und bestimme C.''',
  given="C = symbols('C')",
  body='F = integrate(2*x - 3, x) + C\nF.subs(C, solve(Eq(F.subs(x, 1), 4), C)[0])')
t('''Bestimme die Stammfunktion von f(x) = eˣ + 1, deren Graph durch den Ursprung geht.''',
  given="C = symbols('C')",
  body='F = integrate(exp(x) + 1, x) + C\nF.subs(C, solve(Eq(F.subs(x, 0), 0), C)[0])')
predict("""display(integrate(1, x))
display(integrate(x, x))
display(integrate(exp(x), x))
simplify(diff(integrate(sin(x)**3, x), x) - sin(x)**3)""")

# ---------------------------------------------------------------- 2
sec('Das bestimmte Integral und der Hauptsatz')
expl('''#### ∫ₐᵇ f(x) dx = F(b) − F(a)

Das **bestimmte Integral** von a bis b ist der **orientierte Flächeninhalt**: Flächen oberhalb der x-Achse zählen positiv,
Flächen unterhalb negativ. Nach dem **Hauptsatz der Differential- und Integralrechnung** berechnet man es mit einer
beliebigen Stammfunktion F: ∫ₐᵇ f(x) dx = F(b) − F(a).

In sympy: `integrate(f, (x, a, b))`. Mit `Integral(f, (x, a, b))` wird das Integral nur **hingeschrieben**; `.doit()` rechnet es aus.''',
     """I = Integral(x**2, (x, 0, 3))
display(Eq(I, I.doit()))
F = integrate(x**2, x)
display(F.subs(x, 3) - F.subs(x, 0))
display(integrate(x**3 - 4*x, (x, 0, 2)))
plot(x**2, (x, 0, 3));""")

t('Berechne ∫₁⁴ (2x + 1) dx einmal mit F(4) − F(1) und einmal mit `integrate`.',
  body='F = integrate(2*x + 1, x)\ndisplay(F.subs(x, 4) - F.subs(x, 1))\nintegrate(2*x + 1, (x, 1, 4))')
t('Berechne ∫₀² (x³ − x) dx.', body='integrate(x**3 - x, (x, 0, 2))')
t('Berechne ∫₀^π sin(x) dx und ∫₀^(2π) sin(x) dx.', body='display(integrate(sin(x), (x, 0, pi)))\nintegrate(sin(x), (x, 0, 2*pi))')
t('Berechne ∫₀¹ eˣ dx genau und mit 4 Ziffern.', body='I = integrate(exp(x), (x, 0, 1))\ndisplay(I)\nN(I, 4)')
t('Berechne ∫₁^e (1/x) dx. **(Leistungsfach)**', body='integrate(1 / x, (x, 1, E))')
t('Gib die Gleichung ∫₋₁² x² dx = (Wert) mit `Eq(Integral(...), ...)` aus wie im Beispiel.', body='I = Integral(x**2, (x, -1, 2))\nEq(I, I.doit())')
t('Berechne ∫₀ᵇ (2x) dx allgemein und bestimme b > 0 so, dass das Integral 9 ist.',
  given="b = symbols('b', positive=True)", body='I = integrate(2*x, (x, 0, b))\ndisplay(I)\nsolve(Eq(I, 9), b)')
t('Für welches a > 0 gilt ∫₀ᵃ (x² − 2x) dx = 0?', given="a = symbols('a', positive=True)", body='solve(integrate(x**2 - 2*x, (x, 0, a)), a)')
t('''Prüfe die Regel ∫ₐᵇ f + ∫ᵇᶜ f = ∫ₐᶜ f für f(x) = x² mit a = 0, b = 1, c = 3.''',
  body='f = x**2\nintegrate(f, (x, 0, 1)) + integrate(f, (x, 1, 3)) == integrate(f, (x, 0, 3))')
t('''Prüfe die Regel ∫ₐᵇ f = −∫ᵇᵃ f für f(x) = eˣ mit a = 0, b = 2.''',
  body='integrate(exp(x), (x, 0, 2)) == -integrate(exp(x), (x, 2, 0))')
predict("""display(integrate(x, (x, -1, 1)))
display(integrate(x**2, (x, -1, 1)))
display(integrate(5, (x, 2, 2)))
integrate(1, (x, 0, 7))""")

# ---------------------------------------------------------------- 3
sec('Flächen zwischen Graph und x-Achse')
expl('''#### Erst die Nullstellen, dann integrieren

Das Integral rechnet Flächen unter der x-Achse negativ. Für den **Flächeninhalt** teilt man das Intervall an den Nullstellen auf
und addiert die **Beträge** der Teilintegrale (`Abs()`).

Beispiel: f(x) = x³ − 4x hat die Nullstellen −2, 0, 2. Das Integral von −2 bis 2 ist 0, der Flächeninhalt aber 8.''',
     """f = x**3 - 4*x
display(solve(f, x))
display(integrate(f, (x, -2, 2)))
A = Abs(integrate(f, (x, -2, 0))) + Abs(integrate(f, (x, 0, 2)))
display(A)
plot(f, (x, -2.5, 2.5));""")

t('Berechne den Flächeninhalt zwischen dem Graphen von f(x) = −x² + 4 und der x-Achse.',
  body='f = -x**2 + 4\nns = solve(f, x)\ndisplay(ns)\nintegrate(f, (x, ns[0], ns[1]))')
t('Berechne den Flächeninhalt, den f(x) = x² − 2x mit der x-Achse einschließt.',
  body='f = x**2 - 2*x\nns = solve(f, x)\nAbs(integrate(f, (x, ns[0], ns[1])))')
t('Berechne den Flächeninhalt zwischen dem Graphen von f(x) = x³ − x und der x-Achse (zwei Teilflächen).',
  body='f = x**3 - x\ndisplay(solve(f, x))\nAbs(integrate(f, (x, -1, 0))) + Abs(integrate(f, (x, 0, 1)))')
t('Berechne den Flächeninhalt zwischen dem Graphen von f(x) = sin(x) und der x-Achse über [0, 2π].',
  body='Abs(integrate(sin(x), (x, 0, pi))) + Abs(integrate(sin(x), (x, pi, 2*pi)))')
t('''Berechne den Flächeninhalt zwischen f(x) = x² − 1 und der x-Achse über dem Intervall [0, 2] (Nullstelle bei 1 beachten).''',
  body='f = x**2 - 1\nAbs(integrate(f, (x, 0, 1))) + Abs(integrate(f, (x, 1, 2)))')
t('''Berechne für f(x) = x · e⁻ˣ den Flächeninhalt zwischen Graph und x-Achse über [0, 3] genau und mit 4 Ziffern.''',
  body='A = integrate(x * exp(-x), (x, 0, 3))\ndisplay(A)\nN(A, 4)')
t('''Schreibe eine Funktion `flaeche(f, a, b)`, die die Nullstellen von f im Intervall (a, b) mit `solveset(f, x, Interval.open(a, b))` sucht,
das Intervall dort aufteilt und die Beträge der Teilintegrale addiert. Teste mit f(x) = x³ − 4x auf [−2, 2] und mit f(x) = sin(x) auf [0, 2π].''',
  body="def flaeche(f, a, b):\n    stellen = [a] + sorted(solveset(f, x, Interval.open(a, b))) + [b]\n    A = 0\n    for i in range(len(stellen) - 1):\n        A = A + Abs(integrate(f, (x, stellen[i], stellen[i + 1])))\n    return A\n\ndisplay(flaeche(x**3 - 4*x, -2, 2))\nflaeche(sin(x), 0, 2*pi)")
t('''Für welches k > 0 schließt der Graph von f(x) = −x² + k mit der x-Achse den Flächeninhalt 36 ein?''',
  given="k = symbols('k', positive=True)",
  body='f = -x**2 + k\nns = solve(f, x)\nsolve(Eq(integrate(f, (x, ns[0], ns[1])), 36), k)')
predict("""f = x**2 - 4
display(integrate(f, (x, -2, 2)))
display(Abs(integrate(f, (x, -2, 2))))
integrate(Abs(f), (x, -2, 2))""")

# ---------------------------------------------------------------- 4
sec('Flächen zwischen zwei Graphen')
expl('''#### ∫ (f − g)

Der Flächeninhalt zwischen den Graphen von f und g über [a, b] ist ∫ₐᵇ (f(x) − g(x)) dx, wenn f ≥ g ist.
Die Grenzen sind oft die **Schnittstellen** (f(x) = g(x)). Schneiden sich die Graphen dazwischen, teilt man auf und nimmt Beträge.''',
     """f = -x**2 + 4
g = x + 2
s = solve(Eq(f, g), x)
display(s)
display(integrate(f - g, (x, s[0], s[1])))
plot(f, g, (x, -3, 2));""")

t('Berechne den Flächeninhalt zwischen f(x) = x² und g(x) = x.',
  body='s = solve(Eq(x**2, x), x)\ndisplay(s)\nAbs(integrate(x**2 - x, (x, s[0], s[1])))')
t('Berechne den Flächeninhalt zwischen f(x) = 4 − x² und g(x) = x² − 4.',
  body='s = solve(Eq(4 - x**2, x**2 - 4), x)\nintegrate((4 - x**2) - (x**2 - 4), (x, s[0], s[1]))')
t('Berechne den Flächeninhalt zwischen f(x) = x³ und g(x) = x (zwei Teilflächen).',
  body='display(solve(Eq(x**3, x), x))\nAbs(integrate(x**3 - x, (x, -1, 0))) + Abs(integrate(x**3 - x, (x, 0, 1)))')
t('Berechne den Flächeninhalt zwischen f(x) = eˣ, g(x) = 1 − x und der Geraden x = 1 (Schnittstelle bei 0) genau und mit 4 Ziffern.',
  body='A = integrate(exp(x) - (1 - x), (x, 0, 1))\ndisplay(A)\nN(A, 4)')
t('''Berechne den Flächeninhalt zwischen f(x) = sin(x) und g(x) = cos(x) über [π/4, 5π/4] (dort ist sin ≥ cos).''',
  body='integrate(sin(x) - cos(x), (x, pi/4, 5*pi/4))')
t('''Zeichne f(x) = x² und g(x) = 2x + 3 und berechne den Flächeninhalt zwischen ihnen.''',
  body='f, g = x**2, 2*x + 3\nplot(f, g, (x, -2, 4));\ns = solve(Eq(f, g), x)\nintegrate(g - f, (x, s[0], s[1]))')
t('''Die Gerade y = c teilt die Fläche zwischen f(x) = −x² + 4 und der x-Achse (Inhalt 32/3) in zwei gleich große Teile.
Bestimme c mit `nsolve` (Startwert 1): Die Fläche oberhalb von y = c reicht von −√(4 − c) bis √(4 − c) und soll 16/3 sein.''',
  given="c = symbols('c', positive=True)",
  body='w = sqrt(4 - c)\nA_oben = integrate(-x**2 + 4 - c, (x, -w, w))\nN(nsolve(A_oben - Rational(16, 3), c, 1), 4)')

# ---------------------------------------------------------------- 5
sec('Integralfunktion und Bestand aus Änderungsrate')
expl('''#### Iₐ(x) = ∫ₐˣ f(t) dt

Hält man die untere Grenze fest und lässt die obere Grenze variabel, erhält man die **Integralfunktion** Iₐ(x) = ∫ₐˣ f(t) dt.
Sie ist eine Stammfunktion von f mit Iₐ(a) = 0. Die Integrationsvariable heißt dann t, damit sie sich von der Grenze x unterscheidet.

**Rekonstruktion:** Ist f die **Änderungsrate** einer Größe (z. B. Zuflussrate in Liter pro Minute), dann ist ∫ₐᵇ f(t) dt die
**Änderung des Bestands** von a bis b. Bestand am Ende = Anfangsbestand + Integral.''',
     """I = integrate(t**2 - 1, (t, 0, x))
display(I)
display(diff(I, x))
r = 20 - 2*t
display(integrate(r, (t, 0, 5)))
100 + integrate(r, (t, 0, 5))""")

t('Gib die Integralfunktion I₀(x) = ∫₀ˣ (2t + 3) dt aus und prüfe, dass I₀(0) = 0.',
  body='I = integrate(2*t + 3, (t, 0, x))\ndisplay(I)\nI.subs(x, 0)')
t('Gib die Integralfunktion I₁(x) = ∫₁ˣ 3t² dt aus.', body='integrate(3*t**2, (t, 1, x))')
t('Gib die Integralfunktion I₀(x) = ∫₀ˣ cos(t) dt aus und ihre Ableitung.', body='I = integrate(cos(t), (t, 0, x))\ndisplay(I)\ndiff(I, x)')
t('Bestimme die Nullstellen der Integralfunktion I₀(x) = ∫₀ˣ (t² − 4) dt.', body='solve(integrate(t**2 - 4, (t, 0, x)), x)')
t('''**Wassertank:** In einen Tank mit 200 Litern fließt Wasser mit der Rate r(t) = 30 − 3t (Liter pro Minute, t in Minuten). Wie viel Wasser fließt in den ersten
10 Minuten zu? Wie viel ist dann im Tank?''',
  body='r = 30 - 3*t\nzu = integrate(r, (t, 0, 10))\ndisplay(zu)\n200 + zu')
t('''Wie die vorige Aufgabe: Ab t = 10 ist die Rate negativ (Wasser fließt ab). Gib die Bestandsfunktion B(x) = 200 + ∫₀ˣ r(t) dt aus und den Zeitpunkt, zu dem der Tank leer ist.''',
  given="xp = symbols('xp', positive=True)",
  body='r = 30 - 3*t\nB = 200 + integrate(r, (t, 0, xp))\ndisplay(expand(B))\nsolve(B, xp)')
t('''**Fahrt:** Ein Auto bremst mit der Geschwindigkeit v(t) = 20 − 4t (in m/s). Wann steht es? Welche Strecke legt es bis dahin zurück?''',
  body='v = 20 - 4*t\nts = solve(v, t)[0]\ndisplay(ts)\nintegrate(v, (t, 0, ts))')
t('''**Bevölkerung:** Eine Stadt wächst mit der Rate w(t) = 500 · e^(0,02t) Einwohner pro Jahr (0,02 als `Rational`). Um wie viele Einwohner wächst sie
in den ersten 10 Jahren (genau und gerundet auf eine ganze Zahl mit `round(N(...))`)?''',
  body='w = 500 * exp(Rational(2, 100) * t)\nzuwachs = integrate(w, (t, 0, 10))\ndisplay(zuwachs)\nround(N(zuwachs))')

# ---------------------------------------------------------------- 6
sec('Mittelwert einer Funktion')
expl('''#### m = 1/(b − a) · ∫ₐᵇ f(x) dx

Der **Mittelwert** einer Funktion auf [a, b] ist die Höhe des Rechtecks über [a, b], das denselben (orientierten) Flächeninhalt hat wie die Fläche unter dem Graphen.''',
     """f = x**2
m = integrate(f, (x, 0, 3)) / 3
display(m)
plot(f, m, (x, 0, 3));""")

t('Berechne den Mittelwert von f(x) = x³ auf [0, 2].', body='integrate(x**3, (x, 0, 2)) / 2')
t('Berechne den Mittelwert von f(x) = sin(x) auf [0, π] genau und mit 4 Ziffern.', body='m = integrate(sin(x), (x, 0, pi)) / pi\ndisplay(m)\nN(m, 4)')
t('''**Temperatur:** Die Temperatur an einem Tag ist T(t) = 6 · sin(π/12 · (t − 9)) + 14 (°C, t in Stunden). Berechne die mittlere Temperatur zwischen 6 und 18 Uhr (4 Ziffern).''',
  body='T = 6 * sin(pi / 12 * (t - 9)) + 14\nN(integrate(T, (t, 6, 18)) / 12, 4)')
t('''An welcher Stelle in [0, 3] nimmt f(x) = x² seinen Mittelwert auf [0, 3] an?''',
  body='m = integrate(x**2, (x, 0, 3)) / 3\n[w for w in solve(Eq(x**2, m), x) if 0 <= w <= 3]')

# ---------------------------------------------------------------- 7
sec('Rotationskörper (Leistungsfach)')
expl('''#### V = π · ∫ₐᵇ f(x)² dx

Dreht sich der Graph von f über [a, b] um die x-Achse, entsteht ein **Rotationskörper**. Sein Volumen ist V = π · ∫ₐᵇ f(x)² dx
(viele dünne Zylinderscheiben mit Radius f(x)).''',
     """f = sqrt(x)
V = pi * integrate(f**2, (x, 0, 4))
display(V)
N(V, 4)""")

t('''Ein Kegel entsteht, wenn f(x) = x/2 über [0, 6] um die x-Achse rotiert. Berechne das Volumen und vergleiche mit der Kegelformel V = π r² h / 3.''',
  body='V = pi * integrate((x / 2)**2, (x, 0, 6))\ndisplay(V)\npi * 3**2 * 6 / 3')
t('''Leite die Kugelformel her: Der Halbkreis f(x) = √(r² − x²) rotiert über [−r, r]. Berechne das Volumen allgemein.''',
  given="r = symbols('r', positive=True)",
  body='pi * integrate(sqrt(r**2 - x**2)**2, (x, -r, r))')
t('''Der Graph von f(x) = eˣ rotiert über [0, 1] um die x-Achse. Berechne das Volumen genau und mit 4 Ziffern.''',
  body='V = pi * integrate(exp(x)**2, (x, 0, 1))\ndisplay(V)\nN(V, 4)')
t('''Eine **Vase** hat das Profil f(x) = 0,1x² − x + 4 (x und f in cm, 0 ≤ x ≤ 10, Zahlen als `Rational`). Berechne das Volumen in cm³ (4 Ziffern) und in Litern.''',
  body='f = Rational(1, 10) * x**2 - x + 4\nV = pi * integrate(f**2, (x, 0, 10))\ndisplay(N(V, 4))\nN(V / 1000, 4)')
t('''Das Flächenstück zwischen f(x) = √x und g(x) = x/2 (zwischen ihren Schnittstellen 0 und 4) rotiert um die x-Achse. Berechne das Volumen (außen minus innen).''',
  body='pi * integrate(sqrt(x)**2 - (x / 2)**2, (x, 0, 4))')
t('''Bis zu welcher Höhe h muss die Vase f(x) = √x (Rotation um die x-Achse, 0 ≤ x ≤ h) gefüllt werden, damit sie 50 Volumeneinheiten enthält? (genau und 4 Ziffern)''',
  given="h = symbols('h', positive=True)",
  body='V = pi * integrate(x, (x, 0, h))\nl = solve(Eq(V, 50), h)\ndisplay(l)\nN(l[0], 4)')

# ---------------------------------------------------------------- 8
sec('Uneigentliche Integrale (Leistungsfach)')
expl('''#### Unbegrenzte Flächen

Auch eine unendlich lange Fläche kann einen endlichen Inhalt haben. Man rechnet ∫₁^z f(x) dx und lässt z → ∞ gehen.
Ist der Grenzwert eine Zahl, heißt das **uneigentliche Integral** konvergent. sympy macht das direkt mit der Grenze `oo`.''',
     """z = symbols('z', positive=True)
I = integrate(1 / x**2, (x, 1, z))
display(I)
display(limit(I, z, oo))
display(integrate(1 / x**2, (x, 1, oo)))
integrate(1 / x, (x, 1, oo))""")

t('Berechne ∫₀^∞ e⁻ˣ dx.', body='integrate(exp(-x), (x, 0, oo))')
t('Berechne ∫₁^∞ 1/x³ dx.', body='integrate(1 / x**3, (x, 1, oo))')
t('Berechne ∫₁^∞ 1/√x dx.', body='integrate(1 / sqrt(x), (x, 1, oo))')
t('Berechne ∫₀^∞ x · e⁻ˣ dx.', body='integrate(x * exp(-x), (x, 0, oo))')
t('''Berechne ∫₁^z 1/x³ dx in Abhängigkeit von z und dann den Grenzwert für z → ∞ (wie im Beispiel).''',
  given="z = symbols('z', positive=True)", body='I = integrate(1 / x**3, (x, 1, z))\ndisplay(I)\nlimit(I, z, oo)')
t('''Die Fläche unter f(x) = 1/x über [1, ∞) ist unendlich groß. Rotiert sie aber um die x-Achse, ist das Volumen endlich (**Gabriels Horn**). Berechne es.''',
  body='pi * integrate((1 / x)**2, (x, 1, oo))')
t('''Berechne ∫₀¹ 1/√x dx (hier ist die Funktion bei 0 unbeschränkt).''', body='integrate(1 / sqrt(x), (x, 0, 1))')
t('''Für welches k > 0 ist ∫₀^∞ e^(−kx) dx = 4?''', given="k = symbols('k', positive=True)",
  body='solve(Eq(integrate(exp(-k*x), (x, 0, oo)), 4), k)')

# ---------------------------------------------------------------- 9
sec('Gemischte Übungen')
t('''Berechne den Flächeninhalt zwischen f(x) = x · e^(−x) und der Tangente im Ursprung über [0, 2] (Tangente: y = x) genau und mit 4 Ziffern.''',
  body='f = x * exp(-x)\nA = integrate(x - f, (x, 0, 2))\ndisplay(A)\nN(A, 4)')
t('''Eine Parabel f(x) = a(x² − 9) mit a < 0 soll mit der x-Achse den Flächeninhalt 72 einschließen. Bestimme a.''',
  body='f = a * (x**2 - 9)\nsolve(Eq(integrate(f, (x, -3, 3)), 72), a)')
t('''**Regen:** Die Regenmenge fällt mit der Rate r(t) = 2 · t · e^(−0,5t) (mm pro Stunde, t in Stunden; 0,5 als `Rational`). Wie viel Regen fällt in den ersten 6 Stunden
(4 Ziffern), und wie viel insgesamt (t → ∞)?''',
  body='r = 2 * t * exp(-Rational(1, 2) * t)\ndisplay(N(integrate(r, (t, 0, 6)), 4))\nintegrate(r, (t, 0, oo))')
t('''Bestimme die Stammfunktion von f(x) = sin(x) + 2x, deren Graph durch (0 | 3) geht, und gib ihren Wert an der Stelle π aus.''',
  given="C = symbols('C')",
  body='F = integrate(sin(x) + 2*x, x) + C\nF = F.subs(C, solve(Eq(F.subs(x, 0), 3), C)[0])\ndisplay(F)\nF.subs(x, pi)')
t('''Zeichne f(x) = x³ − 3x und die Integralfunktion I₀(x) = ∫₀ˣ f(t) dt für −2,5 ≤ x ≤ 2,5 in ein Diagramm (mit Legende).''',
  body='I = integrate(t**3 - 3*t, (t, 0, x))\nplot(x**3 - 3*x, I, (x, -2.5, 2.5), legend=True);')

generate('sympy_integrale', 'Integralrechnung: Stammfunktionen, Flächen, Rekonstruktion, Rotationskörper', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
