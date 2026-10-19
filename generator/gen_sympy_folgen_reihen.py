# Erzeugt ../content/sympy_folgen_reihen.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_folgen_reihen.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_folgen_reihen.py
#
# Vertiefungskurs Mathematik BW: Folgen (explizit, rekursiv, arithmetisch, geometrisch), Monotonie und Beschränktheit,
# Grenzwert und Konvergenz (ε-Definition), Reihen (Partialsummen, geometrische Reihe, harmonische Reihe, Teleskopsummen),
# Taylorpolynome (Zusatz). sympy 1.14: limit mit (-1)**n bricht ab (NotImplementedError) → alternierende Folgen über |a_n| behandeln.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = ("from sympy import *\ninit_printing()\nimport matplotlib.pyplot as plt\n"
         "n, k = symbols('n k', integer=True, positive=True)\nx = symbols('x', real=True)\nf = Function('f')")

INTRO = '''In diesem Notebook (Vertiefungskurs) geht es um **Folgen und Reihen**: explizite und rekursive Folgen, Monotonie und Beschränktheit,
**Grenzwerte** und die genaue Definition der **Konvergenz**, unendliche **Reihen** wie die geometrische und die harmonische Reihe
und (als Zusatz) **Taylorpolynome**, mit denen man Funktionen durch Polynome annähert.

Vorausgesetzt werden die Notebooks *Logik und Beweise* (Summen, Induktion) und *Ableitungsregeln* (`limit`).

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy und matplotlib, schaltet die Formel-Ausgabe ein
und legt die natürlichen Zahlen `n`, `k`, die reelle Variable `x` und das Funktionssymbol `f` (für rekursive Folgen) an.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Folgen')
expl('''#### Explizite Folgen

Eine **Folge** (aₙ) ordnet jeder natürlichen Zahl n eine Zahl aₙ zu, z. B. aₙ = 1/n: 1, 1/2, 1/3, ...
Bei einer **expliziten** Folge steht aₙ als Term in n da.

- `a = sequence(term, (n, 1, oo))` legt die Folge an, `a[:5]` gibt die ersten 5 Glieder.
- Ebenso geht `[term.subs(n, i) for i in range(1, 6)]`.
- **Arithmetische Folge:** konstante Differenz d, aₙ = a₁ + (n − 1)·d. **Geometrische Folge:** konstanter Quotient q, aₙ = a₁ · qⁿ⁻¹.''',
     """a = sequence(1 / n, (n, 1, oo))
display(a)
display(a[:5])
an = (2*n - 1) / (n + 1)
werte = [an.subs(n, i) for i in range(1, 11)]
display(werte)
plt.plot(range(1, 11), [N(w) for w in werte], 'o')
plt.show()""")

t('Gib die ersten 6 Glieder der Folge aₙ = n²/(n + 1) aus.', body='sequence(n**2 / (n + 1), (n, 1, oo))[:6]')
t('Gib die ersten 6 Glieder der Folge aₙ = (−1)ⁿ / n aus.', body='sequence((-1)**n / n, (n, 1, oo))[:6]')
t('Gib die ersten 6 Glieder der arithmetischen Folge mit a₁ = 7 und d = −3 aus und das 100. Glied.',
  body='an = 7 + (n - 1) * (-3)\ndisplay([an.subs(n, i) for i in range(1, 7)])\nan.subs(n, 100)')
t('Gib die ersten 6 Glieder der geometrischen Folge mit a₁ = 3 und q = 1/2 aus.', body='an = 3 * Rational(1, 2)**(n - 1)\n[an.subs(n, i) for i in range(1, 7)]')
t('''Eine geometrische Folge hat a₁ = 2 und a₄ = 54. Bestimme q (reell) und den expliziten Term.''',
  given="q = symbols('q', real=True)", body='qs = solve(Eq(2 * q**3, 54), q)\ndisplay(qs)\n2 * qs[0]**(n - 1)')
t('''Ab welchem n ist das Glied der Folge aₙ = 1,05ⁿ größer als 100? (Schleife)''',
  body='m = 1\nwhile Rational(105, 100)**m <= 100:\n    m += 1\nm')
t('''Zeichne die ersten 20 Glieder der Folge aₙ = (−1)ⁿ / n als Punkte.''',
  body="an = (-1)**n / n\nplt.plot(range(1, 21), [N(an.subs(n, i)) for i in range(1, 21)], 'o')\nplt.show()")
predict("""a = sequence(2**n, (n, 1, oo))
display(a[:4])
display(sequence(3*n - 1, (n, 0, oo))[:4])
sequence(Rational(1, 2)**n, (n, 0, oo))[:3]""")

# ---------------------------------------------------------------- 2
sec('Rekursive Folgen')
expl('''#### Jedes Glied aus dem vorigen

