# Erzeugt ../content/sympy_abstaende_winkel.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_abstaende_winkel.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_abstaende_winkel.py
#
# Bildungsplan BW 2016, Kursstufe, Leitidee Raum und Form / Messen:
# Winkel zwischen Vektoren, Geraden und Ebenen (Skalarprodukt), Abstand Punkt–Ebene (Lotfußpunkt, Hessesche Normalform),
# Abstand Punkt–Gerade und Abstand windschiefer Geraden (Leistungsfach), Spiegelungen an Punkt, Ebene und Gerade,
# Flächeninhalte (Vektorprodukt: Leistungsfach) und Volumen von Pyramiden, Anwendungen (Flugbahnen, Schatten).
# Baut auf sympy_ebenen auf.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t_(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = "from sympy import *\ninit_printing()\nx, y, z, r, s, t = symbols('x y z r s t', real=True)"

INTRO = '''In diesem Notebook misst du im Raum: **Winkel** zwischen Vektoren, Geraden und Ebenen, **Abstände** von Punkten zu Ebenen und Geraden
und zwischen Geraden, außerdem **Spiegelungen**, **Flächeninhalte** und **Volumen**. Am Ende stehen Anwendungen wie Flugbahnen und Schatten.

Fast alles beruht auf dem **Skalarprodukt** (`u.dot(v)`) und dem **Betrag** (`u.norm()`). Im Leistungsfach kommt das **Vektorprodukt**
(`u.cross(v)`) dazu. Für einige Abstände gibt es in `sympy.geometry` fertige Befehle; nutze sie zum Kontrollieren.

Vorausgesetzt wird das Notebook *Ebenen*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy, schaltet die Formel-Ausgabe ein
und legt die Koordinaten `x`, `y`, `z` und die Parameter `r`, `s`, `t` an.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Winkel')
expl('''#### cos φ = (u · v) / (|u| · |v|)

Für den Winkel φ zwischen zwei Vektoren gilt cos φ = u · v / (|u| · |v|). `acos()` ist der Arkuskosinus (cos⁻¹) im Bogenmaß,
`deg()` rechnet in Grad um. Nur bei besonderen Werten ist das Ergebnis eine „schöne“ Zahl, sonst rundet man mit `N()`.

