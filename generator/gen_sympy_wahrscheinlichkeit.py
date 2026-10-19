# Erzeugt ../content/sympy_wahrscheinlichkeit.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_wahrscheinlichkeit.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_wahrscheinlichkeit.py
#
# Bildungsplan BW 2016, Leitidee Daten und Zufall: Klassen 7/8 (Ergebnis, Ereignis, Mengenschreibweise, Laplace, Gegenereignis,
# Kombinatorik, Baumdiagramme, Pfadregeln), 9/10 (bedingte Wahrscheinlichkeit, Vierfeldertafel, Unabhängigkeit, Zufallsgröße,
# Wahrscheinlichkeitsverteilung, Erwartungswert, Bernoulli-Kette, Binomialverteilung, fehlender Parameter n, p, k,
# Erwartungswert und Standardabweichung, Histogramm).
# Keine Zufallssimulation (die steht in python-uebungen: random, numpy_zufall_statistik); hier exakte Wahrscheinlichkeiten.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = "from sympy import *\nfrom sympy.stats import *\ninit_printing()\nimport matplotlib.pyplot as plt\nn, k, p = symbols('n k p')"

INTRO = '''In diesem Notebook berechnest du **Wahrscheinlichkeiten** mit sympy: Ereignisse als Mengen, Laplace-Experimente, Kombinatorik,
Baumdiagramme und Pfadregeln, Vierfeldertafeln und bedingte Wahrscheinlichkeiten, Zufallsgrößen mit Erwartungswert und die
**Binomialverteilung**. sympy rechnet dabei mit **exakten Brüchen**; eine Dezimalzahl bekommst du mit `N()`.

Vorausgesetzt wird das Notebook *Zahlen exakt*. Simulationen mit Zufallszahlen findest du in den Python-Übungen (*random*, *numpy: Zufall und Statistik*).

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy und das Modul `sympy.stats`
für Zufallsgrößen, schaltet die Formel-Ausgabe ein, lädt matplotlib für Diagramme und legt die Variablen `n`, `k` und `p` an.

**Achtung:** `sympy.stats` verwendet den Namen `E` für den Erwartungswert. Die Eulersche Zahl schreibst du in diesem Notebook als `exp(1)`.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Ereignisse und Laplace-Wahrscheinlichkeiten')
expl('''#### Ergebnisse und Ereignisse als Mengen

Die **Ergebnismenge** Ω enthält alle möglichen Ergebnisse eines Zufallsexperiments, beim Würfeln Ω = {1, 2, 3, 4, 5, 6}.
Ein **Ereignis** ist eine Teilmenge von Ω, z. B. „gerade Zahl“ E = {2, 4, 6}. In sympy ist das eine `FiniteSet`.

| Mengenoperation | sympy | Bedeutung |
|---|---|---|
| A ∪ B | `A \\| B` oder `Union(A, B)` | A oder B |
| A ∩ B | `A & B` oder `Intersection(A, B)` | A und B |
| Ā | `Complement(Omega, A)` | Gegenereignis „nicht A“ |

`len(E)` ist die Anzahl der Ergebnisse. Bei einem **Laplace-Experiment** (alle Ergebnisse gleich wahrscheinlich) gilt
P(E) = |E| / |Ω|.''',
     """Omega = FiniteSet(1, 2, 3, 4, 5, 6)
gerade = FiniteSet(2, 4, 6)
gross = FiniteSet(5, 6)
display(gerade | gross, gerade & gross, Complement(Omega, gerade))
Rational(len(gerade | gross), len(Omega))""")
expl('''#### Mengen aus Listen und Paare

