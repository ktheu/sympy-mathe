# Erzeugt ../content/sympy_ableitungen.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_ableitungen.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_ableitungen.py
#
# Bildungsplan BW 2016, Klassen 9/10 (Klasse 10), Leitidee Funktionaler Zusammenhang (13)–(24) und Zahl – Variable – Operation (13), (14):
# Differenzenquotient/Sekante, Ableitung als Grenzwert, Tangente und Normale, lineare Approximation, Steigungswinkel,
# Ableitungsfunktion, Faktor-, Summen-, Potenzregel, Ableitung von sin und cos, Monotonie(satz), Extrempunkte (lokal/global),
# Krümmung und Wendepunkte, Zusammenhang zwischen f und f'.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = "from sympy import *\ninit_printing()\nimport matplotlib.pyplot as plt\nx, h, a, b = symbols('x h a b')"

INTRO = '''In diesem Notebook geht es um die **Differentialrechnung**: Wie schnell ändert sich eine Größe? Vom Differenzenquotienten (mittlere
Änderungsrate) kommst du über einen Grenzwert zur **Ableitung** (momentane Änderungsrate). Mit Ableitungen bestimmst du Tangenten,
Monotonie, Hoch-, Tief- und Wendepunkte und löst Optimierungsaufgaben.

sympy kann Grenzwerte (`limit`) und Ableitungen (`diff`) exakt berechnen. Rechne die Ableitungen trotzdem zuerst selbst mit den
Ableitungsregeln und prüfe dann mit sympy.

Vorausgesetzt werden die Notebooks *Terme*, *Gleichungen* und *Funktionen*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy und matplotlib, schaltet die Formel-Ausgabe ein
und legt die Variablen `x`, `h`, `a` und `b` an.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Mittlere Änderungsrate')
expl('''#### Differenzenquotient und Sekante

Die **mittlere Änderungsrate** einer Funktion f auf dem Intervall [a, b] ist der **Differenzenquotient**

(f(b) − f(a)) / (b − a)

Geometrisch ist das die Steigung der **Sekante** durch die Punkte (a | f(a)) und (b | f(b)).''',
     """def f(x):
    return x**2

m = (f(3) - f(1)) / Integer(3 - 1)
display(m)
sekante = m * (x - 1) + f(1)
display(expand(sekante))
plot(f(x), sekante, (x, -0.5, 3.5), legend=True);""")

t('Berechne die mittlere Änderungsrate von `f(x) = x²` auf dem Intervall [1, 4].',
  body='def f(x):\n    return x**2\n\n(f(4) - f(1)) / Integer(4 - 1)')
t('Berechne die mittlere Änderungsrate von `f(x) = x³ − 2x` auf [−1, 2].',
  body='def f(x):\n    return x**3 - 2*x\n\n(f(2) - f(-1)) / Integer(2 - (-1))')
t('Berechne die mittleren Änderungsraten von `f(x) = x²` auf den Intervallen [1, 2], [1; 1,1] und [1; 1,01] exakt. Gib sie als Liste aus.',
  body="def f(x):\n    return x**2\n\n[(f(1 + d) - f(1)) / d for d in [Integer(1), Rational(1, 10), Rational(1, 100)]]")
t('''**Temperatur:** Um 8 Uhr ist es 12 °C, um 14 Uhr 21 °C. Wie groß ist die mittlere Änderungsrate in °C pro Stunde?''',
  body='Rational(21 - 12, 14 - 8)')
t('Gib die Gleichung der Sekante von `f(x) = √x` durch die Punkte bei x = 1 und x = 4 aus.',
  body='m = (sqrt(4) - sqrt(1)) / 3\nexpand(m * (x - 1) + 1)')
t('Berechne den Differenzenquotienten `(f(x0 + h) − f(x0))/h` für `f(x) = x²` und `x0 = 3` vereinfacht.',
  body='def f(x):\n    return x**2\n\nsimplify((f(3 + h) - f(3)) / h)')

# ---------------------------------------------------------------- 2
sec('Von der mittleren zur momentanen Änderungsrate')
expl('''#### Der Grenzwert h → 0

