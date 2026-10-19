# Erzeugt ../content/sympy_normalverteilung.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_normalverteilung.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_normalverteilung.py
#
# Bildungsplan BW 2016, Kursstufe, Leitidee Daten und Zufall (laut Hinweisen des Landesbildungsservers):
# Basisfach: diskrete und stetige Zufallsgrößen (binomial- und normalverteilt), Erwartungswert, Standardabweichung und Glockenkurve,
# Wahrscheinlichkeiten in annähernd normalverteilten Situationen (ohne Dichtefunktion als Begriff).
# Leistungsfach: Dichte- und Verteilungsfunktion, Erwartungswert und Standardabweichung als Integral, Eigenschaften der Glockenkurve
# (Symmetrie zu x = μ, Hochpunkt, Wendepunkte bei μ ± σ).
# sympy.stats: P() mit Abs(X) geht nicht (nur Intervalle wie (X >= a) & (X <= b)).
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = "from sympy import *\nfrom sympy.stats import *\ninit_printing()\nimport matplotlib.pyplot as plt\nx = symbols('x', real=True)"

INTRO = '''In diesem Notebook geht es um die **Normalverteilung**: Körpergrößen, Messfehler, Füllmengen oder Gewichte sind oft annähernd
normalverteilt. Ihre Wahrscheinlichkeiten werden durch die Fläche unter einer **Glockenkurve** beschrieben.

Du berechnest Wahrscheinlichkeiten mit `sympy.stats`, untersuchst, wie die Glockenkurve von Erwartungswert μ und Standardabweichung σ abhängt,
löst Umkehraufgaben (Welcher Wert wird nur von 10 % überschritten?) und nähert die Binomialverteilung durch die Normalverteilung an.
Im **Leistungsfach** untersuchst du die Dichtefunktion mit Mitteln der Analysis.

Vorausgesetzt werden die Notebooks *Wahrscheinlichkeit* und *Integrale*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy und `sympy.stats`, schaltet die Formel-Ausgabe ein,
lädt matplotlib und legt die Variable `x` an. **Achtung:** `sympy.stats` verwendet `E` für den Erwartungswert und `P` für Wahrscheinlichkeiten.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Die Glockenkurve')
expl('''#### Normalverteilte Zufallsgrößen

Eine **stetige** Zufallsgröße kann jeden Wert in einem Intervall annehmen (z. B. eine Körpergröße), eine **diskrete** nur einzelne Werte
(z. B. eine Anzahl). Bei einer **normalverteilten** Zufallsgröße X mit Erwartungswert μ und Standardabweichung σ liegen die Werte
glockenförmig um μ verteilt.

- `X = Normal('X', mu, sigma)` legt sie an (zweiter Wert: Erwartungswert, dritter: **Standardabweichung**).
- `density(X)(x)` ist der Term der **Glockenkurve** (Dichtefunktion).
- Je größer σ, desto breiter und flacher die Kurve. Die Fläche unter der Kurve ist immer 1.

Beispiel: Die Körpergröße erwachsener Männer ist annähernd normalverteilt mit μ = 178 cm und σ = 7 cm.''',
     """X = Normal('X', 178, 7)
f = density(X)(x)
display(f)
display(E(X), std(X))
plot(f, (x, 150, 206));""")

t('Lege X normalverteilt mit μ = 100, σ = 15 an (z. B. IQ-Werte) und gib den Term der Glockenkurve aus.',
  body="X = Normal('X', 100, 15)\ndensity(X)(x)")
t('Zeichne die Glockenkurven für μ = 0 und σ = 1, σ = 2, σ = 0,5 in ein Diagramm (−6 ≤ x ≤ 6, mit Legende).',
  body="plot(*[density(Normal('X', 0, s))(x) for s in [1, 2, Rational(1, 2)]], (x, -6, 6), legend=True);")
t('Zeichne die Glockenkurven für σ = 1 und μ = −2, 0, 3 in ein Diagramm (−6 ≤ x ≤ 7, mit Legende).',
  body="plot(*[density(Normal('X', m, 1))(x) for m in [-2, 0, 3]], (x, -6, 7), legend=True);")
t('Gib die Höhe des Hochpunkts der Glockenkurve für μ = 0 und σ = 1, 2 und 0,5 genau aus (Wert an der Stelle μ).',
  body="[density(Normal('X', 0, s))(0) for s in [1, 2, Rational(1, 2)]]")
t('Zeige mit einer Rechnung, dass die Glockenkurve für μ = 178, σ = 7 symmetrisch zu x = 178 ist: `simplify(f(178 + x) − f(178 − x))` muss 0 sein.',
  body="f = density(Normal('X', 178, 7))\nsimplify(f(178 + x) - f(178 - x))")
predict("""X = Normal('X', 5, 2)
display(E(X))
display(std(X))
variance(X)""")

# ---------------------------------------------------------------- 2
sec('Wahrscheinlichkeiten berechnen')
expl('''#### Flächen unter der Glockenkurve