| Winkel zwischen | Formel |
|---|---|
| zwei Geraden (Richtungsvektoren u, v) | cos φ = \\|u · v\\| / (\\|u\\| · \\|v\\|) (Betrag: spitzer Winkel) |
| zwei Ebenen (Normalenvektoren n₁, n₂) | cos φ = \\|n₁ · n₂\\| / (\\|n₁\\| · \\|n₂\\|) |
| Gerade und Ebene (u und n) | **sin** φ = \\|u · n\\| / (\\|u\\| · \\|n\\|) |''',
     """u = Matrix([1, 0, 1])
v = Matrix([0, 1, 1])
c = u.dot(v) / (u.norm() * v.norm())
display(c, deg(acos(c)))
w = Matrix([2, -1, 2])
c2 = Matrix([1, 2, 2]).dot(w) / (Matrix([1, 2, 2]).norm() * w.norm())
display(c2, N(deg(acos(c2)), 4))""")

t_('Berechne den Winkel zwischen u = (1, 1, 0) und v = (1, 0, 0) in Grad.',
   body='u, v = Matrix([1, 1, 0]), Matrix([1, 0, 0])\ndeg(acos(u.dot(v) / (u.norm() * v.norm())))')
t_('Berechne den Winkel zwischen u = (2, 1, −2) und v = (1, 2, 3) in Grad (4 Ziffern).',
   body='u, v = Matrix([2, 1, -2]), Matrix([1, 2, 3])\nN(deg(acos(u.dot(v) / (u.norm() * v.norm()))), 4)')
t_('''Schreibe eine Funktion `winkel(u, v)`, die den Winkel zwischen zwei Vektoren in Grad mit 4 Ziffern zurückgibt. Teste mit (1, 0, 0), (0, 1, 0)
und mit (1, 2, 3), (−1, 0, 4).''',
   body='def winkel(u, v):\n    return N(deg(acos(u.dot(v) / (u.norm() * v.norm()))), 4)\n\ndisplay(winkel(Matrix([1, 0, 0]), Matrix([0, 1, 0])))\nwinkel(Matrix([1, 2, 3]), Matrix([-1, 0, 4]))')
t_('''Berechne die Innenwinkel des Dreiecks A(1 | 0 | 0), B(0 | 2 | 0), C(0 | 0 | 3) bei A, B und C (4 Ziffern) und ihre Summe.''',
   body="def winkel(u, v):\n    return N(deg(acos(u.dot(v) / (u.norm() * v.norm()))), 4)\n\nA, B, C = Matrix([1, 0, 0]), Matrix([0, 2, 0]), Matrix([0, 0, 3])\nw = [winkel(B - A, C - A), winkel(A - B, C - B), winkel(A - C, B - C)]\ndisplay(w)\nsum(w)")
t_('Berechne den Schnittwinkel der Geraden mit den Richtungsvektoren (1, −1, 2) und (−2, 1, 1) (spitzer Winkel, mit `Abs`, 4 Ziffern).',
   body='u, v = Matrix([1, -1, 2]), Matrix([-2, 1, 1])\nN(deg(acos(Abs(u.dot(v)) / (u.norm() * v.norm()))), 4)')
t_('Berechne den Winkel zwischen den Ebenen x + y + z = 1 und x − y = 0 (über die Normalenvektoren).',
   body='n1, n2 = Matrix([1, 1, 1]), Matrix([1, -1, 0])\ndeg(acos(Abs(n1.dot(n2)) / (n1.norm() * n2.norm())))')
t_('Berechne den Winkel zwischen der Ebene x + y + z = 6 und der x-y-Ebene (Normalenvektor (0, 0, 1)) in Grad (4 Ziffern).',
   body='n1, n2 = Matrix([1, 1, 1]), Matrix([0, 0, 1])\nN(deg(acos(Abs(n1.dot(n2)) / (n1.norm() * n2.norm()))), 4)')
t_('''Berechne den Winkel, unter dem die Gerade mit Richtungsvektor u = (1, 1, 0) die Ebene z = 0 bzw. die Ebene x + y + z = 3 schneidet (mit `asin`, 4 Ziffern).''',
   body='u = Matrix([1, 1, 0])\nfor n in [Matrix([0, 0, 1]), Matrix([1, 1, 1])]:\n    display(N(deg(asin(Abs(u.dot(n)) / (u.norm() * n.norm()))), 4))')
t_('''**Dachneigung:** Ein Dach hat die Ebene 3y + 4z = 24 (Einheit m, die z-Achse zeigt nach oben). Wie steil ist das Dach gegenüber dem waagrechten Boden (Grad, 4 Ziffern)?''',
   body='n1, n2 = Matrix([0, 3, 4]), Matrix([0, 0, 1])\nN(deg(acos(Abs(n1.dot(n2)) / (n1.norm() * n2.norm()))), 4)')
t_('''Kontrolle mit sympy.geometry: Gib den Winkel zwischen den Ebenen x + y + z = 1 und x − y + 2z = 0 mit `Plane(...).angle_between(Plane(...))` in Grad (4 Ziffern) aus.''',
   body='E1 = Plane(Point3D(1, 0, 0), normal_vector=(1, 1, 1))\nE2 = Plane(Point3D(0, 0, 0), normal_vector=(1, -1, 2))\nN(deg(E1.angle_between(E2)), 4)')
predict("""u = Matrix([3, 0, 0])
v = Matrix([0, 0, 5])
display(u.dot(v))
display(deg(acos(u.dot(v) / (u.norm() * v.norm()))))
deg(acos(-1))""")

# ---------------------------------------------------------------- 2
sec('Abstand Punkt–Ebene')
expl('''#### Lotfußpunkt und Hessesche Normalform

**Mit Lotgerade:** Die Gerade durch den Punkt Q mit dem Normalenvektor n als Richtung (Lotgerade) schneidet die Ebene im **Lotfußpunkt** F.
Der Abstand ist |QF|.

**Hessesche Normalform:** Für E: n · x = d ist der Abstand d(Q, E) = |n · q − d| / |n|.