Lässt man das Intervall immer kleiner werden (h → 0), geht die Sekantensteigung gegen die **Tangentensteigung**.
Dieser Grenzwert ist die **Ableitung** von f an der Stelle x₀:

f'(x₀) = lim (h → 0) (f(x₀ + h) − f(x₀)) / h

sympy berechnet Grenzwerte mit `limit(term, h, 0)`. Setzt man statt einer Zahl x₀ die Variable x ein, erhält man die
**Ableitungsfunktion** f'(x).''',
     """def f(x):
    return x**2

dq = (f(3 + h) - f(3)) / h
display(simplify(dq))
display(limit(dq, h, 0))
limit((f(x + h) - f(x)) / h, h, 0)""")

t('Berechne `f\'(2)` für `f(x) = x³` mit dem Grenzwert des Differenzenquotienten.',
  body='def f(x):\n    return x**3\n\nlimit((f(2 + h) - f(2)) / h, h, 0)')
t('Berechne die Ableitungsfunktion von `f(x) = x³` mit dem Grenzwert.',
  body='def f(x):\n    return x**3\n\nlimit((f(x + h) - f(x)) / h, h, 0)')
t('Berechne die Ableitungsfunktion von `f(x) = 1/x` mit dem Grenzwert.',
  body='def f(x):\n    return 1 / x\n\nlimit((f(x + h) - f(x)) / h, h, 0)')
t('Berechne die Ableitungsfunktion von `f(x) = √x` mit dem Grenzwert.',
  body='def f(x):\n    return sqrt(x)\n\nlimit((f(x + h) - f(x)) / h, h, 0)')
t('''Gib für `f(x) = x²` an der Stelle 1 die Werte des Differenzenquotienten für h = 1, 0,1, 0,01, 0,001 als Liste aus (exakt mit `Rational`).''',
  body='def f(x):\n    return x**2\n\n[(f(1 + d) - f(1)) / d for d in [Integer(1), Rational(1, 10), Rational(1, 100), Rational(1, 1000)]]')
t('''Die Betragsfunktion |x| hat an der Stelle 0 einen Knick. Berechne den Grenzwert des Differenzenquotienten von rechts (`limit(..., h, 0, '+')`)
und von links (`'-'`).''',
  body="display(limit(Abs(h) / h, h, 0, '+'))\nlimit(Abs(h) / h, h, 0, '-')")
predict("""display(limit((h**2 + 3*h) / h, h, 0))
display(limit(sin(h) / h, h, 0))
limit(1 / h, h, 0, '+')""")

# ---------------------------------------------------------------- 3
sec('Ableitungsregeln')
expl('''#### `diff()` und die Regeln

`diff(f, x)` berechnet die Ableitung, `diff(f, x, 2)` die zweite Ableitung f''. Für das Rechnen von Hand gelten:

| Regel | Beispiel |
|---|---|
| Potenzregel: (xⁿ)' = n·xⁿ⁻¹ | (x⁵)' = 5x⁴ |
| Faktorregel: (c·f)' = c·f' | (3x²)' = 6x |
| Summenregel: (f + g)' = f' + g' | (x² + x)' = 2x + 1 |
| Konstante: c' = 0 | 7' = 0 |
| sin' = cos, cos' = −sin | (2 sin x)' = 2 cos x |

Die Potenzregel gilt auch für negative und gebrochene Exponenten: (1/x)' = (x⁻¹)' = −x⁻², (√x)' = (x^(1/2))' = 1/(2√x).''',
     """display(diff(x**5, x))
display(diff(3*x**4 - 2*x + 7, x))
display(diff(1 / x, x))
display(diff(sqrt(x), x))
display(diff(sin(x), x), diff(cos(x), x))
diff(x**4, x, 2)""")

