# Erzeugt ../content/sympy_ableitungsregeln.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_ableitungsregeln.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_ableitungsregeln.py
#
# Bildungsplan BW 2016, Kursstufe (Basis- und Leistungsfach), Leitidee Funktionaler Zusammenhang:
# natürliche Exponentialfunktion und ihre Ableitung, natürlicher Logarithmus, Produkt- und Kettenregel,
# Quotientenregel und Ableitung von ln (Leistungsfach), trigonometrische Funktionen mit Parametern a·sin(b(x − c)) + d,
# Tangente und Normale (auch von einem Punkt außerhalb, Leistungsfach), Grenzverhalten und Asymptoten.
# Baut auf sympy_ableitungen (Klasse 10: Potenz-, Faktor-, Summenregel, sin/cos) auf.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = "from sympy import *\ninit_printing()\nimport matplotlib.pyplot as plt\nx = symbols('x', real=True)\na, b, c, d, k, u = symbols('a b c d k u', real=True)"

INTRO = '''In der Kursstufe kommen neue Funktionen dazu: die **e-Funktion**, der **natürliche Logarithmus** und Sinusfunktionen mit Parametern.
Für zusammengesetzte Funktionen brauchst du neue **Ableitungsregeln**: Produktregel, Kettenregel und (im Leistungsfach) Quotientenregel.
Am Ende geht es um Tangenten und um das Verhalten von Funktionen für x → ±∞ (Asymptoten).

Leite immer zuerst **von Hand** ab und prüfe dann mit `diff()`. sympy schreibt Ergebnisse oft anders auf als du (z. B. ausmultipliziert
oder anders sortiert); mit `factor()` und `simplify()` bekommst du eine Form zum Vergleichen.

Vorausgesetzt wird das Notebook *Ableitungen* (Klasse 10). Abschnitte und Aufgaben, die nur im **Leistungsfach** vorkommen, sind markiert.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy und matplotlib, schaltet die Formel-Ausgabe ein
und legt die Variable `x` und die Parameter `a`, `b`, `c`, `d`, `k`, `u` an. `real=True` sagt sympy, dass es reelle Zahlen sind:
Dann sucht `solve()` nur reelle Lösungen und vereinfacht z. B. ln(eˣ) zu x.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Die e-Funktion und der natürliche Logarithmus')
expl('''#### `exp(x)` und `log(x)`

Die **natürliche Exponentialfunktion** f(x) = eˣ (e ≈ 2,718) ist in sympy `exp(x)`. Ihre besondere Eigenschaft:
**Sie ist ihre eigene Ableitung**, (eˣ)' = eˣ.

Der **natürliche Logarithmus** ln(x) ist die Umkehrung: ln(eˣ) = x und e^(ln x) = x (für x > 0). In sympy heißt er `log(x)`
(ohne Basis). Damit löst du Exponentialgleichungen: eˣ = 5 ⟺ x = ln 5.''',
     """display(diff(exp(x), x))
display(exp(1), N(exp(1), 10))
display(simplify(log(exp(x))))
display(solve(Eq(exp(x), 5), x))
plot(exp(x), log(x), (x, -3, 4), ylim=(-3, 5), legend=True);""")
expl('''#### Logarithmusgesetze

| Gesetz | sympy |
|---|---|
| ln(a·b) = ln a + ln b | `expand_log(log(a*b), force=True)` |
| ln(a/b) = ln a − ln b | |
| ln(aʳ) = r·ln a | |
| aˣ = e^(x·ln a) | jede Exponentialfunktion lässt sich mit e schreiben |