`Plane(...).distance(Point3D(...))` und `Plane(...).projection(Point3D(...))` (Lotfußpunkt) prüfen das.''',
     """n = Matrix([2, -1, 2])
d = 3
Q = Matrix([5, 1, 6])
lot = Q + t * n
tF = solve(n.dot(lot) - d, t)[0]
F = lot.subs(t, tF)
display(F, (Q - F).norm())
display(Abs(n.dot(Q) - d) / n.norm())
E = Plane(Point3D(0, 0, Rational(3, 2)), normal_vector=(2, -1, 2))
display(E.distance(Point3D(5, 1, 6)), E.projection(Point3D(5, 1, 6)))""")

t_('Berechne den Abstand des Punktes Q(3 | 2 | 7) von der Ebene E: 2x + y + 2z = 4 mit der Hesseschen Normalform.',
   body='n, d, Q = Matrix([2, 1, 2]), 4, Matrix([3, 2, 7])\nAbs(n.dot(Q) - d) / n.norm()')
t_('Berechne für dieselbe Aufgabe den Lotfußpunkt F mit der Lotgeraden und den Abstand |QF|.',
   body='n, d, Q = Matrix([2, 1, 2]), 4, Matrix([3, 2, 7])\nlot = Q + t * n\nF = lot.subs(t, solve(n.dot(lot) - d, t)[0])\ndisplay(F)\n(Q - F).norm()')
t_('Berechne den Abstand des Ursprungs von der Ebene x + 2y + 2z = 9.', body='n = Matrix([1, 2, 2])\nAbs(n.dot(Matrix([0, 0, 0])) - 9) / n.norm()')
t_('Berechne den Abstand des Punktes (1 | 1 | 1) von der Ebene 3x − 4z = 2 genau und prüfe mit `Plane(...).distance(...)` (die Ebene geht durch (2 | 0 | 1)).',
   body='n = Matrix([3, 0, -4])\ndisplay(Abs(n.dot(Matrix([1, 1, 1])) - 2) / n.norm())\nPlane(Point3D(2, 0, 1), normal_vector=(3, 0, -4)).distance(Point3D(1, 1, 1))')
t_('''Berechne den Abstand der parallelen Ebenen E₁: x − 2y + 2z = 1 und E₂: x − 2y + 2z = 10 (Abstand eines Punktes von E₁ zu E₂; (1 | 0 | 0) liegt in E₁).''',
   body='n = Matrix([1, -2, 2])\nAbs(n.dot(Matrix([1, 0, 0])) - 10) / n.norm()')
t_('''Welche Punkte der Geraden g: x = (0, 0, 0) + t · (1, 1, 1) haben von der Ebene 2x + y + 2z = 0 den Abstand 5? Gib die Werte von t und die Punkte aus.''',
   body='n = Matrix([2, 1, 2])\ng = t * Matrix([1, 1, 1])\nl = solve(Eq(Abs(n.dot(g)) / n.norm(), 5), t)\ndisplay(l)\n[list(g.subs(t, w)) for w in l]')
t_('''Gib die beiden Ebenen an, die zu E: 2x − y + 2z = 3 parallel sind und von ihr den Abstand 2 haben (Koordinatenform: 2x − y + 2z = d, löse |d − 3| / 3 = 2).''',
   given="d = symbols('d', real=True)", body='solve(Eq(Abs(d - 3) / 3, 2), d)')
t_('''Eine **Kugel** mit Mittelpunkt M(2 | 3 | 5) berührt die Ebene x + 2y + 2z = 4. Wie groß ist ihr Radius?''',
   body='n = Matrix([1, 2, 2])\nAbs(n.dot(Matrix([2, 3, 5])) - 4) / n.norm()')

# ---------------------------------------------------------------- 3
sec('Abstand Punkt–Gerade (Leistungsfach)')
expl('''#### Lotfußpunkt auf der Geraden

