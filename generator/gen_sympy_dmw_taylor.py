# Erzeugt ../content/sympy_dmw_taylor.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_dmw_taylor.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_dmw_taylor.py
#
# Wahlfach Digitale Mathematische Werkzeuge (BW 2016, Klassen 11/12), 3.1.4 Taylorentwicklung:
# lineare Approximation an beliebiger Stelle, Verbesserung durch Taylorpolynome höheren Grades, Konstruktionsprinzip an der Stelle 0
# (gleiche Ableitungen → Koeffizienten f⁽ᵏ⁾(0)/k!), Entwicklung um x = a als Verschiebung, Taylorreihen von ganzrationalen
# Funktionen, eˣ und sin(x), Gegenbeispiel f(x) = e^(−1/x) für x > 0, f(x) = 0 für x ≤ 0 (Taylorreihe an 0 stellt f nicht dar).
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = ("from sympy import *\ninit_printing()\nimport matplotlib.pyplot as plt\nx, h = symbols('x h', real=True)\n"
         "k = symbols('k', integer=True, nonnegative=True)")

INTRO = '''Dieses Notebook gehört zum Wahlfach **Digitale Mathematische Werkzeuge**. Taschenrechner und Computer berechnen Werte wie e^0,3 oder sin(0,5)
mit **Polynomen**, denn Polynome brauchen nur Addition und Multiplikation. Die besten Polynome dafür sind die **Taylorpolynome**:
Sie stimmen an einer Stelle mit der Funktion im Funktionswert und in möglichst vielen Ableitungen überein.

Du beginnst mit der Tangente (lineare Näherung), baust dann Taylorpolynome höheren Grades selbst zusammen, verschiebst die Entwicklungsstelle
und untersuchst unendliche **Taylorreihen**. Am Ende steht ein überraschendes Beispiel: eine Funktion, deren Taylorreihe sie nicht darstellt.

Vorausgesetzt werden die Notebooks *Ableitungsregeln* und *Folgen und Reihen*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy und matplotlib, schaltet die Formel-Ausgabe ein
und legt die reellen Variablen `x`, `h` und die natürliche Zahl `k` an.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Lineare Approximation')
expl('''#### Die Tangente als beste Gerade

In der Nähe einer Stelle a ersetzt man f durch die Tangente: f(x) ≈ L(x) = f(a) + f'(a)·(x − a).
L stimmt in der Stelle a mit f im Funktionswert und in der Steigung überein. Der Fehler f(x) − L(x) wird klein, wenn x nahe bei a liegt.''',
     """f = sqrt(x)
a = 4
L = f.subs(x, a) + diff(f, x).subs(x, a) * (x - a)
display(expand(L))
display(L.subs(x, Rational(41, 10)), N(sqrt(Rational(41, 10)), 8))
[N(f.subs(x, a + d) - L.subs(x, a + d), 3) for d in [1, Rational(1, 10), Rational(1, 100)]]""")

LIN = "def linear(f, a):\n    return f.subs(x, a) + diff(f, x).subs(x, a) * (x - a)\n"
t('''Schreibe eine Funktion `linear(f, a)`, die die lineare Approximation zurückgibt. Teste mit f(x) = eˣ an der Stelle 0 und mit f(x) = ln(x) an der Stelle 1.''',
  body=LIN + "\ndisplay(linear(exp(x), 0))\nlinear(log(x), 1)")
t('Nähere ∛(8,3) mit der linearen Approximation von ∛x an der Stelle 8 an (genau und mit 6 Ziffern) und vergleiche mit dem genauen Wert (6 Ziffern).', LIN,
  "L = linear(x**Rational(1, 3), 8)\nw = L.subs(x, Rational(83, 10))\ndisplay(w, N(w, 6))\nN(Rational(83, 10)**Rational(1, 3), 6)")
t('''Für kleine x ist sin(x) ≈ x („Kleinwinkelnäherung“). Berechne den relativen Fehler (sin x − x)/sin x für x = 0,1, 0,2 und 0,5 mit 3 Ziffern.''',
  body="[N((sin(w) - w) / sin(w), 3) for w in [Rational(1, 10), Rational(2, 10), Rational(5, 10)]]")
t('''Nähere (1 + x)^n für kleine x linear an (Stelle 0, n als Symbol). Berechne damit 1,02¹⁰ näherungsweise und genau (4 Ziffern).''', LIN + "n = symbols('n')",
  "L = linear((1 + x)**n, 0)\ndisplay(L)\ndisplay(L.subs({n: 10, x: Rational(2, 100)}))\nN(Rational(102, 100)**10, 4)")
t('''Wie halbiert sich der Fehler? Berechne für f(x) = eˣ an der Stelle 0 den Fehler f(h) − L(h) für h = 0,2, 0,1, 0,05 (4 Ziffern). Der Fehler wird etwa geviertelt, wenn h halbiert wird.''', LIN,
  "L = linear(exp(x), 0)\n[N(exp(w) - L.subs(x, w), 4) for w in [Rational(2, 10), Rational(1, 10), Rational(5, 100)]]")

# ---------------------------------------------------------------- 2
sec('Taylorpolynome an der Stelle 0')
expl('''#### Das Konstruktionsprinzip

