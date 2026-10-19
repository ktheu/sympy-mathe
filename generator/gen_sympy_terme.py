# Erzeugt ../content/sympy_terme.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_terme.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_terme.py
#
# Bildungsplan BW 2016, Leitidee Zahl – Variable – Operation: Klassen 7/8 (Terme mit Variablen, Einsetzen, Rechengesetze,
# Ausmultiplizieren, Ausklammern, binomische Formeln auch zum Faktorisieren, Formeln nach jeder Variablen auflösen),
# 9/10 (Potenzen mit rationalen Exponenten, Potenzgesetze). Bruchterme als Vorbereitung auf Bruchgleichungen.
# Die Setup-Zelle legt x, y, z, a, b, c an und wird beim Prüfen vor jeder Zelle ausgeführt.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = "from sympy import *\ninit_printing()\nx, y, z, a, b, c = symbols('x y z a b c')"

INTRO = '''In diesem Notebook rechnest du mit **Termen**, die Variablen enthalten: einsetzen, zusammenfassen, ausmultiplizieren,
ausklammern, binomische Formeln, Bruchterme, Potenzgesetze und Formeln umstellen. sympy rechnet dabei so wie du auf dem Papier,
nur ohne Rechenfehler. Nutze es, um deine eigenen Umformungen zu **überprüfen**.

Vorausgesetzt wird das Notebook *Zahlen exakt* (insbesondere `Rational`, `display()` und `N()`).

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.
sympy ordnet die Summanden eines Terms selbst. Steht bei dir dasselbe in anderer Reihenfolge, ist es trotzdem richtig.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy, schaltet die Formel-Ausgabe ein
und legt die Variablen `x`, `y`, `z`, `a`, `b` und `c` an, die in den meisten Aufgaben vorkommen.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Variablen und Terme')
expl('''#### Variablen anlegen mit `symbols()`

In Python ist ein Name wie `x` normalerweise eine Variable, in der ein **Wert** gespeichert ist. Für sympy braucht man dagegen
**Symbole**: Platzhalter, mit denen man rechnet, ohne ihren Wert zu kennen. `symbols('p q')` erzeugt zwei Symbole.
Die Setup-Zelle hat `x, y, z, a, b, c` schon angelegt. Andere Buchstaben musst du selbst anlegen.

sympy fasst gleichartige Glieder automatisch zusammen: `x + x + 3*x` wird zu `5x`. Das Malzeichen `*` muss man immer schreiben:
`3*x`, nicht `3x`.''',
     """p, q = symbols('p q')
display(x + x + 3*x)
display(2*a + 3*b - a + b)
p * q * p""")
expl('''#### Einsetzen mit `subs()`

`term.subs(x, 2)` setzt für `x` die Zahl 2 ein. Mehrere Variablen setzt man mit einem Dictionary ein:
`term.subs({x: 2, y: 3})`. Der Term selbst bleibt unverändert.

In Termen gilt: Punktrechnung vor Strichrechnung, und Potenzen zuerst. Mit Brüchen und Wurzeln rechnet `subs()` exakt.''',
     """term = 3*x**2 - 2*x + 5
display(term.subs(x, 2))
display(term.subs(x, Rational(1, 2)))
display((x*y + y**2).subs({x: 2, y: -3}))
term""")

t('Gib den Term `4x + 3y − x + 2y − 7` zusammengefasst aus.', body='4*x + 3*y - x + 2*y - 7')
t('Gib den Term `a · b · a · 3 · b` zusammengefasst aus.', body='a * b * a * 3 * b')
t('Lege die Variablen `u` und `v` an und gib den Term `2u − v + u + 3v` zusammengefasst aus.',
  body="u, v = symbols('u v')\n2*u - v + u + 3*v")
t('Berechne den Wert von `5x² − 3x + 1` für `x = 4`.', body='(5*x**2 - 3*x + 1).subs(x, 4)')
t('Berechne den Wert von `5x² − 3x + 1` für `x = −2/3` exakt.', body='(5*x**2 - 3*x + 1).subs(x, Rational(-2, 3))')
t('Berechne den Wert von `x² − 2xy + y²` für `x = 7` und `y = 3`.', body='(x**2 - 2*x*y + y**2).subs({x: 7, y: 3})')
t('Erstelle eine Wertetabelle des Terms `x² − 4` für die ganzen Zahlen x von −3 bis 3 als Liste.',
  body='[(x**2 - 4).subs(x, k) for k in range(-3, 4)]')
t('''Ein Rechteck ist doppelt so lang wie breit. Lege die Breite als Variable `b` an (ist schon vorhanden) und gib den Term für den Umfang
und den Term für den Flächeninhalt aus.''', body='display(2 * (2*b + b))\n2*b * b')
t('Berechne den Wert von `(a + b)/(a − b)` für `a = √3` und `b = 1` und mache den Nenner rational (`radsimp()`).',
  body='radsimp(((a + b) / (a - b)).subs({a: sqrt(3), b: 1}))')
t('''Setze die Zahlen 0, 1 und 2 in die Terme `(x + 1)²` und `x² + 1` ein und gib als Liste aus, ob die Werte jeweils gleich sind.''',
  body='[((x + 1)**2).subs(x, k) == (x**2 + 1).subs(x, k) for k in range(3)]')
predict("""display(x + x)
display(x * x)
display(x - x)
display(x / x)
(2*x).subs(x, 5)""")

# ---------------------------------------------------------------- 2
sec('Ausmultiplizieren')
expl('''#### `expand()`

