# Erzeugt ../content/sympy_komplexe_zahlen.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_komplexe_zahlen.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_komplexe_zahlen.py
#
# Vertiefungskurs Mathematik BW: komplexe Zahlen (imaginäre Einheit, Rechnen in algebraischer Form, Konjugation, Betrag),
# Gaußsche Zahlenebene, Polar- und Exponentialform, Multiplikation als Drehstreckung, Satz von Moivre, Eulersche Formel,
# Einheitswurzeln, Lösen von Polynomgleichungen (Fundamentalsatz der Algebra), Anwendungen (trigonometrische Formeln).
# sympy: Produkte/Quotienten werden nicht automatisch ausmultipliziert (expand); roots() liefert ein Dictionary (Reihenfolge
# nicht verlässlich) → solve() verwenden.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = ("from sympy import *\ninit_printing()\nimport matplotlib.pyplot as plt\nz = symbols('z')\n"
         "a, b, r, phi = symbols('a b r phi', real=True)")

INTRO = '''In diesem Notebook (Vertiefungskurs) geht es um **komplexe Zahlen**. Mit der **imaginären Einheit** i, für die i² = −1 gilt,
hat jede quadratische Gleichung Lösungen, und jedes Polynom vom Grad n hat genau n Nullstellen. Komplexe Zahlen kann man als Punkte
der **Gaußschen Zahlenebene** darstellen; Multiplizieren bedeutet dort Drehen und Strecken.

In sympy ist die imaginäre Einheit `I` (großes i). **Verwende `I` deshalb nicht als eigenen Variablennamen.**

Vorausgesetzt werden die Notebooks *Gleichungen* und *Geometrie* (Trigonometrie).

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy und matplotlib, schaltet die Formel-Ausgabe ein
und legt die komplexe Variable `z` und die reellen Variablen `a`, `b`, `r`, `phi` an.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Die imaginäre Einheit')
expl('''#### i² = −1

Die Gleichung x² = −1 hat keine reelle Lösung. Man erweitert die Zahlen um die **imaginäre Einheit** i mit i² = −1.
Eine **komplexe Zahl** ist z = a + b·i mit reellen Zahlen a (**Realteil**) und b (**Imaginärteil**).

In sympy: `I`. Wurzeln aus negativen Zahlen sind jetzt erlaubt: √(−4) = 2i. `solve()` gibt bei Gleichungen ohne reelle Lösung
die komplexen Lösungen aus (wenn die Variable nicht als reell angelegt ist).''',
     """display(I**2, I**3, I**4)
display(sqrt(-4), sqrt(-7))
solve(z**2 + 2*z + 5, z)""")

t('Gib i⁵, i⁶, i⁷ und i⁸ als Liste aus.', body='[I**m for m in range(5, 9)]')
t('Gib i¹⁰⁰ und i²⁰²³ aus. (Tipp für die Rechnung von Hand: i⁴ = 1.)', body='display(I**100)\nI**2023')
t('Gib √(−9), √(−12) und √(−1/4) aus.', body='display(sqrt(-9), sqrt(-12))\nsqrt(Rational(-1, 4))')
t('Löse z² = −16.', body='solve(Eq(z**2, -16), z)')
t('Löse z² − 4z + 13 = 0 und prüfe die Lösungen durch Einsetzen (`expand`).', body='l = solve(z**2 - 4*z + 13, z)\ndisplay(l)\n[expand(w**2 - 4*w + 13) for w in l]')
t('Löse z² + z + 1 = 0.', body='solve(z**2 + z + 1, z)')
t('''Berechne die Lösungen von z² + 6z + 10 = 0 mit der Mitternachtsformel z = (−p ± √D)/2 (`sqrt` einer negativen Zahl) und vergleiche mit `solve`.''',
  body='D = 6**2 - 4 * 10\ndisplay(D)\ndisplay([(-6 - sqrt(D)) / 2, (-6 + sqrt(D)) / 2])\nsolve(z**2 + 6*z + 10, z)')
predict("""display(I * I)
display(1 / I)
display(sqrt(-1))
(2 * I)**2""")

# ---------------------------------------------------------------- 2
sec('Rechnen mit komplexen Zahlen')
expl('''#### Grundrechenarten, Konjugation, Betrag

Man rechnet wie mit Termen und ersetzt i² durch −1. sympy multipliziert Produkte **nicht** automatisch aus: Mit `expand()`
bekommt man die Form a + b·i.

