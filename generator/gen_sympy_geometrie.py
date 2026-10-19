# Erzeugt ../content/sympy_geometrie.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_geometrie.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_geometrie.py
#
# Bildungsplan BW 2016: Klassen 7/8 Raum und Form (Winkelsumme, Umkreis-/Inkreismittelpunkt, Strahlensätze),
# Klassen 9/10 Messen (Kreisbogen, Kreissektor, Bogenmaß, Oberfläche/Volumen von Prisma, Pyramide, Zylinder, Kegel, Kugel,
# Abstand zweier Punkte, Betrag eines Vektors) und Raum und Form (Ähnlichkeit, Pythagoras und Kehrsatz, sin/cos/tan,
# sin² + cos² = 1, Vektoren in Tupeldarstellung, Mittelpunkt, Kollinearität, Geraden im Raum, Lagebeziehung, Spurpunkte).
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = "from sympy import *\ninit_printing()\nx, y, z, s, t = symbols('x y z s t')"

INTRO = '''In diesem Notebook rechnest du **Geometrie** mit sympy: Satz des Pythagoras, Trigonometrie im rechtwinkligen Dreieck, Kreise und Körper,
Dreiecke mit Umkreis und Inkreis und schließlich **Vektoren** und **Geraden im Raum**. sympy rechnet dabei mit exakten Werten:
Eine Seitenlänge bleibt √2, ein Winkel π/4, solange du nicht mit `N()` eine Dezimalzahl verlangst.

Vorausgesetzt werden die Notebooks *Zahlen exakt*, *Terme* und *Gleichungen*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy, schaltet die Formel-Ausgabe ein
und legt die Variablen `x`, `y`, `z`, `s` und `t` an.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Satz des Pythagoras')
expl('''#### Seiten im rechtwinkligen Dreieck

Im rechtwinkligen Dreieck mit den Katheten a, b und der Hypotenuse c gilt **a² + b² = c²**.
Gilt umgekehrt a² + b² = c², so ist das Dreieck rechtwinklig (**Kehrsatz**).

sympy rechnet die Wurzel exakt: Die Diagonale eines Quadrats mit der Seite 1 ist √2.''',
     """display(sqrt(3**2 + 4**2))
display(sqrt(1**2 + 1**2))
display(sqrt(10**2 - 6**2))
5**2 + 12**2 == 13**2""")

t('Berechne die Hypotenuse eines rechtwinkligen Dreiecks mit den Katheten 8 und 15.', body='sqrt(8**2 + 15**2)')
t('Berechne die zweite Kathete, wenn die Hypotenuse 10 und eine Kathete 7 lang ist (exakt und mit 4 Ziffern).',
  body='k = sqrt(10**2 - 7**2)\ndisplay(k)\nN(k, 4)')
t('Prüfe mit dem Kehrsatz, ob die Dreiecke mit den Seiten (7, 24, 25), (6, 8, 11) und (9, 40, 41) rechtwinklig sind. Gib eine Liste aus.',
  body='[a**2 + b**2 == c**2 for a, b, c in [(7, 24, 25), (6, 8, 11), (9, 40, 41)]]')
t('Berechne die Diagonale eines Rechtecks mit den Seiten 5 cm und 3 cm exakt.', body='sqrt(5**2 + 3**2)')
t('Berechne die Höhe eines gleichseitigen Dreiecks mit der Seite a allgemein (lege `a` positiv an).',
  given="a = symbols('a', positive=True)", body='sqrt(a**2 - (a / 2)**2)')
t('Berechne die Raumdiagonale eines Quaders mit den Kanten 3, 4 und 12.', body='sqrt(3**2 + 4**2 + 12**2)')
t('Berechne die Raumdiagonale eines Würfels mit der Kante a allgemein.', given="a = symbols('a', positive=True)", body='sqrt(3 * a**2)')
t('''Eine 6 m lange Leiter lehnt an einer Wand. Ihr Fuß steht 1,5 m von der Wand entfernt. Wie hoch reicht sie? Gib das Ergebnis exakt und mit 3 Ziffern aus.''',
  body="hoehe = sqrt(6**2 - Rational('1.5')**2)\ndisplay(hoehe)\nN(hoehe, 3)")
t('Gib alle pythagoreischen Zahlentripel (a, b, c) mit a < b < c ≤ 30 als Liste aus. Prüfe dazu, ob `sqrt(a**2 + b**2)` eine ganze Zahl ≤ 30 ist.',
  body='[(a, b, int(sqrt(a**2 + b**2))) for a in range(1, 30) for b in range(a + 1, 30)\n if sqrt(a**2 + b**2).is_integer and sqrt(a**2 + b**2) <= 30]')
predict("""display(sqrt(2**2 + 2**2))
display(sqrt(1 + 3))
sqrt(2) * sqrt(2) == 2""")

# ---------------------------------------------------------------- 2
sec('Trigonometrie im rechtwinkligen Dreieck')
expl('''#### Sinus, Kosinus und Tangens

