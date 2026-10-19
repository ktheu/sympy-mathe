# Erzeugt ../content/sympy_ebenen.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_ebenen.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_ebenen.py
#
# Bildungsplan BW 2016, Kursstufe, Leitidee Raum und Form / Zahl – Variable – Operation:
# lineare Gleichungssysteme mit dem Gauß-Verfahren (Lösungsmengen), Skalarprodukt und Orthogonalität, Ebenen in Parameter-,
# Normalen- und Koordinatenform, Normalenvektor (über LGS; mit Vektorprodukt im Leistungsfach), Spurpunkte,
# Lagebeziehungen Punkt–Ebene, Gerade–Ebene, Ebene–Ebene, Schnittpunkt und Schnittgerade.
# Baut auf sympy_geometrie (Klasse 10: Vektoren als Matrix, norm, cross für Kollinearität, Geraden im Raum) auf.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t_(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = "from sympy import *\ninit_printing()\nimport matplotlib.pyplot as plt\nx, y, z, r, s, t = symbols('x y z r s t', real=True)"

INTRO = '''In diesem Notebook geht es um **Ebenen im Raum**. Zuerst löst du lineare Gleichungssysteme mit dem **Gauß-Verfahren**,
dann lernst du das **Skalarprodukt** kennen und beschreibst Ebenen in **Parameterform**, **Normalenform** und **Koordinatenform**.
Schließlich untersuchst du, wie Punkte, Geraden und Ebenen zueinander liegen, und berechnest Schnittpunkte und Schnittgeraden.

Vektoren schreibst du wie im Notebook *Geometrie* als Spalten: `Matrix([1, 2, 3])`.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy und matplotlib, schaltet die Formel-Ausgabe ein
und legt die Koordinaten `x`, `y`, `z` und die Parameter `r`, `s`, `t` an.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Lineare Gleichungssysteme und das Gauß-Verfahren')
expl('''#### Erweiterte Koeffizientenmatrix und Stufenform

Ein LGS wie

x + y + z = 6, 2x − y + z = 3, x + 2y − z = 2

schreibt man als **erweiterte Koeffizientenmatrix**: jede Zeile eine Gleichung, die letzte Spalte die rechte Seite.
Beim **Gauß-Verfahren** formt man die Zeilen um (Vielfache addieren), bis eine Stufenform entsteht.

- `M.rref()` liefert die **reduzierte Stufenform** (und die Nummern der Pivotspalten). Ganz rechts steht dann die Lösung.
- `linsolve(M, [x, y, z])` gibt direkt die Lösungsmenge aus.
- Zeilen umformen von Hand: `M.row(1)` ist die zweite Zeile (Zählung ab 0); `M[1, :] = M.row(1) - 2 * M.row(0)` ersetzt sie.''',
     """M = Matrix([[1, 1, 1, 6], [2, -1, 1, 3], [1, 2, -1, 2]])
display(M)
M2 = M.copy()
M2[1, :] = M2.row(1) - 2 * M2.row(0)
M2[2, :] = M2.row(2) - M2.row(0)
display(M2)
display(M.rref()[0])
linsolve(M, [x, y, z])""")
expl('''#### Drei Fälle