- `re(z)`, `im(z)`: Real- und Imaginärteil
- `conjugate(z)`: die **konjugierte** Zahl z̄ = a − b·i
- `Abs(z)`: der **Betrag** |z| = √(a² + b²); es gilt z · z̄ = |z|²
- **Division:** Man erweitert mit dem konjugierten Nenner, dann wird der Nenner reell. `expand()` erledigt das.''',
     """z1 = 3 + 4*I
z2 = 1 - 2*I
display(z1 + z2, z1 * z2, expand(z1 * z2))
display(re(z1), im(z1), conjugate(z1), Abs(z1))
display(expand(z1 * conjugate(z1)))
display(expand(z1 * conjugate(z2)), expand(z2 * conjugate(z2)))
expand(z1 / z2)""")

Z = "z1 = 2 + 3*I\nz2 = 4 - I"
t('Berechne für z₁ = 2 + 3i und z₂ = 4 − i die Summe, die Differenz und das Produkt (ausmultipliziert).', Z,
  'display(z1 + z2, z1 - z2)\nexpand(z1 * z2)')
t('Berechne z₁/z₂ für dieselben Zahlen in der Form a + b·i.', Z, 'expand(z1 / z2)')
t('Berechne z₁/z₂ von Hand nach: Gib den Zähler z₁·z̄₂ und den Nenner z₂·z̄₂ ausmultipliziert aus.', Z,
  'display(expand(z1 * conjugate(z2)))\nexpand(z2 * conjugate(z2))')
t('Gib Real- und Imaginärteil, die konjugierte Zahl und den Betrag von z = −5 + 12i aus.',
  body='w = -5 + 12*I\ndisplay(re(w), im(w))\ndisplay(conjugate(w))\nAbs(w)')
t('Berechne (1 + i)², (1 + i)⁴ und (1 + i)⁸ (ausmultipliziert).', body='[expand((1 + I)**m) for m in [2, 4, 8]]')
t('Berechne 1/(1 + i) und (2 + i)/(2 − i) in der Form a + b·i.', body='display(expand(1 / (1 + I)))\nexpand((2 + I) / (2 - I))')
t('''Zeige allgemein: Für z = a + b·i ist z · z̄ = a² + b² (reell!). Gib das Produkt ausmultipliziert aus.''',
  body='w = a + b*I\nexpand(w * conjugate(w))')
t('''Zeige allgemein: Der Betrag eines Produkts ist das Produkt der Beträge. Gib für z₁ = a + bi, z₂ = 3 + 4i die Differenz |z₁ · z₂| − |z₁| · |z₂| vereinfacht aus.''',
  body='w = a + b*I\nsimplify(Abs(expand(w * (3 + 4*I))) - Abs(w) * Abs(3 + 4*I))')
t('''Löse die Gleichung (2 + i)·z = 3 − i nach z auf.''', body='solve(Eq((2 + I) * z, 3 - I), z)')
t('''Für welche reellen a und b gilt (a + b·i)·(1 + 2i) = 7 + 4i? Vergleiche Real- und Imaginärteil (zwei Gleichungen, `solve`).''',
  body='w = expand((a + b*I) * (1 + 2*I))\nsolve([Eq(re(w), 7), Eq(im(w), 4)], [a, b])')
predict("""w = 3 - 4*I
display(re(w))
display(im(w))
display(Abs(w))
conjugate(conjugate(w))""")

# ---------------------------------------------------------------- 3
sec('Die Gaußsche Zahlenebene')
expl('''#### Komplexe Zahlen als Punkte und Pfeile

Die Zahl z = a + b·i wird als Punkt (a | b) gezeichnet: Realteil nach rechts, Imaginärteil nach oben.
- |z| ist der **Abstand** vom Ursprung, das **Argument** arg(z) der **Winkel** zur positiven reellen Achse (`arg(z)`, im Bogenmaß).
- **Addition** ist Vektoraddition (Pfeile aneinanderhängen).
- **Konjugieren** spiegelt an der reellen Achse.