Im rechtwinkligen Dreieck gilt für einen spitzen Winkel α:

sin(α) = Gegenkathete / Hypotenuse, cos(α) = Ankathete / Hypotenuse, tan(α) = Gegenkathete / Ankathete

sympy rechnet im **Bogenmaß**. Für Winkel in Grad verwendet man `rad(30)` (= π/6). Den Winkel zu einem Seitenverhältnis liefern
`asin()`, `acos()`, `atan()`; mit `deg()` wird er in Grad umgerechnet. Für besondere Winkel kommen exakte Werte heraus.''',
     """display(sin(rad(30)), cos(rad(45)), tan(rad(60)))
display(deg(asin(Rational(1, 2))))
display(N(deg(atan(Rational(3, 4))), 4))
10 * sin(rad(30))""")
expl('''#### Beziehungen zwischen sin, cos und tan

Für alle Winkel gilt sin²(α) + cos²(α) = 1, sin(90° − α) = cos(α) und tan(α) = sin(α)/cos(α).
`trigsimp()` vereinfacht trigonometrische Terme und wendet solche Beziehungen an.''',
     """a = symbols('alpha')
display(trigsimp(sin(a)**2 + cos(a)**2))
display(sin(pi / 2 - a))
trigsimp(sin(a) / cos(a))""")

t('Gib die exakten Werte von sin(60°), cos(30°) und tan(45°) aus.', body='display(sin(rad(60)), cos(rad(30)), tan(rad(45)))')
t('Gib sin(25°) und cos(65°) mit 5 Ziffern aus.', body='display(N(sin(rad(25)), 5), N(cos(rad(65)), 5))')
t('''Ein rechtwinkliges Dreieck hat die Hypotenuse 12 und den Winkel α = 30°. Berechne die Gegenkathete und die Ankathete exakt.''',
  body='display(12 * sin(rad(30)))\n12 * cos(rad(30))')
t('Berechne den Winkel α (in Grad, 4 Ziffern), wenn die Gegenkathete 5 und die Ankathete 8 lang ist.', body='N(deg(atan(Rational(5, 8))), 4)')
t('Berechne den Winkel α (in Grad), wenn die Ankathete 1 und die Hypotenuse 2 lang ist.', body='deg(acos(Rational(1, 2)))')
t('''Eine Rampe ist 4 m lang und überwindet 0,5 m Höhe. Gib den Neigungswinkel in Grad mit 3 Ziffern aus.''', body="N(deg(asin(Rational('0.5') / 4)), 3)")
t('''Von einem 50 m hohen Turm sieht man ein Boot unter einem Tiefenwinkel von 12°. Wie weit ist das Boot vom Fuß des Turms entfernt (4 Ziffern)?''',
  body='N(50 / tan(rad(12)), 4)')
t('Prüfe sin²(30°) + cos²(30°) = 1 mit exakten Werten.', body='sin(rad(30))**2 + cos(rad(30))**2')
t('Vereinfache `(1 − cos²(α)) / sin(α)` mit `trigsimp()`.', given="a = symbols('alpha')", body='trigsimp((1 - cos(a)**2) / sin(a))')
t('Vereinfache `tan(α) · cos(α)`.', given="a = symbols('alpha')", body='trigsimp(tan(a) * cos(a))')
predict("""display(sin(rad(90)), cos(rad(90)))
display(deg(pi / 4))
display(asin(1))
tan(rad(45)) == 1""")

# ---------------------------------------------------------------- 3
sec('Kreise und Kreisteile')
expl('''#### Umfang, Fläche, Bogen und Sektor