Gesucht ist das Polynom T(x) = a₀ + a₁x + a₂x² + ... + aₙxⁿ, das an der Stelle 0 mit f in den Ableitungen 0 bis n übereinstimmt:
T(0) = f(0), T'(0) = f'(0), ..., T⁽ⁿ⁾(0) = f⁽ⁿ⁾(0). Das sind n + 1 Gleichungen für n + 1 Koeffizienten. Allgemein ergibt sich

aₖ = f⁽ᵏ⁾(0) / k!,  also T(x) = Σₖ₌₀ⁿ f⁽ᵏ⁾(0)/k! · xᵏ

sympy kann das direkt: `series(f, x, 0, n + 1)` gibt die Entwicklung bis xⁿ und den Rest O(xⁿ⁺¹); `.removeO()` entfernt den Rest.''',
     """a0, a1, a2, a3 = symbols('a0:4')
T = a0 + a1*x + a2*x**2 + a3*x**3
f = cos(x)
gleichungen = [Eq(diff(T, x, j).subs(x, 0), diff(f, x, j).subs(x, 0)) for j in range(4)]
display(gleichungen)
display(solve(gleichungen, [a0, a1, a2, a3]))
display(sum([diff(f, x, j).subs(x, 0) / factorial(j) * x**j for j in range(4)]))
series(f, x, 0, 4)""")

TAY = "def taylor(f, n, a=0):\n    return sum([diff(f, x, j).subs(x, a) / factorial(j) * (x - a)**j for j in range(n + 1)])\n"
t('''Bestimme das Taylorpolynom 3. Grades von eˣ an der Stelle 0 mit dem Ansatz a₀ + a₁x + a₂x² + a₃x³ und den vier Bedingungen (wie im Beispiel).''',
  given="a0, a1, a2, a3 = symbols('a0:4')",
  body="T = a0 + a1*x + a2*x**2 + a3*x**3\nl = solve([Eq(diff(T, x, j).subs(x, 0), diff(exp(x), x, j).subs(x, 0)) for j in range(4)], [a0, a1, a2, a3])\nT.subs(l)")
t('''Schreibe eine Funktion `taylor(f, n, a=0)`, die das Taylorpolynom n-ten Grades mit der Formel Σ f⁽ʲ⁾(a)/j! · (x − a)ʲ berechnet. Teste mit sin(x), n = 7.''',
  body=TAY + "\ntaylor(sin(x), 7)")
t('Gib die Taylorpolynome von eˣ vom Grad 0 bis 4 als Liste aus.', TAY, "[taylor(exp(x), m) for m in range(5)]")
t('Gib das Taylorpolynom 6. Grades von cos(x) mit `series` aus.', body="series(cos(x), x, 0, 7).removeO()")
t('Gib das Taylorpolynom 4. Grades von 1/(1 − x) und von ln(1 + x) aus.', TAY, "display(taylor(1 / (1 - x), 4))\ntaylor(log(1 + x), 4)")
t('''Zeichne eˣ und die Taylorpolynome vom Grad 1, 2 und 3 für −3 ≤ x ≤ 2 (y von −2 bis 7, mit Legende).''', TAY,
  "plot(exp(x), *[taylor(exp(x), m) for m in [1, 2, 3]], (x, -3, 2), ylim=(-2, 7), legend=True);")
t('''Wie gut nähern die Taylorpolynome von eˣ die Zahl e = e¹ an? Gib für die Grade 2, 4, 6, 8, 10 den Fehler e − Tₙ(1) mit 3 Ziffern aus.''', TAY,
  "[N(E - taylor(exp(x), m).subs(x, 1), 3) for m in [2, 4, 6, 8, 10]]")
t('''Welchen Grad braucht das Taylorpolynom von sin(x), damit der Fehler bei x = 1 kleiner als 10⁻⁸ ist? (Schleife über n = 1, 3, 5, ...)''', TAY,
  "n = 1\nwhile Abs(N(sin(1) - taylor(sin(x), n).subs(x, 1), 20)) >= Rational(1, 10**8):\n    n += 2\nn")
predict("""display(series(x**2 + 3*x + 1, x, 0, 5))
display(series(exp(2*x), x, 0, 3).removeO())
series(sin(x), x, 0, 2).removeO()""")

# ---------------------------------------------------------------- 3
sec('Entwicklung an einer beliebigen Stelle')
expl('''#### Taylorpolynome um x = a