`expand_log(..., force=True)` wendet die Gesetze an (`force=True`, weil sie nur für positive Zahlen gelten),
`logcombine(..., force=True)` fasst wieder zusammen.''',
     """display(expand_log(log(a**2 * b), force=True))
display(logcombine(log(a) - 2*log(b), force=True))
display(N(log(8) / log(2)))
simplify(exp(x * log(2)))""")

t('Gib e³ und e⁻¹ genau und mit 5 Ziffern aus.', body='display(exp(3), N(exp(3), 5))\ndisplay(exp(-1), N(exp(-1), 5))')
t('Löse eˣ = 20 exakt und gib die Lösung auch mit 4 Ziffern aus.', body='l = solve(Eq(exp(x), 20), x)\ndisplay(l)\nN(l[0], 4)')
t('Löse e^(2x − 1) = 7 exakt.', body='solve(Eq(exp(2*x - 1), 7), x)')
t('Löse 3·e^(−0,5x) = 1,2 exakt und mit 4 Ziffern (schreibe 0,5 und 1,2 als `Rational`).',
  body='l = solve(Eq(3 * exp(-Rational(1, 2) * x), Rational(6, 5)), x)\ndisplay(l)\nN(l[0], 4)')
t('Löse e²ˣ − 5eˣ + 6 = 0 (reelle Lösungsmenge mit `solveset`). Tipp für die Rechnung von Hand: Substitution u = eˣ.',
  body='solveset(Eq(exp(2*x) - 5*exp(x) + 6, 0), x, S.Reals)')
t('Löse ln(x) = 2 und ln(3x − 1) = 0.', body="display(solve(Eq(log(x), 2), x))\nsolve(Eq(log(3*x - 1), 0), x)")
t('Fasse `log(a) + 3*log(b) - log(c)` zu einem Logarithmus zusammen.', body='logcombine(log(a) + 3*log(b) - log(c), force=True)')
t('Zerlege ln(a³·√b / c) mit den Logarithmusgesetzen.', body='expand_log(log(a**3 * sqrt(b) / c), force=True)')
t('Schreibe 2ˣ und 0,5ˣ als e-Funktion: Gib `exp(x*log(2))` und `exp(x*log(Rational(1, 2)))` aus und prüfe mit `simplify(... - 2**x)`, dass sie gleich 2ˣ bzw. 0,5ˣ sind.',
  body="display(exp(x*log(2)), exp(x*log(Rational(1, 2))))\ndisplay(simplify(exp(x*log(2)) - 2**x))\nsimplify(exp(x*log(Rational(1, 2))) - Rational(1, 2)**x)")
t('Zeichne die Graphen von eˣ, e⁻ˣ und 2·eˣ für −2 ≤ x ≤ 2 in ein Diagramm (mit Legende).',
  body='plot(exp(x), exp(-x), 2*exp(x), (x, -2, 2), legend=True);')
predict("""display(exp(0))
display(log(1))
display(log(E))
display(exp(log(7)))
log(exp(3))""")

# ---------------------------------------------------------------- 2
sec('Die Produktregel')
expl('''#### (u · v)' = u' · v + u · v'

Ist eine Funktion ein **Produkt** zweier Funktionen u(x) und v(x), dann gilt die **Produktregel**:

f(x) = u(x) · v(x) ⟹ f'(x) = u'(x) · v(x) + u(x) · v'(x)

Beispiel: f(x) = x² · eˣ mit u = x², v = eˣ, also u' = 2x, v' = eˣ:
f'(x) = 2x · eˣ + x² · eˣ = (x² + 2x) · eˣ. Bei e-Funktionen klammert man eˣ aus; das macht `factor()`.''',
     """u = x**2
v = exp(x)
display(diff(u, x) * v + u * diff(v, x))
display(diff(u * v, x))
factor(diff(u * v, x))""")

t('Leite f(x) = x · eˣ ab (mit `factor()` ausgeklammert).', body='factor(diff(x * exp(x), x))')
t('Leite f(x) = x² · sin(x) ab.', body='diff(x**2 * sin(x), x)')
t('Leite f(x) = (2x + 1) · eˣ ab und klammere aus.', body='factor(diff((2*x + 1) * exp(x), x))')
t('Leite f(x) = x³ · e⁻ˣ ab und klammere aus.', body='factor(diff(x**3 * exp(-x), x))')
t('Leite f(x) = sin(x) · cos(x) ab.', body='diff(sin(x) * cos(x), x)')
t('Leite f(x) = eˣ · cos(x) ab und klammere aus.', body='factor(diff(exp(x) * cos(x), x))')
t('''Rechne die Produktregel für f(x) = (x² − 1) · eˣ Schritt für Schritt nach: Lege `u` und `v` an, gib `u'` und `v'` aus und dann
`u'·v + u·v'` mit `factor()`.''',
  body="u = x**2 - 1\nv = exp(x)\ndisplay(diff(u, x), diff(v, x))\nfactor(diff(u, x) * v + u * diff(v, x))")