Für einen Kreis mit Radius r gilt u = 2πr und A = πr². Ein Kreisausschnitt (**Sektor**) mit dem Mittelpunktswinkel α hat

- die **Bogenlänge** b = α/360° · 2πr = r · α (α im Bogenmaß),
- den **Flächeninhalt** A = α/360° · πr² = ½ r² α (α im Bogenmaß).''',
     """r = 5
display(2 * pi * r, pi * r**2)
alpha = rad(72)
display(r * alpha)
display(Rational(1, 2) * r**2 * alpha)
N(r * alpha, 4)""")

t('Berechne Umfang und Flächeninhalt eines Kreises mit dem Radius 7 cm exakt.', body='display(2 * pi * 7)\npi * 7**2')
t('Ein Kreis hat den Flächeninhalt 50 cm². Berechne den Radius exakt und mit 4 Ziffern.', given="r = symbols('r', positive=True)",
  body='rad_ = solve(Eq(pi * r**2, 50), r)[0]\ndisplay(rad_)\nN(rad_, 4)')
t('Berechne die Bogenlänge und den Sektorflächeninhalt für r = 6 cm und α = 120° exakt.', body='alpha = rad(120)\ndisplay(6 * alpha)\nRational(1, 2) * 6**2 * alpha')
t('Ein Sektor eines Kreises mit r = 10 cm hat die Bogenlänge 15 cm. Wie groß ist der Mittelpunktswinkel in Grad (4 Ziffern)?',
  body='N(deg(Rational(15, 10)), 4)')
t('''Ein Rad hat den Durchmesser 70 cm. Wie viele Umdrehungen macht es auf 1 km (4 Ziffern)?''', body='N(100000 / (pi * 70), 4)')
t('Berechne den Flächeninhalt eines Kreisrings mit den Radien 3 cm und 5 cm exakt.', body='pi * 5**2 - pi * 3**2')
t('''Welchen Radius hat ein Kreis, dessen Umfang so groß ist wie der Umfang eines Quadrats mit der Seite 10 cm? Gib den Radius exakt und mit 4 Ziffern aus.''',
  given="r = symbols('r', positive=True)", body='rad_ = solve(Eq(2 * pi * r, 40), r)[0]\ndisplay(rad_)\nN(rad_, 4)')

# ---------------------------------------------------------------- 4
sec('Körper: Volumen und Oberfläche')
expl('''#### Die Formeln

| Körper | Volumen | Oberfläche |
|---|---|---|
| Prisma | G · h | 2G + Mantel |
| Zylinder | πr²h | 2πr² + 2πrh |
| Pyramide | ⅓ G · h | G + Mantel |
| Kegel | ⅓ πr²h | πr² + πrs mit der Mantellinie s = √(r² + h²) |
| Kugel | 4/3 πr³ | 4πr² |