`expand(term)` multipliziert alle Klammern aus (Distributivgesetz) und fasst zusammen.

- a(b + c) = ab + ac
- (a + b)(c + d) = ac + ad + bc + bd
- Ein Minus vor der Klammer ändert alle Vorzeichen in der Klammer: −(a − b) = −a + b.''',
     """display(expand(3*(x + 2)))
display(expand((a + b) * (c - 2)))
display(expand(x - (2*x - 5)))
expand((x + 1) * (x - 2) * (x + 3))""")

t('Multipliziere `4(2x − 3)` aus.', body='expand(4 * (2*x - 3))')
t('Multipliziere `−3a(2a − b + 4)` aus.', body='expand(-3*a * (2*a - b + 4))')
t('Multipliziere `(x + 5)(x − 2)` aus.', body='expand((x + 5) * (x - 2))')
t('Multipliziere `(2a − 3b)(4a + b)` aus.', body='expand((2*a - 3*b) * (4*a + b))')
t('Vereinfache `5x − (3x − 4) + 2(x − 1)`.', body='expand(5*x - (3*x - 4) + 2*(x - 1))')
t('Multipliziere `(x + 1)(x + 2)(x + 3)` aus.', body='expand((x + 1) * (x + 2) * (x + 3))')
t('Multipliziere `(x² − x + 1)(x + 1)` aus.', body='expand((x**2 - x + 1) * (x + 1))')
t('''Prüfe die Umformung eines Schülers: Er hat `(x − 4)(x + 3) = x² − x − 7` gerechnet. Gib `expand((x - 4)*(x + 3))` aus und darunter,
ob es gleich `x² − x − 7` ist.''', body='e = expand((x - 4) * (x + 3))\ndisplay(e)\ne == x**2 - x - 7')
t('''Ein Quadrat mit Seitenlänge `x` wird an einer Seite um 3 verlängert und an der anderen um 2 verkürzt. Gib den Flächeninhalt des neuen
Rechtecks ausmultipliziert aus und darunter die Änderung gegenüber dem Quadrat.''', body='A = expand((x + 3) * (x - 2))\ndisplay(A)\nA - x**2')
predict("""display(expand(2*(x + y)))
display(expand(-(a - b)))
display(expand((x + 1)*(x - 1)))
expand(x*(x + 1) - x**2)""")

# ---------------------------------------------------------------- 3
sec('Binomische Formeln')
expl('''#### Die drei binomischen Formeln

1. (a + b)² = a² + 2ab + b²
2. (a − b)² = a² − 2ab + b²
3. (a + b)(a − b) = a² − b²

sympy rechnet sie mit `expand()` aus. Umgekehrt erkennt `factor()` sie in einem Term wieder (siehe nächster Abschnitt).''',
     """display(expand((a + b)**2))
display(expand((a - b)**2))
display(expand((a + b)*(a - b)))
expand((3*x - 2)**2)""")
expl('''#### Höhere Potenzen