Ein LGS hat **genau eine**, **keine** oder **unendlich viele** Lösungen. In der Stufenform erkennt man:
- eine Zeile 0 0 0 | c mit c ≠ 0: Widerspruch, keine Lösung (`linsolve` gibt ∅)
- eine Nullzeile 0 0 0 | 0: eine Variable ist frei wählbar, unendlich viele Lösungen (`linsolve` gibt die Lösung mit dieser Variablen).''',
     """A = Matrix([[1, 1, 1, 6], [2, 2, 2, 10], [1, -1, 0, 0]])
display(A.rref()[0], linsolve(A, [x, y, z]))
B = Matrix([[1, 1, 1, 6], [2, 2, 2, 12], [1, -1, 0, 0]])
display(B.rref()[0], linsolve(B, [x, y, z]))""")

t_('Löse das LGS x + 2y − z = 3, 2x − y + z = 4, x + y + 2z = 5 mit `linsolve` und der erweiterten Matrix.',
   body='M = Matrix([[1, 2, -1, 3], [2, -1, 1, 4], [1, 1, 2, 5]])\nlinsolve(M, [x, y, z])')
t_('Gib die reduzierte Stufenform der Matrix aus der vorigen Aufgabe aus.', body='Matrix([[1, 2, -1, 3], [2, -1, 1, 4], [1, 1, 2, 5]]).rref()[0]')
t_('''Führe den ersten Gauß-Schritt von Hand aus: Ziehe für M = [[1, 2, −1, 3], [2, −1, 1, 4], [1, 1, 2, 5]] das 2-Fache der ersten Zeile von der zweiten
und die erste Zeile von der dritten ab. Gib die neue Matrix aus.''',
   body='M = Matrix([[1, 2, -1, 3], [2, -1, 1, 4], [1, 1, 2, 5]])\nM[1, :] = M.row(1) - 2 * M.row(0)\nM[2, :] = M.row(2) - M.row(0)\nM')
t_('Löse das LGS 2x + y = 1, x − y + z = 2, 3x + z = 3 (auch mit Gleichungen möglich: `linsolve([Eq(...), ...], [x, y, z])`).',
   body='linsolve([Eq(2*x + y, 1), Eq(x - y + z, 2), Eq(3*x + z, 3)], [x, y, z])')
t_('Löse das LGS x + y − z = 1, 2x + 2y − 2z = 3, x − y = 0. Gib die Stufenform und die Lösungsmenge aus.',
   body='M = Matrix([[1, 1, -1, 1], [2, 2, -2, 3], [1, -1, 0, 0]])\ndisplay(M.rref()[0])\nlinsolve(M, [x, y, z])')
t_('Löse das LGS x + y − z = 1, 2x + 2y − 2z = 2, x − y = 0. Gib die Stufenform und die Lösungsmenge aus.',
   body='M = Matrix([[1, 1, -1, 1], [2, 2, -2, 2], [1, -1, 0, 0]])\ndisplay(M.rref()[0])\nlinsolve(M, [x, y, z])')
t_('''Für welches a hat das LGS x + y = 2, x + a·y = 3 keine Lösung? Berechne dazu die **Determinante** der Koeffizientenmatrix
(`Matrix([[1, 1], [1, a]]).det()`) und löse det = 0. (Ist die Determinante nicht 0, gibt es genau eine Lösung.)''',
   given="a = symbols('a', real=True)", body='d = Matrix([[1, 1], [1, a]]).det()\ndisplay(d)\nsolve(d, a)')
t_('''Löse das LGS mit vier Unbekannten: w + x + y + z = 10, w − x = −1, x − y = −1, y − z = −1.''',
   given="w = symbols('w', real=True)",
   body='linsolve([Eq(w + x + y + z, 10), Eq(w - x, -1), Eq(x - y, -1), Eq(y - z, -1)], [w, x, y, z])')
predict("""display(linsolve([Eq(x + y, 2), Eq(x - y, 0)], [x, y]))
display(linsolve([Eq(x + y, 2), Eq(2*x + 2*y, 4)], [x, y]))
linsolve([Eq(x + y, 2), Eq(x + y, 3)], [x, y])""")

# ---------------------------------------------------------------- 2
sec('Skalarprodukt und Orthogonalität')
expl('''#### u · v = u₁v₁ + u₂v₂ + u₃v₃

Das **Skalarprodukt** zweier Vektoren ist eine Zahl: `u.dot(v)`. Es gilt:
- u · v = 0 genau dann, wenn u und v **orthogonal** (senkrecht) sind.
- u · u = |u|²