t('Leite f(x) = x · ln(x) ab. **(Leistungsfach: (ln x)\' = 1/x)**', body='diff(x * log(x), x)')
t('Bilde f\' und f\'\' von f(x) = x · eˣ (beide ausgeklammert). Gib dann f⁽¹⁰⁾ aus.',
  body='f = x * exp(x)\ndisplay(factor(diff(f, x)), factor(diff(f, x, 2)))\nfactor(diff(f, x, 10))')
t('Für welche x hat f(x) = x · e⁻ˣ eine waagrechte Tangente? Löse f\'(x) = 0.', body='solve(diff(x * exp(-x), x), x)')
predict("""display(diff(x * x, x))
display(diff(5 * exp(x), x))
diff(x * sin(x), x)""")

# ---------------------------------------------------------------- 3
sec('Die Kettenregel')
expl('''#### Äußere mal innere Ableitung

Bei einer **Verkettung** f(x) = u(v(x)) steckt eine Funktion in einer anderen, z. B. f(x) = e^(3x) (außen eᵘ, innen 3x)
oder f(x) = (x² + 1)⁵ (außen u⁵, innen x² + 1). Es gilt die **Kettenregel**:

f'(x) = u'(v(x)) · v'(x) — „äußere Ableitung mal innere Ableitung“

Wichtige Sonderfälle: (e^(kx))' = k · e^(kx), (sin(kx))' = k · cos(kx), ((ax + b)ⁿ)' = n·a·(ax + b)ⁿ⁻¹.

Mit sympy kannst du die Kettenregel nachrechnen: Schreibe die äußere Funktion mit `u`, leite nach `u` ab und setze mit `subs` die innere ein.''',
     """display(diff(exp(3*x), x))
display(diff((x**2 + 1)**5, x))
aussen = u**5
innen = x**2 + 1
diff(aussen, u).subs(u, innen) * diff(innen, x)""")

t('Leite f(x) = e^(5x) ab.', body='diff(exp(5*x), x)')
t('Leite f(x) = e^(−x²) ab.', body='diff(exp(-x**2), x)')
t('Leite f(x) = (3x − 2)⁴ ab.', body='diff((3*x - 2)**4, x)')
t('Leite f(x) = sin(2x) und g(x) = cos(πx) ab.', body='display(diff(sin(2*x), x))\ndiff(cos(pi*x), x)')
t('Leite f(x) = √(x² + 1) ab.', body='diff(sqrt(x**2 + 1), x)')
t('Leite f(x) = 1/(2x + 1) ab. (Schreibe (2x + 1)⁻¹ und verwende die Kettenregel.)', body='diff(1 / (2*x + 1), x)')
t('Leite f(x) = sin²(x) = (sin x)² ab.', body='diff(sin(x)**2, x)')
t('Leite f(x) = 4 · e^(−0,2x) + 1 ab (0,2 als `Rational`).', body='diff(4 * exp(-Rational(1, 5) * x) + 1, x)')
t('Leite f(x) = e^(kx) nach x ab (k ist ein Parameter).', body='diff(exp(k*x), x)')
t('''Rechne die Kettenregel für f(x) = e^(x² − 3x) wie im Beispiel nach: äußere Funktion `exp(u)`, innere `x**2 - 3*x`.''',
  body="aussen = exp(u)\ninnen = x**2 - 3*x\ndiff(aussen, u).subs(u, innen) * diff(innen, x)")
t('Leite f(x) = ln(x² + 1) ab. **(Leistungsfach)**', body='diff(log(x**2 + 1), x)')
t('Leite f(x) = x · e^(−2x) ab (Produkt- **und** Kettenregel) und klammere aus.', body='factor(diff(x * exp(-2*x), x))')
t('Leite f(x) = (x + 1)² · e^(−x) ab und klammere aus.', body='factor(diff((x + 1)**2 * exp(-x), x))')
t('Bilde f\' und f\'\' von f(x) = e^(−x²) (ausgeklammert).', body='f = exp(-x**2)\ndisplay(factor(diff(f, x)))\nfactor(diff(f, x, 2))')
predict("""display(diff(exp(-x), x))
display(diff(exp(2*x), x, 3))
diff(sin(3*x), x)""")