Auch (a + b)³, (a + b)⁴, ... kann man ausmultiplizieren. Die Zahlen vor den Summanden heißen **Binomialkoeffizienten**;
sie stehen im Pascalschen Dreieck. `binomial(n, k)` berechnet sie.''',
     """display(expand((a + b)**3))
display(expand((a + b)**4))
[binomial(4, k) for k in range(5)]""")

t('Multipliziere `(x + 4)²` aus.', body='expand((x + 4)**2)')
t('Multipliziere `(2a − 5)²` aus.', body='expand((2*a - 5)**2)')
t('Multipliziere `(3x + 2y)²` aus.', body='expand((3*x + 2*y)**2)')
t('Multipliziere `(7 − x)(7 + x)` aus.', body='expand((7 - x) * (7 + x))')
t('Multipliziere `(x/2 + 1)²` aus.', body='expand((x/2 + 1)**2)')
t('Multipliziere `(√2 + x)²` aus.', body='expand((sqrt(2) + x)**2)')
t('Berechne 101² geschickt als `(100 + 1)²`: Gib `expand((a + b)**2).subs({a: 100, b: 1})` aus.',
  body='expand((a + b)**2).subs({a: 100, b: 1})')
t('Berechne 49 · 51 mit der dritten binomischen Formel als `(50 − 1)(50 + 1)`. Setze in `a² − b²` ein.',
  body='(a**2 - b**2).subs({a: 50, b: 1})')
t('Multipliziere `(x + 1)⁵` aus.', body='expand((x + 1)**5)')
t('Gib die Zeile 6 des Pascalschen Dreiecks (die Koeffizienten von (a + b)⁶) als Liste aus.', body='[binomial(6, k) for k in range(7)]')
t('''Ergänze den Term `x² + 6x + ...` zu einem vollständigen Quadrat: Prüfe mit `expand()`, dass `(x + 3)²` den Term `x² + 6x + 9` ergibt,
und gib dann `x**2 + 6*x + 9 - (x + 3)**2` vereinfacht (mit `expand()`) aus.''',
  body='display(expand((x + 3)**2))\nexpand(x**2 + 6*x + 9 - (x + 3)**2)')
t('Prüfe, ob `(a − b)² = (b − a)²` gilt: Gib `expand((a - b)**2 - (b - a)**2)` aus.', body='expand((a - b)**2 - (b - a)**2)')
predict("""display(expand((x - 1)**2))
display(expand((x + y)**2 - (x - y)**2))
expand((1 - x)*(1 + x))""")

# ---------------------------------------------------------------- 4
sec('Ausklammern und Faktorisieren')
expl('''#### `factor()`

`factor(term)` ist die Umkehrung von `expand()`: Es schreibt einen Term als **Produkt**.
Dabei klammert sympy gemeinsame Faktoren aus und erkennt binomische Formeln.

Ein quadratischer Term wie x² − 5x + 6 wird in **Linearfaktoren** zerlegt: (x − 2)(x − 3). Daran sieht man sofort,
für welche x der Term 0 wird (Satz vom Nullprodukt).''',
     """display(factor(6*x**2 + 9*x))
display(factor(x**2 - 9))
display(factor(x**2 + 10*x + 25))
factor(x**2 - 5*x + 6)""")
expl('''#### Ordnen mit `collect()`

`collect(term, x)` sortiert einen Term nach Potenzen von `x` und fasst die Faktoren vor jeder Potenz zusammen.
Das ist nützlich, wenn mehrere Variablen vorkommen.''',
     """term = a*x**2 + b*x**2 + 3*x + a*x - 5
display(term)
collect(term, x)""")

t('Klammere aus: `12x² − 8x`.', body='factor(12*x**2 - 8*x)')
t('Klammere aus: `3ab + 6a² − 9a`.', body='factor(3*a*b + 6*a**2 - 9*a)')
t('Faktorisiere mit einer binomischen Formel: `x² − 16`.', body='factor(x**2 - 16)')
t('Faktorisiere: `4a² − 12ab + 9b²`.', body='factor(4*a**2 - 12*a*b + 9*b**2)')
t('Faktorisiere: `25x² − 1`.', body='factor(25*x**2 - 1)')
t('Zerlege in Linearfaktoren: `x² + x − 12`.', body='factor(x**2 + x - 12)')
t('Zerlege in Linearfaktoren: `2x² − 8x + 6`.', body='factor(2*x**2 - 8*x + 6)')
t('Zerlege in Linearfaktoren: `x³ − x`.', body='factor(x**3 - x)')
t('Zerlege `x⁴ − 1` in Faktoren.', body='factor(x**4 - 1)')
t('''Gib einen quadratischen Term an, der genau für x = −2 und x = 5 null wird: Multipliziere `(x + 2)(x − 5)` aus. Prüfe danach mit `factor()`.''',
  body='term = expand((x + 2) * (x - 5))\ndisplay(term)\nfactor(term)')
t('Ordne den Term `a x² + 2x² − b x + 4x + a − 1` mit `collect()` nach Potenzen von x.',
  body='collect(a*x**2 + 2*x**2 - b*x + 4*x + a - 1, x)')
t('Prüfe, dass `factor()` und `expand()` sich aufheben: Gib `expand(factor(x**2 - 7*x + 10))` aus.', body='expand(factor(x**2 - 7*x + 10))')
t('Versuche, `x² + 1` zu faktorisieren. Gib das Ergebnis aus.', body='factor(x**2 + 1)')
predict("""display(factor(x**2 - 2*x + 1))
display(factor(2*x + 2*y))
display(factor(x**2 - 2))
factor(x**2 + 2*x)""")

# ---------------------------------------------------------------- 5
sec('Bruchterme')
expl('''#### Kürzen und zusammenfassen