Einen Vektor n, der zu zwei Vektoren u und v orthogonal ist, findet man mit dem LGS n · u = 0, n · v = 0.
Eine Variable ist dabei frei wählbar (es gibt unendlich viele solche Vektoren); man wählt eine einfache Zahl.''',
     """u = Matrix([1, 2, 3])
v = Matrix([2, 0, -1])
display(u.dot(v))
display(Matrix([1, 1, 0]).dot(Matrix([1, -1, 5])))
n1, n2, n3 = symbols('n1 n2 n3', real=True)
n = Matrix([n1, n2, n3])
l = linsolve([n.dot(u), n.dot(v)], [n1, n2, n3])
display(l)
Matrix(list(l)[0]).subs(n3, 2)""")

N3 = "n1, n2, n3 = symbols('n1 n2 n3', real=True)\nn = Matrix([n1, n2, n3])"
t_('Berechne das Skalarprodukt von u = (2, −1, 4) und v = (3, 2, −1).', body='Matrix([2, -1, 4]).dot(Matrix([3, 2, -1]))')
t_('Prüfe, ob u = (1, 2, −2) und v = (4, −1, 1) orthogonal sind.', body='Matrix([1, 2, -2]).dot(Matrix([4, -1, 1])) == 0')
t_('Berechne |u|² für u = (2, 3, 6) einmal mit `u.dot(u)` und einmal mit `u.norm()**2`.', body='u = Matrix([2, 3, 6])\ndisplay(u.dot(u))\nu.norm()**2')
t_('Für welches a sind u = (a, 2, 1) und v = (3, a, −4) orthogonal?', given="a = symbols('a', real=True)",
   body='solve(Matrix([a, 2, 1]).dot(Matrix([3, a, -4])), a)')
t_('''Bestimme einen Vektor n, der zu u = (1, 0, 2) und v = (0, 1, −1) orthogonal ist (wie im Beispiel, setze dann n3 = 1).''', N3,
   'l = linsolve([n.dot(Matrix([1, 0, 2])), n.dot(Matrix([0, 1, -1]))], [n1, n2, n3])\nMatrix(list(l)[0]).subs(n3, 1)')
t_('''**(Leistungsfach)** Das **Vektorprodukt** u × v (`u.cross(v)`) ist immer zu u und v orthogonal. Berechne es für u = (1, 0, 2), v = (0, 1, −1)
und prüfe mit dem Skalarprodukt, dass es zu u und v orthogonal ist.''',
   body='u, v = Matrix([1, 0, 2]), Matrix([0, 1, -1])\nn = u.cross(v)\ndisplay(n)\n(n.dot(u), n.dot(v))')
t_('''Prüfe, ob das Dreieck A(1 | 0 | 0), B(3 | 2 | 1), C(0 | 2 | 2) bei A einen rechten Winkel hat (Skalarprodukt von AB und AC).''',
   body='A, B, C = Matrix([1, 0, 0]), Matrix([3, 2, 1]), Matrix([0, 2, 2])\n(B - A).dot(C - A)')
predict("""u = Matrix([1, 0, 0])
v = Matrix([0, 5, 0])
display(u.dot(v))
display(u.dot(u))
display(v.dot(v))
(2 * u).dot(v + u)""")

# ---------------------------------------------------------------- 3
sec('Ebenen in Parameterform')
expl('''#### E: x⃗ = p⃗ + r · u⃗ + s · v⃗

Eine Ebene ist festgelegt durch einen **Stützpunkt** P und zwei **Spannvektoren** u, v, die nicht kollinear sind.
Jeder Punkt der Ebene ergibt sich für passende Werte der Parameter r und s.

Ebene durch drei Punkte A, B, C: Stützvektor A, Spannvektoren AB und AC.

