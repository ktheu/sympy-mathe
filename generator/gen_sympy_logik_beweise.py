# Erzeugt ../content/sympy_logik_beweise.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_logik_beweise.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_logik_beweise.py
#
# Vertiefungskurs Mathematik BW (Themen laut Kursbeschreibungen und Zertifikatsklausur der Uni Stuttgart):
# Aussagenlogik (Verknüpfungen, Wahrheitstafeln, Tautologien, logische Gesetze), Beweistechniken (direkter Beweis,
# Kontraposition, Widerspruch, Fallunterscheidung, Gegenbeispiel), vollständige Induktion, Ungleichungen (Lösungsmengen,
# Beweis allgemeingültiger Ungleichungen). sympy prüft und rechnet; der Beweisgedanke steht in den Erklärungen.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = ("from sympy import *\nfrom sympy.logic.boolalg import truth_table\ninit_printing()\n"
         "A, B, C = symbols('A B C')\nn, k = symbols('n k', integer=True, positive=True)\nx = symbols('x', real=True)\n"
         "a, b = symbols('a b', positive=True)")

INTRO = '''In diesem Notebook (Vertiefungskurs) geht es um **Logik und Beweise**: Aussagen verknüpfen, Wahrheitstafeln aufstellen, logische
Gesetze prüfen, Beweistechniken (direkter Beweis, Kontraposition, Widerspruch, Fallunterscheidung) und die **vollständige Induktion**.
Am Ende löst und beweist du **Ungleichungen**.

sympy kann einen Beweis nicht für dich führen. Es kann aber Wahrheitstafeln erstellen, logische Ausdrücke vereinfachen, die
Rechenschritte eines Beweises (z. B. den Induktionsschritt) nachrechnen und nach **Gegenbeispielen** suchen.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy und die Funktion `truth_table`, schaltet die
Formel-Ausgabe ein und legt an: die Aussagen `A`, `B`, `C`, die natürlichen Zahlen `n`, `k`, die reelle Zahl `x` und die positiven Zahlen `a`, `b`.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Aussagen und Verknüpfungen')
expl('''#### Und, oder, nicht, wenn-dann, genau-dann-wenn

Eine **Aussage** ist entweder wahr oder falsch. In sympy stehen die Symbole `A`, `B`, `C` für Aussagen.

| Verknüpfung | Zeichen | sympy | wahr, wenn ... |
|---|---|---|---|
| Konjunktion (und) | A ∧ B | `A & B` oder `And(A, B)` | beide wahr |
| Disjunktion (oder) | A ∨ B | `A \\| B` oder `Or(A, B)` | mindestens eine wahr |
| Negation (nicht) | ¬A | `~A` oder `Not(A)` | A falsch |
| Implikation | A ⇒ B | `Implies(A, B)` | nicht (A wahr und B falsch) |
| Äquivalenz | A ⇔ B | `Equivalent(A, B)` | beide gleich |
| ausschließendes Oder | A ⊕ B | `Xor(A, B)` | genau eine wahr |