- `FiniteSet(*liste)` macht aus einer Liste eine Menge (der Stern `*` übergibt die Listenelemente einzeln).
- `ProductSet(A, B)` ist die Menge aller Paare (a, b) mit a aus A und b aus B, z. B. alle Ergebnisse beim Werfen zweier Würfel. sympy zeigt `ProductSet(M, M)` kurz als M² an.
  Mit `for w in ...` durchläufst du die Paare; `w[0]` und `w[1]` sind die beiden Einträge.''',
     """ungerade = FiniteSet(*[i for i in range(1, 7) if i % 2 == 1])
display(ungerade)
M = FiniteSet(1, 2)
paare = ProductSet(M, M)
display(paare, len(paare))
[w for w in paare if w[0] < w[1]]""")

O = 'Omega = FiniteSet(1, 2, 3, 4, 5, 6)'
t('Gib für das Würfeln das Ereignis „Primzahl“ als Menge und seine Wahrscheinlichkeit aus.', O,
  'E = FiniteSet(2, 3, 5)\ndisplay(E)\nRational(len(E), len(Omega))')
t('Gib das Gegenereignis von „mindestens 5“ als Menge und seine Wahrscheinlichkeit aus.', O,
  'E = Complement(Omega, FiniteSet(5, 6))\ndisplay(E)\nRational(len(E), len(Omega))')
t('Gib die Wahrscheinlichkeit für „gerade oder größer als 4“ aus.', O,
  'Rational(len(FiniteSet(2, 4, 6) | FiniteSet(5, 6)), len(Omega))')
t('Gib die Wahrscheinlichkeit für „gerade und größer als 4“ aus.', O,
  'Rational(len(FiniteSet(2, 4, 6) & FiniteSet(5, 6)), len(Omega))')
t('''Eine Urne enthält die Kugeln 1 bis 20. Gib die Menge der Vielfachen von 3 aus (`FiniteSet(*[...])` mit einer List Comprehension)
und die Wahrscheinlichkeit, eine solche Kugel zu ziehen.''',
  body='E = FiniteSet(*[i for i in range(1, 21) if i % 3 == 0])\ndisplay(E)\nRational(len(E), 20)')
t('''Beim Werfen zweier Würfel ist Ω die Menge aller Paare. Erzeuge sie mit `ProductSet(W, W)` für `W = FiniteSet(1, ..., 6)` und gib ihre Mächtigkeit aus.
Gib dann die Wahrscheinlichkeit für die Augensumme 7 aus (Paare mit Summe 7 zählen).''',
  body='W = FiniteSet(1, 2, 3, 4, 5, 6)\nOmega2 = ProductSet(W, W)\ndisplay(len(Omega2))\nRational(len([w for w in Omega2 if w[0] + w[1] == 7]), len(Omega2))')
t('Gib für zwei Würfel die Wahrscheinlichkeiten aller Augensummen 2 bis 12 als Liste aus.',
  body='W = FiniteSet(1, 2, 3, 4, 5, 6)\nOmega2 = ProductSet(W, W)\n[Rational(len([w for w in Omega2 if w[0] + w[1] == s]), 36) for s in range(2, 13)]')
t('Gib die Wahrscheinlichkeit für einen Pasch (beide Würfel gleich) bei zwei Würfeln aus.',
  body='W = FiniteSet(1, 2, 3, 4, 5, 6)\nRational(len([w for w in ProductSet(W, W) if w[0] == w[1]]), 36)')
predict("""A = FiniteSet(1, 2, 3)
B = FiniteSet(3, 4)
display(A | B)
display(A & B)
display(len(A | B))
Complement(A, B)""")

# ---------------------------------------------------------------- 2
sec('Kombinatorik')
expl('''#### Anzahlen bestimmen

