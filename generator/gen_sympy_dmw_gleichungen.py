# Erzeugt ../content/sympy_dmw_gleichungen.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_dmw_gleichungen.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_dmw_gleichungen.py
#
# Wahlfach Digitale Mathematische Werkzeuge (BW 2016, Klassen 11/12), 3.1.1 Bekannte mathematische Fragestellungen weiterentwickeln:
# Gleichungslehre kulturhistorisch (Khayyam: x³ + px = q grafisch mit Kreis und Normalparabel; al-Chwarizmi, Cardano),
# Lösbarkeit und Lösungsanzahl kubischer Gleichungen, Notwendigkeit der komplexen Zahlen (Bombelli), Satz von Vieta und
# nichtlineare Gleichungssysteme mit komplexen Lösungen in der Gaußschen Zahlenebene, zⁿ = 1 und kubische Gleichungen komplex,
# Fundamentalsatz der Algebra, Lösungsmengen als algebraische Kurven.
# Kurven mit der Hilfsfunktion kurve() aus der Setup-Zelle (contour); plot_implicit ist in sympy 1.14 adaptiv nicht
# reproduzierbar (Hash-Reihenfolge) und mit adaptive=False fehlerhaft.
# sympy: cbrt() einer negativen Zahl ist die komplexe Hauptwurzel → real_root(a, 3) für die reelle Kubikwurzel.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = ("from sympy import *\ninit_printing()\nimport matplotlib.pyplot as plt\nimport numpy as np\n"
         "x, y = symbols('x y', real=True)\np, q = symbols('p q', real=True)\nz, w = symbols('z w')\n\n"
         "def kurve(*gleichungen, xb=(-3, 3), yb=(-3, 3), var=(x, y)):\n"
         "    \"\"\"Zeichnet die Lösungsmengen von Gleichungen mit zwei Variablen (jede in einer eigenen Farbe).\"\"\"\n"
         "    X, Y = np.meshgrid(np.linspace(*xb, 401), np.linspace(*yb, 401))\n"
         "    for i, gl in enumerate(gleichungen):\n"
         "        f = lambdify(var, gl.lhs - gl.rhs, 'numpy')\n"
         "        plt.contour(X, Y, f(X, Y) + 0 * X, [0], colors=f'C{i}')\n"
         "    plt.xlabel(str(var[0]))\n"
         "    plt.ylabel(str(var[1]))\n"
         "    plt.grid(True)\n"
         "    plt.gca().set_aspect('equal')\n"
         "    plt.show()")

INTRO = '''Dieses Notebook gehört zum Wahlfach **Digitale Mathematische Werkzeuge**. Es verfolgt eine alte Frage weiter: **Wie löst man Gleichungen?**
Für quadratische Gleichungen kennst du die Lösungsformel. Für **kubische** Gleichungen haben Mathematiker jahrhundertelang gesucht:
Omar Khayyam (um 1100) löste sie geometrisch, Cardano (1545) fand eine Formel und musste dabei mit „unmöglichen“ Wurzeln aus negativen Zahlen
rechnen. So entstanden die **komplexen Zahlen**. Am Ende siehst du, dass Lösungsmengen von Gleichungen mit zwei Variablen **Kurven** sind.

Vorausgesetzt werden die Notebooks *Gleichungen* und *Komplexe Zahlen*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy, matplotlib und numpy, schaltet die Formel-Ausgabe ein und legt die reellen Variablen `x`, `y`, `p`, `q` und die
komplexen Variablen `z`, `w` an.

Außerdem definiert sie die Hilfsfunktion `kurve`, die **Kurven zeichnet, die durch eine Gleichung gegeben sind**, auch wenn man nicht nach y auflösen kann:
`kurve(Eq(x**2 + y**2, 1), xb=(-2, 2), yb=(-2, 2))` zeichnet den Einheitskreis. Mehrere Gleichungen (durch Kommas getrennt) werden in verschiedenen Farben
in ein Bild gezeichnet. `xb` und `yb` sind die Bereiche, `var=(p, q)` wählt andere Variablen als x und y. (Die Funktion berechnet die linke minus die rechte
Seite auf einem Gitter von Punkten und lässt matplotlib die Linie zeichnen, auf der dieser Wert 0 ist.)''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Kubische Gleichungen geometrisch lösen (Khayyam)')
expl('''#### Kreis und Parabel