Der **Lotfußpunkt** F auf g: x = p + t · v ist der Punkt der Geraden, für den QF senkrecht auf v steht: (q − (p + t·v)) · v = 0.
Daraus folgt t, dann F und der Abstand |QF|. Kontrolle: `Line3D(Point3D(...), direction_ratio=(...)).distance(Point3D(...))`.''',
     """g = Matrix([1, 0, 0]) + t * Matrix([1, 1, 0])
Q = Matrix([3, 1, 4])
tF = solve((Q - g).dot(Matrix([1, 1, 0])), t)[0]
F = g.subs(t, tF)
display(F, (Q - F).norm())
Line3D(Point3D(1, 0, 0), direction_ratio=(1, 1, 0)).distance(Point3D(3, 1, 4))""")

t_('Berechne den Lotfußpunkt und den Abstand des Punktes Q(4 | 2 | 1) von g: x = (0, 0, 0) + t · (1, 2, 2).',
   body='v = Matrix([1, 2, 2])\ng = t * v\nQ = Matrix([4, 2, 1])\nF = g.subs(t, solve((Q - g).dot(v), t)[0])\ndisplay(F)\n(Q - F).norm()')
t_('Prüfe das Ergebnis der vorigen Aufgabe mit `Line3D(...).distance(...)`.',
   body='Line3D(Point3D(0, 0, 0), direction_ratio=(1, 2, 2)).distance(Point3D(4, 2, 1))')
t_('Berechne den Abstand des Punktes Q(1 | 5 | 2) von der Geraden durch A(1 | 1 | 0) und B(3 | 1 | 2).',
   body='A, B, Q = Matrix([1, 1, 0]), Matrix([3, 1, 2]), Matrix([1, 5, 2])\ng = A + t * (B - A)\nF = g.subs(t, solve((Q - g).dot(B - A), t)[0])\n(Q - F).norm()')
t_('''Berechne den Abstand mit einer anderen Methode: Minimiere die Funktion d(t)² = |Q − g(t)|² für die Gerade g aus der ersten Aufgabe (Ableitung null).''',
   body='v = Matrix([1, 2, 2])\nQ = Matrix([4, 2, 1])\nd2 = expand((Q - t * v).dot(Q - t * v))\ndisplay(d2)\ntm = solve(diff(d2, t), t)[0]\nsqrt(d2.subs(t, tm))')
t_('''Berechne die Höhe des Dreiecks A(0 | 0 | 0), B(4 | 0 | 0), C(1 | 3 | 2) auf der Seite AB (Abstand von C zur Geraden AB) und damit den Flächeninhalt.''',
   body='A, B, C = Matrix([0, 0, 0]), Matrix([4, 0, 0]), Matrix([1, 3, 2])\ng = A + t * (B - A)\nF = g.subs(t, solve((C - g).dot(B - A), t)[0])\nh = (C - F).norm()\ndisplay(h)\n(B - A).norm() * h / 2')

# ---------------------------------------------------------------- 4
sec('Abstand windschiefer Geraden (Leistungsfach)')
expl('''#### Gemeinsames Lot

Zwei **windschiefe** Geraden g: x = p + s·u und h: x = q + t·v haben einen kürzesten Abstand. Die Verbindungsstrecke steht auf beiden
Geraden senkrecht. Zwei Wege:

1. Der Vektor n = u × v ist zu beiden Geraden orthogonal. Abstand = |(q − p) · n| / |n|.
2. Lotfußpunkte: Löse das LGS (g(s) − h(t)) · u = 0 und (g(s) − h(t)) · v = 0. Dann ist der Abstand |g(s) − h(t)|.''',
     """p, u = Matrix([0, 0, 0]), Matrix([1, 0, 0])
q, v = Matrix([0, 1, 2]), Matrix([0, 1, 1])
n = u.cross(v)
display(n, Abs((q - p).dot(n)) / n.norm())
g, h = p + s * u, q + t * v
l = solve([(g - h).dot(u), (g - h).dot(v)], [s, t])
display(l, g.subs(l), h.subs(l))
(g - h).subs(l).norm()""")

t_('Berechne den Abstand der windschiefen Geraden g: x = (1, 0, 0) + s · (1, 1, 0) und h: x = (0, 0, 2) + t · (0, 1, 1) mit dem Vektorprodukt.',
   body='p, u = Matrix([1, 0, 0]), Matrix([1, 1, 0])\nq, v = Matrix([0, 0, 2]), Matrix([0, 1, 1])\nn = u.cross(v)\nAbs((q - p).dot(n)) / n.norm()')
t_('Berechne für dieselben Geraden die Lotfußpunkte (zwei Punkte) und ihren Abstand.',
   body='g = Matrix([1, 0, 0]) + s * Matrix([1, 1, 0])\nh = Matrix([0, 0, 2]) + t * Matrix([0, 1, 1])\nl = solve([(g - h).dot(Matrix([1, 1, 0])), (g - h).dot(Matrix([0, 1, 1]))], [s, t])\ndisplay(g.subs(l), h.subs(l))\n(g - h).subs(l).norm()')
t_('Kontrolle: Gib den Abstand mit `Line3D(...).distance(Line3D(...))` aus.',
   body='Line3D(Point3D(1, 0, 0), direction_ratio=(1, 1, 0)).distance(Line3D(Point3D(0, 0, 2), direction_ratio=(0, 1, 1)))')
t_('''Berechne den Abstand der Geraden durch A(0 | 0 | 0), B(2 | 2 | 0) und der Geraden durch C(2 | 0 | 3), D(0 | 2 | 3).''',
   body='u = Matrix([2, 2, 0])\nv = Matrix([0, 2, 3]) - Matrix([2, 0, 3])\nn = u.cross(v)\nAbs((Matrix([2, 0, 3]) - Matrix([0, 0, 0])).dot(n)) / n.norm()')
t_('''Berechne den Abstand der **parallelen** Geraden g: x = (0, 0, 0) + s · (1, 2, 2) und h: x = (3, 0, 0) + t · (1, 2, 2) (Abstand eines Punktes von h zur Geraden g).''',
   body='v = Matrix([1, 2, 2])\nQ = Matrix([3, 0, 0])\nF = (s * v).subs(s, solve((Q - s * v).dot(v), s)[0])\n(Q - F).norm()')

# ---------------------------------------------------------------- 5
sec('Spiegelungen')
expl('''#### Punkt an Punkt, Ebene und Gerade spiegeln

- **An einem Punkt Z:** Q' = 2·z − q (Z ist der Mittelpunkt von Q und Q').
- **An einer Ebene:** Lotfußpunkt F bestimmen, dann Q' = 2·f − q (also an F spiegeln). Mit der Lotgeraden q + t·n:
  der Spiegelpunkt gehört zum doppelten Parameterwert.
- **An einer Geraden:** genauso mit dem Lotfußpunkt auf der Geraden.''',
     """Q = Matrix([5, 1, 6])
n, d = Matrix([2, -1, 2]), 3
lot = Q + t * n
tF = solve(n.dot(lot) - d, t)[0]
display(lot.subs(t, tF))
display(lot.subs(t, 2 * tF))
2 * Matrix([1, 1, 1]) - Q""")

t_('Spiegele den Punkt Q(3 | −1 | 4) am Punkt Z(1 | 2 | 0).', body='2 * Matrix([1, 2, 0]) - Matrix([3, -1, 4])')
t_('Spiegele den Punkt Q(3 | 2 | 7) an der Ebene 2x + y + 2z = 4.',
   body='n, d, Q = Matrix([2, 1, 2]), 4, Matrix([3, 2, 7])\nlot = Q + t * n\nlot.subs(t, 2 * solve(n.dot(lot) - d, t)[0])')
t_('Spiegele den Punkt Q(1 | 2 | 3) an der x-y-Ebene (z = 0) und an der Ebene x = y (Normalenvektor (1, −1, 0)).',
   body="for n, d in [(Matrix([0, 0, 1]), 0), (Matrix([1, -1, 0]), 0)]:\n    lot = Matrix([1, 2, 3]) + t * n\n    display(lot.subs(t, 2 * solve(n.dot(lot) - d, t)[0]))")
t_('Spiegele den Punkt Q(4 | 2 | 1) an der Geraden g: x = t · (1, 2, 2) (Lotfußpunkt F, dann Q\' = 2f − q).',
   body='v = Matrix([1, 2, 2])\nQ = Matrix([4, 2, 1])\nF = (t * v).subs(t, solve((Q - t * v).dot(v), t)[0])\n2 * F - Q')
t_('''Prüfe, dass Q'(−5 | −2 | −1) das Spiegelbild von Q(3 | 2 | 7) an der Ebene 2x + y + 2z = 4 ist: Der Mittelpunkt M von Q und Q' muss in der Ebene liegen (n · m = 4)
und QQ' muss zu n parallel sein (Kreuzprodukt = Nullvektor).''',
   given="Qs = Matrix([-5, -2, -1])",
   body='Q, n = Matrix([3, 2, 7]), Matrix([2, 1, 2])\nM = (Q + Qs) / 2\ndisplay(n.dot(M))\n(Qs - Q).cross(n)')