| Situation | Anzahl | sympy |
|---|---|---|
| k Stufen mit je n Möglichkeiten (Zahlenschloss) | nᵏ | `n**k` |
| n Dinge anordnen | n! = n·(n−1)·…·1 | `factorial(n)` |
| k aus n auswählen, Reihenfolge wichtig | n·(n−1)·…·(n−k+1) | `ff(n, k)` |
| k aus n auswählen, Reihenfolge egal (Lotto) | „n über k“ | `binomial(n, k)` |''',
     """display(10**4)
display(factorial(5))
display(ff(10, 3))
binomial(49, 6)""")

t('Wie viele vierstellige Zahlenkombinationen hat ein Fahrradschloss mit den Ziffern 0 bis 9?', body='10**4')
t('Auf wie viele Arten können sich 6 Personen in eine Reihe stellen?', body='factorial(6)')
t('Bei einem Wettlauf mit 8 Läufern werden Gold, Silber und Bronze vergeben. Wie viele Möglichkeiten gibt es?', body='ff(8, 3)')
t('Wie viele Möglichkeiten gibt es, aus 25 Schülern 4 für den Klassenrat auszuwählen?', body='binomial(25, 4)')
t('Wie groß ist die Wahrscheinlichkeit für 6 Richtige im Lotto 6 aus 49 (exakt und mit 3 Ziffern)?', body='p6 = 1 / binomial(49, 6)\ndisplay(p6)\nN(p6, 3)')
t('Wie groß ist die Wahrscheinlichkeit für genau 3 Richtige im Lotto 6 aus 49? (3 der 6 Gewinnzahlen und 3 der 43 anderen Zahlen) Exakt und mit 4 Ziffern.',
  body='p3 = binomial(6, 3) * binomial(43, 3) / binomial(49, 6)\ndisplay(p3)\nN(p3, 4)')
t('Gib die Zeile 8 des Pascalschen Dreiecks (`binomial(8, k)` für k = 0 bis 8) als Liste aus und darunter ihre Summe.',
  body='zeile = [binomial(8, i) for i in range(9)]\ndisplay(zeile)\nsum(zeile)')
t('Ein Passwort besteht aus 8 Zeichen (26 Kleinbuchstaben, 26 Großbuchstaben, 10 Ziffern). Wie viele Passwörter gibt es? Gib die Zahl und die Normdarstellung mit 3 Ziffern aus.',
  body='anzahl = 62**8\ndisplay(anzahl)\nN(anzahl, 3)')
predict("""display(factorial(0))
display(binomial(5, 0), binomial(5, 5))
display(binomial(5, 2) == binomial(5, 3))
ff(5, 5) == factorial(5)""")

# ---------------------------------------------------------------- 3
sec('Mehrstufige Experimente und Pfadregeln')
expl('''#### Pfadregeln im Baumdiagramm

- **Produktregel:** Die Wahrscheinlichkeit eines Pfades ist das Produkt der Wahrscheinlichkeiten entlang des Pfades.
- **Summenregel:** Die Wahrscheinlichkeit eines Ereignisses ist die Summe der Wahrscheinlichkeiten seiner Pfade.
- **Gegenereignis:** P(„mindestens einmal“) = 1 − P(„keinmal“).

Mit `Rational` bleiben die Ergebnisse exakte Brüche.