Mit `.subs({A: True, B: False})` setzt man Wahrheitswerte ein. `truth_table(ausdruck, [A, B])` liefert die **Wahrheitstafel**
Zeile für Zeile (1 = wahr, 0 = falsch).''',
     """e = Implies(A, B)
display(e)
display(e.subs({A: True, B: False}))
for zeile in truth_table(e, [A, B]):
    print(zeile)""")

t('Gib die Wahrheitstafel von A ∧ B aus (wie im Beispiel mit `print`).', body='for zeile in truth_table(A & B, [A, B]):\n    print(zeile)')
t('Gib die Wahrheitstafel von A ∨ ¬B aus.', body='for zeile in truth_table(A | ~B, [A, B]):\n    print(zeile)')
t('Gib die Wahrheitstafel von A ⇔ B aus.', body='for zeile in truth_table(Equivalent(A, B), [A, B]):\n    print(zeile)')
t('Gib die Wahrheitstafel von (A ∧ B) ⇒ C aus (8 Zeilen).', body='for zeile in truth_table(Implies(A & B, C), [A, B, C]):\n    print(zeile)')
t('Berechne den Wahrheitswert von (A ∨ B) ∧ ¬C für A = falsch, B = wahr, C = falsch.', body='((A | B) & ~C).subs({A: False, B: True, C: False})')
t('''Übersetze und prüfe: „Wenn es regnet (R), ist die Straße nass (S).“ Es regnet nicht, die Straße ist nass. Ist die Aussage wahr?''',
  given="R, S_ = symbols('R S_')", body='Implies(R, S_).subs({R: False, S_: True})')
t('''Gib die Wahrheitstafel von A ⊕ B (`Xor`) aus und den vereinfachten Ausdruck ohne Xor (`simplify_logic`).''',
  body='for zeile in truth_table(Xor(A, B), [A, B]):\n    print(zeile)\nsimplify_logic(Xor(A, B))')
predict("""display(And(True, False))
display(Or(True, False))
display(Implies(False, False))
Not(Equivalent(True, False))""")

# ---------------------------------------------------------------- 2
sec('Logische Gesetze und Tautologien')
expl('''#### Immer wahr: Tautologie

Ein Ausdruck, der für **alle** Wahrheitswerte wahr ist, heißt **Tautologie**. Zwei Ausdrücke sind **logisch gleichwertig**, wenn
`Equivalent(ausdruck1, ausdruck2)` eine Tautologie ist.

- `simplify_logic(ausdruck)` vereinfacht; bei einer Tautologie kommt `True` heraus, bei einem Widerspruch `False`.
- `satisfiable(ausdruck)` sucht eine Belegung, die den Ausdruck wahr macht, und gibt sie als Dictionary aus (oder `False`, wenn es keine gibt).
  Die Reihenfolge im Dictionary kann wechseln; mit `m[A]` liest du den Wert von A ab.

Wichtige Gesetze: **De Morgan** ¬(A ∧ B) ⇔ ¬A ∨ ¬B, **Kontraposition** (A ⇒ B) ⇔ (¬B ⇒ ¬A), (A ⇒ B) ⇔ ¬A ∨ B.''',
     """display(simplify_logic(Equivalent(~(A & B), ~A | ~B)))
display(simplify_logic(Equivalent(Implies(A, B), Implies(~B, ~A))))
display(simplify_logic(Implies(A, B)))
display(satisfiable(A & ~A))
m = satisfiable(Implies(A, B) & A)
(m[A], m[B])""")

t('Prüfe das zweite De-Morgan-Gesetz ¬(A ∨ B) ⇔ ¬A ∧ ¬B.', body='simplify_logic(Equivalent(~(A | B), ~A & ~B))')
t('Prüfe, ob (A ⇒ B) und (B ⇒ A) gleichwertig sind (die **Umkehrung** einer Aussage).', body='simplify_logic(Equivalent(Implies(A, B), Implies(B, A)))')
t('Finde mit `satisfiable` eine Belegung, für die (A ⇒ B) wahr, aber (B ⇒ A) falsch ist. Gib die Werte (A, B) als Tupel aus.', body='m = satisfiable(Implies(A, B) & ~Implies(B, A))\n(m[A], m[B])')
t('Prüfe das Distributivgesetz A ∧ (B ∨ C) ⇔ (A ∧ B) ∨ (A ∧ C).', body='simplify_logic(Equivalent(A & (B | C), (A & B) | (A & C)))')
t('Prüfe, ob der **Modus ponens** ((A ⇒ B) ∧ A) ⇒ B eine Tautologie ist.', body='simplify_logic(Implies(Implies(A, B) & A, B))')
t('Prüfe, ob ((A ⇒ B) ∧ B) ⇒ A eine Tautologie ist (ein häufiger Fehlschluss). Gib auch eine Gegen-Belegung (A, B) aus.',
  body='e = Implies(Implies(A, B) & B, A)\ndisplay(simplify_logic(e))\nm = satisfiable(~e)\n(m[A], m[B])')
t('Prüfe die **Kettenschlussregel** ((A ⇒ B) ∧ (B ⇒ C)) ⇒ (A ⇒ C).', body='simplify_logic(Implies(Implies(A, B) & Implies(B, C), Implies(A, C)))')
t('Vereinfache ¬(A ⇒ B) und (A ∧ B) ∨ (A ∧ ¬B) ∨ (¬A ∧ B).', body='display(simplify_logic(~Implies(A, B)))\nsimplify_logic((A & B) | (A & ~B) | (~A & B))')
t('''Prüfe, ob A ⇒ (B ⇒ A) eine Tautologie ist und ob (A ∨ B) ∧ ¬A ∧ ¬B erfüllbar ist.''',
  body='display(simplify_logic(Implies(A, Implies(B, A))))\nsatisfiable((A | B) & ~A & ~B)')
predict("""display(simplify_logic(A | ~A))
display(simplify_logic(A & ~A))
display(simplify_logic(~~A))
simplify_logic(A & (A | B))""")

# ---------------------------------------------------------------- 3
sec('Gegenbeispiele und Beweistechniken')
expl('''#### Für alle n? Ein Gegenbeispiel genügt