Omar Khayyam löste x³ + a²·x = a²·b (mit a, b > 0) ohne Formel, nur mit Kreis und Parabel:
- Parabel: x² = a·y
- Kreis mit dem Durchmesser von (0 | 0) bis (b | 0): (x − b/2)² + y² = (b/2)²

Die x-Koordinate des Schnittpunkts (außer dem Ursprung) ist die Lösung. Denn aus der Parabel folgt y = x²/a; eingesetzt in den Kreis
ergibt sich x · (x³/a² + x − b) = 0.

Für x³ + p·x = q ist also a = √p und b = q/p.''',
     """a, b = 2, 3
parabel = x**2 / a
display(expand(((x - Rational(b, 2))**2 + parabel**2 - Rational(b, 2)**2) * a**2))
s = solve(x**3 + a**2 * x - a**2 * b, x)
display(s)
kreis_oben = sqrt(Rational(b, 2)**2 - (x - Rational(b, 2))**2)
plot(parabel, kreis_oben, -kreis_oben, (x, 0, b), aspect_ratio=(1, 1), ylim=(-2, 2));""")

t('''Löse x³ + 4x = 16 wie Khayyam: a = 2, b = 4. Gib die reelle Lösung mit `real_roots` aus und prüfe, dass der Punkt (x | x²/a) auf dem Kreis
(x − b/2)² + y² = (b/2)² liegt (Differenz 0).''',
  body="a, b = 2, 4\nxs = real_roots(x**3 + 4*x - 16)[0]\ndisplay(xs)\nsimplify((xs - Rational(b, 2))**2 + (xs**2 / a)**2 - Rational(b, 2)**2)")
t('''Zeichne für x³ + 4x = 16 die Parabel x² = 2y und den Kreis (oberen und unteren Halbkreis) wie im Beispiel für 0 ≤ x ≤ 4.''',
  body="a, b = 2, 4\nkreis_oben = sqrt(Rational(b, 2)**2 - (x - Rational(b, 2))**2)\nplot(x**2 / a, kreis_oben, -kreis_oben, (x, 0, b), aspect_ratio=(1, 1), ylim=(-2.5, 2.5));")
t('''Bestimme für x³ + 9x = 18 die Parameter a = √p und b = q/p und die Lösung näherungsweise (4 Ziffern).''',
  body="pp, qq = 9, 18\ndisplay(sqrt(pp), Rational(qq, pp))\nN(real_roots(x**3 + pp*x - qq)[0], 4)")
t('''Zeichne die Parabel x² = 3y und den Kreis (x − 1)² + y² = 1 für x³ + 9x = 18 mit `kurve` in ein Bild (0 ≤ x ≤ 2, −1,2 ≤ y ≤ 1,2).''',
  body="kurve(Eq(x**2, 3*y), Eq((x - 1)**2 + y**2, 1), xb=(0, 2), yb=(-1.2, 1.2))")

# ---------------------------------------------------------------- 2
sec('Wie viele Lösungen hat eine kubische Gleichung?')
expl('''#### Graph und Diskriminante

Jede kubische Gleichung lässt sich durch eine Verschiebung x → x − b/3 auf die **reduzierte Form** x³ + p·x + q = 0 bringen.
Der Graph von f(x) = x³ + px + q kommt von −∞ und geht nach +∞, deshalb gibt es **mindestens eine** reelle Lösung, höchstens drei.