# ---------------------------------------------------------------- 4
sec('Die Quotientenregel (Leistungsfach)')
expl('''#### (u / v)' = (u' · v − u · v') / v²

Für einen **Quotienten** f(x) = u(x) / v(x) gilt die **Quotientenregel**:

f'(x) = (u'(x) · v(x) − u(x) · v'(x)) / v(x)²

sympy gibt die Ableitung oft als Summe zweier Brüche aus. Mit `factor()` (oder `together()`) wird daraus ein Bruch.''',
     """u = x
v = x**2 + 1
display(diff(u / v, x))
display(factor(diff(u / v, x)))
factor((diff(u, x) * v - u * diff(v, x)) / v**2)""")

t('Leite f(x) = (2x + 1)/(x − 3) ab (als ein Bruch).', body='factor(diff((2*x + 1) / (x - 3), x))')
t('Leite f(x) = x²/(x + 1) ab (als ein Bruch).', body='factor(diff(x**2 / (x + 1), x))')
t('Leite f(x) = eˣ/x ab (als ein Bruch).', body='factor(diff(exp(x) / x, x))')
t('Leite f(x) = ln(x)/x ab und vereinfache mit `simplify()`.', body='simplify(diff(log(x) / x, x))')
t('Leite f(x) = tan(x) = sin(x)/cos(x) ab: einmal als `diff(sin(x)/cos(x), x)` mit `simplify()`, einmal als `diff(tan(x), x)`.',
  body='display(simplify(diff(sin(x) / cos(x), x)))\ndiff(tan(x), x)')
t('''Rechne die Quotientenregel für f(x) = (x² − 1)/(x² + 1) wie im Beispiel nach (mit `u`, `v`) und vergleiche mit `diff` (beides mit `factor`).''',
  body='u = x**2 - 1\nv = x**2 + 1\ndisplay(factor((diff(u, x) * v - u * diff(v, x)) / v**2))\nfactor(diff(u / v, x))')
t('Wo hat f(x) = x/(x² + 4) waagrechte Tangenten?', body='solve(diff(x / (x**2 + 4), x), x)')

# ---------------------------------------------------------------- 5
sec('Trigonometrische Funktionen mit Parametern')
expl('''#### f(x) = a · sin(b · (x − c)) + d

Die Parameter verändern den Graphen der Sinusfunktion:

| Parameter | Wirkung |
|---|---|
| a | **Amplitude** \\|a\\| (Streckung in y-Richtung) |
| b | **Periode** p = 2π / b (Streckung in x-Richtung) |
| c | Verschiebung in x-Richtung |
| d | Verschiebung in y-Richtung (Mittellinie y = d) |

`periodicity(f, x)` gibt die Periode aus. Die Ableitung bekommst du mit der Kettenregel: f'(x) = a · b · cos(b · (x − c)).''',
     """f = 2 * sin(pi / 2 * (x - 1)) + 3
display(periodicity(f, x))
display(diff(f, x))
plot(f, (x, -1, 9));""")

t('Gib die Periode von f(x) = 3 · sin(4x) und g(x) = sin(πx/3) aus.', body='display(periodicity(3 * sin(4*x), x))\nperiodicity(sin(pi * x / 3), x)')
t('Leite f(x) = 2 · sin(3x) − 1 ab.', body='diff(2 * sin(3*x) - 1, x)')
t('Leite f(x) = 4 · cos(π/6 · (x − 2)) + 5 ab.', body='diff(4 * cos(pi / 6 * (x - 2)) + 5, x)')
t('Leite f(x) = a · sin(b · (x − c)) + d allgemein nach x ab.', body='diff(a * sin(b * (x - c)) + d, x)')
t('''Bestimme b so, dass f(x) = sin(b·x) die Periode 8 hat (b > 0). Löse `Eq(2*pi/b, 8)`.''', body='solve(Eq(2 * pi / b, 8), b)')
t('''Gib die Nullstellen von f(x) = 2 · sin(x) − 1 im Intervall [0, 2π] aus (`solveset` mit `domain=Interval(0, 2*pi)`).''',
  body='solveset(Eq(2 * sin(x) - 1, 0), x, domain=Interval(0, 2*pi))')