Eine Aussage „für alle n gilt ...“ kann man durch Ausprobieren **nicht beweisen**, aber durch **ein Gegenbeispiel widerlegen**.
Ein bekanntes Beispiel: n² + n + 41 ist für n = 0, 1, ..., 39 eine Primzahl, aber nicht für alle n.

`all(liste)` ist True, wenn alle Einträge wahr sind; `isprime(z)` prüft, ob z eine Primzahl ist.''',
     """display(all([isprime(m**2 + m + 41) for m in range(40)]))
gegen = [m for m in range(100) if not isprime(m**2 + m + 41)]
display(gegen[:3])
factorint(40**2 + 40 + 41)""")
expl('''#### Direkter Beweis, Fallunterscheidung, Kontraposition, Widerspruch

- **Direkter Beweis:** Aus der Voraussetzung durch Umformen die Behauptung folgern. Beispiel: Die Summe dreier aufeinanderfolgender
  Zahlen n + (n + 1) + (n + 2) = 3(n + 1) ist durch 3 teilbar. Die Umformung prüft `factor()`.
- **Fallunterscheidung:** Jede ganze Zahl lässt bei Division durch 3 den Rest 0, 1 oder 2; man prüft jeden Fall einzeln.
  Ist m = 3q + r, dann hat m² denselben Rest wie r² (Modulo-Operator `%`).