t('Leite `f(x) = 4x³ − 2x² + 5x − 1` ab.', body='diff(4*x**3 - 2*x**2 + 5*x - 1, x)')
t('Leite `f(x) = x⁶/3 + 2/x` ab.', body='diff(x**6 / 3 + 2 / x, x)')
t('Leite `f(x) = 3√x` ab.', body='diff(3 * sqrt(x), x)')
t('Leite `f(x) = 1/x²` ab.', body='diff(1 / x**2, x)')
t('Leite `f(x) = (x + 1)²` ab. Multipliziere vorher aus und vergleiche mit `diff((x + 1)**2, x)` (ausmultipliziert).',
  body='display(diff(expand((x + 1)**2), x))\nexpand(diff((x + 1)**2, x))')
t('Leite `f(x) = 2 sin(x) − 3 cos(x)` ab.', body='diff(2*sin(x) - 3*cos(x), x)')
t('Bilde die ersten drei Ableitungen von `f(x) = x⁴ − 2x³` (als Liste).', body='f = x**4 - 2*x**3\n[diff(f, x, k) for k in range(1, 4)]')
t('Leite `f(x) = a·x² + b·x` nach x ab (a und b sind Parameter).', body='diff(a*x**2 + b*x, x)')
t('Berechne `f\'(2)` für `f(x) = x³ − 4x`: Leite ab und setze ein.', body='diff(x**3 - 4*x, x).subs(x, 2)')
t('''Prüfe die Ableitung eines Schülers: Er hat für `f(x) = 5x³ − 2x + 4` die Ableitung `15x² − 2x` angegeben. Gib die richtige Ableitung aus
und darunter, ob seine stimmt.''', body='richtig = diff(5*x**3 - 2*x + 4, x)\ndisplay(richtig)\nrichtig == 15*x**2 - 2*x')
t('An welchen Stellen hat `f(x) = x³ − 3x² + 1` die Steigung 9? Löse `f\'(x) = 9`.', body='solve(Eq(diff(x**3 - 3*x**2 + 1, x), 9), x)')
predict("""display(diff(7, x))
display(diff(x, x))
display(diff(x**2, x, 3))
diff(sin(x), x, 2)""")

# ---------------------------------------------------------------- 4
sec('Tangente, Normale und Steigungswinkel')
expl('''#### Tangente und Normale

Die **Tangente** an den Graphen von f im Punkt (x₀ | f(x₀)) hat die Steigung f'(x₀):

t(x) = f'(x₀) · (x − x₀) + f(x₀)

Die **Normale** steht senkrecht auf der Tangente, ihre Steigung ist −1/f'(x₀). Der **Steigungswinkel** α der Tangente
erfüllt tan(α) = f'(x₀), also α = arctan(f'(x₀)) (`atan()`, mit `deg()` in Grad).

In der Nähe von x₀ ist die Tangente eine gute **Näherung** für f (lineare Approximation).''',
     """f = x**2 / 2
x0 = 2
m = diff(f, x).subs(x, x0)
tangente = expand(m * (x - x0) + f.subs(x, x0))
normale = expand(-1 / m * (x - x0) + f.subs(x, x0))
display(tangente, normale)
display(N(deg(atan(m)), 4))
plot(f, tangente, normale, (x, -1, 5), ylim=(-1, 6), legend=True);""")

t('Bestimme die Gleichung der Tangente an `f(x) = x²` im Punkt mit x₀ = 3.',
  body='f = x**2\nm = diff(f, x).subs(x, 3)\nexpand(m * (x - 3) + f.subs(x, 3))')
t('Bestimme die Gleichung der Tangente an `f(x) = x³ − 2x` bei x₀ = −1.',
  body='f = x**3 - 2*x\nm = diff(f, x).subs(x, -1)\nexpand(m * (x + 1) + f.subs(x, -1))')
t('Bestimme die Gleichung der Normale an `f(x) = x²` bei x₀ = 1.',
  body='f = x**2\nm = diff(f, x).subs(x, 1)\nexpand(-1 / m * (x - 1) + f.subs(x, 1))')