Bei einer **rekursiven** Folge ist ein Anfangswert gegeben und eine Regel, wie man aus aₙ das nächste Glied aₙ₊₁ berechnet,
z. B. a₁ = 3, aₙ₊₁ = 2·aₙ. Die Glieder berechnet man mit einer Schleife.

`rsolve(gleichung, f(n), {f(1): 3})` sucht einen **expliziten** Term (mit dem Funktionssymbol f): Die Rekursion wird als
Ausdruck geschrieben, der null sein soll, z. B. f(n + 1) − 2·f(n).''',
     """folge = [3]
for i in range(5):
    folge.append(2 * folge[-1])
display(folge)
display(rsolve(f(n + 1) - 2 * f(n), f(n), {f(1): 3}))
rsolve(f(n + 1) - f(n) - 3, f(n), {f(0): 2})""")

t('Berechne die ersten 8 Glieder der Folge a₁ = 1, aₙ₊₁ = 3·aₙ − 1 mit einer Schleife.',
  body='folge = [1]\nfor i in range(7):\n    folge.append(3 * folge[-1] - 1)\nfolge')
t('Bestimme mit `rsolve` den expliziten Term der Folge aus der vorigen Aufgabe und prüfe ihn für n = 1 bis 5.',
  body='an = rsolve(f(n + 1) - 3 * f(n) + 1, f(n), {f(1): 1})\ndisplay(an)\n[an.subs(n, i) for i in range(1, 6)]')
t('''Die **Fibonacci-Folge**: f₀ = 0, f₁ = 1, fₙ₊₂ = fₙ₊₁ + fₙ. Berechne die ersten 15 Glieder mit einer Schleife und vergleiche mit `fibonacci(i)`.''',
  body='folge = [0, 1]\nfor i in range(13):\n    folge.append(folge[-1] + folge[-2])\ndisplay(folge)\nfolge == [fibonacci(i) for i in range(15)]')
t('Bestimme mit `rsolve` den expliziten Term der Fibonacci-Folge (Formel von Binet).',
  body='rsolve(f(n + 2) - f(n + 1) - f(n), f(n), {f(0): 0, f(1): 1})')
t('''Die Quotienten fₙ₊₁/fₙ aufeinanderfolgender Fibonacci-Zahlen nähern sich dem **goldenen Schnitt**. Gib die Quotienten für n = 10, 20, 30 mit 10 Ziffern aus
und den goldenen Schnitt (1 + √5)/2 mit 10 Ziffern.''',
  body='display([N(Rational(fibonacci(i + 1), fibonacci(i)), 10) for i in [10, 20, 30]])\nN((1 + sqrt(5)) / 2, 10)')
t('''**Medikament:** Jeden Tag werden 3 mg eingenommen, über Nacht werden 50 % abgebaut: a₀ = 0, aₙ₊₁ = 0,5·aₙ + 3. Gib den expliziten Term (`rsolve`) und den Grenzwert für n → ∞ aus.''',
  body='an = rsolve(f(n + 1) - Rational(1, 2) * f(n) - 3, f(n), {f(0): 0})\ndisplay(an)\nlimit(an, n, oo)')
t('''**Heron-Verfahren:** Die Folge x₁ = 1, xₙ₊₁ = (xₙ + 2/xₙ)/2 nähert √2 an. Berechne x₁ bis x₅ genau (als Brüche) und x₅ − √2 mit 3 Ziffern.''',
  body='folge = [Integer(1)]\nfor i in range(4):\n    folge.append((folge[-1] + 2 / folge[-1]) / 2)\ndisplay(folge)\nN(folge[-1] - sqrt(2), 3)')
predict("""folge = [1]
for i in range(4):
    folge.append(folge[-1] + 2)
folge""")

# ---------------------------------------------------------------- 3
sec('Monotonie und Beschränktheit')
expl('''#### Steigt die Folge?