An der Stelle a lautet das Taylorpolynom T(x) = Σ f⁽ᵏ⁾(a)/k! · (x − a)ᵏ. Das ist dasselbe Konstruktionsprinzip, nur **verschoben**:
Setzt man x = a + h, wird daraus ein Taylorpolynom in h an der Stelle 0, nämlich das von g(h) = f(a + h).

`series(f, x, a, n + 1)` entwickelt an der Stelle a.''',
     """f = log(x)
display(series(f, x, 1, 4).removeO())
g = f.subs(x, 1 + h)
display(series(g, h, 0, 4).removeO())
plot(f, series(f, x, 1, 4).removeO(), (x, 0.1, 3), ylim=(-3, 2), legend=True);""")

t('Gib das Taylorpolynom 3. Grades von eˣ an der Stelle 1 aus (mit der Funktion `taylor` von oben).', TAY, "taylor(exp(x), 3, 1)")
t('Gib das Taylorpolynom 2. Grades von √x an der Stelle 4 aus und berechne damit √4,1 (8 Ziffern).', TAY,
  "T = taylor(sqrt(x), 2, 4)\ndisplay(T)\nN(T.subs(x, Rational(41, 10)), 8)")
t('''Prüfe die Verschiebung: Das Taylorpolynom von sin(x) an der Stelle π/2 (Grad 4) ist das von cos(h) an der Stelle 0, wenn man h = x − π/2 setzt.
Berechne beide und vergleiche (Differenz vereinfacht).''', TAY,
  "T1 = taylor(sin(x), 4, pi/2)\nT2 = taylor(cos(x), 4).subs(x, x - pi/2)\ndisplay(T1)\nsimplify(T1 - T2)")
t('''Ein **Polynom** ist seine eigene Taylorreihe. Entwickle f(x) = x³ − 2x + 1 an der Stelle 1 (Grad 3) und multipliziere das Ergebnis aus.''', TAY,
  "T = taylor(x**3 - 2*x + 1, 3, 1)\ndisplay(T)\nexpand(T)")
t('''Zeichne ln(x) und seine Taylorpolynome vom Grad 1, 3 und 5 an der Stelle 1 für 0,1 ≤ x ≤ 3 (y von −3 bis 2, mit Legende).''', TAY,
  "plot(log(x), *[taylor(log(x), m, 1) for m in [1, 3, 5]], (x, 0.1, 3), ylim=(-3, 2), legend=True);")

# ---------------------------------------------------------------- 4
sec('Taylorreihen')
expl('''#### Unendlich viele Glieder