Bei stetigen Zufallsgrößen haben **Intervalle** eine Wahrscheinlichkeit, einzelne Werte nicht: P(X = a) = 0.
Deshalb ist P(X ≤ a) = P(X < a).

- P(X ≤ a): `P(X <= a)`
- P(a ≤ X ≤ b): `P((X >= a) & (X <= b))`
- P(X ≥ a): `P(X >= a)` = 1 − P(X ≤ a)

Die Ergebnisse enthalten die Fehlerfunktion `erf`; mit `N()` bekommst du Zahlen.

Zum Zeichnen mit matplotlib (z. B. Flächen färben mit `plt.fill_between`) braucht man eine Python-Funktion statt eines sympy-Terms:
`fl = lambdify(x, term)` erzeugt sie, `fl(3.5)` berechnet dann einen Wert.''',
     """X = Normal('X', 178, 7)
display(P(X <= 185))
display(N(P(X <= 185), 4))
display(N(P((X >= 170) & (X <= 185)), 4))
display(N(P(X >= 190), 4))
P(Eq(X, 180))""")

M = "X = Normal('X', 178, 7)"
t('Wie groß ist die Wahrscheinlichkeit, dass ein Mann (μ = 178, σ = 7) kleiner als 170 cm ist? (4 Ziffern)', M, 'N(P(X <= 170), 4)')
t('Wie groß ist die Wahrscheinlichkeit, dass ein Mann zwischen 175 und 185 cm groß ist? (4 Ziffern)', M, 'N(P((X >= 175) & (X <= 185)), 4)')
t('Wie viel Prozent der Männer sind größer als 2 m? (3 Ziffern)', M, 'N(100 * P(X >= 200), 3)')
t('''Eine Maschine füllt Zuckerpakete mit μ = 1000 g und σ = 8 g. Ein Paket mit weniger als 985 g ist Ausschuss. Wie viel Prozent Ausschuss gibt es? (3 Ziffern)''',
  body="X = Normal('X', 1000, 8)\nN(100 * P(X <= 985), 3)")
t('''Wie groß ist für die Maschine aus der vorigen Aufgabe die Wahrscheinlichkeit, dass ein Paket um höchstens 10 g von 1000 g abweicht? (4 Ziffern)''',
  body="X = Normal('X', 1000, 8)\nN(P((X >= 990) & (X <= 1010)), 4)")
t('''Ein Bus braucht für eine Strecke im Mittel 24 Minuten mit σ = 3 Minuten. Mit welcher Wahrscheinlichkeit braucht er länger als 30 Minuten?
Wie viele von 200 Fahrten dauern also etwa länger als 30 Minuten (gerundet)?''',
  body="X = Normal('X', 24, 3)\np = P(X >= 30)\ndisplay(N(p, 4))\nround(N(200 * p))")
t('''Zeichne die Glockenkurve für μ = 178, σ = 7 und markiere die Fläche für 175 ≤ X ≤ 185 mit `plt.fill_between`. Verwende dafür Listen von x-Werten und Funktionswerten
(`lambdify` macht aus dem sympy-Term eine Python-Funktion: `fl = lambdify(x, f)`).''',
  body="f = density(Normal('X', 178, 7))(x)\nfl = lambdify(x, f)\nxs = [150 + i / 10 for i in range(561)]\nplt.plot(xs, [fl(w) for w in xs])\nxf = [175 + i / 10 for i in range(101)]\nplt.fill_between(xf, [fl(w) for w in xf], alpha=0.4)\nplt.show()")
predict("""X = Normal('X', 0, 1)
display(P(X <= 0))
display(P(X >= 0))
P(Eq(X, 0))""")

# ---------------------------------------------------------------- 3
sec('Die Sigma-Regeln')
expl('''#### Wie viel liegt in μ ± kσ?