**Punktprobe:** Liegt Q in E? Löse p + r·u + s·v = q nach r und s (drei Gleichungen, zwei Unbekannte).''',
     """P = Matrix([1, 0, 2])
u = Matrix([1, 1, 0])
v = Matrix([0, 1, 1])
E = P + r * u + s * v
display(E)
display(E.subs({r: 2, s: -1}))
display(solve(list(E - Matrix([3, 3, 3])), [r, s]))
solve(list(E - Matrix([3, 3, 4])), [r, s])""")

EP = "E = Matrix([1, 0, 2]) + r * Matrix([1, 1, 0]) + s * Matrix([0, 1, 1])"
t_('Gib für die Ebene E aus dem Beispiel die Punkte für (r, s) = (0, 0), (1, 0) und (1, 1) als Liste aus.', EP,
   '[list(E.subs({r: a, s: b})) for a, b in [(0, 0), (1, 0), (1, 1)]]')
t_('Prüfe, ob Q(0 | −2 | 0) in E liegt.', EP, 'solve(list(E - Matrix([0, -2, 0])), [r, s])')
t_('Prüfe, ob Q(2 | 4 | 5) in E liegt.', EP, 'solve(list(E - Matrix([2, 4, 5])), [r, s])')
t_('Gib eine Parameterform der Ebene durch A(1 | 2 | 0), B(3 | 0 | 1) und C(0 | 1 | 4) aus.',
   body='A, B, C = Matrix([1, 2, 0]), Matrix([3, 0, 1]), Matrix([0, 1, 4])\nA + r * (B - A) + s * (C - A)')
t_('''Liegen die Punkte A(1 | 1 | 1), B(2 | 3 | 1) und C(4 | 7 | 1) so, dass sie eine Ebene festlegen? Prüfe, ob AB und AC kollinear sind (Kreuzprodukt).''',
   body='A, B, C = Matrix([1, 1, 1]), Matrix([2, 3, 1]), Matrix([4, 7, 1])\n(B - A).cross(C - A)')
t_('''Für welches a liegt Q(a | 3 | 4) in der Ebene E aus dem Beispiel? Löse nach r, s und a.''', EP,
   "a = symbols('a', real=True)\nsolve(list(E - Matrix([a, 3, 4])), [r, s, a])")

# ---------------------------------------------------------------- 4
sec('Normalenform und Koordinatenform')
expl('''#### n⃗ · (x⃗ − p⃗) = 0 und ax + by + cz = d

Ein **Normalenvektor** n steht senkrecht auf der Ebene. Ein Punkt X liegt genau dann in E, wenn X − P orthogonal zu n ist:
**Normalenform** n · (x − p) = 0. Multipliziert man aus, entsteht die **Koordinatenform** n₁x + n₂y + n₃z = d.
Die Koeffizienten vor x, y, z sind der Normalenvektor.

Von der Parameterform zur Koordinatenform: Normalenvektor bestimmen (LGS wie in Abschnitt 2 oder im Leistungsfach mit dem Vektorprodukt),
dann d = n · p.