- **Kontraposition:** Statt A ⇒ B beweist man ¬B ⇒ ¬A. Beispiel: „n² gerade ⇒ n gerade“ folgt aus „n ungerade ⇒ n² ungerade“: (2q + 1)² = 2(2q² + 2q) + 1.
- **Widerspruchsbeweis:** Man nimmt das Gegenteil an und folgert etwas Falsches (z. B. dass √2 ein gekürzter Bruch p/q ist, führt dazu,
  dass p und q beide gerade sind).''',
     """display(factor(n + (n + 1) + (n + 2)))
display([r**2 % 3 for r in range(3)])
q = symbols('q', integer=True)
expand((2*q + 1)**2)""")

t('''Widerlege: „Für alle natürlichen Zahlen n ist 2^(2ⁿ) + 1 eine Primzahl.“ Gib das kleinste Gegenbeispiel n (Schleife ab n = 0, `isprime`) und die Zerlegung mit `factorint` aus.''',
  body='m = 0\nwhile isprime(2**(2**m) + 1):\n    m += 1\ndisplay(m)\nfactorint(2**(2**m) + 1)')
t('''Widerlege: „n² − n + 11 ist für alle n ≥ 1 eine Primzahl.“ Gib die ersten drei Gegenbeispiele bis 100 aus.''',
  body='[m for m in range(1, 101) if not isprime(m**2 - m + 11)][:3]')
t('''Prüfe für n = 1 bis 1000, dass n³ − n immer durch 6 teilbar ist (`all`), und zeige mit `factor`, warum: Das Produkt dreier aufeinanderfolgender Zahlen.''',
  body='display(all([(m**3 - m) % 6 == 0 for m in range(1, 1001)]))\nfactor(n**3 - n)')
t('''**Direkter Beweis:** Zeige mit `expand`, dass die Differenz zweier aufeinanderfolgender Quadratzahlen (n + 1)² − n² immer ungerade ist.''',
  body='expand((n + 1)**2 - n**2)')
t('''**Direkter Beweis:** Die Summe von vier aufeinanderfolgenden Zahlen ist nie durch 4 teilbar. Zeige mit `expand`, dass sie 4n + 6 ist (Rest 2 bei Division durch 4).''',
  body='expand(n + (n + 1) + (n + 2) + (n + 3))')
t('''**Fallunterscheidung:** Welche Reste kann eine Quadratzahl bei Division durch 4 lassen? Prüfe alle Reste r = 0, 1, 2, 3 und gib die Menge der Reste von r² aus.''',
  body='set([r**2 % 4 for r in range(4)])')
t('''**Fallunterscheidung:** Zeige, dass n⁵ − n immer durch 5 teilbar ist: Prüfe die Reste r = 0, ..., 4 (Rest von r⁵ − r bei Division durch 5).''',
  body='[(r**5 - r) % 5 for r in range(5)]')
t('''**Kontraposition:** Zeige „ist n² durch 3 teilbar, dann auch n“ über die Kontraposition: Für n = 3q + 1 und n = 3q + 2 ist n² nicht durch 3 teilbar. Gib (3q + 1)² und (3q + 2)² ausmultipliziert aus.''',
  given="q = symbols('q', integer=True)", body='display(expand((3*q + 1)**2))\nexpand((3*q + 2)**2)')
t('''**Widerspruch:** Angenommen √2 = p/q mit teilerfremden p, q. Dann ist p² = 2q². Gib für p = 2r die Gleichung (2r)² = 2q² nach q² aufgelöst aus. (Dann ist auch q gerade – Widerspruch zur Teilerfremdheit.)''',
  given="p, q, r = symbols('p q r', integer=True, positive=True)", body='solve(Eq((2*r)**2, 2*q**2), q**2)')

# ---------------------------------------------------------------- 4
sec('Vollständige Induktion')
expl('''#### Induktionsanfang und Induktionsschritt

Um eine Aussage A(n) für alle n ≥ 1 zu beweisen:
1. **Induktionsanfang:** A(1) ist wahr.
2. **Induktionsschritt:** Aus A(n) (Induktionsvoraussetzung) folgt A(n + 1).

Beispiel: 1 + 2 + ... + n = n(n + 1)/2. Im Induktionsschritt rechnet man: Summe bis n + 1 = (Summe bis n) + (n + 1) = n(n + 1)/2 + (n + 1).
Zu zeigen ist, dass das gleich (n + 1)(n + 2)/2 ist. sympy prüft diesen Rechenschritt mit `simplify(... - ...) == 0`.