Mit sympy stellt man die Formeln als Terme auf, setzt ein oder stellt sie mit `solve()` nach einer Größe um.''',
     """r, h = symbols('r h', positive=True)
V_kegel = Rational(1, 3) * pi * r**2 * h
display(V_kegel.subs({r: 3, h: 4}))
s_ = sqrt(r**2 + h**2)
display((pi * r**2 + pi * r * s_).subs({r: 3, h: 4}))
solve(Eq(V_kegel, 100), h)[0]""")

t('Berechne Volumen und Oberfläche eines Zylinders mit r = 4 cm und h = 10 cm exakt.',
  given="r, h = symbols('r h', positive=True)", body='display((pi * r**2 * h).subs({r: 4, h: 10}))\n(2*pi*r**2 + 2*pi*r*h).subs({r: 4, h: 10})')
t('Berechne Volumen und Oberfläche einer Kugel mit r = 6 cm exakt.', body='display(Rational(4, 3) * pi * 6**3)\n4 * pi * 6**2')
t('Eine quadratische Pyramide hat die Grundkante 6 cm und die Höhe 4 cm. Berechne das Volumen und die Höhe einer Seitenfläche (mit Pythagoras).',
  body='display(Rational(1, 3) * 6**2 * 4)\nsqrt(4**2 + 3**2)')
t('Berechne die Oberfläche der Pyramide aus der vorigen Aufgabe (Grundfläche + 4 Dreiecke).', body='hs = sqrt(4**2 + 3**2)\n6**2 + 4 * Rational(1, 2) * 6 * hs')
t('Eine Kugel hat das Volumen 1000 cm³. Berechne den Radius exakt und mit 4 Ziffern.', given="r = symbols('r', positive=True)",
  body='rad_ = solve(Eq(Rational(4, 3) * pi * r**3, 1000), r)[0]\ndisplay(rad_)\nN(rad_, 4)')
t('Ein Kegel hat den Radius 3 cm und die Mantellinie 5 cm. Berechne die Höhe und das Volumen exakt.',
  body='h_ = sqrt(5**2 - 3**2)\ndisplay(h_)\nRational(1, 3) * pi * 3**2 * h_')
t('''Ein Zylinder und eine Kugel haben denselben Radius r, der Zylinder hat die Höhe 2r. Gib das Verhältnis der Volumina `V_Kugel / V_Zylinder` vereinfacht aus.''',
  given="r = symbols('r', positive=True)", body='(Rational(4, 3) * pi * r**3) / (pi * r**2 * 2*r)')
t('''Ein zylinderförmiges Glas mit Radius 3 cm soll 0,25 l (250 cm³) fassen. Wie hoch muss es mindestens sein (exakt und mit 3 Ziffern)?''',
  given="h = symbols('h', positive=True)", body='h_ = solve(Eq(pi * 3**2 * h, 250), h)[0]\ndisplay(h_)\nN(h_, 3)')
t('''Wie ändert sich das Volumen einer Kugel, wenn man den Radius verdoppelt? Gib `V(2r) / V(r)` aus.''',
  given="r = symbols('r', positive=True)", body='V = Rational(4, 3) * pi * r**3\nV.subs(r, 2*r) / V')

# ---------------------------------------------------------------- 5
sec('Dreiecke mit sympy.geometry')
expl('''#### Punkte, Strecken, Dreiecke

Das Modul `sympy.geometry` (in `from sympy import *` enthalten) kennt geometrische Objekte:

- `Point(x, y)`, `Segment(P, Q)` (Strecke), `Line(P, Q)` (Gerade), `Circle(M, r)`, `Triangle(A, B, C)`
- `P.distance(Q)` ist der Abstand, `Segment(P, Q).midpoint` der Mittelpunkt
- Ein Dreieck kennt `area` (Fläche), `perimeter` (Umfang), `angles` (die Winkel an den Ecken, im Bogenmaß),
  `circumcenter` und `circumradius` (Umkreis), `incenter` und `inradius` (Inkreis)