t_('''Spiegele die Gerade g: x = (1, 0, 3) + t · (1, 1, 0) an der x-y-Ebene (spiegele Stützpunkt und Richtungsvektor: z-Koordinate negieren).''',
   body='Matrix([1, 0, -3]) + t * Matrix([1, 1, 0])')

# ---------------------------------------------------------------- 6
sec('Flächeninhalte und Volumen')
expl('''#### Dreieck, Parallelogramm, Pyramide

- **Leistungsfach:** Der Betrag des Vektorprodukts |u × v| ist der Flächeninhalt des **Parallelogramms**, das u und v aufspannen.
  Das Dreieck ABC hat den Inhalt ½ · |AB × AC|.
- Ohne Vektorprodukt: Grundseite mal Höhe (Höhe als Abstand Punkt–Gerade) oder ½ · |AB| · |AC| · sin(α).
- **Pyramide:** V = ⅓ · G · h, wobei die Höhe h der Abstand der Spitze von der Grundflächen-Ebene ist.
- **(Zusatz) Spatprodukt:** Das Volumen des Spats aus u, v, w ist |(u × v) · w|, eine dreiseitige Pyramide hat ⅙ davon.''',
     """A, B, C = Matrix([1, 0, 0]), Matrix([0, 2, 0]), Matrix([0, 0, 3])
display((B - A).cross(C - A).norm() / 2)
S = Matrix([0, 0, 0])
E = Plane(Point3D(1, 0, 0), Point3D(0, 2, 0), Point3D(0, 0, 3))
h = E.distance(Point3D(0, 0, 0))
display(h)
display(Rational(1, 3) * (B - A).cross(C - A).norm() / 2 * h)
Abs((B - S).cross(C - S).dot(A - S)) / 6""")

t_('**(Leistungsfach)** Berechne den Flächeninhalt des Dreiecks A(1 | 1 | 0), B(4 | 1 | 0), C(1 | 5 | 0).',
   body='A, B, C = Matrix([1, 1, 0]), Matrix([4, 1, 0]), Matrix([1, 5, 0])\n(B - A).cross(C - A).norm() / 2')
t_('**(Leistungsfach)** Berechne den Flächeninhalt des Parallelogramms, das u = (2, 1, 0) und v = (0, 1, 3) aufspannen.',
   body='Matrix([2, 1, 0]).cross(Matrix([0, 1, 3])).norm()')
t_('''Berechne den Flächeninhalt des Dreiecks A(1 | 0 | 0), B(0 | 2 | 0), C(0 | 0 | 3) ohne Vektorprodukt mit ½ · |AB| · |AC| · sin(α).
Berechne dafür cos α und sin α = √(1 − cos² α).''',
   body='A, B, C = Matrix([1, 0, 0]), Matrix([0, 2, 0]), Matrix([0, 0, 3])\nu, v = B - A, C - A\ncos_a = u.dot(v) / (u.norm() * v.norm())\nsimplify(u.norm() * v.norm() * sqrt(1 - cos_a**2) / 2)')
t_('''Eine Pyramide hat die quadratische Grundfläche A(0 | 0 | 0), B(4 | 0 | 0), C(4 | 4 | 0), D(0 | 4 | 0) und die Spitze S(2 | 2 | 6). Berechne das Volumen.''',
   body='G = 4 * 4\nh = 6\nRational(1, 3) * G * h')