t('Bestimme den Steigungswinkel des Graphen von `f(x) = x³/3` bei x₀ = 1 in Grad.',
  body='m = diff(x**3 / 3, x).subs(x, 1)\ndeg(atan(m))')
t('Bestimme den Steigungswinkel des Graphen von `f(x) = 0,5x²` bei x₀ = 3 in Grad mit 4 Ziffern.',
  body='m = diff(x**2 / 2, x).subs(x, 3)\nN(deg(atan(m)), 4)')
t('Zeichne `f(x) = sin(x)` und die Tangente bei x₀ = 0 für x von −π bis π.',
  body='m = diff(sin(x), x).subs(x, 0)\nplot(sin(x), m * x, (x, -pi, pi), ylim=(-2, 2));')
t('''**Lineare Approximation:** Nähere √4,1 mit der Tangente an `√x` bei x₀ = 4 an. Gib den Näherungswert exakt, als Dezimalzahl mit 8 Ziffern
und darunter den genauen Wert `N(sqrt(4.1), 8)` aus.''',
  body="f = sqrt(x)\nm = diff(f, x).subs(x, 4)\nnaeherung = m * (Rational('4.1') - 4) + 2\ndisplay(naeherung, N(naeherung, 8))\nN(sqrt(Rational('4.1')), 8)")
t('In welchem Punkt hat der Graph von `f(x) = x² − 4x + 5` eine waagerechte Tangente? Gib den Punkt als Tupel aus.',
  body='f = x**2 - 4*x + 5\nxs = solve(diff(f, x), x)[0]\n(xs, f.subs(x, xs))')
t('''An welchen Stellen ist die Tangente an `f(x) = x³/3 − x` parallel zur Geraden `y = 3x`?''',
  body='solve(Eq(diff(x**3 / 3 - x, x), 3), x)')

# ---------------------------------------------------------------- 5
sec('Monotonie')
expl('''#### Monotoniesatz

Ist f'(x) > 0 auf einem Intervall, so ist f dort **streng monoton steigend**, ist f'(x) < 0, so ist f **streng monoton fallend**.
Die Umkehrung gilt nicht ganz: f(x) = x³ ist überall steigend, obwohl f'(0) = 0 ist.

Mit `solveset(diff(f, x) > 0, x, domain=S.Reals)` bestimmt man, wo f steigt. `is_increasing(f, Interval(a, b))` prüft das direkt.''',
     """f = x**3 - 3*x
display(diff(f, x))
display(solveset(diff(f, x) > 0, x, domain=S.Reals))
display(solveset(diff(f, x) < 0, x, domain=S.Reals))
is_increasing(x**3, S.Reals)""")

t('Bestimme, wo `f(x) = x² − 6x` steigt.', body='solveset(diff(x**2 - 6*x, x) > 0, x, domain=S.Reals)')
t('Bestimme, wo `f(x) = −x³ + 12x` fällt.', body='solveset(diff(-x**3 + 12*x, x) < 0, x, domain=S.Reals)')
t('Prüfe mit `is_increasing()`, ob `f(x) = x³ + x` auf ganz ℝ steigt.', body='is_increasing(x**3 + x, S.Reals)')
t('Prüfe mit `is_decreasing()`, ob `f(x) = 1/x` auf dem Intervall (0, ∞) fällt.', body='is_decreasing(1 / x, Interval.open(0, oo))')
t('Bestimme die Monotonie-Intervalle von `f(x) = x⁴ − 2x²`: Gib aus, wo f steigt und wo f fällt.',
  body='f1 = diff(x**4 - 2*x**2, x)\ndisplay(solveset(f1 > 0, x, domain=S.Reals))\nsolveset(f1 < 0, x, domain=S.Reals)')
t('Zeichne `f(x) = x³ − 3x` und `f\'(x)` in ein Diagramm für x von −2,5 bis 2,5. Wo f\' positiv ist, steigt f.',
  body='f = x**3 - 3*x\nplot(f, diff(f, x), (x, -2.5, 2.5), ylim=(-5, 8), legend=True);')