- `intersection(g, h)` berechnet Schnittpunkte von Geraden, Strecken und Kreisen''',
     """A, B, C = Point(0, 0), Point(4, 0), Point(0, 3)
d = Triangle(A, B, C)
display(d.area, d.perimeter)
display(deg(d.angles[B]))
display(d.circumcenter, d.circumradius)
display(d.incenter, d.inradius)
intersection(Line(A, Point(1, 1)), Line(B, C))""")

t('Berechne den Abstand der Punkte P(1, 2) und Q(7, 10).', body='Point(1, 2).distance(Point(7, 10))')
t('Berechne den Mittelpunkt der Strecke von P(−2, 5) nach Q(4, 1).', body='Segment(Point(-2, 5), Point(4, 1)).midpoint')
t('Berechne Flächeninhalt und Umfang des Dreiecks A(1, 1), B(7, 1), C(4, 5).',
  body='d = Triangle(Point(1, 1), Point(7, 1), Point(4, 5))\ndisplay(d.area)\nd.perimeter')
t('Berechne für das Dreieck A(1, 1), B(7, 1), C(4, 5) den Winkel bei C in Grad mit 4 Ziffern.',
  body='A, B, C = Point(1, 1), Point(7, 1), Point(4, 5)\nN(deg(Triangle(A, B, C).angles[C]), 4)')
t('Prüfe die Winkelsumme im Dreieck A(0, 0), B(5, 1), C(2, 4): Gib die Summe der drei Winkel in Grad aus (mit `simplify`).',
  body='d = Triangle(Point(0, 0), Point(5, 1), Point(2, 4))\nN(deg(sum(d.angles.values())), 6)')
t('Bestimme Umkreismittelpunkt und Umkreisradius des Dreiecks A(0, 0), B(6, 0), C(2, 4).',
  body='d = Triangle(Point(0, 0), Point(6, 0), Point(2, 4))\ndisplay(d.circumcenter)\nd.circumradius')
t('Bestimme Inkreismittelpunkt und Inkreisradius des Dreiecks A(0, 0), B(6, 0), C(0, 8).',
  body='d = Triangle(Point(0, 0), Point(6, 0), Point(0, 8))\ndisplay(d.incenter)\nd.inradius')
t('''**Thales:** Prüfe, dass der Winkel bei C im Dreieck A(−5, 0), B(5, 0), C(3, 4) ein rechter Winkel ist (C liegt auf dem Kreis mit Durchmesser AB).
Gib den Winkel in Grad aus.''', body='A, B, C = Point(-5, 0), Point(5, 0), Point(3, 4)\ndeg(Triangle(A, B, C).angles[C])')
t('Bestimme den Schnittpunkt der Geraden durch (0, 1) und (2, 5) mit der Geraden durch (0, 6) und (3, 0).',
  body='intersection(Line(Point(0, 1), Point(2, 5)), Line(Point(0, 6), Point(3, 0)))')
t('Bestimme die Schnittpunkte des Kreises um (0, 0) mit Radius 5 und der Geraden durch (−7, 1) und (7, 1).',
  body='intersection(Circle(Point(0, 0), 5), Line(Point(-7, 1), Point(7, 1)))')
t('''Ähnlichkeit: Das Dreieck (0, 0), (2, 0), (0, 1) wird mit dem Faktor 3 vom Ursprung aus gestreckt (`scale(3, 3)`). Gib das Verhältnis der Flächeninhalte aus.''',
  body='d = Triangle(Point(0, 0), Point(2, 0), Point(0, 1))\nd.scale(3, 3).area / d.area')
predict("""P = Point(0, 0)
display(P.distance(Point(3, 4)))
display(Segment(P, Point(4, 6)).midpoint)
Triangle(P, Point(2, 0), Point(0, 2)).area""")

# ---------------------------------------------------------------- 6
sec('Vektoren')
expl('''#### Vektoren als Spalten

Ein **Vektor** im Raum wird als Spalte mit drei Koordinaten geschrieben: `Matrix([1, 2, 3])`. Er kann einen **Punkt** (Ortsvektor) oder
eine **Verschiebung** beschreiben. Der Vektor von P nach Q ist Q − P.

- Addition, Subtraktion und Multiplikation mit einer Zahl funktionieren koordinatenweise: `u + v`, `3*u`.
- `u.norm()` ist der **Betrag** (die Länge) des Vektors.
- Der **Mittelpunkt** einer Strecke PQ ist (P + Q)/2.''',
     """P = Matrix([1, 2, 3])
Q = Matrix([5, 0, 7])
PQ = Q - P
display(PQ)
display(PQ.norm())
display((P + Q) / 2)
2 * PQ + Matrix([1, 1, 1])""")
expl('''#### Linearkombination und Kollinearität