Für **jede** Normalverteilung gilt (unabhängig von μ und σ):

| Intervall | Wahrscheinlichkeit |
|---|---|
| [μ − σ, μ + σ] | ≈ 68,3 % |
| [μ − 2σ, μ + 2σ] | ≈ 95,4 % |
| [μ − 3σ, μ + 3σ] | ≈ 99,7 % |

Mit der **Standardnormalverteilung** (μ = 0, σ = 1) lässt sich das nachrechnen.''',
     """Z = Normal('Z', 0, 1)
[N(P((Z >= -k) & (Z <= k)), 4) for k in [1, 2, 3]]""")

t('Prüfe die 1-σ-Regel für μ = 178, σ = 7: Berechne P(171 ≤ X ≤ 185) mit 4 Ziffern.', body="X = Normal('X', 178, 7)\nN(P((X >= 171) & (X <= 185)), 4)")
t('Berechne für die Standardnormalverteilung P(−1,96 ≤ Z ≤ 1,96) und P(−2,58 ≤ Z ≤ 2,58) mit 4 Ziffern (Zahlen als `Rational`).',
  body="Z = Normal('Z', 0, 1)\ndisplay(N(P((Z >= -Rational(196, 100)) & (Z <= Rational(196, 100))), 4))\nN(P((Z >= -Rational(258, 100)) & (Z <= Rational(258, 100))), 4)")
t('''Der IQ ist normalverteilt mit μ = 100 und σ = 15. In welchem Intervall liegen etwa 95,4 % aller Werte? Gib die Grenzen μ ± 2σ aus.''',
  body="mu, sigma = 100, 15\n(mu - 2 * sigma, mu + 2 * sigma)")
t('''Bestimme für die Standardnormalverteilung den Wert k mit P(−k ≤ Z ≤ k) = 0,9. `P` kann nicht mit einem Symbol k als Grenze rechnen; verwende deshalb
die Verteilungsfunktion F = `cdf(Z)` (F(k) = P(Z ≤ k)): Wegen der Symmetrie ist P(−k ≤ Z ≤ k) = 2·F(k) − 1. Löse mit `nsolve` (Startwert 1,5, 4 Ziffern).''',
  given="k = symbols('k', positive=True)",
  body="F = cdf(Normal('Z', 0, 1))\nN(nsolve(2 * F(k) - 1 - Rational(9, 10), k, 1.5), 4)")

# ---------------------------------------------------------------- 4
sec('Umkehraufgaben')
expl('''#### Grenzen und Parameter bestimmen

- **Grenze gesucht:** Welche Körpergröße wird von 90 % der Männer nicht überschritten? Gesucht ist a mit P(X ≤ a) = 0,9.
  `quantile(X)(Rational(9, 10))` gibt a direkt aus (das **Quantil**).