- `count_roots(polynom)` zählt die reellen Nullstellen, `real_roots(polynom)` gibt sie aus.
- Die **Diskriminante** Δ = −4p³ − 27q² (`discriminant(polynom, x)`) entscheidet: Δ > 0 drei verschiedene, Δ = 0 mehrfache, Δ < 0 eine reelle Lösung.''',
     """for pp, qq in [(-3, 1), (-3, 2), (-3, 3)]:
    f = x**3 + pp*x + qq
    print(f, '  Anzahl:', count_roots(f), '  Diskriminante:', discriminant(f, x))
plot(x**3 - 3*x + 1, x**3 - 3*x + 2, x**3 - 3*x + 3, (x, -2.5, 2), ylim=(-3, 6), legend=True);""")

t('Gib die Anzahl der reellen Lösungen und die Diskriminante von x³ − 6x + 2 = 0 aus.', body="f = x**3 - 6*x + 2\ndisplay(count_roots(f))\ndiscriminant(f, x)")
t('Gib die allgemeine Diskriminante von x³ + px + q aus.', body="discriminant(x**3 + p*x + q, x)")
t('''Für welche q hat x³ − 3x + q = 0 genau zwei verschiedene Lösungen (Diskriminante 0)? Gib die q-Werte und für jedes die Lösungen aus.''',
  body="qs = solve(discriminant(x**3 - 3*x + q, x), q)\ndisplay(qs)\n[solve(x**3 - 3*x + w, x) for w in qs]")
t('''Für welche q hat x³ − 3x + q = 0 drei verschiedene reelle Lösungen? (Lösungsmenge von Δ > 0 über ℝ)''',
  body="solveset(discriminant(x**3 - 3*x + q, x) > 0, q, S.Reals)")
t('''Bringe x³ + 6x² + 9x + 4 = 0 auf die reduzierte Form: Setze x = t − 2 ein (b/3 = 2) und multipliziere aus. Gib die reduzierte Gleichung und ihre Lösungen
in t aus und dann die Lösungen in x.''',
  given="t = symbols('t')",
  body="red = expand((t - 2)**3 + 6*(t - 2)**2 + 9*(t - 2) + 4)\ndisplay(red)\nlt = solve(red, t)\ndisplay(lt)\n[w - 2 for w in lt]")
t('''Zeichne in der p-q-Ebene die Kurve 4p³ + 27q² = 0 (`kurve` mit `var=(p, q)`, −4 ≤ p ≤ 1, −3 ≤ q ≤ 3). Auf der linken Seite zwischen den Ästen liegen
die Gleichungen mit drei reellen Lösungen.''',
  body="kurve(Eq(4*p**3 + 27*q**2, 0), xb=(-4, 1), yb=(-3, 3), var=(p, q))")
predict("""display(count_roots(x**3 - x))
display(count_roots(x**3 + x))
count_roots(x**3)""")

# ---------------------------------------------------------------- 3
sec('Die Formel von Cardano')
expl('''#### x = ∛(−q/2 + √D) + ∛(−q/2 − √D)

Für die reduzierte Gleichung x³ + px + q = 0 mit D = (q/2)² + (p/3)³ ≥ 0 liefert die **Formel von Cardano** eine Lösung:

x = ∛(−q/2 + √D) + ∛(−q/2 − √D)

**Achtung:** In sympy ist `cbrt(-8)` nicht −2, sondern eine komplexe Kubikwurzel. Für die **reelle** Kubikwurzel gibt es `real_root(a, 3)`.

Beispiel (Cardano selbst): x³ + 6x = 20.''',
     """pp, qq = 6, -20
D = (Rational(qq, 2))**2 + (Rational(pp, 3))**3
display(D)
x1 = real_root(-Rational(qq, 2) + sqrt(D), 3) + real_root(-Rational(qq, 2) - sqrt(D), 3)
display(x1)
display(N(x1))
display(N(cbrt(-8)), real_root(-8, 3))
solve(x**3 + pp*x + qq, x)""")

t('''Schreibe eine Funktion `cardano(pp, qq)`, die D und die Lösung nach der Formel von Cardano (mit `real_root`) als Paar zurückgibt (Zahlen mit `Rational`). Teste mit x³ + 6x − 20 = 0
und gib die Lösung mit `N()` aus.''',
  body="def cardano(pp, qq):\n    D = Rational(qq, 2)**2 + Rational(pp, 3)**3\n    return D, real_root(-Rational(qq, 2) + sqrt(D), 3) + real_root(-Rational(qq, 2) - sqrt(D), 3)\n\nD, x1 = cardano(6, -20)\ndisplay(D)\nN(x1)")
t('''Löse x³ + 3x − 4 = 0 mit der Formel von Cardano (Funktion von oben). Gib D und die Lösung mit 10 Ziffern aus und prüfe, dass x = 1 eine Lösung ist.''',
  body="def cardano(pp, qq):\n    D = Rational(qq, 2)**2 + Rational(pp, 3)**3\n    return D, real_root(-Rational(qq, 2) + sqrt(D), 3) + real_root(-Rational(qq, 2) - sqrt(D), 3)\n\nD, x1 = cardano(3, -4)\ndisplay(D, N(x1, 10))\n(1**3 + 3*1 - 4) == 0")
t('''Prüfe die Formel von Cardano allgemein: Setze u = ∛(−q/2 + √D) und v = ∛(−q/2 − √D). Zeige mit `expand`, dass u³ + v³ = −q und u³ · v³ = −(p/3)³ ist
(setze u³ und v³ direkt als −q/2 ± √D ein).''',
  given="D = (q / 2)**2 + (p / 3)**3",
  body="u3 = -q / 2 + sqrt(D)\nv3 = -q / 2 - sqrt(D)\ndisplay(expand(u3 + v3))\nexpand(u3 * v3)")
t('''**Al-Chwarizmi** löste quadratische Gleichungen x² + px = q mit „quadratischer Ergänzung“ als Flächen: x = √((p/2)² + q) − p/2. Löse x² + 10x = 39 so
und vergleiche mit `solve`.''',
  body="pp, qq = 10, 39\ndisplay(sqrt(Rational(pp, 2)**2 + qq) - Rational(pp, 2))\nsolve(x**2 + pp*x - qq, x)")

# ---------------------------------------------------------------- 4
sec('Warum man komplexe Zahlen braucht')
expl('''#### Bombellis Beispiel: x³ = 15x + 4