Ein Vektor w ist eine **Linearkombination** von u und v, wenn es Zahlen r₁, r₂ gibt mit w = r₁·u + r₂·v. Das ist ein Gleichungssystem für r₁ und r₂.

Zwei Vektoren sind **kollinear** (parallel), wenn der eine ein Vielfaches des anderen ist. Im Raum prüft man das am einfachsten mit dem
**Kreuzprodukt** `u.cross(v)`: Es ist genau dann der Nullvektor, wenn u und v kollinear sind.''',
     """u = Matrix([1, 2, 0])
v = Matrix([0, 1, 1])
w = Matrix([2, 7, 3])
r1, r2 = symbols('r_1 r_2')
display(solve(list(r1*u + r2*v - w), [r1, r2]))
display(Matrix([2, 4, 6]).cross(Matrix([1, 2, 3])))
Matrix([2, 4, 6]).cross(Matrix([1, 2, 4]))""")

t('Berechne den Vektor von P(2, −1, 4) nach Q(5, 3, 4) und seinen Betrag.', body='PQ = Matrix([5, 3, 4]) - Matrix([2, -1, 4])\ndisplay(PQ)\nPQ.norm()')
t('Berechne `3u − 2v` für u = (1, 0, 2) und v = (4, −1, 1).', body='3 * Matrix([1, 0, 2]) - 2 * Matrix([4, -1, 1])')
t('Berechne den Mittelpunkt der Strecke von A(1, 5, −2) nach B(3, −1, 6).', body='(Matrix([1, 5, -2]) + Matrix([3, -1, 6])) / 2')
t('Berechne den Abstand der Punkte A(1, 2, 3) und B(4, 6, 3).', body='(Matrix([4, 6, 3]) - Matrix([1, 2, 3])).norm()')
t('Berechne die Länge des Vektors (1, 1, 1) exakt und bringe ihn auf die Länge 1 (Einheitsvektor).',
  body='v = Matrix([1, 1, 1])\ndisplay(v.norm())\nv / v.norm()')
t('Prüfe mit dem Kreuzprodukt, ob u = (3, −6, 9) und v = (−1, 2, −3) kollinear sind.', body='Matrix([3, -6, 9]).cross(Matrix([-1, 2, -3]))')
t('Prüfe, ob die Punkte A(1, 1, 1), B(3, 2, 4) und C(7, 4, 10) auf einer Geraden liegen (AB und AC kollinear?).',
  body='A, B, C = Matrix([1, 1, 1]), Matrix([3, 2, 4]), Matrix([7, 4, 10])\n(B - A).cross(C - A)')
t('Stelle w = (3, 5, 2) als Linearkombination von u = (1, 1, 0) und v = (1, 2, 1) dar: Löse `r₁·u + r₂·v = w`.',
  given="r1, r2 = symbols('r_1 r_2')", body='solve(list(r1 * Matrix([1, 1, 0]) + r2 * Matrix([1, 2, 1]) - Matrix([3, 5, 2])), [r1, r2])')
t('''Ergänze das Viereck ABCD mit A(1, 0, 2), B(4, 1, 2), C(5, 4, 3) zu einem Parallelogramm: D = A + (C − B).''',
  body='A, B, C = Matrix([1, 0, 2]), Matrix([4, 1, 2]), Matrix([5, 4, 3])\nA + (C - B)')
predict("""u = Matrix([1, 2, 2])
display(u.norm())
display(2 * u)
u.cross(u)""")

# ---------------------------------------------------------------- 7
sec('Geraden im Raum')
expl('''#### Parameterform

Eine Gerade durch den Punkt P mit dem **Richtungsvektor** v besteht aus allen Punkten

X = P + t · v (t ∈ ℝ)