Eine Folge ist **streng monoton steigend**, wenn aₙ₊₁ − aₙ > 0 für alle n, **fallend**, wenn aₙ₊₁ − aₙ < 0. Man berechnet die Differenz
allgemein und vereinfacht sie (`factor`/`simplify`), bis man das Vorzeichen sieht. Bei positiven Gliedern kann man auch den Quotienten
aₙ₊₁/aₙ mit 1 vergleichen.

Eine Folge ist **beschränkt**, wenn es Zahlen S und s gibt mit s ≤ aₙ ≤ S für alle n.''',
     """an = (2*n - 1) / (n + 1)
d = factor(an.subs(n, n + 1) - an)
display(d)
display(d > 0)
display(simplify(an - 2))""")

t('Untersuche die Monotonie von aₙ = (3n + 2)/(n + 1): Gib aₙ₊₁ − aₙ faktorisiert aus.', body='an = (3*n + 2) / (n + 1)\nfactor(an.subs(n, n + 1) - an)')
t('Untersuche die Monotonie von aₙ = n/2ⁿ: Gib den Quotienten aₙ₊₁/aₙ vereinfacht aus und für welche n er kleiner als 1 ist (Liste für n = 1 bis 5).',
  body='an = n / 2**n\nqu = simplify(an.subs(n, n + 1) / an)\ndisplay(qu)\n[qu.subs(n, i) < 1 for i in range(1, 6)]')
t('Zeige, dass aₙ = (3n + 2)/(n + 1) durch 3 nach oben beschränkt ist: Gib 3 − aₙ vereinfacht aus (positiv für alle n).',
  body='simplify(3 - (3*n + 2) / (n + 1))')
t('Untersuche die Monotonie von aₙ = n² − 6n: Gib aₙ₊₁ − aₙ aus und ab welchem n die Folge steigt (`solveset` über `Interval(1, oo)`).',
  body="d = expand((n + 1)**2 - 6*(n + 1) - (n**2 - 6*n))\ndisplay(d)\nnr = symbols('nr', real=True)\nsolveset(d.subs(n, nr) > 0, nr, Interval(1, oo))")
t('''Ist die Folge aₙ = (1 + 1/n)ⁿ monoton steigend? Gib die ersten 6 Glieder mit 5 Ziffern aus.''',
  body='an = (1 + 1/n)**n\n[N(an.subs(n, i), 5) for i in range(1, 7)]')

# ---------------------------------------------------------------- 4
sec('Grenzwert und Konvergenz')
expl('''#### Die ε-Definition

Eine Folge (aₙ) **konvergiert** gegen den Grenzwert g, wenn für **jedes** ε > 0 ab einem Index n₀ alle Glieder im Streifen
g − ε < aₙ < g + ε liegen, also |aₙ − g| < ε für alle n ≥ n₀. Eine Folge ohne Grenzwert heißt **divergent**.

- `limit(an, n, oo)` berechnet den Grenzwert.
- Für ein bestimmtes ε berechnet man n₀: Löse |aₙ − g| < ε nach n (mit einer reellen Variablen `nr`). Ist die Lösung ein Intervall `l`,
  ist `l.inf` seine untere Grenze; `floor(l.inf) + 1` ist dann die kleinste ganze Zahl im Intervall (bei offenem Intervall).