`Plane(Point3D(...), normal_vector=(...))` ist eine sympy-Ebene; `.equation(x, y, z)` gibt die Koordinatenform als Term ... = 0 aus.''',
     """P = Matrix([1, 0, 2])
n = Matrix([1, -1, 1])
X = Matrix([x, y, z])
display(expand(n.dot(X - P)))
display(Eq(n.dot(X), n.dot(P)))
E = Plane(Point3D(1, 0, 2), normal_vector=(1, -1, 1))
display(E.equation(x, y, z))
Plane(Point3D(1, 0, 0), Point3D(0, 2, 0), Point3D(0, 0, 3)).equation(x, y, z)""")

X = 'X = Matrix([x, y, z])'
t_('Gib die Koordinatenform der Ebene durch P(2 | 1 | −1) mit dem Normalenvektor n = (3, −2, 1) aus (als `Eq`).', X,
   'n, P = Matrix([3, -2, 1]), Matrix([2, 1, -1])\nEq(n.dot(X), n.dot(P))')
t_('Prüfe, ob die Punkte Q(1 | 1 | 1) und R(0 | 0 | 3) in der Ebene E: 3x − 2y + z = 3 liegen (zwei Wahrheitswerte).',
   body='ebene = Eq(3*x - 2*y + z, 3)\ndisplay(ebene.subs({x: 1, y: 1, z: 1}))\nebene.subs({x: 0, y: 0, z: 3})')
t_('''Wandle die Parameterform E: x = (1, 0, 2) + r · (1, 1, 0) + s · (0, 1, 1) in Koordinatenform um. Bestimme n mit dem LGS (n3 = 1) und dann d.''',
   N3 + '\n' + X,
   'l = linsolve([n.dot(Matrix([1, 1, 0])), n.dot(Matrix([0, 1, 1]))], [n1, n2, n3])\nnv = Matrix(list(l)[0]).subs(n3, 1)\ndisplay(nv)\nEq(nv.dot(X), nv.dot(Matrix([1, 0, 2])))')
t_('''**(Leistungsfach)** Dieselbe Umwandlung mit dem Vektorprodukt: n = u × v, dann d = n · p.''', X,
   'n = Matrix([1, 1, 0]).cross(Matrix([0, 1, 1]))\ndisplay(n)\nEq(n.dot(X), n.dot(Matrix([1, 0, 2])))')
t_('Gib die Koordinatenform der Ebene durch A(1 | 2 | 0), B(3 | 0 | 1) und C(0 | 1 | 4) mit `Plane(...).equation(x, y, z)` aus.',
   body='Plane(Point3D(1, 2, 0), Point3D(3, 0, 1), Point3D(0, 1, 4)).equation(x, y, z)')
t_('Gib einen Normalenvektor und einen Punkt der Ebene E: 2x + y − 3z = 6 aus (einen Punkt findest du z. B. mit y = z = 0).',
   body='display(Matrix([2, 1, -3]))\nsolve(Eq(2*x, 6), x)')
t_('''Wandle die Koordinatenform E: x + 2y − z = 4 in eine Parameterform um: Löse die Gleichung nach x auf, setze y = r und z = s.''',
   body='xr = solve(Eq(x + 2*y - z, 4), x)[0]\nMatrix([xr, y, z]).subs({y: r, z: s})')
t_('''Gib die Koordinatenform der Ebene, die durch P(1 | 1 | 1) geht und zur Ebene 2x − y + 2z = 7 parallel ist, aus (gleicher Normalenvektor).''', X,
   'n = Matrix([2, -1, 2])\nEq(n.dot(X), n.dot(Matrix([1, 1, 1])))')
t_('''Gib die Koordinatenform der Ebene aus, die durch P(0 | 2 | 1) geht und senkrecht zur Geraden g: x = (1, 0, 0) + t · (1, 2, −2) steht.''', X,
   'n = Matrix([1, 2, -2])\nEq(n.dot(X), n.dot(Matrix([0, 2, 1])))')
predict("""E = Eq(x + y + z, 3)
display(E.subs({x: 1, y: 1, z: 1}))
display(E.subs({x: 3, y: 0, z: 0}))
E.subs({x: 1, y: 2, z: 3})""")

# ---------------------------------------------------------------- 5
sec('Spurpunkte und Darstellung')
expl('''#### Schnittpunkte mit den Koordinatenachsen

Die **Spurpunkte** einer Ebene sind ihre Schnittpunkte mit den Koordinatenachsen. Für die x₁-Achse setzt man y = z = 0 usw.
Mit den Spurpunkten kann man die Ebene als Dreieck im Koordinatensystem zeichnen.