Für jeden Wert des Parameters t erhält man einen Punkt der Geraden. Ob ein Punkt Q auf der Geraden liegt, prüft man mit `solve()`:
Gibt es ein t mit P + t·v = Q?''',
     """P = Matrix([1, 2, 0])
v = Matrix([2, -1, 3])
g = P + t * v
display(g)
display(g.subs(t, 2))
solve(list(g - Matrix([5, 0, 6])), t)""")
expl('''#### Lagebeziehung und Schnittpunkt

Zwei Geraden im Raum können **identisch**, **parallel**, **sich schneidend** oder **windschief** sein.

- Sind die Richtungsvektoren kollinear (Kreuzprodukt = Nullvektor), sind die Geraden parallel oder identisch.
- Sonst setzt man die Geraden gleich: P + t·u = Q + s·v. Hat das Gleichungssystem eine Lösung, schneiden sie sich, sonst sind sie windschief.

`Line3D(Point3D(...), Point3D(...))` und `intersection()` erledigen das ebenfalls.''',
     """g = Matrix([1, 0, 0]) + t * Matrix([1, 1, 0])
h = Matrix([3, 1, 1]) + s * Matrix([0, 1, -1])
l = solve(list(g - h), [t, s])
display(l)
display(g.subs(t, l[t]))
intersection(Line3D(Point3D(1, 0, 0), Point3D(2, 1, 0)), Line3D(Point3D(3, 1, 1), Point3D(3, 2, 0)))""")

t('Gib die Gerade durch A(2, 0, 1) und B(4, 3, 1) in Parameterform aus (Stützvektor A, Richtungsvektor B − A).',
  body='A, B = Matrix([2, 0, 1]), Matrix([4, 3, 1])\nA + t * (B - A)')
t('Berechne die Punkte der Geraden `X = (1, 1, 0) + t·(2, 0, 1)` für t = −1, 0, 1, 2 als Liste.',
  body='g = Matrix([1, 1, 0]) + t * Matrix([2, 0, 1])\n[list(g.subs(t, k)) for k in [-1, 0, 1, 2]]')
t('Prüfe, ob der Punkt Q(7, 1, 3) auf der Geraden `X = (1, 1, 0) + t·(2, 0, 1)` liegt.',
  body='g = Matrix([1, 1, 0]) + t * Matrix([2, 0, 1])\nsolve(list(g - Matrix([7, 1, 3])), t)')
t('Prüfe, ob der Punkt Q(5, 2, 2) auf der Geraden `X = (1, 1, 0) + t·(2, 0, 1)` liegt.',
  body='g = Matrix([1, 1, 0]) + t * Matrix([2, 0, 1])\nsolve(list(g - Matrix([5, 2, 2])), t)')
t('''Bestimme den Schnittpunkt der Geraden `g: X = (0, 0, 1) + t·(1, 2, 0)` und `h: X = (2, 0, 1) + s·(0, 2, 0)`.''',
  body='g = Matrix([0, 0, 1]) + t * Matrix([1, 2, 0])\nh = Matrix([2, 0, 1]) + s * Matrix([0, 2, 0])\nl = solve(list(g - h), [t, s])\ng.subs(t, l[t])')
t('''Untersuche die Lage von `g: X = (1, 0, 0) + t·(1, 1, 0)` und `h: X = (0, 0, 1) + s·(0, 1, 1)`: Gib das Kreuzprodukt der Richtungsvektoren
und die Lösung des Gleichungssystems `g = h` aus.''',
  body='display(Matrix([1, 1, 0]).cross(Matrix([0, 1, 1])))\ng = Matrix([1, 0, 0]) + t * Matrix([1, 1, 0])\nh = Matrix([0, 0, 1]) + s * Matrix([0, 1, 1])\nsolve(list(g - h), [t, s])')
t('''Prüfe, ob die Geraden `g: X = (1, 2, 3) + t·(2, 4, 6)` und `h: X = (0, 0, 0) + s·(1, 2, 3)` parallel oder identisch sind:
Gib das Kreuzprodukt der Richtungsvektoren aus und prüfe, ob (0, 0, 0) auf g liegt.''',
  body='display(Matrix([2, 4, 6]).cross(Matrix([1, 2, 3])))\nsolve(list(Matrix([1, 2, 3]) + t * Matrix([2, 4, 6])), t)')
t('''Bestimme die **Spurpunkte** der Geraden `X = (2, 4, 6) + t·(1, −1, −2)`, also die Schnittpunkte mit den Koordinatenebenen
(x₃ = 0, x₂ = 0 und x₁ = 0). Gib sie als Liste aus.''',
  body='g = Matrix([2, 4, 6]) + t * Matrix([1, -1, -2])\n[list(g.subs(t, solve(g[i], t)[0])) for i in [2, 1, 0]]')
t('''**Flugbahn:** Ein Flugzeug startet im Punkt (0, 0, 0) und fliegt pro Minute um den Vektor (6, 8, 0,5) (in km). Gib seine Position nach 10 Minuten aus
und die zurückgelegte Strecke nach 10 Minuten mit 4 Ziffern.''',
  body="v = Matrix([6, 8, Rational('0.5')])\ndisplay(10 * v)\nN((10 * v).norm(), 4)")
predict("""g = Matrix([0, 0, 0]) + t * Matrix([1, 0, 0])
display(g.subs(t, 3))
solve(list(g - Matrix([2, 1, 0])), t)""")

# ---------------------------------------------------------------- 8
sec('Gemischte Übungen')
t('''Ein gleichschenkliges Dreieck hat die Basis 10 cm und die Schenkel 13 cm. Berechne Höhe, Flächeninhalt und den Basiswinkel in Grad (4 Ziffern).''',
  body='h = sqrt(13**2 - 5**2)\ndisplay(h, 10 * h / 2)\nN(deg(acos(Rational(5, 13))), 4)')
t('''Zeige mit `sympy.geometry`, dass die Seitenhalbierenden des Dreiecks A(0, 0), B(8, 0), C(2, 6) sich in einem Punkt schneiden (dem Schwerpunkt):
Gib den Schnittpunkt zweier Seitenhalbierender und `Triangle(A, B, C).centroid` aus.''',
  body='A, B, C = Point(0, 0), Point(8, 0), Point(2, 6)\ndisplay(intersection(Line(A, Segment(B, C).midpoint), Line(B, Segment(A, C).midpoint)))\nTriangle(A, B, C).centroid')
t('''Ein Würfel hat die Kante a. Gib das Verhältnis aus Volumen der Umkugel (Radius = halbe Raumdiagonale) und Würfelvolumen vereinfacht aus.''',
  given="a = symbols('a', positive=True)", body='r = sqrt(3) * a / 2\nsimplify(Rational(4, 3) * pi * r**3 / a**3)')
t('''Die Punkte A(2, 1, 0), B(4, 5, 0), C(0, 3, 0) bilden ein Dreieck. Prüfe mit den Seitenlängen und dem Kehrsatz des Pythagoras, ob es rechtwinklig ist:
Gib die Quadrate der drei Seitenlängen als Liste aus.''',
  body='A, B, C = Matrix([2, 1, 0]), Matrix([4, 5, 0]), Matrix([0, 3, 0])\n[(B - A).norm()**2, (C - A).norm()**2, (C - B).norm()**2]')
t('''Ein Kegel und ein Zylinder haben dieselbe Grundfläche und dasselbe Volumen. Wie verhalten sich ihre Höhen? Löse `πr²·hz = ⅓πr²·hk` nach `hk` auf.''',
  given="r, hz, hk = symbols('r h_z h_k', positive=True)", body='solve(Eq(pi * r**2 * hz, Rational(1, 3) * pi * r**2 * hk), hk)')

generate('sympy_geometrie', 'Geometrie: Pythagoras, Trigonometrie, Körper, Vektoren und Geraden', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