# ---------------------------------------------------------------- 6
sec('Extrempunkte')
expl('''#### Hoch- und Tiefpunkte

An einer Extremstelle hat der Graph eine waagerechte Tangente: f'(x) = 0 (**notwendige Bedingung**).
Ob es ein Hoch- oder Tiefpunkt ist, entscheidet die zweite Ableitung (**hinreichende Bedingung**):

- f'(x₀) = 0 und f''(x₀) < 0: **Hochpunkt** (lokales Maximum)
- f'(x₀) = 0 und f''(x₀) > 0: **Tiefpunkt** (lokales Minimum)
- Ist f''(x₀) = 0, hilft ein Vorzeichenwechsel von f'.

Ein **lokales** Maximum ist der größte Wert in der Umgebung, ein **globales** der größte Wert überhaupt (auf einem Intervall).
`maximum(f, x, Interval(a, b))` liefert den globalen größten Wert auf dem Intervall.''',
     """f = x**3 - 3*x
f1 = diff(f, x)
f2 = diff(f, x, 2)
for xe in solve(f1, x):
    art = 'Hochpunkt' if f2.subs(x, xe) < 0 else 'Tiefpunkt'
    print(art, (xe, f.subs(x, xe)))
maximum(f, x, Interval(-2, 3))""")

t('Bestimme die Extremstelle von `f(x) = x² − 8x + 3`. Gib den Punkt als Tupel aus und darunter, ob `f\'\'` dort positiv ist (dann ist es ein Tiefpunkt).',
  body="f = x**2 - 8*x + 3\nxe = solve(diff(f, x), x)[0]\ndisplay((xe, f.subs(x, xe)))\ndiff(f, x, 2).subs(x, xe) > 0")
t('Bestimme die Hoch- und Tiefpunkte von `f(x) = x³ − 12x`. Gib für jede Extremstelle Art und Punkt aus (wie im Beispiel mit `print`).',
  body="f = x**3 - 12*x\nfor xe in solve(diff(f, x), x):\n    art = 'Hochpunkt' if diff(f, x, 2).subs(x, xe) < 0 else 'Tiefpunkt'\n    print(art, (xe, f.subs(x, xe)))")
t('Bestimme die Extrempunkte von `f(x) = −x⁴ + 2x²`.',
  body="f = -x**4 + 2*x**2\nfor xe in solve(diff(f, x), x):\n    art = 'Hochpunkt' if diff(f, x, 2).subs(x, xe) < 0 else 'Tiefpunkt'\n    print(art, (xe, f.subs(x, xe)))")
t('Bestimme die Extremstellen von `f(x) = x³ − 6x² + 9x + 1` und die zugehörigen Werte von `f\'\'`.',
  body='f = x**3 - 6*x**2 + 9*x + 1\nl = solve(diff(f, x), x)\ndisplay(l)\n[diff(f, x, 2).subs(x, w) for w in l]')
t('''`f(x) = x⁴` hat bei 0 die Ableitung 0 und auch `f''(0) = 0`. Prüfe das Vorzeichen von `f'` links und rechts von 0 (bei −0,1 und 0,1).''',
  body="f1 = diff(x**4, x)\ndisplay(f1.subs(x, 0), diff(x**4, x, 2).subs(x, 0))\n[f1.subs(x, Rational(-1, 10)), f1.subs(x, Rational(1, 10))]")
t('Bestimme den größten und den kleinsten Wert von `f(x) = x³ − 3x` auf dem Intervall [−3, 2] (globale Extrema).',
  body='f = x**3 - 3*x\ndisplay(maximum(f, x, Interval(-3, 2)))\nminimum(f, x, Interval(-3, 2))')
t('Bestimme die Extrempunkte von `f(x) = sin(x) + cos(x)` im Intervall [0, 2π]. Gib die Stellen (mit `solveset`) und die Funktionswerte aus.',
  body="f = sin(x) + cos(x)\nstellen = solveset(diff(f, x), x, domain=Interval(0, 2*pi))\ndisplay(stellen)\n[simplify(f.subs(x, w)) for w in stellen]")