Zum Zeichnen braucht matplotlib Kommazahlen: `float(re(z))`.''',
     """w = 3 + 4*I
display(Abs(w), arg(w), N(deg(arg(w)), 4))
punkte = [3 + 4*I, 1 - 2*I, 4 + 2*I, 3 - 4*I]
for p in punkte:
    plt.plot([0, float(re(p))], [0, float(im(p))], 'o-')
plt.axhline(0, color='black')
plt.axvline(0, color='black')
plt.gca().set_aspect('equal')
plt.show()""")

t('Gib Betrag und Argument (genau und in Grad) von z = 1 + i aus.', body='w = 1 + I\ndisplay(Abs(w), arg(w))\ndeg(arg(w))')
t('Gib die Argumente von 1, i, −1 und −i in Grad als Liste aus.', body='[deg(arg(w)) for w in [1, I, -1, -I]]')
t('Gib Betrag und Argument (in Grad, 4 Ziffern) von z = −3 + 2i aus.', body='w = -3 + 2*I\ndisplay(Abs(w))\nN(deg(arg(w)), 4)')
t('Wie weit sind z₁ = 1 + 2i und z₂ = 4 − 2i in der Zahlenebene voneinander entfernt? (|z₁ − z₂|)', body='Abs((1 + 2*I) - (4 - 2*I))')
t('''Multipliziere z = 3 + 2i viermal hintereinander mit i und gib die Zahlen als Liste aus. Zeichne die fünf Punkte (z, iz, i²z, ...) in die Zahlenebene.''',
  body="liste = [expand(I**m * (3 + 2*I)) for m in range(5)]\ndisplay(liste)\nplt.plot([float(re(p)) for p in liste], [float(im(p)) for p in liste], 'o-')\nplt.gca().set_aspect('equal')\nplt.show()")
t('''Zeichne z₁ = 3 + i, z₂ = 1 + 2i und ihre Summe als Pfeile vom Ursprung (wie im Beispiel).''',
  body="for p in [3 + I, 1 + 2*I, 4 + 3*I]:\n    plt.plot([0, float(re(p))], [0, float(im(p))], 'o-')\nplt.gca().set_aspect('equal')\nplt.show()")
t('''Bestimme alle z = a + bi mit |z| = 5 und Re(z) = 3 (zwei Lösungen: löse a = 3, a² + b² = 25).''',
  body='l = solve([Eq(a, 3), Eq(a**2 + b**2, 25)], [a, b])\n[w[0] + w[1] * I for w in l]')

# ---------------------------------------------------------------- 4
sec('Polarform und Exponentialform')
expl('''#### z = r · (cos φ + i · sin φ) = r · e^(iφ)

Mit Betrag r = |z| und Argument φ = arg(z) schreibt man z in **Polarform** z = r · (cos φ + i sin φ). Nach der **Eulerschen Formel**
e^(iφ) = cos φ + i sin φ ist das z = r · e^(iφ) (**Exponentialform**). Berühmt: e^(iπ) + 1 = 0.

`expand_complex(...)` wandelt in die Form a + b·i um.

**Multiplikation:** Beträge multiplizieren, Argumente addieren: r₁e^(iφ₁) · r₂e^(iφ₂) = r₁r₂ · e^(i(φ₁ + φ₂)) (eine **Drehstreckung**).
**Satz von Moivre:** (r e^(iφ))ⁿ = rⁿ · e^(inφ).''',
     """display(expand_complex(exp(I * phi)))
display(exp(I * pi) + 1)
w = 2 * exp(I * pi / 3)
display(expand_complex(w))
display(Abs(w), arg(w))
display(expand_complex(w**3))
expand_complex(2 * exp(I * pi / 4) * 3 * exp(I * pi / 2))""")

t('Wandle z = 4 · e^(iπ/6) in die Form a + b·i um.', body='expand_complex(4 * exp(I * pi / 6))')
t('Wandle z = 2 · (cos(3π/4) + i sin(3π/4)) in die Form a + b·i um.', body='2 * (cos(3*pi/4) + I * sin(3*pi/4))')
t('Gib die Exponentialform von z = 1 + √3·i aus: Betrag und Argument berechnen, dann `r * exp(I * phi)` mit diesen Werten.',
  body='w = 1 + sqrt(3) * I\nr0, p0 = Abs(w), arg(w)\ndisplay(r0, p0)\nr0 * exp(I * p0)')
t('Gib die Exponentialform von z = −2 − 2i aus.', body='w = -2 - 2*I\nAbs(w) * exp(I * arg(w))')
t('''Berechne (1 + i)²⁰ mit dem Satz von Moivre: (√2)²⁰ · e^(i·20·π/4). Gib das Ergebnis mit `expand_complex` aus und vergleiche mit `expand((1 + I)**20)`.''',
  body='display(expand_complex(sqrt(2)**20 * exp(I * 20 * pi / 4)))\nexpand((1 + I)**20)')
t('''Multipliziere z₁ = 3 · e^(iπ/6) und z₂ = 2 · e^(iπ/3): Gib das Produkt in Exponentialform (Beträge mal, Argumente plus) und als a + b·i aus.''',
  body='display(6 * exp(I * (pi/6 + pi/3)))\nexpand_complex(3 * exp(I * pi / 6) * 2 * exp(I * pi / 3))')
t('''Beweise mit der Eulerschen Formel: Gib e^(iφ) · e^(−iφ) vereinfacht und Re(e^(iφ)) und Im(e^(iφ)) aus.''',
  body='display(simplify(exp(I * phi) * exp(-I * phi)))\ndisplay(re(exp(I * phi)))\nim(exp(I * phi))')
t('''**Drehung:** Drehe den Punkt z = 4 + i um 60° gegen den Uhrzeigersinn um den Ursprung (multipliziere mit e^(iπ/3)). Gib das Ergebnis als a + b·i aus.''',
  body='expand(expand_complex((4 + I) * exp(I * pi / 3)))')
predict("""display(exp(I * pi / 2))
display(exp(2 * pi * I))
display(Abs(exp(I * 5)))
exp(I * pi) * exp(I * pi)""")

# ---------------------------------------------------------------- 5
sec('Polynomgleichungen und Einheitswurzeln')
expl('''#### Fundamentalsatz der Algebra