t_('''Eine dreiseitige Pyramide hat die Grundfläche A(2 | 0 | 0), B(0 | 4 | 0), C(0 | 0 | 4) und die Spitze S(3 | 3 | 3). Berechne die Höhe (Abstand von S zur Ebene ABC)
und das Volumen.''',
   body='E = Plane(Point3D(2, 0, 0), Point3D(0, 4, 0), Point3D(0, 0, 4))\nh = E.distance(Point3D(3, 3, 3))\ndisplay(h)\nA, B, C = Matrix([2, 0, 0]), Matrix([0, 4, 0]), Matrix([0, 0, 4])\nRational(1, 3) * (B - A).cross(C - A).norm() / 2 * h')
t_('''**(Zusatz)** Berechne das Volumen der Pyramide aus der vorigen Aufgabe mit dem Spatprodukt ⅙ · |(AB × AC) · AS|.''',
   body='A, B, C, S = Matrix([2, 0, 0]), Matrix([0, 4, 0]), Matrix([0, 0, 4]), Matrix([3, 3, 3])\nAbs((B - A).cross(C - A).dot(S - A)) / 6')
t_('''Für welche Spitzen S(t | t | t) hat die Pyramide mit der Grundfläche aus der vorigen Aufgabe das Volumen 8? (Spatprodukt, zwei Lösungen)''',
   body='A, B, C = Matrix([2, 0, 0]), Matrix([0, 4, 0]), Matrix([0, 0, 4])\nS = Matrix([t, t, t])\nsolve(Eq(Abs((B - A).cross(C - A).dot(S - A)) / 6, 8), t)')

# ---------------------------------------------------------------- 7
sec('Anwendungen')
expl('''#### Flugbahnen

Zwei Flugzeuge bewegen sich geradlinig: Position nach t Minuten f₁(t) = p₁ + t · v₁ und f₂(t) = p₂ + t · v₂ (Einheit km).
Ihr Abstand zur **gleichen** Zeit t ist d(t) = |f₁(t) − f₂(t)|. Der kleinste Abstand ergibt sich, wenn d(t)² minimal ist.
(Das ist etwas anderes als der Abstand der Flugbahnen als Geraden!)''',
     """f1 = Matrix([0, 0, 10]) + t * Matrix([8, 6, 0])
f2 = Matrix([40, 0, 9]) + t * Matrix([-6, 8, 0])
d2 = expand((f1 - f2).dot(f1 - f2))
display(d2)
tm = solve(diff(d2, t), t)[0]
display(tm, sqrt(d2.subs(t, tm)))""")

t_('''Berechne für die Flugzeuge aus dem Beispiel die Positionen zum Zeitpunkt des kleinsten Abstands und den Abstand der Flugbahnen als Geraden (Vektorprodukt).''',
   body='f1 = Matrix([0, 0, 10]) + t * Matrix([8, 6, 0])\nf2 = Matrix([40, 0, 9]) + t * Matrix([-6, 8, 0])\ndisplay(f1.subs(t, 2), f2.subs(t, 2))\nn = Matrix([8, 6, 0]).cross(Matrix([-6, 8, 0]))\nAbs((Matrix([40, 0, 9]) - Matrix([0, 0, 10])).dot(n)) / n.norm()')
t_('''Ein Flugzeug startet in (0 | 0 | 0) und steigt geradlinig in Richtung (4, 3, 1) (km pro Minute). Wann erreicht es 6 km Höhe, und wo ist es dann?
Unter welchem Winkel steigt es gegenüber dem Boden (Grad, 4 Ziffern)?''',
   body='f = t * Matrix([4, 3, 1])\nt6 = solve(f[2] - 6, t)[0]\ndisplay(t6, f.subs(t, t6))\nu, n = Matrix([4, 3, 1]), Matrix([0, 0, 1])\nN(deg(asin(Abs(u.dot(n)) / (u.norm() * n.norm()))), 4)')
t_('''**Schatten:** Die Sonne scheint in Richtung v = (1, 2, −4). Ein 6 m hoher Mast steht senkrecht im Punkt (0 | 0 | 0). Wo liegt der Schatten der Mastspitze
auf dem Boden (z = 0), und wie lang ist der Schatten?''',
   body='g = Matrix([0, 0, 6]) + t * Matrix([1, 2, -4])\nP = g.subs(t, solve(g[2], t)[0])\ndisplay(P)\nP.norm()')