**Wichtig:** `limit` kann Folgen mit (−1)ⁿ in sympy 1.14 nicht berechnen. Dann hilft der Betrag: Geht |aₙ| → 0, geht auch aₙ → 0.''',
     """an = (2*n + 1) / (n + 3)
g = limit(an, n, oo)
display(g)
nr = symbols('nr', positive=True)
abstand = simplify(Abs(an.subs(n, nr) - g))
display(abstand)
display(solveset(abstand < Rational(1, 100), nr, Interval(0, oo)))
limit(1 / n, n, oo)""")

NR = "nr = symbols('nr', positive=True)"
t('Berechne die Grenzwerte von aₙ = (5n² − 1)/(2n² + n) und bₙ = (n + 1)/n².', body='display(limit((5*n**2 - 1) / (2*n**2 + n), n, oo))\nlimit((n + 1) / n**2, n, oo)')
t('Berechne die Grenzwerte von aₙ = √(n + 1) − √n und bₙ = n · (√(n² + 1) − n).',
  body='display(limit(sqrt(n + 1) - sqrt(n), n, oo))\nlimit(n * (sqrt(n**2 + 1) - n), n, oo)')
t('Berechne den Grenzwert der Folge aₙ = (1 + 1/n)ⁿ und von bₙ = (1 + 2/n)ⁿ.', body='display(limit((1 + 1/n)**n, n, oo))\nlimit((1 + 2/n)**n, n, oo)')
t('Berechne die Grenzwerte von aₙ = n/2ⁿ, bₙ = n^(1/n) und cₙ = sin(n)/n.',
  body='display(limit(n / 2**n, n, oo))\ndisplay(limit(n**(1/n), n, oo))\nlimit(sin(n) / n, n, oo)')
t('''Für aₙ = (3n + 2)/(n + 1) mit Grenzwert 3: Ab welchem Index n₀ gilt |aₙ − 3| < 0,001? Gib die Lösungsmenge für nr und das kleinste ganze n₀ aus.''', NR,
  "l = solveset(Abs((3*nr + 2) / (nr + 1) - 3) < Rational(1, 1000), nr, Interval(0, oo))\ndisplay(l)\nfloor(l.inf) + 1")
t('''Für aₙ = 1/n²: Bestimme in Abhängigkeit von ε > 0 die Grenze, ab der 1/n² < ε gilt (löse 1/n² = ε nach nr > 0). Das zeigt: Für jedes ε gibt es ein n₀.
Gib auch die Grenze für ε = 1/10000 aus.''',
  NR + "\neps = symbols('epsilon', positive=True)", 'grenze = solve(Eq(1 / nr**2, eps), nr)[0]\ndisplay(grenze)\ngrenze.subs(eps, Rational(1, 10000))')
t('''Die Folge aₙ = (−1)ⁿ / n: `limit` funktioniert hier nicht. Berechne stattdessen den Grenzwert von |aₙ| = 1/n.''', body='limit(1 / n, n, oo)')
t('''Die Folge aₙ = (−1)ⁿ ist divergent: Sie hat die beiden **Häufungspunkte** −1 und 1. Gib die Grenzwerte der Teilfolgen a₂ₙ und a₂ₙ₋₁ aus (setze 2n bzw. 2n − 1 ein und vereinfache).''',
  body='display(simplify((-1)**(2*n)))\nsimplify((-1)**(2*n - 1))')
t('Gib die Grenzwerte von aₙ = 2ⁿ/n² und bₙ = n!/nⁿ aus.', body='display(limit(2**n / n**2, n, oo))\nlimit(factorial(n) / n**n, n, oo)')
predict("""display(limit(5 + 1/n, n, oo))
display(limit(n**2, n, oo))
display(limit(Rational(1, 2)**n, n, oo))
limit((n**2 + 1) / (n**2 - 1), n, oo)""")

# ---------------------------------------------------------------- 5
sec('Reihen')
expl('''#### Partialsummen und unendliche Summen

Eine **Reihe** ist die Folge der **Partialsummen** sₙ = a₁ + a₂ + ... + aₙ. Konvergiert sₙ, schreibt man den Grenzwert als unendliche Summe Σ aₖ.