Jedes Polynom vom Grad n hat (mit Vielfachheit gezählt) genau **n komplexe Nullstellen** und zerfällt in n Linearfaktoren.
Bei Polynomen mit reellen Koeffizienten kommen nicht-reelle Nullstellen immer als **konjugiertes Paar** vor.

`factor(term, extension=I)` zerlegt auch mit komplexen Zahlen.

Die Lösungen von zⁿ = 1 heißen **n-te Einheitswurzeln**: zₖ = e^(2πik/n), k = 0, ..., n − 1. Sie bilden ein regelmäßiges n-Eck auf dem Einheitskreis.''',
     """display(solve(z**3 - 1, z))
display(factor(z**2 + 4, extension=I))
wurzeln = [exp(2 * pi * I * j / 6) for j in range(6)]
display([expand_complex(w) for w in wurzeln])
plt.plot([float(re(w)) for w in wurzeln] + [1], [float(im(w)) for w in wurzeln] + [0], 'o-')
plt.gca().set_aspect('equal')
plt.show()""")

t('Löse z⁴ = 1.', body='solve(z**4 - 1, z)')
t('Löse z⁴ = −16.', body='solve(z**4 + 16, z)')
t('Löse z³ = 8i.', body='solve(z**3 - 8*I, z)')
t('Löse z² = 3 + 4i und prüfe eine Lösung durch Quadrieren.', body='l = solve(z**2 - (3 + 4*I), z)\ndisplay(l)\nexpand(l[0]**2)')
t('Zerlege z⁴ − 1 vollständig in Linearfaktoren (`extension=I`).', body='factor(z**4 - 1, extension=I)')
t('''Das Polynom z³ − 3z² + 4z − 2 hat die Nullstelle z = 1. Bestimme alle Nullstellen und prüfe, dass die nicht-reellen konjugiert zueinander sind.''',
  body='l = solve(z**3 - 3*z**2 + 4*z - 2, z)\ndisplay(l)\nconjugate(l[1]) == l[2]')
t('''Gib die 8-ten Einheitswurzeln e^(2πik/8) (k = 0, ..., 7) in der Form a + b·i als Liste aus und ihre Summe.''',
  body='w8 = [expand_complex(exp(2 * pi * I * j / 8)) for j in range(8)]\ndisplay(w8)\nsimplify(sum(w8))')
t('''Zeichne die 5-ten Einheitswurzeln als regelmäßiges Fünfeck (wie im Beispiel, den ersten Punkt am Ende wiederholen).''',
  body="wurzeln = [exp(2 * pi * I * j / 5) for j in range(5)]\nplt.plot([float(re(w)) for w in wurzeln] + [1], [float(im(w)) for w in wurzeln] + [0], 'o-')\nplt.gca().set_aspect('equal')\nplt.show()")
t('''Gib ein Polynom mit reellen Koeffizienten an, das die Nullstellen 2 und 1 + i hat (dann auch 1 − i): (z − 2)(z − (1 + i))(z − (1 − i)) ausmultipliziert.''',
  body='expand((z - 2) * (z - (1 + I)) * (z - (1 - I)))')

# ---------------------------------------------------------------- 6
sec('Anwendungen')
expl('''#### Trigonometrische Formeln und Mengen in der Zahlenebene