Beispiel: Eine Urne enthält 3 rote und 2 blaue Kugeln. Es wird zweimal **ohne Zurücklegen** gezogen.''',
     """p_rr = Rational(3, 5) * Rational(2, 4)
p_bb = Rational(2, 5) * Rational(1, 4)
display(p_rr, p_bb)
display(p_rr + p_bb)
1 - p_rr - p_bb""")

t('Eine Münze wird dreimal geworfen. Wie groß ist die Wahrscheinlichkeit für dreimal Kopf?', body='Rational(1, 2)**3')
t('Eine Münze wird dreimal geworfen. Wie groß ist die Wahrscheinlichkeit für mindestens einmal Kopf? Verwende das Gegenereignis.', body='1 - Rational(1, 2)**3')
t('Ein Würfel wird viermal geworfen. Wie groß ist die Wahrscheinlichkeit für mindestens eine Sechs (exakt und mit 4 Ziffern)?',
  body='p = 1 - Rational(5, 6)**4\ndisplay(p)\nN(p, 4)')
t('Eine Urne enthält 4 rote und 6 weiße Kugeln. Es wird zweimal **mit** Zurücklegen gezogen. Gib P(zwei rote) und P(verschiedene Farben) aus.',
  body='r, w = Rational(4, 10), Rational(6, 10)\ndisplay(r * r)\nr * w + w * r')
t('Dieselbe Urne, aber **ohne** Zurücklegen. Gib P(zwei rote) und P(verschiedene Farben) aus.',
  body='display(Rational(4, 10) * Rational(3, 9))\nRational(4, 10) * Rational(6, 9) + Rational(6, 10) * Rational(4, 9)')
t('''Aus einer Urne mit 5 roten und 3 blauen Kugeln werden drei Kugeln ohne Zurücklegen gezogen. Wie groß ist die Wahrscheinlichkeit für genau eine blaue Kugel?
(Drei Pfade: bRR, RbR, RRb.)''',
  body='Rational(3, 8) * Rational(5, 7) * Rational(4, 6) + Rational(5, 8) * Rational(3, 7) * Rational(4, 6) + Rational(5, 8) * Rational(4, 7) * Rational(3, 6)')
t('''Prüfe das Ergebnis der vorigen Aufgabe mit Kombinatorik: `binomial(3, 1) * binomial(5, 2) / binomial(8, 3)`.''',
  body='binomial(3, 1) * binomial(5, 2) / binomial(8, 3)')
t('''Wie oft muss man mindestens würfeln, damit die Wahrscheinlichkeit für mindestens eine Sechs über 90 % liegt? Löse `1 − (5/6)ⁿ ≥ 0,9` (mit `solve()`)
und gib die kleinste ganze Zahl mit `ceiling()` aus.''',
  given="n = symbols('n', positive=True)",
  body="grenze = solve(Eq(1 - Rational(5, 6)**n, Rational(9, 10)), n)[0]\ndisplay(N(grenze, 4))\nceiling(grenze)")
predict("""display(Rational(1, 2) * Rational(1, 3))
display(1 - Rational(1, 2)**2)
Rational(1, 6) + Rational(1, 6)""")

# ---------------------------------------------------------------- 4
sec('Vierfeldertafel und bedingte Wahrscheinlichkeit')
expl('''#### Bedingte Wahrscheinlichkeit

Die **bedingte Wahrscheinlichkeit** P_B(A) = P(A | B) ist die Wahrscheinlichkeit für A, wenn man schon weiß, dass B eingetreten ist:

P_B(A) = P(A ∩ B) / P(B)

Eine **Vierfeldertafel** ordnet die Wahrscheinlichkeiten (oder Anzahlen) von A, Ā, B, B̄ und ihren Schnitten an. Mit einer `Matrix`
lässt sie sich übersichtlich darstellen. A und B heißen **unabhängig**, wenn P(A ∩ B) = P(A) · P(B).