- `summation(term, (k, 1, n))` gibt die Partialsumme allgemein, `summation(term, (k, 1, oo))` die unendliche Summe.
- `Sum(term, (k, 1, oo))` schreibt die Summe nur hin; `.doit()` rechnet, `.is_convergent()` prüft die Konvergenz.
- **Geometrische Reihe:** Σₖ₌₀^∞ qᵏ = 1/(1 − q) für |q| < 1.
- **Harmonische Reihe:** Σ 1/k divergiert, obwohl 1/k → 0 geht. Σ 1/k² konvergiert dagegen (gegen π²/6).''',
     """display(summation(Rational(1, 2)**k, (k, 0, n)))
s = Sum(Rational(1, 2)**k, (k, 0, oo))
display(Eq(s, s.doit()))
display(Sum(1/k, (k, 1, oo)).is_convergent(), Sum(1/k**2, (k, 1, oo)).is_convergent())
summation(1/k**2, (k, 1, oo))""")

t('Berechne die Summe der geometrischen Reihe Σₖ₌₀^∞ (2/3)ᵏ und Σₖ₌₁^∞ 3 · (1/4)ᵏ.', body='display(summation(Rational(2, 3)**k, (k, 0, oo)))\nsummation(3 * Rational(1, 4)**k, (k, 1, oo))')
t('Schreibe die periodische Dezimalzahl 0,777... als geometrische Reihe Σₖ₌₁^∞ 7 · (1/10)ᵏ und berechne sie.', body='summation(7 * Rational(1, 10)**k, (k, 1, oo))')
t('''**Teleskopsumme:** Zerlege 1/(k(k + 1)) mit `apart` in Partialbrüche, gib die Partialsumme bis n und die unendliche Summe aus.''',
  body='display(apart(1 / (k * (k + 1)), k))\ndisplay(simplify(summation(1 / (k * (k + 1)), (k, 1, n))))\nsummation(1 / (k * (k + 1)), (k, 1, oo))')
t('Prüfe mit `is_convergent()`, welche der Reihen Σ 1/√k, Σ 1/k³, Σ k/2ᵏ konvergieren (Liste).',
  body='[Sum(t, (k, 1, oo)).is_convergent() for t in [1 / sqrt(k), 1 / k**3, k / 2**k]]')
t('Berechne Σₖ₌₁^∞ k/2ᵏ und Σₖ₌₀^∞ 1/k!.', body='display(summation(k / 2**k, (k, 1, oo)))\nsummation(1 / factorial(k), (k, 0, oo))')
t('''Die harmonische Reihe wächst sehr langsam. Ab welchem n ist die Partialsumme 1 + 1/2 + ... + 1/n größer als 5? (Schleife mit Kommazahlen: `s += 1 / m`)''',
  body='s, m = 0, 0\nwhile s <= 5:\n    m += 1\n    s += 1 / m\nm')
t('''**Achilles und die Schildkröte:** Achilles läuft 10 m/s, die Schildkröte 1 m/s mit 100 m Vorsprung. Bis Achilles den Vorsprung aufgeholt hat, ist die Schildkröte 10 m weiter usw.
Die Zeiten bilden die Reihe 10 + 1 + 0,1 + ... Berechne die Gesamtzeit als geometrische Reihe Σₖ₌₀^∞ 10 · (1/10)ᵏ.''',
  body='summation(10 * Rational(1, 10)**k, (k, 0, oo))')
t('''Gib die alternierende harmonische Reihe 1 − 1/2 + 1/3 − ... als Summe Σ (−1)ᵏ⁺¹/k aus.''', body='summation((-1)**(k + 1) / k, (k, 1, oo))')
t('''Zeichne die ersten 30 Partialsummen von Σ 1/k² und die Gerade y = π²/6.''',
  body="s = [N(summation(1 / k**2, (k, 1, m))) for m in range(1, 31)]\nplt.plot(range(1, 31), s, 'o')\nplt.axhline(N(pi**2 / 6), color='red')\nplt.show()")
predict("""display(summation(1, (k, 1, 10)))
display(summation(k, (k, 1, 10)))
summation(Rational(1, 2)**k, (k, 1, oo))""")

# ---------------------------------------------------------------- 6
sec('Taylorpolynome (Zusatz)')
expl('''#### Funktionen durch Polynome annähern

Das **Taylorpolynom** vom Grad m einer Funktion an der Stelle 0 hat dieselben Ableitungen bis zur Ordnung m wie die Funktion:
T(x) = f(0) + f'(0)·x + f''(0)/2!·x² + ... + f⁽ᵐ⁾(0)/m!·xᵐ.