Die Gleichung x³ − 15x − 4 = 0 hat die Lösung x = 4 (Probe!) und noch zwei weitere reelle. Cardanos Formel liefert aber
D = (−2)² + (−5)³ = −121 < 0, also eine Wurzel aus einer **negativen** Zahl: x = ∛(2 + √−121) + ∛(2 − √−121).

Bombelli (1572) rechnete einfach weiter mit √−121 = 11i. Es gilt (2 + i)³ = 2 + 11i und (2 − i)³ = 2 − 11i, also
x = (2 + i) + (2 − i) = 4. Der Umweg über die komplexen Zahlen führt zu einer reellen Lösung, obwohl es **ohne** ihn nicht geht
(„casus irreducibilis“: drei reelle Lösungen, aber D < 0).

Mit `N(..., chop=True)` werden winzige Rundungsreste im Imaginärteil weggelassen.''',
     """display(Rational(-4, 2)**2 + Rational(-15, 3)**3)
display(sqrt(-121))
display(expand((2 + I)**3), expand((2 - I)**3))
display((2 + I) + (2 - I))
display(real_roots(x**3 - 15*x - 4))
[N(s, 5, chop=True) for s in solve(z**3 - 15*z - 4, z)]""")

t('Berechne D für x³ − 6x − 4 = 0 und gib die reellen Lösungen aus.', body="display(Rational(-4, 2)**2 + Rational(-6, 3)**3)\nreal_roots(x**3 - 6*x - 4)")
t('''Für x³ − 6x − 4 = 0 liefert Cardano x = ∛(2 + 2i) + ∛(2 − 2i). Prüfe: (−1 + i)³ = 2 + 2i. Gib (−1 + i)³ und (−1 − i)³ ausmultipliziert aus
und dann die Summe (−1 + i) + (−1 − i).''',
  body="display(expand((-1 + I)**3), expand((-1 - I)**3))\n(-1 + I) + (-1 - I)")
t('''Gib für x³ − 3x + 1 = 0 die Diskriminante D nach Cardano, die Anzahl der reellen Lösungen und alle Lösungen mit 5 Ziffern aus (`solve` mit z, `N` mit `chop=True`).''',
  body="display(Rational(1, 2)**2 + Rational(-3, 3)**3)\ndisplay(count_roots(x**3 - 3*x + 1))\n[N(s, 5, chop=True) for s in solve(z**3 - 3*z + 1, z)]")
t('''Bestimme alle Lösungen von z³ + z + 10 = 0 (eine reelle, zwei komplexe) und zeichne sie als Punkte in die Gaußsche Zahlenebene.''',
  body="l = solve(z**3 + z + 10, z)\ndisplay(l)\nplt.plot([float(re(s)) for s in l], [float(im(s)) for s in l], 'o')\nplt.axhline(0, color='black')\nplt.axvline(0, color='black')\nplt.gca().set_aspect('equal')\nplt.show()")

# ---------------------------------------------------------------- 5
sec('Satz von Vieta und nichtlineare Gleichungssysteme')
expl('''#### Summe und Produkt der Lösungen

**Satz von Vieta:** Hat x² + px + q = 0 die Lösungen x₁, x₂, dann gilt x₁ + x₂ = −p und x₁ · x₂ = q.
Bei kubischen Gleichungen x³ + ax² + bx + c = 0: x₁ + x₂ + x₃ = −a, x₁x₂ + x₁x₃ + x₂x₃ = b, x₁x₂x₃ = −c.