`summation(term, (k, 1, n))` berechnet Summen auch allgemein, das ist eine gute Kontrolle für die Formel.''',
     """Sn = n * (n + 1) / 2
display(Sn.subs(n, 1))
display(simplify(Sn + (n + 1) - Sn.subs(n, n + 1)))
display(summation(k, (k, 1, n)))
[summation(k, (k, 1, m)) == m * (m + 1) / 2 for m in range(1, 6)]""")

t('''Beweise 1 + 3 + 5 + ... + (2n − 1) = n²: Gib den Induktionsanfang (Formel für n = 1 und erster Summand) und den Induktionsschritt (Differenz muss 0 sein) aus.''',
  body='Sn = n**2\ndisplay((Sn.subs(n, 1), 2*1 - 1))\nsimplify(Sn + (2*(n + 1) - 1) - Sn.subs(n, n + 1))')
t('''Beweise 1² + 2² + ... + n² = n(n + 1)(2n + 1)/6 (Anfang und Schritt wie oben).''',
  body='Sn = n * (n + 1) * (2*n + 1) / 6\ndisplay(Sn.subs(n, 1))\nsimplify(Sn + (n + 1)**2 - Sn.subs(n, n + 1))')
t('''Beweise 1³ + 2³ + ... + n³ = (n(n + 1)/2)².''',
  body='Sn = (n * (n + 1) / 2)**2\ndisplay(Sn.subs(n, 1))\nsimplify(Sn + (n + 1)**3 - Sn.subs(n, n + 1))')
t('''Bestimme mit `summation` eine Formel für 1·2 + 2·3 + ... + n(n + 1) (mit `factor`) und prüfe den Induktionsschritt für diese Formel.''',
  body='Sn = factor(summation(k * (k + 1), (k, 1, n)))\ndisplay(Sn)\nsimplify(Sn + (n + 1) * (n + 2) - Sn.subs(n, n + 1))')
t('''**Geometrische Summe:** Beweise 1 + 2 + 4 + ... + 2ⁿ⁻¹ = 2ⁿ − 1.''',
  body='Sn = 2**n - 1\ndisplay(Sn.subs(n, 1))\nsimplify(Sn + 2**n - Sn.subs(n, n + 1))')
t('''**Teilbarkeit:** Beweise, dass n³ + 2n immer durch 3 teilbar ist. Induktionsschritt: Die Differenz f(n + 1) − f(n) muss durch 3 teilbar sein. Gib f(1) und die Differenz faktorisiert aus.''',
  body='f = n**3 + 2*n\ndisplay(f.subs(n, 1))\nfactor(expand(f.subs(n, n + 1) - f))')
t('''**Teilbarkeit:** Beweise, dass 5ⁿ − 1 durch 4 teilbar ist. Zeige: 5ⁿ⁺¹ − 1 = 5·(5ⁿ − 1) + 4 (Differenz der beiden Seiten mit `simplify`).''',
  body='simplify((5**(n + 1) - 1) - (5 * (5**n - 1) + 4))')
t('''**Ungleichung:** 2ⁿ > n² gilt für n ≥ 5. Prüfe die Aussage für n = 1 bis 10 (Liste von Wahrheitswerten) – für welche kleinen n gilt sie nicht?''',
  body='[2**m > m**2 for m in range(1, 11)]')
t('''Der Induktionsschritt für 2ⁿ > n²: Aus 2ⁿ > n² folgt 2ⁿ⁺¹ = 2·2ⁿ > 2n². Es bleibt 2n² ≥ (n + 1)² zu zeigen. Für welche n gilt das? (`solveset` von 2x² − (x + 1)² ≥ 0 über ℝ)''',
  body='solveset(2*x**2 - (x + 1)**2 >= 0, x, S.Reals)')
t('''**Rekursiv definierte Folge:** a₁ = 1, aₙ₊₁ = aₙ + 2n + 1. Vermutung: aₙ = n². Berechne die ersten 8 Glieder mit einer Schleife und prüfe den Induktionsschritt n² + 2n + 1 = (n + 1)².''',
  body='folge = [1]\nfor m in range(1, 8):\n    folge.append(folge[-1] + 2*m + 1)\ndisplay(folge)\nsimplify(n**2 + 2*n + 1 - (n + 1)**2)')
predict("""display(summation(1, (k, 1, n)))
display(summation(2, (k, 1, 10)))
summation(k, (k, 1, 100))""")

# ---------------------------------------------------------------- 5
sec('Ungleichungen')
expl('''#### Lösungsmengen bestimmen