`plot3d` zeichnet eine Ebene, die man nach z auflösen kann, als Fläche. Es muss extra geladen werden: `from sympy.plotting import plot3d`.''',
     """ebene = 6*x + 3*y + 2*z - 6
display(solve(ebene.subs({y: 0, z: 0}), x))
display(solve(ebene.subs({x: 0, z: 0}), y))
display(solve(ebene.subs({x: 0, y: 0}), z))
zf = solve(ebene, z)[0]
display(zf)
from sympy.plotting import plot3d
plot3d(zf, (x, 0, 1), (y, 0, 2));""")

t_('Gib die Spurpunkte der Ebene 2x + 4y + z = 8 als Liste von Punkten (Listen mit drei Koordinaten) aus.',
   body='e = 2*x + 4*y + z - 8\n[[solve(e.subs({y: 0, z: 0}), x)[0], 0, 0], [0, solve(e.subs({x: 0, z: 0}), y)[0], 0], [0, 0, solve(e.subs({x: 0, y: 0}), z)[0]]]')
t_('Gib die Spurpunkte der Ebene 3x − 2y + 6z = 12 aus.',
   body='e = 3*x - 2*y + 6*z - 12\n[solve(e.subs({y: 0, z: 0}), x), solve(e.subs({x: 0, z: 0}), y), solve(e.subs({x: 0, y: 0}), z)]')
t_('''Die Ebene x + y = 4 hat keinen Spurpunkt mit der z-Achse. Gib die Lösung für x = y = 0 aus (leere Liste) und die beiden anderen Spurpunkte (x und y).''',
   body='e = x + y - 4\ndisplay(solve(e.subs({x: 0, y: 0}), z))\n[solve(e.subs({y: 0}), x), solve(e.subs({x: 0}), y)]')
t_('''Bestimme die Koordinatenform der Ebene mit den Spurpunkten (2 | 0 | 0), (0 | 4 | 0) und (0 | 0 | 5) (Achsenabschnittsform x/2 + y/4 + z/5 = 1, mit 20 multipliziert).''',
   body='Plane(Point3D(2, 0, 0), Point3D(0, 4, 0), Point3D(0, 0, 5)).equation(x, y, z)')
t_('Zeichne die Ebene 2x + 4y + z = 8 mit `plot3d` für 0 ≤ x ≤ 4, 0 ≤ y ≤ 2.',
   body='from sympy.plotting import plot3d\nplot3d(solve(2*x + 4*y + z - 8, z)[0], (x, 0, 4), (y, 0, 2));')

# ---------------------------------------------------------------- 6
sec('Lage von Gerade und Ebene')
expl('''#### Gerade in die Koordinatenform einsetzen

Setzt man die Koordinaten der Geraden g: x = p + t · v in die Koordinatenform von E ein, entsteht eine Gleichung für t:
- genau eine Lösung: g **schneidet** E (Schnittpunkt durch Einsetzen von t in g)
- keine Lösung: g ist **parallel** zu E (fällt t beim Einsetzen weg, zeigt sympy gleich `False` an)
- jedes t ist Lösung (die Gleichung wird zu True): g **liegt in** E