predict("""f = x**2
display(solve(diff(f, x), x))
display(diff(f, x, 2))
solve(diff(x**3, x), x)""")

# ---------------------------------------------------------------- 7
sec('Krümmung und Wendepunkte')
expl("""#### Krümmungsverhalten und Wendepunkte

- f''(x) > 0: Der Graph ist **linksgekrümmt** (wie eine nach oben offene Schale), f' steigt.
- f''(x) < 0: Der Graph ist **rechtsgekrümmt**, f' fällt.
- An einem **Wendepunkt** wechselt die Krümmung: f''(x₀) = 0 und f'''(x₀) ≠ 0.
  Ein Wendepunkt mit waagerechter Tangente (f'(x₀) = 0) heißt **Sattelpunkt**.""",
     """f = x**3 - 3*x**2 + 1
f2 = diff(f, x, 2)
display(f2)
display(solveset(f2 > 0, x, domain=S.Reals))
xw = solve(f2, x)[0]
display(diff(f, x, 3).subs(x, xw))
(xw, f.subs(x, xw))""")

t('Bestimme den Wendepunkt von `f(x) = x³ + 3x²` als Tupel.', body='f = x**3 + 3*x**2\nxw = solve(diff(f, x, 2), x)[0]\n(xw, f.subs(x, xw))')
t('Bestimme, wo der Graph von `f(x) = x³ + 3x²` linksgekrümmt ist.', body='solveset(diff(x**3 + 3*x**2, x, 2) > 0, x, domain=S.Reals)')
t('Bestimme die Wendestellen von `f(x) = x⁴ − 6x²`.', body='solve(diff(x**4 - 6*x**2, x, 2), x)')
t('Prüfe, ob `f(x) = x³` bei 0 einen Sattelpunkt hat: Gib `f\'(0)`, `f\'\'(0)` und `f\'\'\'(0)` als Liste aus.',
  body='[diff(x**3, x, k).subs(x, 0) for k in range(1, 4)]')
t('Bestimme die Wendetangente von `f(x) = x³ − 3x² + 1` (Tangente im Wendepunkt).',
  body='f = x**3 - 3*x**2 + 1\nxw = solve(diff(f, x, 2), x)[0]\nm = diff(f, x).subs(x, xw)\nexpand(m * (x - xw) + f.subs(x, xw))')
t('Zeichne `f(x) = x³ − 3x² + 1`, `f\'` und `f\'\'` für x von −1,5 bis 3,5 mit Legende.',
  body='f = x**3 - 3*x**2 + 1\nplot(f, diff(f, x), diff(f, x, 2), (x, -1.5, 3.5), ylim=(-6, 8), legend=True);')

# ---------------------------------------------------------------- 8
sec('Kurvendiskussion')
expl('''#### Eine Funktion vollständig untersuchen

Eine **Kurvendiskussion** fasst alles zusammen: Symmetrie, Nullstellen, Verhalten für x → ±∞, Extrempunkte, Wendepunkte, Graph.
Mit sympy prüfst du jeden Schritt.''',
     """f = x**4 / 4 - 2*x**2
display(simplify(f.subs(x, -x) - f) == 0)
display(solve(f, x))
display(limit(f, x, oo))
f1, f2 = diff(f, x), diff(f, x, 2)
print('Extremstellen:', solve(f1, x), [f2.subs(x, w) for w in solve(f1, x)])
print('Wendestellen:', solve(f2, x))
plot(f, (x, -3.2, 3.2), ylim=(-5, 5));""")

t('''Untersuche `f(x) = x³ − 3x`: Gib Nullstellen, Extremstellen mit Art (Werte von f'') und Wendestelle jeweils mit `display()` aus und zeichne den Graphen
für x von −2,2 bis 2,2.''',
  body='f = x**3 - 3*x\ndisplay(solve(f, x))\nl = solve(diff(f, x), x)\ndisplay(l, [diff(f, x, 2).subs(x, w) for w in l])\ndisplay(solve(diff(f, x, 2), x))\nplot(f, (x, -2.2, 2.2));')