- **Parameter gesucht:** Wie groß darf σ höchstens sein, damit ...? Man stellt die Gleichung mit einem Symbol auf und löst sie mit `nsolve`.''',
     """X = Normal('X', 178, 7)
a = quantile(X)(Rational(9, 10))
display(N(a, 5))
display(N(P(X <= a), 4))
s = symbols('s', positive=True)
Y = Normal('Y', 1000, s)
N(nsolve(P(Y <= 985) - Rational(1, 100), s, 5), 4)""")

t('Welche Körpergröße wird von 95 % der Männer (μ = 178, σ = 7) nicht überschritten? (4 Ziffern)', M, 'N(quantile(X)(Rational(95, 100)), 4)')
t('Unterhalb welcher Größe liegen die kleinsten 10 % der Männer? (4 Ziffern)', M, 'N(quantile(X)(Rational(1, 10)), 4)')
t('''Bestimme das Intervall [μ − c, μ + c] für μ = 178, σ = 7, in dem die mittleren 80 % der Körpergrößen liegen (Grenzen mit den Quantilen 0,1 und 0,9, 4 Ziffern).''', M,
  '(N(quantile(X)(Rational(1, 10)), 4), N(quantile(X)(Rational(9, 10)), 4))')
t('''Ein IQ-Test: Die besten 2 % sollen eine Auszeichnung bekommen. Ab welchem Wert gibt es sie (μ = 100, σ = 15, 4 Ziffern)?''',
  body="N(quantile(Normal('X', 100, 15))(Rational(98, 100)), 4)")
t('''Auf welchen Mittelwert μ muss die Zuckermaschine (σ = 8 g) eingestellt werden, damit nur 1 % der Pakete unter 985 g wiegen? (`nsolve`, Startwert 1000, 5 Ziffern)''',
  given="m = symbols('m', real=True)",
  body="N(nsolve(P(Normal('X', m, 8) <= 985) - Rational(1, 100), m, 1000), 5)")
t('''Ein Lehrer gibt eine Klausur. Die Punkte sind normalverteilt mit μ = 30. Wie groß ist σ, wenn 16 % der Schüler mehr als 40 Punkte haben? (`nsolve`, Startwert 8, 4 Ziffern)''',
  given="s = symbols('s', positive=True)",
  body="N(nsolve(P(Normal('X', 30, s) >= 40) - Rational(16, 100), s, 8), 4)")

# ---------------------------------------------------------------- 5
sec('Näherung der Binomialverteilung')
expl('''#### Binomialverteilung ≈ Normalverteilung

Für großes n sieht das Histogramm der Binomialverteilung wie eine Glockenkurve aus. Man nähert sie durch die Normalverteilung mit
μ = n·p und σ = √(n·p·(1 − p)) an. Faustregel: Die Näherung ist brauchbar, wenn σ > 3.

Weil die Binomialverteilung nur ganze Zahlen kennt, rechnet man bei P(X ≤ k) mit der Grenze k + 0,5 (**Stetigkeitskorrektur**).''',
     """n, p = 100, Rational(1, 2)
B = Binomial('B', n, p)
mu, sigma = n * p, sqrt(n * p * (1 - p))
X = Normal('X', mu, sigma)
display(mu, sigma)
display(N(P(B <= 45), 4), N(P(X <= Rational(91, 2)), 4))
d = density(B).dict
werte = list(range(30, 71))
plt.bar(werte, [N(d[k]) for k in werte])
fl = lambdify(x, density(X)(x))
plt.plot(werte, [fl(k) for k in werte], 'r')
plt.show()""")

t('''Ein Würfel wird 600-mal geworfen, B ist die Anzahl der Sechsen. Gib μ und σ (4 Ziffern) aus und prüfe die Faustregel σ > 3.''',
  body="n, p = 600, Rational(1, 6)\nsigma = sqrt(n * p * (1 - p))\ndisplay(n * p, N(sigma, 4))\nsigma > 3")
t('''Berechne für den Würfel aus der vorigen Aufgabe P(B ≤ 90) exakt mit der Binomialverteilung und genähert mit der Normalverteilung (mit Stetigkeitskorrektur), beide mit 4 Ziffern.''',
  body="n, p = 600, Rational(1, 6)\nB = Binomial('B', n, p)\nX = Normal('X', n * p, sqrt(n * p * (1 - p)))\ndisplay(N(P(B <= 90), 4))\nN(P(X <= Rational(181, 2)), 4)")
t('''Berechne P(90 ≤ B ≤ 110) für den Würfel exakt (über `cdf(B)`) und genähert (Grenzen 89,5 und 110,5), beide mit 4 Ziffern.''',
  body="n, p = 600, Rational(1, 6)\nF = cdf(Binomial('B', n, p))\nX = Normal('X', n * p, sqrt(n * p * (1 - p)))\ndisplay(N(F[110] - F[89], 4))\nN(P((X >= Rational(179, 2)) & (X <= Rational(221, 2))), 4)")
t('''Für n = 20, p = 0,1 ist σ < 3. Vergleiche P(B ≤ 1) exakt und genähert (Grenze 1,5), beide mit 4 Ziffern.''',
  body="n, p = 20, Rational(1, 10)\nB = Binomial('B', n, p)\nX = Normal('X', n * p, sqrt(n * p * (1 - p)))\ndisplay(N(P(B <= 1), 4))\nN(P(X <= Rational(3, 2)), 4)")
t('''Zeichne wie im Beispiel das Histogramm der Binomialverteilung für n = 50, p = 0,3 (0 ≤ k ≤ 30) zusammen mit der Glockenkurve der Näherung.''',
  body="n, p = 50, Rational(3, 10)\nd = density(Binomial('B', n, p)).dict\nwerte = list(range(31))\nplt.bar(werte, [N(d[k]) for k in werte])\nfl = lambdify(x, density(Normal('X', n * p, sqrt(n * p * (1 - p))))(x))\nplt.plot(werte, [fl(k) for k in werte], 'r')\nplt.show()")

# ---------------------------------------------------------------- 6
sec('Dichtefunktion und Integral (Leistungsfach)')
expl('''#### Wahrscheinlichkeit = Integral der Dichte