t('''Gib die Stellen mit waagrechter Tangente von f(x) = 3 · sin(2x) im Intervall [0, π] aus.''',
  body='solveset(diff(3 * sin(2*x), x), x, domain=Interval(0, pi))')
t('''**Tageslänge:** In Stuttgart ist die Tageslänge (in Stunden) am Tag t des Jahres ungefähr L(t) = 4 · sin(2π/365 · (t − 80)) + 12,2
(12,2 als `Rational(61, 5)`). Berechne die Tageslänge am Tag 172 (21. Juni) mit 3 Ziffern und die Änderung L'(t) am Tag 80 in Minuten pro Tag (mit 3 Ziffern).''',
  given="t = symbols('t', real=True)",
  body="L = 4 * sin(2*pi/365 * (t - 80)) + Rational(61, 5)\ndisplay(N(L.subs(t, 172), 3))\nN(diff(L, t).subs(t, 80) * 60, 3)")
t('Zeichne f(x) = 2 · sin(x) und g(x) = sin(2x) für 0 ≤ x ≤ 2π in ein Diagramm (mit Legende).',
  body='plot(2 * sin(x), sin(2*x), (x, 0, 2*pi), legend=True);')
predict("""display(periodicity(sin(x), x))
display(periodicity(cos(2*pi*x), x))
diff(sin(x) + cos(x), x, 2)""")

# ---------------------------------------------------------------- 6
sec('Tangenten und Normalen')
expl('''#### Tangente in einem Punkt

Die Tangente an den Graphen von f an der Stelle x₀ ist t(x) = f'(x₀) · (x − x₀) + f(x₀),
die **Normale** (senkrecht dazu) hat die Steigung −1 / f'(x₀).''',
     """f = x * exp(-x)
x0 = 0
m = diff(f, x).subs(x, x0)
y0 = f.subs(x, x0)
display(m * (x - x0) + y0)
display(-1 / m * (x - x0) + y0)
plot(f, m * (x - x0) + y0, (x, -1, 4), ylim=(-1, 1));""")
expl('''#### Tangente durch einen Punkt außerhalb (Leistungsfach)

Gesucht sind Tangenten an f, die durch einen Punkt P(p | q) gehen, der **nicht** auf dem Graphen liegt. Man setzt die Tangente in
einem unbekannten Berührpunkt u an und verlangt, dass P auf ihr liegt: f'(u) · (p − u) + f(u) = q. Diese Gleichung löst man nach u.''',
     """f = exp(x)
tang = diff(f, x).subs(x, u) * (x - u) + f.subs(x, u)
l = solve(Eq(tang.subs(x, 0), 0), u)
display(l)
tang.subs(u, l[0])""")

t('Gib die Tangente an f(x) = eˣ an der Stelle x₀ = 1 aus (ausmultipliziert mit `expand`).',
  body='f = exp(x)\nexpand(diff(f, x).subs(x, 1) * (x - 1) + f.subs(x, 1))')
t('Gib die Tangente an f(x) = sin(2x) an der Stelle x₀ = 0 aus.', body='f = sin(2*x)\ndiff(f, x).subs(x, 0) * x + f.subs(x, 0)')
t('Gib die Tangente und die Normale an f(x) = x · eˣ an der Stelle x₀ = 0 aus.',
  body='f = x * exp(x)\nm = diff(f, x).subs(x, 0)\ndisplay(m * x + f.subs(x, 0))\n-1 / m * x + f.subs(x, 0)')
t('Gib die Tangente an f(x) = ln(x) an der Stelle x₀ = e aus und vereinfache mit `simplify`. **(Leistungsfach)**',
  body='f = log(x)\nsimplify(diff(f, x).subs(x, E) * (x - E) + f.subs(x, E))')