Beispiel: In einer Schule mit 200 Schülern spielen 80 ein Instrument (I), 120 treiben Sport im Verein (S), 50 tun beides.''',
     """IS, I_nS = Rational(50, 200), Rational(30, 200)
nI_S, nI_nS = Rational(70, 200), Rational(50, 200)
tafel = Matrix([[IS, I_nS, IS + I_nS], [nI_S, nI_nS, nI_S + nI_nS], [IS + nI_S, I_nS + nI_nS, 1]])
display(tafel)
P_S = IS + nI_S
display(IS / P_S)
IS == (IS + I_nS) * P_S""")

t('''Berechne für das Beispiel aus der Erklärung P_I(S): die Wahrscheinlichkeit, dass jemand Sport treibt, wenn er ein Instrument spielt.''',
  body='Rational(50, 200) / Rational(80, 200)')
t('''In einer Klasse sind 12 Mädchen und 16 Jungen. 9 Mädchen und 6 Jungen tragen eine Brille. Stelle die Vierfeldertafel mit den Anzahlen als `Matrix` auf
(Zeilen: Mädchen, Jungen, Summe; Spalten: Brille, keine Brille, Summe).''',
  body='Matrix([[9, 3, 12], [6, 10, 16], [15, 13, 28]])')
t('''Berechne mit den Zahlen der vorigen Aufgabe: P(Brille), P_Mädchen(Brille) und P_Brille(Mädchen).''',
  body='display(Rational(15, 28))\ndisplay(Rational(9, 12))\nRational(9, 15)')
t('''Prüfe, ob die Ereignisse „Mädchen“ und „Brille“ unabhängig sind: Vergleiche P(Mädchen ∩ Brille) mit P(Mädchen) · P(Brille).''',
  body='Rational(9, 28) == Rational(12, 28) * Rational(15, 28)')
t('''**Test auf eine Krankheit:** 1 % der Bevölkerung ist krank. Der Test erkennt Kranke mit 99 % Sicherheit, bei Gesunden ist er in 2 % der Fälle
fälschlich positiv. Berechne P(positiv) und P_positiv(krank) exakt und mit 3 Ziffern.''',
  body="krank, gesund = Rational(1, 100), Rational(99, 100)\npos = krank * Rational(99, 100) + gesund * Rational(2, 100)\ndisplay(pos)\nkp = krank * Rational(99, 100) / pos\ndisplay(kp)\nN(kp, 3)")
t('''Wie verändert sich P_positiv(krank), wenn 10 % der Bevölkerung krank sind (sonst wie in der vorigen Aufgabe)? Gib den Wert mit 3 Ziffern aus.''',
  body="krank, gesund = Rational(10, 100), Rational(90, 100)\npos = krank * Rational(99, 100) + gesund * Rational(2, 100)\nN(krank * Rational(99, 100) / pos, 3)")
t('''Zwei Würfel werden geworfen. A: „Augensumme 7“, B: „erster Würfel zeigt 3“. Prüfe mit `ProductSet`, ob A und B unabhängig sind.''',
  body='W = FiniteSet(1, 2, 3, 4, 5, 6)\nOm = list(ProductSet(W, W))\nPA = Rational(len([w for w in Om if w[0] + w[1] == 7]), 36)\nPB = Rational(len([w for w in Om if w[0] == 3]), 36)\nPAB = Rational(len([w for w in Om if w[0] + w[1] == 7 and w[0] == 3]), 36)\nPAB == PA * PB')

# ---------------------------------------------------------------- 5
sec('Zufallsgrößen und Erwartungswert')
expl('''#### Zufallsgrößen mit `sympy.stats`

Eine **Zufallsgröße** X ordnet jedem Ergebnis eine Zahl zu, z. B. den Gewinn bei einem Spiel. Ihre **Wahrscheinlichkeitsverteilung**
gibt an, mit welcher Wahrscheinlichkeit sie welchen Wert annimmt.

- `Die('X', 6)` ist ein fairer Würfel, `FiniteRV('X', {wert: wahrscheinlichkeit, ...})` eine beliebige endliche Verteilung.
- `P(X > 4)`, `P(Eq(X, 3))` sind Wahrscheinlichkeiten (für „X = 3“ schreibt man `Eq(X, 3)`).
- `E(X)` ist der **Erwartungswert** (der Mittelwert auf lange Sicht), `variance(X)` die Varianz, `std(X)` die Standardabweichung.
- `density(X).dict` gibt die Verteilung als Dictionary aus.''',
     """X = Die('X', 6)
display(density(X).dict)
display(P(X > 4), E(X), variance(X))
G = FiniteRV('G', {-1: Rational(5, 6), 4: Rational(1, 6)})
E(G)""")

t('Gib für einen fairen Würfel `X` die Wahrscheinlichkeit P(X ≤ 2) und den Erwartungswert aus.', body="X = Die('X', 6)\ndisplay(P(X <= 2))\nE(X)")
t('Gib für einen achtseitigen fairen Würfel den Erwartungswert und die Standardabweichung aus.', body="X = Die('X', 8)\ndisplay(E(X))\nstd(X)")
t('''Ein Glücksrad zeigt mit Wahrscheinlichkeit 1/2 „0 €“, mit 1/3 „1 €“ und mit 1/6 „5 €“. Gib die Verteilung als `FiniteRV` an und berechne den Erwartungswert.''',
  body="G = FiniteRV('G', {0: Rational(1, 2), 1: Rational(1, 3), 5: Rational(1, 6)})\nE(G)")
t('''Ein Spiel kostet 2 € Einsatz. Man wirft einen Würfel und bekommt die Augenzahl in Euro ausgezahlt. Wie groß ist der erwartete Gewinn (Auszahlung minus Einsatz)?''',
  body="X = Die('X', 6)\nE(X) - 2")
t('''Bei welchem Einsatz `e` ist das Spiel aus der vorigen Aufgabe fair (erwarteter Gewinn 0)?''',
  given="e = symbols('e')", body="X = Die('X', 6)\nsolve(Eq(E(X) - e, 0), e)")
t('''Zwei Würfel X und Y werden geworfen. Gib den Erwartungswert der Augensumme `E(X + Y)` und `P(Eq(X + Y, 7))` aus.''',
  body="X, Y = Die('X', 6), Die('Y', 6)\ndisplay(E(X + Y))\nP(Eq(X + Y, 7))")
t('''Gib die Verteilung der Augensumme zweier Würfel als Dictionary aus (`density(X + Y).dict`).''',
  body="X, Y = Die('X', 6), Die('Y', 6)\ndensity(X + Y).dict")
predict("""X = Die('X', 6)
display(P(X > 6))
display(P(X >= 1))
E(2 * X)""")

# ---------------------------------------------------------------- 6
sec('Binomialverteilung')
expl('''#### Bernoulli-Ketten