Kontrolle: g ist genau dann parallel zu E oder liegt in E, wenn v · n = 0.''',
     """g = Matrix([1, 0, 2]) + t * Matrix([1, 1, 1])
gl = Eq(6*g[0] + 3*g[1] + 2*g[2], 6)
display(gl)
l = solve(gl, t)
display(l)
g.subs(t, l[0])""")

t_('Berechne den Schnittpunkt der Geraden g: x = (0, 0, 1) + t · (1, 2, 1) mit der Ebene E: x + y + z = 9.',
   body='g = Matrix([0, 0, 1]) + t * Matrix([1, 2, 1])\nl = solve(Eq(g[0] + g[1] + g[2], 9), t)\ng.subs(t, l[0])')
t_('Untersuche die Lage von g: x = (1, 1, 1) + t · (1, −1, 0) und E: x + y + z = 5 (Gleichung für t und Lösung ausgeben).',
   body='g = Matrix([1, 1, 1]) + t * Matrix([1, -1, 0])\ngl = Eq(g[0] + g[1] + g[2], 5)\ndisplay(gl)\nsolve(gl, t)')
t_('Untersuche die Lage von g: x = (1, 1, 1) + t · (1, −1, 0) und E: x + y + z = 3.',
   body='g = Matrix([1, 1, 1]) + t * Matrix([1, -1, 0])\nEq(g[0] + g[1] + g[2], 3)')
t_('Prüfe mit dem Skalarprodukt v · n, ob g: x = (2, 0, 1) + t · (1, 2, 4) parallel zu E: 2x + y − z = 3 ist oder in ihr liegt.',
   body='Matrix([1, 2, 4]).dot(Matrix([2, 1, -1]))')
t_('''Berechne den Schnittpunkt der Geraden durch A(1 | 2 | 3) und B(3 | 3 | 1) mit der x-y-Ebene (z = 0).''',
   body='A, B = Matrix([1, 2, 3]), Matrix([3, 3, 1])\ng = A + t * (B - A)\ng.subs(t, solve(g[2], t)[0])')
t_('''Berechne mit `Plane(...).intersection(Line3D(...))` den Schnittpunkt von E: 6x + 3y + 2z = 6 (durch die Spurpunkte gegeben) mit der Geraden durch (0|0|0) und (1|1|1).''',
   body='E = Plane(Point3D(1, 0, 0), Point3D(0, 2, 0), Point3D(0, 0, 3))\nE.intersection(Line3D(Point3D(0, 0, 0), Point3D(1, 1, 1)))')
t_('''**Lichtstrahl:** Ein Lichtstrahl geht von L(6 | 2 | 8) in Richtung v = (−2, 1, −4). Wo trifft er die Ebene z = 0 (den Boden)?''',
   body='g = Matrix([6, 2, 8]) + t * Matrix([-2, 1, -4])\ng.subs(t, solve(g[2], t)[0])')
t_('''Für welches a ist die Gerade g: x = (0, 0, 0) + t · (1, a, 2) parallel zur Ebene E: 3x − y + z = 4?''',
   given="a = symbols('a', real=True)", body='solve(Matrix([1, a, 2]).dot(Matrix([3, -1, 1])), a)')

# ---------------------------------------------------------------- 7
sec('Lage zweier Ebenen und Schnittgerade')
expl('''#### Zwei Koordinatengleichungen als LGS