Ein **Bruchterm** hat eine Variable im Nenner.

- `cancel(term)` kürzt einen Bruchterm (Zähler und Nenner werden dazu faktorisiert).
- `together(term)` bringt mehrere Brüche auf einen gemeinsamen Nenner. Mit `cancel(together(...))` wird das Ergebnis noch gekürzt.
- `fraction(term)` liefert Zähler und Nenner als Paar, `numer(term)` nur den Zähler, `denom(term)` nur den Nenner.

Für Werte, bei denen der Nenner 0 ist, ist ein Bruchterm **nicht definiert**. Setzt man sie ein, gibt sympy `zoo` (komplex unendlich) oder `nan` aus.''',
     """display(cancel((x**2 - 1) / (x + 1)))
display(together(1/x + 1/(x + 1)))
display(fraction((x + 2) / (x**2 - 4)))
(1 / (x - 2)).subs(x, 2)""")

t('Kürze den Bruchterm `(x² − 9)/(x − 3)`.', body='cancel((x**2 - 9) / (x - 3))')
t('Kürze `(4a² + 4a)/(2a)`.', body='cancel((4*a**2 + 4*a) / (2*a))')
t('Kürze `(x² − 6x + 9)/(x² − 9)`.', body='cancel((x**2 - 6*x + 9) / (x**2 - 9))')
t('Fasse zusammen: `1/x + 1/(2x)`.', body='together(1/x + 1/(2*x))')
t('Fasse zusammen: `3/(x − 1) − 2/(x + 1)` und kürze, falls möglich.', body='cancel(together(3/(x - 1) - 2/(x + 1)))')
t('Vereinfache `(x/(x − 1)) · ((x − 1)/x²)`.', body='cancel((x / (x - 1)) * ((x - 1) / x**2))')
t('Vereinfache den Doppelbruch `(1 + 1/x)/(1 − 1/x)`.', body='cancel((1 + 1/x) / (1 - 1/x))')
t('Gib Zähler und Nenner des Terms `(x² + x)/(x³ − x)` nach dem Kürzen aus.', body='fraction(cancel((x**2 + x) / (x**3 - x)))')
t('Gib den Nenner von `(x + 1)/(x² − 4)` faktorisiert aus. Daran siehst du, für welche x der Bruchterm nicht definiert ist.',
  body='factor(denom((x + 1) / (x**2 - 4)))')
t('Setze in `(x + 1)/(x² − 4)` die Werte 0, 2 und 3 ein und gib die Ergebnisse als Liste aus.',
  body='[((x + 1) / (x**2 - 4)).subs(x, k) for k in [0, 2, 3]]')
predict("""display(cancel((x**2 + x) / x))
display(together(1/a + 1/b))
cancel((x - 1) / (1 - x))""")

# ---------------------------------------------------------------- 6
sec('Potenzgesetze und rationale Exponenten')
expl('''#### Potenzgesetze

| Gesetz | Beispiel |
|---|---|
| aᵐ · aⁿ = aᵐ⁺ⁿ | x² · x³ = x⁵ |
| aᵐ : aⁿ = aᵐ⁻ⁿ | x⁵ : x² = x³ |
| (aᵐ)ⁿ = aᵐ·ⁿ | (x²)³ = x⁶ |
| aⁿ · bⁿ = (ab)ⁿ | x³ · y³ = (xy)³ |
| a⁻ⁿ = 1/aⁿ | x⁻² = 1/x² |