Lässt man den Grad gegen unendlich gehen, erhält man die **Taylorreihe** Σₖ₌₀^∞ f⁽ᵏ⁾(a)/k! · (x − a)ᵏ. Für eˣ, sin(x) und cos(x) konvergiert sie
für **alle** x gegen die Funktion:

eˣ = Σ xᵏ/k!,  sin(x) = Σ (−1)ᵏ x²ᵏ⁺¹/(2k + 1)!,  cos(x) = Σ (−1)ᵏ x²ᵏ/(2k)!

Andere Reihen konvergieren nur in einem Bereich: 1/(1 − x) = Σ xᵏ (geometrische Reihe) nur für |x| < 1.''',
     """display(summation(x**k / factorial(k), (k, 0, oo)))
display(summation((-1)**k * x**(2*k + 1) / factorial(2*k + 1), (k, 0, oo)))
summation(x**k, (k, 0, oo))""")

t('Berechne die Reihe Σₖ₌₀^∞ (−1)ᵏ x²ᵏ/(2k)! mit `summation`.', body="summation((-1)**k * x**(2*k) / factorial(2*k), (k, 0, oo))")
t('Berechne mit der Reihe von eˣ die Summe Σₖ₌₀^∞ 2ᵏ/k! und Σₖ₌₀^∞ (−1)ᵏ/k!.', body="display(summation(2**k / factorial(k), (k, 0, oo)))\nsummation((-1)**k / factorial(k), (k, 0, oo))")
t('''Die Taylorreihe von ln(1 + x) ist Σₖ₌₁^∞ (−1)ᵏ⁺¹ xᵏ/k. Berechne die Partialsummen mit 20 und 40 Gliedern für x = 1/2 und x = 2 (je 4 Ziffern). Für x = 2 konvergiert
die Reihe nicht.''',
  body="def s(w, m):\n    return N(sum([(-1)**(j + 1) * Rational(w)**j / j for j in range(1, m + 1)]), 4)\n\ndisplay([s(Rational(1, 2), 20), s(Rational(1, 2), 40), N(log(Rational(3, 2)), 4)])\n[s(2, 20), s(2, 40)]")
t('''Zeichne 1/(1 − x) und die Taylorpolynome vom Grad 2, 5, 10 für −1,5 ≤ x ≤ 1 (y von −2 bis 6). Außerhalb von |x| < 1 entfernen sich die Polynome.''',
  body="plot(1 / (1 - x), *[series(1 / (1 - x), x, 0, m + 1).removeO() for m in [2, 5, 10]], (x, -1.5, 0.9), ylim=(-2, 6), legend=True);")
t('''**π berechnen:** Die Taylorreihe von arctan(x) ist Σ (−1)ᵏ x²ᵏ⁺¹/(2k + 1). Mit arctan(1) = π/4 ist π = 4 · (1 − 1/3 + 1/5 − ...). Berechne die Näherung mit 100 und mit 1000 Gliedern
(je 6 Ziffern). Sie konvergiert sehr langsam.''',
  body="def pi_naeherung(m):\n    return N(4 * sum([Rational((-1)**j, 2*j + 1) for j in range(m)]), 6)\n\n[pi_naeherung(100), pi_naeherung(1000), N(pi, 6)]")
t('''Schneller geht es mit der **Formel von Machin**: π/4 = 4·arctan(1/5) − arctan(1/239). Berechne π mit je 10 Gliedern der arctan-Reihe (15 Ziffern).''',
  body="def arctan_reihe(w, m):\n    return sum([(-1)**j * w**(2*j + 1) / (2*j + 1) for j in range(m)])\n\nN(4 * (4 * arctan_reihe(Rational(1, 5), 10) - arctan_reihe(Rational(1, 239), 10)), 15)")

# ---------------------------------------------------------------- 5
sec('Ein Gegenbeispiel')
expl('''#### Eine Funktion, deren Taylorreihe sie nicht darstellt