Eine **Dichtefunktion** f ist nie negativ und hat die Gesamtfläche ∫₋∞^∞ f(x) dx = 1. Für eine stetige Zufallsgröße mit Dichte f gilt

P(a ≤ X ≤ b) = ∫ₐᵇ f(x) dx, E(X) = μ = ∫₋∞^∞ x · f(x) dx, Var(X) = σ² = ∫₋∞^∞ (x − μ)² · f(x) dx.

Die **Verteilungsfunktion** F(x) = P(X ≤ x) ist eine Integralfunktion der Dichte: F' = f. In sympy: `cdf(X)(x)`.

Die Glockenkurve von Normal(μ, σ) ist f(x) = 1/(σ√(2π)) · e^(−(x − μ)²/(2σ²)).''',
     """mu, sigma = symbols('mu sigma', positive=True)
f = exp(-(x - mu)**2 / (2 * sigma**2)) / (sigma * sqrt(2 * pi))
display(f)
display(simplify(f - density(Normal('X', mu, sigma))(x)))
display(simplify(integrate(f, (x, -oo, oo))))
display(solve(diff(f, x), x), solve(diff(f, x, 2), x))
Fx = cdf(Normal('X', mu, sigma))(x)
display(Fx)
simplify(diff(Fx, x) - f)""")

t('''Berechne für μ = 178, σ = 7 die Wahrscheinlichkeit P(175 ≤ X ≤ 185) als Integral der Dichte (4 Ziffern) und vergleiche mit `P(...)`.''',
  body="X = Normal('X', 178, 7)\nf = density(X)(x)\ndisplay(N(integrate(f, (x, 175, 185)), 4))\nN(P((X >= 175) & (X <= 185)), 4)")
t('''Berechne den Erwartungswert der Normalverteilung mit μ = 3, σ = 2 als Integral ∫ x · f(x) dx.''',
  body="f = density(Normal('X', 3, 2))(x)\nsimplify(integrate(x * f, (x, -oo, oo)))")
t('''Berechne die Varianz der Normalverteilung mit μ = 3, σ = 2 als Integral ∫ (x − 3)² · f(x) dx.''',
  body="f = density(Normal('X', 3, 2))(x)\nsimplify(integrate((x - 3)**2 * f, (x, -oo, oo)))")
t('''Bestimme für die Glockenkurve mit μ = 178, σ = 7 den Hochpunkt und die Wendestellen.''',
  body="f = density(Normal('X', 178, 7))(x)\ndisplay(solve(diff(f, x), x))\nsolve(diff(f, x, 2), x)")
t('''Prüfe, ob f(x) = 3/4 · (1 − x²) für −1 ≤ x ≤ 1 (sonst 0) eine Dichtefunktion ist: Gib das Integral über [−1, 1] aus und den kleinsten Wert von f auf [−1, 1].''',
  body="f = Rational(3, 4) * (1 - x**2)\ndisplay(integrate(f, (x, -1, 1)))\nminimum(f, x, Interval(-1, 1))")
t('''Berechne für die Dichte aus der vorigen Aufgabe P(0 ≤ X ≤ 0,5), den Erwartungswert und die Standardabweichung (alle genau).''',
  body="f = Rational(3, 4) * (1 - x**2)\ndisplay(integrate(f, (x, 0, Rational(1, 2))))\nmu = integrate(x * f, (x, -1, 1))\ndisplay(mu)\nsqrt(integrate((x - mu)**2 * f, (x, -1, 1)))")
t('''Bestimme c so, dass f(x) = c · x · (4 − x) auf [0, 4] eine Dichtefunktion ist.''',
  given="c = symbols('c', positive=True)", body="solve(Eq(integrate(c * x * (4 - x), (x, 0, 4)), 1), c)")
t('''**Wartezeit:** Die Wartezeit an einer Haltestelle hat die Dichte f(t) = 0,2 · e^(−0,2t) für t ≥ 0 (Minuten). Prüfe ∫₀^∞ f = 1 und berechne P(T ≤ 5) (4 Ziffern)
und die mittlere Wartezeit.''',
  given="tt = symbols('t', positive=True)",
  body="f = Rational(1, 5) * exp(-Rational(1, 5) * tt)\ndisplay(integrate(f, (tt, 0, oo)))\ndisplay(N(integrate(f, (tt, 0, 5)), 4))\nintegrate(tt * f, (tt, 0, oo))")

# ---------------------------------------------------------------- 7
sec('Gemischte Übungen')
t('''Äpfel einer Sorte wiegen im Mittel 180 g mit σ = 20 g. Äpfel der Klasse I wiegen mindestens 160 g. Wie viel Prozent sind Klasse I (3 Ziffern)?
Wie viele von 500 Äpfeln sind es etwa (gerundet)?''',
  body="X = Normal('X', 180, 20)\np = P(X >= 160)\ndisplay(N(100 * p, 3))\nround(N(500 * p))")
t('''Bei einer Klausur sind die Punkte normalverteilt mit μ = 32 und σ = 8. Die besten 15 % bekommen eine 1. Ab wie vielen Punkten (4 Ziffern)?''',
  body="N(quantile(Normal('X', 32, 8))(Rational(85, 100)), 4)")
t('''Schrauben sollen 40 mm lang sein. Eine Schraube ist brauchbar, wenn sie zwischen 39,7 und 40,3 mm lang ist. Die Maschine arbeitet mit μ = 40 mm. Wie groß darf σ höchstens
sein, damit 99 % brauchbar sind? (`nsolve`, Startwert 0,1, 4 Ziffern)''',
  given="s = symbols('s', positive=True)",
  body="X = Normal('X', 40, s)\nN(nsolve(P((X >= Rational(397, 10)) & (X <= Rational(403, 10))) - Rational(99, 100), s, 0.1), 4)")
t('''Ein Flugzeug hat 200 Plätze. Erfahrungsgemäß erscheinen 8 % der Gebuchten nicht. Die Fluggesellschaft verkauft 210 Tickets. Wie groß ist die Wahrscheinlichkeit, dass mehr als
200 Passagiere erscheinen? Rechne exakt mit der Binomialverteilung und mit der Normalverteilungsnäherung (Grenze 200,5), beide mit 4 Ziffern.''',
  body="n, p = 210, Rational(92, 100)\nB = Binomial('B', n, p)\nX = Normal('X', n * p, sqrt(n * p * (1 - p)))\ndisplay(N(P(B >= 201), 4))\nN(P(X >= Rational(401, 2)), 4)")

generate('sympy_normalverteilung', 'Normalverteilung: Glockenkurve, Wahrscheinlichkeiten, Näherung, Dichtefunktion', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