t('An welcher Stelle hat f(x) = e^(2x) die Steigung 4? Gib die Stelle und die Tangente dort aus (Tangente mit `expand`).',
  body='f = exp(2*x)\nx0 = solve(Eq(diff(f, x), 4), x)[0]\ndisplay(x0)\nexpand(4 * (x - x0) + f.subs(x, x0))')
t('Berechne den Steigungswinkel der Tangente an f(x) = eˣ im Punkt (0 | 1) in Grad (`atan` und `deg`).',
  body='deg(atan(diff(exp(x), x).subs(x, 0)))')
t('''**(Leistungsfach)** Bestimme alle Tangenten an f(x) = x², die durch den Punkt P(1 | −3) gehen (Berührstellen u und Tangentengleichungen, ausmultipliziert).''',
  body="f = x**2\ntang = diff(f, x).subs(x, u) * (x - u) + f.subs(x, u)\nl = solve(Eq(tang.subs(x, 1), -3), u)\ndisplay(l)\n[expand(tang.subs(u, w)) for w in l]")
t('''**(Leistungsfach)** Welche Tangente an f(x) = ln(x) geht durch den Ursprung? Gib die Berührstelle und die Tangente aus (`simplify`).''',
  body="f = log(x)\ntang = diff(f, x).subs(x, u) * (x - u) + f.subs(x, u)\nl = solve(Eq(tang.subs(x, 0), 0), u)\ndisplay(l)\nsimplify(tang.subs(u, l[0]))")

# ---------------------------------------------------------------- 7
sec('Grenzverhalten und Asymptoten')
expl('''#### Grenzwerte für x → ±∞

`limit(f, x, oo)` berechnet den Grenzwert für x → ∞ (`oo` sind zwei kleine o und bedeuten ∞), `limit(f, x, -oo)` für x → −∞.
Ist der Grenzwert eine Zahl g, ist y = g eine **waagrechte Asymptote**.

Wichtig für e-Funktionen: e⁻ˣ → 0 für x → ∞, und eˣ wächst schneller als jede Potenz von x. Deshalb geht z. B. x² · e⁻ˣ → 0.''',
     """display(limit(exp(-x), x, oo))
display(limit(x**2 * exp(-x), x, oo))
display(limit(x**2 * exp(-x), x, -oo))
limit(3 - 2 * exp(-x), x, oo)""")
expl('''#### Senkrechte Asymptoten (Polstellen)

An einer Definitionslücke (z. B. Nenner null) kann die Funktion gegen ±∞ gehen: eine **senkrechte Asymptote**.
`limit(f, x, 2, '+')` ist der Grenzwert von rechts, `limit(f, x, 2, '-')` von links. **Ohne Angabe rechnet sympy nur von rechts!**
Mit `'+-'` prüfst du beide Seiten: Unterscheiden sie sich, gibt sympy `zoo` aus (komplex unendlich, das heißt hier „kein Grenzwert“).''',
     """f = 1 / (x - 2)
display(limit(f, x, 2, '+'), limit(f, x, 2, '-'))
display(limit(f, x, 2, '+-'))
display(limit(1 / (x - 2)**2, x, 2, '+-'))
plot(f, (x, -2, 6), ylim=(-6, 6));""")

t('Berechne die Grenzwerte von f(x) = 2 + e⁻ˣ für x → ∞ und x → −∞.', body="f = 2 + exp(-x)\ndisplay(limit(f, x, oo))\nlimit(f, x, -oo)")
t('Berechne die Grenzwerte von f(x) = x · eˣ für x → ∞ und x → −∞.', body="f = x * exp(x)\ndisplay(limit(f, x, oo))\nlimit(f, x, -oo)")
t('Berechne die Grenzwerte von f(x) = x³ · e^(−x) für x → ∞ und x → −∞.', body="f = x**3 * exp(-x)\ndisplay(limit(f, x, oo))\nlimit(f, x, -oo)")
t('Berechne den Grenzwert von f(x) = (2x² + 1)/(x² − 4) für x → ∞ (waagrechte Asymptote).', body='limit((2*x**2 + 1) / (x**2 - 4), x, oo)')
t('Berechne für f(x) = (2x² + 1)/(x² − 4) die Grenzwerte bei x = 2 von links und von rechts.',
  body="f = (2*x**2 + 1) / (x**2 - 4)\ndisplay(limit(f, x, 2, '-'))\nlimit(f, x, 2, '+')")