t_('''Wo liegt der Schatten der Mastspitze aus der vorigen Aufgabe auf einer schrägen Ebene (Hang) x + y + 2z = 3? Wie weit ist der Schattenpunkt von der Mastspitze entfernt (4 Ziffern)?''',
   body='g = Matrix([0, 0, 6]) + t * Matrix([1, 2, -4])\nP = g.subs(t, solve(g[0] + g[1] + 2*g[2] - 3, t)[0])\ndisplay(P)\nN((P - Matrix([0, 0, 6])).norm(), 4)')
t_('''Zwei Schiffe bewegen sich auf dem Meer (z = 0): S₁(t) = (0, 0, 0) + t · (3, 4, 0), S₂(t) = (10, 0, 0) + t · (−1, 5, 0) (Einheit km, t in Stunden).
Wann sind sie sich am nächsten, und wie weit sind sie dann voneinander entfernt (4 Ziffern)?''',
   body='S1 = t * Matrix([3, 4, 0])\nS2 = Matrix([10, 0, 0]) + t * Matrix([-1, 5, 0])\nd2 = expand((S1 - S2).dot(S1 - S2))\ntm = solve(diff(d2, t), t)[0]\ndisplay(tm)\nN(sqrt(d2.subs(t, tm)), 4)')

# ---------------------------------------------------------------- 8
sec('Gemischte Übungen')
t_('''Gegeben sind A(2 | 0 | 0), B(0 | 2 | 0), C(0 | 0 | 2) und D(2 | 2 | 2). Berechne den Abstand von D zur Ebene ABC, das Volumen der Pyramide ABCD (Grundfläche
mal Höhe durch 3, Grundfläche mit dem Vektorprodukt) und den Winkel zwischen AD und der Ebene (4 Ziffern).''',
   body='A, B, C, D = Matrix([2, 0, 0]), Matrix([0, 2, 0]), Matrix([0, 0, 2]), Matrix([2, 2, 2])\nn = (B - A).cross(C - A)\nh = Abs(n.dot(D - A)) / n.norm()\ndisplay(h)\ndisplay(Rational(1, 3) * n.norm() / 2 * h)\nu = D - A\nN(deg(asin(Abs(u.dot(n)) / (u.norm() * n.norm()))), 4)')
t_('''Welcher Punkt der Ebene x + 2y + 2z = 18 liegt dem Ursprung am nächsten? Wie weit ist er entfernt?''',
   body='n = Matrix([1, 2, 2])\nlot = t * n\nF = lot.subs(t, solve(n.dot(lot) - 18, t)[0])\ndisplay(F)\nF.norm()')
t_('''Ein Würfel hat die Kantenlänge 4 und die Ecken (0 | 0 | 0) bis (4 | 4 | 4). Berechne den Winkel zwischen einer Raumdiagonalen (0 | 0 | 0) → (4 | 4 | 4) und einer
Flächendiagonalen (0 | 0 | 0) → (4 | 4 | 0) in Grad (4 Ziffern) sowie den Abstand der Ecke (4 | 0 | 0) von der Raumdiagonalen.''',
   body='u, v = Matrix([4, 4, 4]), Matrix([4, 4, 0])\ndisplay(N(deg(acos(u.dot(v) / (u.norm() * v.norm()))), 4))\nLine3D(Point3D(0, 0, 0), Point3D(4, 4, 4)).distance(Point3D(4, 0, 0))')
t_('''Für welche Werte von a hat der Punkt P(a | 1 | 1) von der Ebene 2x − y + 2z = 1 den Abstand 3?''',
   given="a = symbols('a', real=True)",
   body='n = Matrix([2, -1, 2])\nsolve(Eq(Abs(n.dot(Matrix([a, 1, 1])) - 1) / n.norm(), 3), a)')

generate('sympy_abstaende_winkel', 'Abstände und Winkel im Raum, Spiegelungen, Flächen und Volumen', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