sympy wendet die ersten Gesetze automatisch an. `powsimp()` fasst Potenzen mit gleichem Exponenten zusammen,
`expand_power_base()` zerlegt (ab)ⁿ in aⁿbⁿ.''',
     """display(x**2 * x**3)
display(x**5 / x**2)
display(x**(-2))
display(powsimp(x**3 * y**3))
expand_power_base((2*x)**3)""")
expl('''#### Rationale Exponenten und positive Variablen

Eine Potenz mit Bruch-Exponent ist eine Wurzel: x^(1/2) = √x, x^(1/3) = ∛x, x^(3/4) = ⁴√(x³).
In sympy schreibt man den Exponenten mit `Rational`, z. B. `x**Rational(1, 2)`.

Manche Gesetze gelten nur für **positive** Zahlen: √(x²) ist nur dann x, wenn x ≥ 0 ist (sonst |x|).
Bei einem gewöhnlichen Symbol weiß sympy nichts über das Vorzeichen und lässt √(x²) deshalb stehen.
Weiß sympy, dass eine Variable positiv ist, vereinfacht es mehr. Dafür legt man sie mit `symbols('r', positive=True)` an.''',
     """r = symbols('r', positive=True)
display(x**Rational(1, 2))
display(sqrt(x**2))
display(sqrt(r**2))
display((r**6)**Rational(1, 3))
simplify(r**Rational(1, 2) * r**Rational(1, 3))""")

t('Vereinfache `a³ · a⁴ · a`.', body='a**3 * a**4 * a')
t('Vereinfache `x⁷ : x³`.', body='x**7 / x**3')
t('Vereinfache `(x³)⁴`.', body='(x**3)**4')
t('Vereinfache `x⁻³ · x⁵`.', body='x**(-3) * x**5')
t('Vereinfache `(2a²b)³` und zerlege mit `expand_power_base()`.', body='expand_power_base((2*a**2*b)**3)')
t('Vereinfache `(a⁴ b⁶)/(a² b²)`.', body='(a**4 * b**6) / (a**2 * b**2)')
t('Fasse `a³ · b³` mit `powsimp()` zu einer Potenz zusammen.', body='powsimp(a**3 * b**3)')
t('Schreibe `x^(2/3)` mit `Rational` und gib es aus.', body='x**Rational(2, 3)')
t('Lege `r` positiv an und vereinfache `√(r⁶)`.', body="r = symbols('r', positive=True)\nsqrt(r**6)")
t('Lege `r` positiv an und vereinfache `r^(1/2) · r^(1/4)`.', body="r = symbols('r', positive=True)\nr**Rational(1, 2) * r**Rational(1, 4)")
t('Lege `r` positiv an und vereinfache `(r^(3/2))²`.', body="r = symbols('r', positive=True)\n(r**Rational(3, 2))**2")
t('Gib `√(x²)` einmal für das normale `x` und einmal für ein positives `r` aus.',
  body="r = symbols('r', positive=True)\ndisplay(sqrt(x**2))\nsqrt(r**2)")
t('Berechne `8^(2/3)`, `16^(3/4)` und `27^(−1/3)` exakt.', body='display(Integer(8)**Rational(2, 3), Integer(16)**Rational(3, 4), Integer(27)**Rational(-1, 3))')
predict("""r = symbols('r', positive=True)
display(x**0)
display((x**2)**Rational(1, 2))
display((r**2)**Rational(1, 2))
x**Rational(1, 2) * x**Rational(1, 2)""")

# ---------------------------------------------------------------- 7
sec('Terme vereinfachen und vergleichen')
expl('''#### `simplify()` und Termvergleich

`simplify(term)` versucht, einen Term so einfach wie möglich zu schreiben. Es probiert dazu viele Umformungen aus.