t('''Untersuche `f(x) = −x³ + 3x² − 4`: Gib Nullstellen mit Vielfachheit (`roots`), Extrempunkte und Wendepunkt (als Tupel) aus.''',
  body='f = -x**3 + 3*x**2 - 4\ndisplay(roots(f, x))\ndisplay([(w, f.subs(x, w)) for w in solve(diff(f, x), x)])\nxw = solve(diff(f, x, 2), x)[0]\n(xw, f.subs(x, xw))')
t('''Untersuche `f(x) = x⁴ − 4x³`: Gib die Extrempunkte, die Wendepunkte (als Tupel) und den Graphen für x von −1,5 bis 4,5 aus.''',
  body='f = x**4 - 4*x**3\ndisplay([(w, f.subs(x, w)) for w in solve(diff(f, x), x)])\ndisplay([(w, f.subs(x, w)) for w in solve(diff(f, x, 2), x)])\nplot(f, (x, -1.5, 4.5));')

# ---------------------------------------------------------------- 9
sec('Optimierungsaufgaben')
expl('''#### Extremwertaufgaben

So geht man vor:
1. **Zielfunktion** aufstellen (die Größe, die maximal oder minimal werden soll).
2. Mit einer **Nebenbedingung** auf eine Variable reduzieren.
3. **Definitionsbereich** überlegen.
4. Ableitung null setzen, Art prüfen, auch die Ränder betrachten.

Beispiel: Aus einem 20 cm × 20 cm großen Blech wird eine oben offene Schachtel gefaltet, indem man an den Ecken Quadrate der Seite x ausschneidet.
Das Volumen ist V(x) = x(20 − 2x)² mit 0 < x < 10.''',
     """V = x * (20 - 2*x)**2
l = solveset(diff(V, x), x, domain=Interval.open(0, 10))
display(l)
xopt = list(l)[0]
display(diff(V, x, 2).subs(x, xopt))
display(V.subs(x, xopt))
plot(V, (x, 0, 10));""")

t('''Ein rechteckiger Garten soll mit 40 m Zaun eingezäunt werden. Welche Maße ergeben den größten Flächeninhalt? Sei x die Breite, die Länge ist 20 − x.
Gib die optimale Breite und den größten Flächeninhalt aus.''',
  body='A = x * (20 - x)\nxopt = solve(diff(A, x), x)[0]\ndisplay(xopt)\nA.subs(x, xopt)')
t('''Ein Garten liegt an einer Mauer, nur drei Seiten werden mit 60 m Zaun eingezäunt: zwei Seiten der Länge x und eine der Länge 60 − 2x.
Gib die optimale Seitenlänge x und den größten Flächeninhalt aus.''',
  body='A = x * (60 - 2*x)\nxopt = solve(diff(A, x), x)[0]\ndisplay(xopt)\nA.subs(x, xopt)')
t('''Aus einem 30 cm × 16 cm großen Karton wird eine oben offene Schachtel gefaltet (Eckquadrate der Seite x). Das Volumen ist `x(30 − 2x)(16 − 2x)` mit 0 < x < 8.
Gib die optimale Seite x und das größte Volumen aus.''',
  body='V = x * (30 - 2*x) * (16 - 2*x)\nxopt = list(solveset(diff(V, x), x, domain=Interval.open(0, 8)))[0]\ndisplay(xopt)\nV.subs(x, xopt)')
t('''Die Summe zweier positiver Zahlen ist 12. Wann ist das Produkt aus der ersten Zahl und dem Quadrat der zweiten am größten? Sei x die erste Zahl.
Gib die erste Zahl und das größte Produkt aus.''',
  body='P = x * (12 - x)**2\nxopt = list(solveset(diff(P, x), x, domain=Interval.open(0, 12)))[0]\ndisplay(xopt)\nP.subs(x, xopt)')