Umgekehrt: Sucht man zwei Zahlen mit gegebener Summe s und gegebenem Produkt P (das **nichtlineare** System z + w = s, z · w = P),
dann sind z und w die Lösungen von t² − s·t + P = 0. Ist die Diskriminante negativ, sind die Lösungen **komplex konjugiert**.''',
     """display(solve([Eq(z + w, 5), Eq(z * w, 6)], [z, w]))
l = solve([Eq(z + w, 2), Eq(z * w, 5)], [z, w])
display(l)
t_ = symbols('t')
solve(t_**2 - 2*t_ + 5, t_)""")

t('''Prüfe den Satz von Vieta für x² − 7x + 10 = 0: Gib die Lösungen, ihre Summe und ihr Produkt aus.''', body="l = solve(x**2 - 7*x + 10, x)\ndisplay(l)\n(l[0] + l[1], l[0] * l[1])")
t('''Prüfe den Satz von Vieta für die kubische Gleichung x³ − 6x² + 11x − 6 = 0 (Summe, Summe der Zweierprodukte, Produkt der drei Lösungen).''',
  body="a1, a2, a3 = solve(x**3 - 6*x**2 + 11*x - 6, x)\n(a1 + a2 + a3, a1*a2 + a1*a3 + a2*a3, a1*a2*a3)")
t('''Löse das System z + w = 4, z · w = 13 und zeichne die Lösungen z in die Gaußsche Zahlenebene.''',
  body="l = solve([Eq(z + w, 4), Eq(z * w, 13)], [z, w])\ndisplay(l)\nplt.plot([float(re(s[0])) for s in l], [float(im(s[0])) for s in l], 'o')\nplt.gca().set_aspect('equal')\nplt.show()")
t('''Löse das System x² + y² = 25, x · y = 12 (reell) und gib die Lösungspaare aus.''', body="solve([Eq(x**2 + y**2, 25), Eq(x * y, 12)], [x, y])")
t('''Löse das System x² + y² = 4, x + y = 3 (komplex, mit z und w) und gib die Lösungen aus. Es gibt keine reelle Lösung, weil die Gerade
x + y = 3 den Kreis nicht schneidet: Prüfe, dass ihr Abstand vom Ursprung (3/√2) größer als der Radius 2 ist (Wahrheitswert).''',
  body="display(solve([Eq(z**2 + w**2, 4), Eq(z + w, 3)], [z, w]))\n3 / sqrt(2) > 2")
t('''Stelle eine quadratische Gleichung auf, deren Lösungen 3 + 2i und 3 − 2i sind (nach Vieta: Summe und Produkt berechnen).''',
  given="t_ = symbols('t')",
  body="s = expand((3 + 2*I) + (3 - 2*I))\nP = expand((3 + 2*I) * (3 - 2*I))\ndisplay(s, P)\nt_**2 - s*t_ + P")

# ---------------------------------------------------------------- 6
sec('Potenzgleichungen und Fundamentalsatz der Algebra')
expl('''#### Jede Gleichung n-ten Grades hat n Lösungen

Die **n-ten Einheitswurzeln** (Lösungen von zⁿ = 1) liegen als regelmäßiges n-Eck auf dem Einheitskreis.
Der **Fundamentalsatz der Algebra** (Gauß, 1799) sagt: Jedes Polynom vom Grad n ≥ 1 hat in den komplexen Zahlen genau n Nullstellen
(mit Vielfachheit gezählt). Mit den komplexen Zahlen ist die Frage „Hat die Gleichung eine Lösung?“ also endgültig beantwortet.