Zwei Terme sind **äquivalent** (gleichwertig), wenn sie für alle Einsetzungen denselben Wert haben. Das prüft man so:
`simplify(term1 - term2) == 0`. Der Vergleich `term1 == term2` prüft dagegen nur, ob beide **gleich aufgeschrieben** sind
(nach den einfachen Umformungen, die sympy immer automatisch macht, z. B. `2*(x + 3)` → `2x + 6`).''',
     """t1 = (x + 1)**2
t2 = x**2 + 2*x + 1
display(t1 == t2)
display(simplify(t1 - t2) == 0)
simplify((x**2 - 1) / (x - 1) + (x**2 - 4) / (x + 2))""")

t('Vereinfache `(a + b)² − (a − b)²`.', body='simplify((a + b)**2 - (a - b)**2)')
t('Vereinfache `(x² − 4)/(x − 2) − x`.', body='simplify((x**2 - 4) / (x - 2) - x)')
t('Prüfe, ob `(x − 3)(x + 3)` und `x² − 9` äquivalent sind.', body='simplify((x - 3) * (x + 3) - (x**2 - 9)) == 0')
t('Prüfe, ob `(x + y)²` und `x² + y²` äquivalent sind.', body='simplify((x + y)**2 - (x**2 + y**2)) == 0')
t('Prüfe, ob die Terme `(x − 2)(x + 2)` und `x² − 4` gleich sind, zuerst mit `==` und dann mit `simplify()`. Gib beide Ergebnisse aus.',
  body='display((x - 2)*(x + 2) == x**2 - 4)\nsimplify((x - 2)*(x + 2) - (x**2 - 4)) == 0')
t('''Ein Schüler hat `(x + 2)/(x + 4)` gekürzt zu `2/4 = 1/2`. Zeige, dass das falsch ist: Setze x = 1 in den ursprünglichen Term ein.''',
  body='((x + 2) / (x + 4)).subs(x, 1)')
t('''Die Summe von drei aufeinanderfolgenden ganzen Zahlen `n`, `n + 1`, `n + 2` ist immer durch 3 teilbar. Lege `n` an und gib die Summe
faktorisiert aus.''', body="n = symbols('n')\nfactor(n + (n + 1) + (n + 2))")
t('''Das Produkt zweier aufeinanderfolgender ungerader Zahlen `(2n − 1)(2n + 1)` ist um 1 kleiner als eine Quadratzahl. Gib das ausmultiplizierte
Produkt plus 1 aus.''', body="n = symbols('n')\nexpand((2*n - 1) * (2*n + 1) + 1)")

# ---------------------------------------------------------------- 8
sec('Formeln umstellen')
expl('''#### `Eq()` und `solve()`

`Eq(links, rechts)` ist eine **Gleichung**. `solve(gleichung, variable)` stellt sie nach der Variablen um und gibt
eine Liste der Lösungen zurück (meist ist es nur eine). Mit `[0]` bekommt man den ersten Eintrag.

Damit kann man jede Formel nach jeder Größe auflösen, z. B. v = s/t nach t. Bei Wurzeln sind positive Variablen hilfreich,
sonst liefert sympy auch die negative Lösung.''',
     """s, t, v = symbols('s t v', positive=True)
formel = Eq(v, s / t)
display(formel)
display(solve(formel, t))
solve(formel, s)[0]""")
expl('''#### Erst umstellen, dann einsetzen