t('''Prüfe mit `'+-'`, ob f(x) = 1/x² bzw. g(x) = 1/x bei x = 0 einen (beidseitigen) Grenzwert ∞ haben.''',
  body="display(limit(1 / x**2, x, 0, '+-'))\nlimit(1 / x, x, 0, '+-')")
t('''**Medikament:** Die Konzentration im Blut ist c(t) = 20 · t · e^(−0,5t) (mg/l, t in Stunden; 0,5 als `Rational`). Berechne den Grenzwert für t → ∞,
den Zeitpunkt der höchsten Konzentration und diese Konzentration mit 4 Ziffern.''',
  given="t = symbols('t', positive=True)",
  body="c = 20 * t * exp(-Rational(1, 2) * t)\ndisplay(limit(c, t, oo))\ntmax = solve(diff(c, t), t)[0]\ndisplay(tmax)\nN(c.subs(t, tmax), 4)")
t('''Zeichne f(x) = 3 − 2 · e^(−x) und die Asymptote y = 3 für −1 ≤ x ≤ 5 in ein Diagramm.''',
  body='plot(3 - 2 * exp(-x), 3, (x, -1, 5));')
predict("""display(limit(1 / x, x, oo))
display(limit(exp(x), x, -oo))
display(limit(exp(x) / x**10, x, oo))
limit(1 / x, x, 0)""")

# ---------------------------------------------------------------- 8
sec('Gemischte Übungen')
t('Leite f(x) = (x² + 1) · e^(−x) ab, klammere aus und bestimme die Stellen mit waagrechter Tangente.',
  body='fs = factor(diff((x**2 + 1) * exp(-x), x))\ndisplay(fs)\nsolve(fs, x)')
t('Leite f(x) = e^(sin x) ab.', body='diff(exp(sin(x)), x)')
t('Leite f(x) = √x · eˣ ab und klammere aus.', body='factor(diff(sqrt(x) * exp(x), x))')
t('Leite f(x) = sin(x²) und g(x) = sin²(x) ab (nicht verwechseln!).', body='display(diff(sin(x**2), x))\ndiff(sin(x)**2, x)')
t('Bestimme k so, dass f(x) = e^(kx) an der Stelle 0 die Steigung 3 hat.', body='solve(Eq(diff(exp(k*x), x).subs(x, 0), 3), k)')
t('''Prüfe, dass f(x) = 5 · e^(−2x) die Gleichung f'(x) = −2 · f(x) erfüllt (`simplify(f' + 2·f)` muss 0 sein).''',
  body='f = 5 * exp(-2*x)\nsimplify(diff(f, x) + 2 * f)')
t('''Prüfe, dass f(x) = sin(3x) die Gleichung f''(x) = −9 · f(x) erfüllt.''', body='f = sin(3*x)\nsimplify(diff(f, x, 2) + 9 * f)')
t('''Ein Schüler hat für f(x) = x · e^(2x) die Ableitung f'(x) = e^(2x) + 2x · e^(2x) angegeben, eine Schülerin (1 + 2x) · e^(2x). Prüfe beide mit `simplify(... - f')`.''',
  body='fs = diff(x * exp(2*x), x)\ndisplay(simplify(exp(2*x) + 2*x*exp(2*x) - fs))\nsimplify((1 + 2*x) * exp(2*x) - fs)')
t('''**Population:** Eine Bakterienkultur wächst nach N(t) = 500 · e^(0,3t) (t in Stunden; 0,3 als `Rational`). Wann sind es 5000 Bakterien (4 Ziffern)?
Wie schnell wächst die Kultur zu diesem Zeitpunkt (Bakterien pro Stunde)?''',
  given="t = symbols('t', real=True)",
  body="N_t = 500 * exp(Rational(3, 10) * t)\nt1 = solve(Eq(N_t, 5000), t)[0]\ndisplay(N(t1, 4))\nsimplify(diff(N_t, t).subs(t, t1))")

generate('sympy_ableitungsregeln', 'Ableitungsregeln: e-Funktion, Produkt-, Ketten- und Quotientenregel', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