Geometrisch: Multiplizieren mit einer Einheitswurzel e^(2πi/n) dreht um 360°/n; deshalb bilden die Lösungen ein regelmäßiges n-Eck.''',
     """l = solve(z**5 - 1, z)
display([N(s, 3, chop=True) for s in l])
plt.plot([float(re(s)) for s in l], [float(im(s)) for s in l], 'o')
plt.gca().set_aspect('equal')
plt.show()""")

t('Löse z³ = 1 und z³ = −1.', body="display(solve(z**3 - 1, z))\nsolve(z**3 + 1, z)")
t('Löse z⁴ = 16 und zeichne die Lösungen in die Zahlenebene.',
  body="l = solve(z**4 - 16, z)\ndisplay(l)\nplt.plot([float(re(s)) for s in l], [float(im(s)) for s in l], 'o')\nplt.gca().set_aspect('equal')\nplt.show()")
t('''Prüfe den Fundamentalsatz an Beispielen: Gib für z⁷ − 1, z⁴ + z + 1 und (z − 1)³(z + 2) die Anzahl der Nullstellen mit Vielfachheit aus
(`roots(...)` gibt ein Dictionary Nullstelle → Vielfachheit; summiere die Vielfachheiten mit `sum(roots(f).values())`, bei z⁴ + z + 1 mit `Poly(f, z).degree()`).''',
  body="display(sum(roots(z**7 - 1, z).values()))\ndisplay(Poly(z**4 + z + 1, z).degree(), len(solve(z**4 + z + 1, z)))\nsum(roots((z - 1)**3 * (z + 2), z).values())")
t('''Multipliziere die Einheitswurzel ζ = e^(2πi/6) nacheinander mit sich selbst (ζ¹, ..., ζ⁶) und gib die Ergebnisse in der Form a + bi aus.''',
  body="zeta = exp(2 * pi * I / 6)\n[expand_complex(zeta**k) for k in range(1, 7)]")
t('''Zerlege z³ − 1 in Linearfaktoren (`factor(..., extension=sqrt(3)*I)`).''', body="factor(z**3 - 1, extension=sqrt(3)*I)")

# ---------------------------------------------------------------- 7
sec('Lösungsmengen als algebraische Kurven')
expl('''#### Gleichungen in x und y

Die Lösungsmenge einer Gleichung mit zwei Variablen x und y ist eine **Kurve** in der Ebene, z. B. x² + y² = 1 (Kreis).
Ist die Gleichung ein Polynom in x und y, heißt die Kurve **algebraisch**. Die Hilfsfunktion `kurve` aus der Setup-Zelle zeichnet sie,
auch wenn man nicht nach y auflösen kann.

Bekannte Beispiele: das **Kartesische Blatt** x³ + y³ = 3xy, die **Lemniskate** (x² + y²)² = 2(x² − y²), **elliptische Kurven** y² = x³ + ax + b.''',
     """kurve(Eq(x**3 + y**3, 3*x*y))
display(Eq(x**3 + y**3, 3*x*y).subs({x: Rational(3, 2), y: Rational(3, 2)}))""")

t('Zeichne die Ellipse x²/9 + y²/4 = 1 mit `kurve` (−4 ≤ x, y ≤ 4).', body="kurve(Eq(x**2 / 9 + y**2 / 4, 1), xb=(-4, 4), yb=(-4, 4))")
t('Zeichne die Lemniskate (x² + y²)² = 2(x² − y²) (−2 ≤ x ≤ 2, −1 ≤ y ≤ 1).', body="kurve(Eq((x**2 + y**2)**2, 2*(x**2 - y**2)), xb=(-2, 2), yb=(-1, 1))")
t('Zeichne die elliptische Kurve y² = x³ − x (−2 ≤ x ≤ 3, −4 ≤ y ≤ 4).', body="kurve(Eq(y**2, x**3 - x), xb=(-2, 3), yb=(-4, 4))")
t('''Prüfe, welche der Punkte (0 | 0), (1 | 0), (2 | √6) und (2 | 3) auf der Kurve y² = x³ − x liegen (Liste von Wahrheitswerten).''',
  body="kurve = Eq(y**2, x**3 - x)\n[kurve.subs({x: a, y: b}) for a, b in [(0, 0), (1, 0), (2, sqrt(6)), (2, 3)]]")
t('''Berechne die Schnittpunkte des Kreises x² + y² = 5 mit der Hyperbel x · y = 2 und zeichne beide Kurven in ein Bild (−3 ≤ x, y ≤ 3).''',
  body="display(solve([Eq(x**2 + y**2, 5), Eq(x * y, 2)], [x, y]))\nkurve(Eq(x**2 + y**2, 5), Eq(x * y, 2))")
t('''Berechne die Schnittpunkte des Kreises x² + y² = 4 mit der Parabel y = x² − 2 und zeichne beide Kurven in ein Bild (−3 ≤ x, y ≤ 3).''',
  body="display(solve([Eq(x**2 + y**2, 4), Eq(y, x**2 - 2)], [x, y]))\nkurve(Eq(x**2 + y**2, 4), Eq(y, x**2 - 2))")

generate('sympy_dmw_gleichungen', 'DMW: Kubische Gleichungen, komplexe Zahlen und algebraische Kurven', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