`solveset(ungleichung, x, S.Reals)` gibt die Lösungsmenge einer Ungleichung als Intervall oder Vereinigung von Intervallen aus.
Das klappt auch mit Beträgen `Abs()` und Brüchen. Rechne von Hand mit Fallunterscheidungen (Betrag: x − 3 ≥ 0 oder x − 3 < 0;
Bruch: Nenner positiv oder negativ) und prüfe mit sympy.''',
     """display(solveset(Abs(x - 3) < 2, x, S.Reals))
display(solveset(Abs(2*x + 1) >= 3, x, S.Reals))
display(solveset((x - 1) / (x + 2) > 0, x, S.Reals))
solveset(x**2 - 5*x + 6 <= 0, x, S.Reals)""")
expl('''#### Allgemeingültige Ungleichungen beweisen

Eine Ungleichung wie (a + b)/2 ≥ √(ab) (für a, b > 0, **arithmetisches ≥ geometrisches Mittel**) beweist man, indem man sie auf eine
offensichtlich wahre Aussage zurückführt: (a + b)/2 − √(ab) = (√a − √b)²/2 ≥ 0, denn Quadrate sind nie negativ.
sympy prüft die Umformung mit `simplify(... - ...) == 0`.''',
     """links = (a + b) / 2 - sqrt(a * b)
rechts = (sqrt(a) - sqrt(b))**2 / 2
simplify(links - rechts)""")

t('Bestimme die Lösungsmenge von |x + 1| ≤ 4.', body='solveset(Abs(x + 1) <= 4, x, S.Reals)')
t('Bestimme die Lösungsmenge von |3x − 6| > 9.', body='solveset(Abs(3*x - 6) > 9, x, S.Reals)')
t('Bestimme die Lösungsmenge von |x − 1| + |x + 2| ≤ 5.', body='solveset(Abs(x - 1) + Abs(x + 2) <= 5, x, S.Reals)')
t('Bestimme die Lösungsmenge von |x − 2| < |x + 4|.', body='solveset(Abs(x - 2) < Abs(x + 4), x, S.Reals)')
t('Bestimme die Lösungsmenge von (2x − 1)/(x − 3) ≤ 1.', body='solveset((2*x - 1) / (x - 3) <= 1, x, S.Reals)')
t('Bestimme die Lösungsmenge von x³ − 4x > 0.', body='solveset(x**3 - 4*x > 0, x, S.Reals)')
t('Bestimme die Lösungsmenge von x² − 2x + 5 > 0 (für alle x?) und begründe mit `factor`/quadratischer Ergänzung: Gib (x − 1)² + 4 − (x² − 2x + 5) vereinfacht aus.',
  body='display(solveset(x**2 - 2*x + 5 > 0, x, S.Reals))\nexpand((x - 1)**2 + 4 - (x**2 - 2*x + 5))')
t('''Beweise a/b + b/a ≥ 2 für a, b > 0: Zeige a/b + b/a − 2 = (a − b)²/(ab).''', body='simplify(a/b + b/a - 2 - (a - b)**2 / (a * b))')
t('''Beweise a² + b² ≥ 2ab: Zeige a² + b² − 2ab = (a − b)².''', body='expand(a**2 + b**2 - 2*a*b - (a - b)**2)')
t('''**Bernoulli-Ungleichung:** (1 + x)ⁿ ≥ 1 + n·x für x ≥ −1. Prüfe sie für x = −1/2, 1/10, 3 und n = 1, ..., 10 (`all`).''',
  body='all([(1 + w)**m >= 1 + m*w for w in [Rational(-1, 2), Rational(1, 10), 3] for m in range(1, 11)])')
t('''Induktionsschritt der Bernoulli-Ungleichung: (1 + x)ⁿ⁺¹ = (1 + x)ⁿ(1 + x) ≥ (1 + nx)(1 + x). Zeige: (1 + nx)(1 + x) − (1 + (n + 1)x) = n·x² (≥ 0).''',
  body='expand((1 + n*x) * (1 + x) - (1 + (n + 1)*x))')
predict("""display(solveset(Abs(x) < 0, x, S.Reals))
display(solveset(Abs(x) >= 0, x, S.Reals))
solveset(x**2 < 4, x, S.Reals)""")

generate('sympy_logik_beweise', 'Logik und Beweise: Aussagenlogik, Beweistechniken, Induktion, Ungleichungen', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