**Formeln herleiten:** Nach Moivre ist (cos φ + i sin φ)³ = cos(3φ) + i sin(3φ). Multipliziert man links aus und vergleicht Real- und
Imaginärteil, erhält man Formeln für cos(3φ) und sin(3φ).

**Mengen:** |z − z₀| = r beschreibt einen **Kreis** um z₀ mit Radius r. Setzt man z = a + b·i ein, erhält man die Kreisgleichung.''',
     """links = expand((cos(phi) + I * sin(phi))**3)
display(links)
display(re(links), im(links))
w = a + b*I
expand(Abs(w - (1 + 2*I))**2)""")

t('Leite mit Moivre (n = 2) die Formeln für cos(2φ) und sin(2φ) her (Real- und Imaginärteil von (cos φ + i sin φ)²).',
  body='links = expand((cos(phi) + I * sin(phi))**2)\ndisplay(re(links))\nim(links)')
t('''Prüfe die Formel cos(3φ) = cos³φ − 3 cos φ sin²φ: `expand_trig(cos(3*phi))` schreibt cos(3φ) mit cos φ und sin φ.
Gib die vereinfachte Differenz aus (0 bedeutet: die Formel stimmt).''',
  body='simplify(expand_trig(cos(3*phi)) - (cos(phi)**3 - 3*cos(phi)*sin(phi)**2))')
t('Gib die Kreisgleichung für |z − (2 − i)| = 3 aus: Setze z = a + b·i ein und gib |z − z₀|² ausmultipliziert als Gleichung mit 9 aus.',
  body='w = a + b*I\nEq(expand(Abs(w - (2 - I))**2), 9)')
t('''Welche Menge beschreibt |z − 1| = |z + i|? Setze z = a + b·i ein, quadriere beide Seiten und vereinfache die Differenz (eine Gerade).''',
  body='w = a + b*I\nexpand(Abs(w - 1)**2 - Abs(w + I)**2)')
t('''**Wechselstrom (Zusatz):** In der Elektrotechnik rechnet man mit komplexen Widerständen. Ein Widerstand R = 30 Ω und eine Spule mit X = 40 Ω in Reihe ergeben
Z = 30 + 40i. Gib den Betrag (Scheinwiderstand) und den Phasenwinkel in Grad (4 Ziffern) aus.''',
  body='Zw = 30 + 40*I\ndisplay(Abs(Zw))\nN(deg(arg(Zw)), 4)')

# ---------------------------------------------------------------- 7
sec('Gemischte Übungen')
t('''Berechne ((1 + i)/(1 − i))¹⁰⁰.''', body='expand(((1 + I) / (1 - I))**100)')
t('''Berechne i^i (i hoch i): Schreibe i = e^(iπ/2), dann ist i^i = e^(i · iπ/2). Gib das Ergebnis genau und mit 5 Ziffern aus. (Es ist reell!)''',
  body='w = exp(I * pi / 2 * I)\ndisplay(w)\nN(w, 5)')
t('''Bestimme alle komplexen Lösungen von z⁶ + 7z³ − 8 = 0 (Substitution u = z³ von Hand, prüfe mit `solve`).''', body='solve(z**6 + 7*z**3 - 8, z)')
t('''Ein Quadrat hat die Ecken 0, 1, 1 + i und i. Drehe es um 45° und strecke es mit dem Faktor √2 (multipliziere mit 1 + i). Gib die neuen Ecken aus.''',
  body='[expand((1 + I) * w) for w in [0, 1, 1 + I, I]]')
t('''Zeige, dass die Summe der n-ten Einheitswurzeln 0 ist, für n = 3, 4, 5, 6 (Liste der Summen; vor `simplify` mit `expand_complex` in die Form a + b·i bringen).''',
  body='[simplify(expand_complex(sum([exp(2 * pi * I * j / m) for j in range(m)]))) for m in [3, 4, 5, 6]]')

generate('sympy_komplexe_zahlen', 'Komplexe Zahlen: Rechnen, Zahlenebene, Polarform, Einheitswurzeln', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