`series(f, x, 0, m + 1)` gibt die Entwicklung bis xᵐ und den Rest O(xᵐ⁺¹), `.removeO()` entfernt den Rest.''',
     """display(series(exp(x), x, 0, 5))
T = series(sin(x), x, 0, 8).removeO()
display(T)
plot(sin(x), T, (x, -5, 5), ylim=(-2, 2), legend=True);""")

t('Gib das Taylorpolynom 4. Grades von cos(x) an der Stelle 0 aus.', body='series(cos(x), x, 0, 5).removeO()')
t('Gib das Taylorpolynom 4. Grades von ln(1 + x) an der Stelle 0 aus.', body='series(log(1 + x), x, 0, 5).removeO()')
t('''Berechne das Taylorpolynom 3. Grades von eˣ von Hand mit der Formel (Summe f⁽ʲ⁾(0)/j! · xʲ) und vergleiche mit `series`.''',
  body='T = sum([diff(exp(x), x, j).subs(x, 0) / factorial(j) * x**j for j in range(4)])\ndisplay(T)\nT == series(exp(x), x, 0, 4).removeO()')
t('''Wie gut nähert das Taylorpolynom 6. Grades von eˣ die Zahl e an? Setze x = 1 ein und gib den Fehler e − T(1) mit 3 Ziffern aus.''',
  body='T = series(exp(x), x, 0, 7).removeO()\ndisplay(T.subs(x, 1))\nN(E - T.subs(x, 1), 3)')
t('''Zeichne cos(x) und seine Taylorpolynome vom Grad 2, 4 und 6 für −5 ≤ x ≤ 5 (y von −2 bis 2, mit Legende).''',
  body='plot(cos(x), *[series(cos(x), x, 0, m + 1).removeO() for m in [2, 4, 6]], (x, -5, 5), ylim=(-2, 2), legend=True);')

# ---------------------------------------------------------------- 7
sec('Gemischte Übungen')
t('''**Zinseszins:** 1000 € werden mit 4 % pro Jahr verzinst. Gib das Kapital nach 25 Jahren (auf Cent gerundet) und die Formel für das Kapital nach n Jahren aus (geometrische Folge).''',
  body='Kn = 1000 * Rational(104, 100)**n\ndisplay(round(N(Kn.subs(n, 25)), 2))\nKn')
t('''**Sparplan:** Am Anfang jedes Jahres werden 500 € eingezahlt, Zins 3 %. Das Kapital nach n Jahren ist Σₖ₌₁ⁿ 500 · qᵏ mit q = 1,03.
Nach der Summenformel der geometrischen Reihe ist das 500 · q · (qⁿ − 1)/(q − 1). Gib diese Formel und den Wert nach 10 Jahren (auf Cent) aus und vergleiche mit `summation`.''',
  body='q = Rational(103, 100)\nKn = 500 * q * (q**n - 1) / (q - 1)\ndisplay(Kn)\ndisplay(round(N(Kn.subs(n, 10)), 2))\nround(N(summation(500 * q**k, (k, 1, 10))), 2)')
t('''Ein Ball fällt aus 2 m Höhe und springt jedes Mal auf 60 % der vorigen Höhe zurück. Wie lang ist der gesamte Weg (nach unten und oben)? 2 + 2 · Σₖ₌₁^∞ 2 · 0,6ᵏ.''',
  body='2 + 2 * summation(2 * Rational(6, 10)**k, (k, 1, oo))')
t('''**Koch-Schneeflocke:** Der Umfang wächst mit jedem Schritt um den Faktor 4/3 (Startumfang 3), die Fläche ist A = √3/4 · (1 + Σₖ₌₁^∞ 3 · 4ᵏ⁻¹ / 9ᵏ). Gib den Grenzwert des Umfangs
(3 · (4/3)ⁿ für n → ∞) und den Flächeninhalt aus.''',
  body='display(limit(3 * Rational(4, 3)**n, n, oo))\nsimplify(sqrt(3) / 4 * (1 + summation(3 * 4**(k - 1) / 9**k, (k, 1, oo))))')

generate('sympy_folgen_reihen', 'Folgen und Reihen: Rekursion, Konvergenz, Reihen, Taylorpolynome', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