Zwei Ebenen sind **parallel** oder **identisch**, wenn ihre Normalenvektoren kollinear sind (Kreuzprodukt = Nullvektor). Sonst schneiden sie
sich in einer **Schnittgeraden**. Man findet sie, indem man das LGS aus den beiden Koordinatengleichungen löst: Eine Variable bleibt frei,
sie wird zum Parameter t.''',
     """l = linsolve([Eq(2*x - y + z, 3), Eq(x + y - z, 0)], [x, y, z])
display(l)
g = Matrix(list(l)[0]).subs(z, t)
display(g)
display(g.subs(t, 0), g.diff(t))
Matrix([2, -1, 1]).cross(Matrix([1, 1, -1]))""")

t_('Bestimme die Schnittgerade der Ebenen x + y + z = 6 und x − y + 2z = 3 (freie Variable z wird zu t).',
   body='l = linsolve([Eq(x + y + z, 6), Eq(x - y + 2*z, 3)], [x, y, z])\nMatrix(list(l)[0]).subs(z, t)')
t_('Gib für die Schnittgerade der vorigen Aufgabe den Stützvektor (t = 0) und den Richtungsvektor (`g.diff(t)`) aus.',
   body='g = Matrix([Rational(9, 2) - 3*t/2, Rational(3, 2) + t/2, t])\ndisplay(g.subs(t, 0))\ng.diff(t)')
t_('Untersuche, ob die Ebenen 2x − 4y + 6z = 5 und −x + 2y − 3z = 1 parallel sind (Kreuzprodukt der Normalenvektoren) und ob sie gemeinsame Punkte haben (`linsolve`).',
   body='display(Matrix([2, -4, 6]).cross(Matrix([-1, 2, -3])))\nlinsolve([Eq(2*x - 4*y + 6*z, 5), Eq(-x + 2*y - 3*z, 1)], [x, y, z])')
t_('Untersuche die Ebenen 2x − 4y + 6z = −2 und −x + 2y − 3z = 1 (`linsolve` mit beiden Gleichungen).',
   body='linsolve([Eq(2*x - 4*y + 6*z, -2), Eq(-x + 2*y - 3*z, 1)], [x, y, z])')
t_('Bestimme die Schnittgerade der Ebene 2x + y + z = 4 mit der x-y-Ebene (z = 0). Die freie Variable ist y; setze y = t.',
   body='l = linsolve([Eq(2*x + y + z, 4), Eq(z, 0)], [x, y, z])\nMatrix(list(l)[0]).subs(y, t)')
t_('''Bestimme den Schnittpunkt dreier Ebenen x + y + z = 6, x − y = 1, y − z = −1.''',
   body='linsolve([Eq(x + y + z, 6), Eq(x - y, 1), Eq(y - z, -1)], [x, y, z])')
t_('''Berechne die Schnittgerade der Ebenen mit `Plane(...).intersection(Plane(...))` für E₁: x + y + z = 6 (Normalenvektor (1, 1, 1) durch (6 | 0 | 0)) und
E₂: x − y + 2z = 3 (Normalenvektor (1, −1, 2) durch (3 | 0 | 0)).''',
   body='E1 = Plane(Point3D(6, 0, 0), normal_vector=(1, 1, 1))\nE2 = Plane(Point3D(3, 0, 0), normal_vector=(1, -1, 2))\nE1.intersection(E2)')

# ---------------------------------------------------------------- 8
sec('Gemischte Übungen')
t_('''Eine Pyramide hat die Grundfläche A(0 | 0 | 0), B(4 | 0 | 0), C(4 | 4 | 0), D(0 | 4 | 0) und die Spitze S(2 | 2 | 6).
Gib die Koordinatenform der Seitenfläche durch B, C und S aus.''',
   body='Plane(Point3D(4, 0, 0), Point3D(4, 4, 0), Point3D(2, 2, 6)).equation(x, y, z)')
t_('''Wo trifft die Gerade durch P(0 | 6 | 2) mit dem Richtungsvektor (1, −2, 1) die Ebene der vorigen Aufgabe (3x + z − 12 = 0)?''',
   body='g = Matrix([0, 6, 2]) + t * Matrix([1, -2, 1])\ng.subs(t, solve(3*g[0] + g[2] - 12, t)[0])')
t_('''Für welches a liegt der Punkt P(1 | a | 2) in der Ebene durch A(1 | 0 | 0), B(0 | 1 | 0), C(0 | 0 | 1)?''',
   given="a = symbols('a', real=True)",
   body='e = Plane(Point3D(1, 0, 0), Point3D(0, 1, 0), Point3D(0, 0, 1)).equation(x, y, z)\nsolve(e.subs({x: 1, y: a, z: 2}), a)')
t_('''Gegeben ist die Ebenenschar Eₐ: a·x + y + z = 2. Für welches a ist Eₐ parallel zur Geraden g: x = t · (1, 2, 3)? Für welches a enthält Eₐ den Punkt (1 | 1 | 1)?''',
   given="a = symbols('a', real=True)",
   body='display(solve(Matrix([a, 1, 1]).dot(Matrix([1, 2, 3])), a))\nsolve(a + 1 + 1 - 2, a)')
t_('''Prüfe, ob die vier Punkte A(1 | 0 | 0), B(0 | 2 | 0), C(0 | 0 | 3) und D(1 | 2 | −3) in einer Ebene liegen (Ebene durch A, B, C, dann D einsetzen).''',
   body='e = Plane(Point3D(1, 0, 0), Point3D(0, 2, 0), Point3D(0, 0, 3)).equation(x, y, z)\ne.subs({x: 1, y: 2, z: -3}) == 0')

generate('sympy_ebenen', 'Ebenen: LGS, Skalarprodukt, Ebenengleichungen, Lagebeziehungen', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