t('''**Dose:** Eine zylindrische Dose soll 1 Liter (1000 cm³) fassen und möglichst wenig Blech verbrauchen. Mit dem Radius r ist die Höhe h = 1000/(πr²)
und die Oberfläche O(r) = 2πr² + 2000/r. Gib den optimalen Radius exakt und mit 4 Ziffern sowie die zugehörige Höhe mit 4 Ziffern aus.''',
  given="r = symbols('r', positive=True)",
  body='O = 2*pi*r**2 + 2000 / r\nropt = solve(diff(O, r), r)[0]\ndisplay(ropt, N(ropt, 4))\nN(1000 / (pi * ropt**2), 4)')
t('''Welcher Punkt auf der Parabel `y = x²` liegt dem Punkt (0, 3) am nächsten? Minimiere das Quadrat des Abstands `d(x) = x² + (x² − 3)²`.
Gib die x-Werte und den kleinsten Abstand aus.''',
  body='d = x**2 + (x**2 - 3)**2\nl = [w for w in solve(diff(d, x), x) if diff(d, x, 2).subs(x, w) > 0]\ndisplay(l)\nsqrt(d.subs(x, l[0]))')

# ---------------------------------------------------------------- 10
sec('Gemischte Übungen')
t('''Bestimme eine Parabel `f(x) = ax² + bx + c`, die durch (0, 1) geht und bei x = 2 einen Tiefpunkt mit dem Funktionswert −3 hat.
Stelle dazu drei Gleichungen auf (f(0) = 1, f(2) = −3, f'(2) = 0) und löse sie.''',
  given="c = symbols('c')",
  body='f = a*x**2 + b*x + c\nl = solve([Eq(f.subs(x, 0), 1), Eq(f.subs(x, 2), -3), Eq(diff(f, x).subs(x, 2), 0)], [a, b, c])\nf.subs(l)')
t('''Ein Körper bewegt sich nach dem Weg-Zeit-Gesetz `s(t) = t³ − 6t² + 9t` (t in s, s in m). Die Geschwindigkeit ist s'(t), die Beschleunigung s''(t).
Gib v(t) und a(t) aus und die Zeitpunkte, zu denen der Körper stillsteht.''',
  given="t = symbols('t')",
  body='s = t**3 - 6*t**2 + 9*t\nv = diff(s, t)\ndisplay(v, diff(s, t, 2))\nsolve(v, t)')
t('''Für welchen Wert von `k` hat `f(x) = x³ − kx` an der Stelle x = 2 eine waagerechte Tangente?''',
  given="k = symbols('k')", body='solve(Eq(diff(x**3 - k*x, x).subs(x, 2), 0), k)')
t('''Bestimme die Gleichungen der beiden Tangenten an `f(x) = x²`, die durch den Punkt (0, −1) gehen. Für den Berührpunkt bei x₀ = u gilt:
Die Tangente u-abhängig aufstellen und den Punkt (0, −1) einsetzen.''',
  given="u = symbols('u')",
  body='tang = 2*u*(x - u) + u**2\nl = solve(Eq(tang.subs(x, 0), -1), u)\n[expand(tang.subs(u, w)) for w in l]')
t('''Ein Unternehmen hat die Kostenfunktion `K(x) = x³ − 6x² + 15x + 10` und verkauft zum Preis von 12 pro Stück. Der Gewinn ist `G(x) = 12x − K(x)`.
Bei welcher Menge x > 0 ist der Gewinn maximal? Gib die Menge (mit 4 Ziffern) und den Gewinn (mit 4 Ziffern) aus.''',
  body='G = 12*x - (x**3 - 6*x**2 + 15*x + 10)\nl = [w for w in solve(diff(G, x), x) if diff(G, x, 2).subs(x, w) < 0]\ndisplay(N(l[0], 4))\nN(G.subs(x, l[0]), 4)')

generate('sympy_ableitungen', 'Ableitungen: Änderungsrate, Tangente, Extrem- und Wendepunkte', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