Hat man die Formel umgestellt, setzt man mit `subs()` Zahlen ein. Zum Beispiel: Wie groß ist der Radius eines Kreises mit dem
Flächeninhalt 50 cm²?''',
     """A, r = symbols('A r', positive=True)
r_formel = solve(Eq(A, pi * r**2), r)[0]
display(r_formel)
display(r_formel.subs(A, 50))
N(r_formel.subs(A, 50), 4)""")

t('Stelle die Formel `v = s/t` nach `s` um.', given="s, t, v = symbols('s t v', positive=True)", body='solve(Eq(v, s / t), s)[0]')
t('Stelle die Flächenformel des Rechtecks `A = a·b` nach `b` um.', given="A, a, b = symbols('A a b', positive=True)",
  body='solve(Eq(A, a * b), b)[0]')
t('Stelle die Flächenformel des Dreiecks `A = g·h/2` nach `h` um.', given="A, g, h = symbols('A g h', positive=True)",
  body='solve(Eq(A, g * h / 2), h)[0]')
t('Stelle die Flächenformel des Trapezes `A = (a + c)/2 · h` nach `c` um.', given="A, a, c, h = symbols('A a c h', positive=True)",
  body='solve(Eq(A, (a + c) / 2 * h), c)[0]')
t('Stelle die Formel für das Kugelvolumen `V = 4/3 π r³` nach `r` um.', given="V, r = symbols('V r', positive=True)",
  body='solve(Eq(V, Rational(4, 3) * pi * r**3), r)[0]')
t('Stelle die Formel für den Satz des Pythagoras `c² = a² + b²` nach `a` um.', given="a, b, c = symbols('a b c', positive=True)",
  body='solve(Eq(c**2, a**2 + b**2), a)[0]')
t('Stelle die Zinsformel `Z = K · p/100` nach `p` um.', given="Z, K, p = symbols('Z K p', positive=True)",
  body='solve(Eq(Z, K * p / 100), p)[0]')
t('Stelle die Zinseszinsformel `Kn = K0 · q^n` nach `K0` um.', given="Kn, K0, q, n = symbols('Kn K0 q n', positive=True)",
  body='solve(Eq(Kn, K0 * q**n), K0)[0]')
t('''Wie lang ist die Seite eines Würfels mit dem Volumen 1000 cm³? Stelle `V = a³` nach `a` um und setze 1000 ein.''',
  given="V, a = symbols('V a', positive=True)", body='a_formel = solve(Eq(V, a**3), a)[0]\na_formel.subs(V, 1000)')
t('''Ein Zylinder hat das Volumen `V = π r² h`. Stelle nach `h` um und berechne die Höhe für V = 1000 cm³ und r = 5 cm exakt und auf 2 Nachkommastellen.''',
  given="V, r, h = symbols('V r h', positive=True)",
  body='h_formel = solve(Eq(V, pi * r**2 * h), h)[0]\nwert = h_formel.subs({V: 1000, r: 5})\ndisplay(wert)\nround(N(wert), 2)')
t('''Ein Auto fährt mit 90 km/h. Wie lange braucht es für 225 km? Stelle `v = s/t` nach `t` um und setze ein.''',
  given="s, t, v = symbols('s t v', positive=True)", body='solve(Eq(v, s / t), t)[0].subs({s: 225, v: 90})')
predict("""m, k = symbols('m k', positive=True)
display(solve(Eq(m, 2*k), k))
display(solve(Eq(m, k**2), k))
solve(Eq(x**2, 9), x)""")

# ---------------------------------------------------------------- 9
sec('Gemischte Übungen')
t('''Zeige, dass `(n + 1)² − n²` immer ungerade ist: Lege `n` an und gib den vereinfachten Term aus.''',
  body="n = symbols('n')\nexpand((n + 1)**2 - n**2)")
t('''Ein Rechteck hat den Umfang 20. Seine Breite ist `x`. Stelle den Term für den Flächeninhalt auf (die Länge ist `10 − x`),
multipliziere aus und gib danach die Werte für x = 1, 2, ..., 9 als Liste aus.''',
  body='A = expand(x * (10 - x))\ndisplay(A)\n[A.subs(x, k) for k in range(1, 10)]')
t('''Prüfe die Formel `1 + 2 + ... + n = n(n + 1)/2` für n = 100: Berechne die Summe mit `sum(range(1, 101))` und setze 100 in den Term ein.''',
  body="n = symbols('n')\ndisplay(sum(range(1, 101)))\n(n * (n + 1) / 2).subs(n, 100)")
t('''Multipliziere `(x + y + z)²` aus.''', body='expand((x + y + z)**2)')
t('''Vereinfache den Term `(x² − y²)/(x + y) + y` und prüfe das Ergebnis mit x = 5, y = 2 durch Einsetzen in den ursprünglichen Term.''',
  body='term = (x**2 - y**2) / (x + y) + y\ndisplay(simplify(term))\nterm.subs({x: 5, y: 2})')
t('''Ein Kapital von 1000 € wird mit dem Zinsfaktor `q` drei Jahre verzinst. Gib den Term `1000 q³` für q = 1 + p/100 ausmultipliziert nach p aus.''',
  given="p = symbols('p', positive=True)", body='expand(1000 * (1 + p / 100)**3)')
t('''Stelle die Oberflächenformel des Zylinders `O = 2πr² + 2πrh` nach `h` um und vereinfache.''',
  given="O, r, h = symbols('O r h', positive=True)", body='simplify(solve(Eq(O, 2*pi*r**2 + 2*pi*r*h), h)[0])')

generate('sympy_terme', 'Terme: Einsetzen, Ausmultiplizieren, Faktorisieren, Formeln umstellen', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