Die Funktion f(x) = e^(−1/x) für x > 0 und f(x) = 0 für x ≤ 0 ist überall beliebig oft differenzierbar. An der Stelle 0 sind **alle** Ableitungen 0:
Die Grenzwerte der Ableitungen von rechts sind 0, und links ist f konstant 0. Ihre Taylorreihe an der Stelle 0 ist deshalb die **Nullreihe** 0 + 0·x + 0·x² + ...
Sie konvergiert zwar (gegen 0), aber für x > 0 nicht gegen f(x), denn dort ist f(x) > 0. Die Taylorreihe stellt f also nicht dar.

`Piecewise((term1, bedingung1), (term2, True))` definiert eine stückweise Funktion.''',
     """f = Piecewise((exp(-1/x), x > 0), (0, True))
display(f)
display([limit(diff(exp(-1/x), x, j), x, 0, '+') for j in range(5)])
display(f.subs(x, Rational(1, 2)), N(f.subs(x, Rational(1, 2)), 4))
plot(f, (x, -1, 3));""")

t('Gib die ersten drei Ableitungen von e^(−1/x) aus (mit `simplify`).', body="[simplify(diff(exp(-1/x), x, j)) for j in range(1, 4)]")
t('Berechne die Grenzwerte der Ableitungen 1 bis 6 von e^(−1/x) für x → 0 von rechts (Liste).', body="[limit(diff(exp(-1/x), x, j), x, 0, '+') for j in range(1, 7)]")
t('''Gib f(x) und den Wert der (Null-)Taylorreihe an den Stellen 0,1, 0,5, 1, 2 mit 4 Ziffern als Liste von Paaren aus.''',
  body="f = Piecewise((exp(-1/x), x > 0), (0, True))\n[(N(f.subs(x, w), 4), 0) for w in [Rational(1, 10), Rational(1, 2), 1, 2]]")
t('''Zeichne den rechten Teil e^(−1/x) für 0,02 ≤ x ≤ 1 (so sieht man, wie flach f an die x-Achse anschließt) und gib f(0,1) und f(0,05) mit 3 Ziffern aus.''',
  body="plot(exp(-1/x), (x, 0.02, 1));\n[N(exp(-1/w), 3) for w in [Rational(1, 10), Rational(5, 100)]]")

# ---------------------------------------------------------------- 6
sec('Anwendungen')
t('''**Pendel:** Für kleine Auslenkungen φ ersetzt man sin(φ) durch φ. Bis zu welchem Winkel (in Grad, ganze Zahl) ist der relative Fehler (φ − sin φ)/sin φ kleiner als 1 %?
(Schleife über ganze Grad)''',
  body="g = 1\nwhile N((g*pi/180 - sin(g*pi/180)) / sin(g*pi/180)) < Rational(1, 100):\n    g += 1\ng - 1")
t('''**Relativitätstheorie:** Die Energie ist E = m c² / √(1 − v²/c²). Entwickle 1/√(1 − u) an der Stelle u = 0 bis zum Grad 2 und setze u = v²/c² ein (ausmultiplizieren).
Das zweite Glied ist die bekannte kinetische Energie ½ m v².''',
  given="m, c, v, uu = symbols('m c v u', positive=True)",
  body="T = series(1 / sqrt(1 - uu), uu, 0, 3).removeO()\ndisplay(T)\nexpand(m * c**2 * T.subs(uu, v**2 / c**2))")
t('''Berechne e^0,3 mit dem Taylorpolynom 5. Grades von eˣ (8 Ziffern) und den Fehler (3 Ziffern).''', TAY,
  "T = taylor(exp(x), 5)\nw = T.subs(x, Rational(3, 10))\ndisplay(N(w, 8))\nN(exp(Rational(3, 10)) - w, 3)")
t('''Berechne das bestimmte Integral ∫₀¹ e^(−x²) dx (keine elementare Stammfunktion!) näherungsweise, indem du das Taylorpolynom 10. Grades von e^(−x²) integrierst (8 Ziffern).
Vergleiche mit `N(Integral(...))`.''',
  body="T = series(exp(-x**2), x, 0, 11).removeO()\ndisplay(N(integrate(T, (x, 0, 1)), 8))\nN(Integral(exp(-x**2), (x, 0, 1)), 8)")

generate('sympy_dmw_taylor', 'DMW: Taylorpolynome und Taylorreihen', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