Ein **Bernoulli-Experiment** hat nur zwei Ausgänge: Treffer (Wahrscheinlichkeit p) oder Niete. Wiederholt man es n-mal unabhängig,
ist die Anzahl X der Treffer **binomialverteilt**:

P(X = k) = (n über k) · pᵏ · (1 − p)ⁿ⁻ᵏ (Formel von Bernoulli)

In sympy: `X = Binomial('X', n, p)`, dann `P(Eq(X, k))`, `P(X <= k)`, `E(X)` (= n·p) und `std(X)` (= √(n·p·(1 − p))).''',
     """X = Binomial('X', 10, Rational(1, 6))
display(P(Eq(X, 2)))
display(binomial(10, 2) * Rational(1, 6)**2 * Rational(5, 6)**8)
display(N(P(Eq(X, 2)), 4), N(P(X <= 2), 4))
display(E(X), std(X))""")
expl('''#### Histogramm

Das **Histogramm** einer Binomialverteilung zeigt die Wahrscheinlichkeiten P(X = k) als Balken. Mit `plt.bar()` aus matplotlib:''',
     """X = Binomial('X', 20, Rational(3, 10))
werte = list(range(21))
wk = [N(P(Eq(X, i))) for i in werte]
plt.bar(werte, wk)
plt.xlabel('k')
plt.ylabel('P(X = k)')
plt.show()""")

B = "X = Binomial('X', 20, Rational(1, 4))"
t('X ist binomialverteilt mit n = 20 und p = 1/4. Berechne P(X = 5) mit 4 Ziffern.', B, 'N(P(Eq(X, 5)), 4)')
t('Berechne P(X = 5) für dieselbe Verteilung mit der Formel von Bernoulli (`binomial()`) und vergleiche (4 Ziffern).', B,
  'N(binomial(20, 5) * Rational(1, 4)**5 * Rational(3, 4)**15, 4)')
t('Berechne P(X ≤ 3), P(X ≥ 8) und P(4 ≤ X ≤ 6) mit je 4 Ziffern.', B,
  'display(N(P(X <= 3), 4), N(P(X >= 8), 4))\nN(P((X >= 4) & (X <= 6)), 4)')
t('Gib Erwartungswert und Standardabweichung aus (exakt und die Standardabweichung mit 4 Ziffern).', B, 'display(E(X), std(X))\nN(std(X), 4)')
t('Zeichne das Histogramm der Verteilung (k von 0 bis 20).', B,
  'werte = list(range(21))\nplt.bar(werte, [N(P(Eq(X, i))) for i in werte])\nplt.show()')
t('''Ein Multiple-Choice-Test hat 10 Fragen mit je 4 Antworten, von denen eine richtig ist. Jemand rät. Mit welcher Wahrscheinlichkeit hat er
mindestens 5 richtig (4 Ziffern)?''', body="X = Binomial('X', 10, Rational(1, 4))\nN(P(X >= 5), 4)")
t('''Ein Medikament wirkt bei 80 % der Patienten. Es werden 15 Patienten behandelt. Wie groß ist die Wahrscheinlichkeit, dass es bei höchstens 10 wirkt (4 Ziffern)?''',
  body="X = Binomial('X', 15, Rational(4, 5))\nN(P(X <= 10), 4)")
t('''**Fehlendes n:** Wie oft muss man einen Würfel mindestens werfen, damit mit mindestens 99 % Wahrscheinlichkeit wenigstens eine Sechs fällt?
Probiere n = 1, 2, 3, ... mit einer Schleife, bis `1 - Rational(5, 6)**n >= Rational(99, 100)` gilt, und gib n aus.''',
  body='n = 1\nwhile 1 - Rational(5, 6)**n < Rational(99, 100):\n    n += 1\nn')
t('''**Fehlendes k:** X ist binomialverteilt mit n = 50 und p = 0,3. Bestimme das kleinste k mit P(X ≤ k) ≥ 0,95 mit einer Schleife.''',
  body="X = Binomial('X', 50, Rational(3, 10))\nk = 0\nwhile P(X <= k) < Rational(95, 100):\n    k += 1\nk")
t('''**Fehlendes p:** Bei 10 Würfen soll die Wahrscheinlichkeit für „keinmal Treffer“ genau 0,1 sein. Löse `(1 − p)¹⁰ = 0,1` für p zwischen 0 und 1 (4 Ziffern).''',
  body="l = solveset(Eq((1 - p)**10, Rational(1, 10)), p, domain=Interval(0, 1))\nN(list(l)[0], 4)")
predict("""X = Binomial('X', 4, Rational(1, 2))
display(P(Eq(X, 0)))
display(E(X))
density(X).dict""")

# ---------------------------------------------------------------- 7
sec('Gemischte Übungen')
t('''Beim „Mensch ärgere dich nicht“ darf man dreimal würfeln, um eine Sechs zu bekommen. Wie groß ist die Wahrscheinlichkeit, es zu schaffen?''',
  body='1 - Rational(5, 6)**3')
t('''**Geburtstagsproblem:** Wie groß ist die Wahrscheinlichkeit, dass in einer Klasse mit 25 Personen mindestens zwei am selben Tag Geburtstag haben
(365 Tage, alle gleich wahrscheinlich)? Berechne `1 − (365·364·…·341)/365²⁵` mit `ff()` und gib das Ergebnis mit 4 Ziffern aus.''',
  body='N(1 - ff(365, 25) / Integer(365)**25, 4)')
t('''Ein Schütze trifft mit 70 % Wahrscheinlichkeit. Er schießt 8-mal. Gib die Wahrscheinlichkeiten für 0 bis 8 Treffer mit 3 Ziffern als Liste aus
und den wahrscheinlichsten Wert (das k mit der größten Wahrscheinlichkeit).''',
  body="X = Binomial('X', 8, Rational(7, 10))\nwk = [N(P(Eq(X, i)), 3) for i in range(9)]\ndisplay(wk)\nwk.index(max(wk))")
t('''Ein Spiel: Man zahlt 1 € und wirft zwei Münzen. Bei zweimal Kopf bekommt man 3 €, bei genau einmal Kopf 1 €, sonst nichts.
Gib den erwarteten Gewinn aus.''',
  body="G = FiniteRV('G', {2: Rational(1, 4), 0: Rational(1, 2), -1: Rational(1, 4)})\nE(G)")
t('''Eine Firma weiß, dass 5 % ihrer Bauteile defekt sind. Sie prüft 100 Bauteile. Gib Erwartungswert und Standardabweichung der Anzahl defekter Teile
(mit 4 Ziffern) aus und die Wahrscheinlichkeit, dass mehr als 10 defekt sind (4 Ziffern).''',
  body="X = Binomial('X', 100, Rational(5, 100))\ndisplay(E(X), N(std(X), 4))\nN(P(X > 10), 4)")

generate('sympy_wahrscheinlichkeit', 'Wahrscheinlichkeit: Laplace, Pfadregeln, Vierfeldertafel, Binomialverteilung', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
