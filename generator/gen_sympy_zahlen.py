# Erzeugt ../content/sympy_zahlen.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_zahlen.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_zahlen.py
#
# Bildungsplan BW 2016, Leitidee Zahl – Variable – Operation: Klassen 5/6 (Teilbarkeit, Primzahlen, Brüche, Dezimalzahlen,
# Prozent, Potenzen, Runden), 7/8 (Quadratwurzeln, teilweises Wurzelziehen, irrationale Zahlen, Iterationsverfahren),
# 9/10 (Normdarstellung, Potenzen mit negativen Exponenten).
# Die Setup-Zelle (from sympy import *, init_printing()) wird beim Prüfen vor jeder Zelle ausgeführt.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = 'from sympy import *\ninit_printing()'

INTRO = '''**sympy** ist ein Computer-Algebra-System für Python: Es rechnet nicht nur mit Kommazahlen, sondern **exakt** mit Brüchen,
Wurzeln und Variablen, so wie du auf dem Papier. In diesem ersten Notebook geht es um **Zahlen**: Teiler und Primzahlen,
Brüche, Dezimalzahlen und Prozente, Potenzen und Wurzeln.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.

**So verwendest du sympy:** Rechne die Aufgaben ruhig zuerst im Kopf oder auf Papier und prüfe dann mit sympy.
sympy zeigt das Ergebnis der **letzten Zeile** einer Zelle als schön gesetzte Formel an. Mehrere Ergebnisse gibst du mit
`display(a, b)` aus. `print()` verwendest du nur für Text.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). `from sympy import *` lädt alle Funktionen
von sympy, `init_printing()` sorgt dafür, dass Ergebnisse als Formeln angezeigt werden. Beim ersten Mal dauert das ein paar Sekunden.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Exakt rechnen')
expl('''#### Kommazahl oder Bruch?

Python rechnet `1/3` als **Kommazahl** (`float`) mit etwa 16 Stellen, also nur ungefähr. sympy kennt **exakte Brüche**:
`Rational(1, 3)` ist genau ein Drittel. Mit Brüchen rechnet sympy exakt weiter und kürzt automatisch.

Sobald in einer Rechnung **eine** ganze sympy-Zahl vorkommt, rechnet sympy exakt: `Integer(1) / 3` ist ebenfalls ein Bruch.
Eine Kommazahl wie `0.5` macht das Ergebnis aber wieder zur Kommazahl.''',
     """display(1 / 3)
display(Rational(1, 3))
display(Rational(1, 3) + Rational(1, 6))
display(Integer(1) / 3 * 3)
Rational(1, 3) + 0.5""")
expl('''#### Dezimalzahlen mit `N()`

`N(zahl)` gibt einen Näherungswert als Dezimalzahl, `N(zahl, 30)` mit 30 gültigen Ziffern. Dasselbe macht `zahl.evalf(30)`.

Für die Kreiszahl π gibt es in sympy das Symbol `pi`, für die Eulersche Zahl e das Symbol `E`. sympy rechnet mit ihnen wie mit √2:
Das Symbol steht für die genaue Zahl und bleibt im Ergebnis stehen, z. B. ist der Flächeninhalt eines Kreises mit Radius 5 genau `25π`.
Dezimalstellen speichert sympy dafür nicht. Erst `N()` berechnet so viele Stellen, wie du angibst.''',
     """display(N(Rational(1, 3)))
display(pi * 5**2)
display(N(pi * 5**2))
display(N(pi, 30))
Rational(22, 7).evalf(10)""")

t('Berechne `1/4 + 2/3` exakt mit `Rational`.', body='Rational(1, 4) + Rational(2, 3)')
t('Berechne `2/3 · 3/4` exakt.', body='Rational(2, 3) * Rational(3, 4)')
t('Berechne `5/6 − 7/9` exakt.', body='Rational(5, 6) - Rational(7, 9)')
t('Berechne `(3/5) : (9/10)` exakt.', body='Rational(3, 5) / Rational(9, 10)')
t('Gib den Kehrwert von `3/8` aus. Verwende `1 / ...`.', body='1 / Rational(3, 8)')
t('Gib π mit 25 gültigen Ziffern aus.', body='N(pi, 25)')
t('Gib `1/7` als Dezimalzahl mit 30 gültigen Ziffern aus.', body='N(Rational(1, 7), 30)')
t('Berechne `0.1 + 0.2` einmal mit Kommazahlen und einmal exakt mit `Rational(1, 10) + Rational(2, 10)`. Gib beides mit `display()` aus.',
  body='display(0.1 + 0.2)\ndisplay(Rational(1, 10) + Rational(2, 10))')
t('Berechne exakt `1/2 + 1/3 + 1/4 + 1/5 + 1/6`. Verwende `Integer(1) / 2` usw.',
  body='Integer(1) / 2 + Integer(1) / 3 + Integer(1) / 4 + Integer(1) / 5 + Integer(1) / 6')
t('Wie gut ist die Näherung `22/7` für π? Gib die Differenz `22/7 − π` mit 10 gültigen Ziffern aus.',
  body='N(Rational(22, 7) - pi, 10)')
predict("""display(Rational(6, 8))
display(Rational(1, 2) + 1)
display(1 / 2 + Rational(1, 3))
Rational(10, 5)""")

# ---------------------------------------------------------------- 2
sec('Teiler und Primzahlen')
expl('''#### Primzahlen und Primfaktorzerlegung

| Funktion | Ergebnis |
|---|---|
| `isprime(n)` | `True`, wenn `n` eine Primzahl ist |
| `list(primerange(a, b))` | alle Primzahlen von `a` bis unter `b` |
| `prime(k)` | die `k`-te Primzahl, `nextprime(n)` die nächste Primzahl nach `n` |
| `factorint(n)` | Primfaktorzerlegung als Dictionary {Primzahl: Exponent} |
| `primefactors(n)` | die Primfaktoren ohne Wiederholung |

`factorint(360)` ergibt `{2: 3, 3: 2, 5: 1}`, also 360 = 2³ · 3² · 5.''',
     """display(isprime(91))
display(list(primerange(1, 30)))
display(factorint(360))
primefactors(360)""")
expl('''#### Teiler, ggT und kgV

- `divisors(n)` liefert alle Teiler von `n`, `divisor_count(n)` ihre Anzahl.
- `gcd(a, b)` ist der **größte gemeinsame Teiler** (ggT), `lcm(a, b)` das **kleinste gemeinsame Vielfache** (kgV).
- Ob `a` durch `b` teilbar ist, prüfst du mit dem Modulo-Operator: `a % b == 0`.''',
     """display(divisors(60))
display(gcd(84, 126))
lcm(12, 18)""")

t('Prüfe, ob 97 eine Primzahl ist.', body='isprime(97)')
t('Prüfe, ob 221 eine Primzahl ist, und gib danach seine Primfaktorzerlegung aus.', body='display(isprime(221))\nfactorint(221)')
t('Gib alle Primzahlen unter 60 als Liste aus.', body='list(primerange(1, 60))')
t('Gib die 20. Primzahl aus.', body='prime(20)')
t('Gib die erste Primzahl nach 1000 aus.', body='nextprime(1000)')
t('Gib die Primfaktorzerlegung von 1260 aus.', body='factorint(1260)')
t('Gib alle Teiler von 84 aus und darunter ihre Anzahl.', body='display(divisors(84))\ndivisor_count(84)')
t('Bestimme den ggT von 252 und 198.', body='gcd(252, 198)')
t('Bestimme das kgV von 15 und 25.', body='lcm(15, 25)')
t('Bestimme das kgV von 4, 6 und 10. Berechne dazu zuerst das kgV von 4 und 6.', body='lcm(lcm(4, 6), 10)')
t('''Eine Zahl heißt **vollkommen**, wenn die Summe ihrer Teiler ohne die Zahl selbst gleich der Zahl ist (z. B. 6 = 1 + 2 + 3).
Prüfe das für 28: Gib `sum(divisors(28)) - 28` aus.''', body='sum(divisors(28)) - 28')
t('Gib alle vollkommenen Zahlen unter 10000 als Liste aus. Verwende eine List Comprehension.',
  body='[n for n in range(2, 10000) if sum(divisors(n)) - n == n]')
t('''**Primzahlzwillinge** sind Primzahlen mit dem Abstand 2, z. B. 11 und 13. Gib alle Paare `(p, p + 2)` unter 100 als Liste aus.''',
  body='[(p, p + 2) for p in primerange(2, 100) if isprime(p + 2)]')
t('Prüfe mit dem Modulo-Operator, ob 123456 durch 3, durch 4 und durch 9 teilbar ist. Gib die drei Ergebnisse als Liste aus.',
  body='[123456 % 3 == 0, 123456 % 4 == 0, 123456 % 9 == 0]')
t('''Prüfe die Teilbarkeitsregel für 3 an der Zahl 7425: Berechne die Quersumme mit `sum(int(z) for z in str(7425))`
und gib die Quersumme und den Rest der Quersumme bei Division durch 3 aus.''',
  body='quersumme = sum(int(z) for z in str(7425))\ndisplay(quersumme)\nquersumme % 3')
predict("""display(factorint(64))
display(divisors(13))
display(gcd(12, 35))
lcm(6, 9)""")

# ---------------------------------------------------------------- 3
sec('Brüche')
expl('''#### Rechnen mit `Rational`

sympy kürzt Brüche **automatisch**: `Rational(84, 126)` ergibt sofort `2/3`.
Zähler und Nenner eines Bruchs `b` bekommst du mit `b.p` und `b.q` (oder `numer(b)` und `denom(b)`).

Brüche kann man vergleichen (`<`, `>`, `==`), sortieren (`sorted()`) und mit `max()` und `min()` den größten und kleinsten finden.''',
     """b = Rational(84, 126)
display(b)
display(b.p, b.q)
display(Rational(5, 8) < Rational(7, 11))
sorted([Rational(3, 4), Rational(2, 3), Rational(5, 6)])""")
expl('''#### Gemischte Zahlen

Eine gemischte Zahl wie 3 ²⁄₅ = 17/5 bekommt man mit der ganzzahligen Division `//` und dem Modulo-Operator `%`:
Die ganze Zahl ist `p // q`, der Rest `p % q` ist der neue Zähler.''',
     """b = Rational(17, 5)
display(b.p // b.q)
Rational(b.p % b.q, b.q)""")

t('Kürze den Bruch 84/105 mit sympy.', body='Rational(84, 105)')
t('Gib Zähler und Nenner von 45/60 nach dem Kürzen aus (mit `display()`).', body='b = Rational(45, 60)\ndisplay(b.p, b.q)')
t('Berechne `3/4 + 5/6 − 1/3`.', body='Rational(3, 4) + Rational(5, 6) - Rational(1, 3)')
t('Berechne `(2/3 + 1/4) · 6/11`.', body='(Rational(2, 3) + Rational(1, 4)) * Rational(6, 11)')
t('Prüfe, ob `5/8` größer als `7/11` ist.', body='Rational(5, 8) > Rational(7, 11)')
t('Sortiere die Brüche der Größe nach.', given='brueche = [Rational(3, 7), Rational(2, 5), Rational(4, 9), Rational(5, 12)]',
  body='sorted(brueche)')
t('Gib den größten und den kleinsten Bruch der Liste aus.', given='brueche = [Rational(3, 7), Rational(2, 5), Rational(4, 9), Rational(5, 12)]',
  body='display(max(brueche))\nmin(brueche)')
t('Berechne 3/5 von 240 €.', body='Rational(3, 5) * 240')
t('Berechne den Mittelwert von `2/3` und `3/4`.', body='(Rational(2, 3) + Rational(3, 4)) / 2')
t('Schreibe 23/6 als gemischte Zahl: Gib die ganze Zahl und den Bruchteil aus.', body='b = Rational(23, 6)\ndisplay(b.p // b.q)\nRational(b.p % b.q, b.q)')
t('Berechne exakt die Summe `1/1 + 1/2 + 1/3 + ... + 1/10`. Verwende `sum()` und `Rational(1, n)`.',
  body='sum(Rational(1, n) for n in range(1, 11))')
t('Berechne exakt `1/(1·2) + 1/(2·3) + ... + 1/(99·100)`. Das Ergebnis ist überraschend einfach.',
  body='sum(Rational(1, n * (n + 1)) for n in range(1, 100))')
t('Ein Drittel einer Klasse fährt mit dem Bus, ein Viertel mit dem Rad, ein Sechstel wird gebracht. Welcher Anteil geht zu Fuß?',
  body='1 - Rational(1, 3) - Rational(1, 4) - Rational(1, 6)')
predict("""b = Rational(12, 18)
display(b.p + b.q)
display(Rational(1, 2) == Rational(2, 4))
Rational(7, 3) - 2""")

# ---------------------------------------------------------------- 4
sec('Dezimalzahlen und Prozente')
expl('''#### Dezimalzahl → Bruch

- `Rational('0.375')` macht aus einer **abbrechenden** Dezimalzahl (in Anführungszeichen) einen exakten Bruch.
- `nsimplify(0.375)` versucht, zu einer Kommazahl einen einfachen Bruch zu finden.

Eine **periodische** Dezimalzahl wandelt man mit einer Regel um: Die Periode geteilt durch so viele Neunen, wie sie Ziffern hat.
0,(27) = 27/99, 0,(142857) = 142857/999999.''',
     """display(Rational('0.375'))
display(nsimplify(0.125))
display(Rational(27, 99))
N(Rational(27, 99), 20)""")
expl('''#### Prozente

Prozent heißt „Hundertstel“: 15 % = 15/100. Mit `Rational` rechnet man exakt:

- Prozentwert = Prozentsatz · Grundwert, z. B. `Rational(15, 100) * 240`
- Prozentsatz = Prozentwert / Grundwert (als Bruch, mal 100 in Prozent)
- Grundwert = Prozentwert / Prozentsatz''',
     """display(Rational(15, 100) * 240)
display(Rational(36, 120) * 100)
Rational(45) / Rational(15, 100)""")

t('Wandle 0,875 in einen Bruch um.', body="Rational('0.875')")
t('Wandle 2,45 in einen Bruch um.', body="Rational('2.45')")
t('Wandle 5/8 in eine Dezimalzahl um.', body='N(Rational(5, 8))')
t('Gib 7/12 mit 20 gültigen Ziffern aus.', body='N(Rational(7, 12), 20)')
t('Wandle die periodische Dezimalzahl 0,(36) in einen Bruch um.', body='Rational(36, 99)')
t('Wandle 0,(123) in einen Bruch um und gib zur Kontrolle den Bruch mit 15 Ziffern aus.', body='b = Rational(123, 999)\ndisplay(b)\nN(b, 15)')
t('Prüfe mit `nsimplify()`, welcher Bruch zu der Kommazahl 0.4375 gehört.', body='nsimplify(0.4375)')
t('Berechne 15 % von 240.', body='Rational(15, 100) * 240')
t('Wie viel Prozent sind 36 von 120?', body='Rational(36, 120) * 100')
t('Ein Pullover kostet nach 20 % Rabatt noch 48 €. Wie viel hat er vorher gekostet?', body='48 / (1 - Rational(20, 100))')
t('Wandle 3/8 in Prozent um, einmal als Bruch und einmal als Dezimalzahl.', body='p = Rational(3, 8) * 100\ndisplay(p)\nN(p)')
t('''Welche der Brüche 1/n für n von 2 bis 20 haben eine **abbrechende** Dezimaldarstellung? Das ist genau dann der Fall,
wenn der Nenner nur die Primfaktoren 2 und 5 hat. Gib die passenden Nenner als Liste aus. Tipp: `set(primefactors(n)) <= {2, 5}`.''',
  body='[n for n in range(2, 21) if set(primefactors(n)) <= {2, 5}]')
predict("""display(Rational('0.5') + Rational(1, 4))
display(N(Rational(1, 3), 5))
Rational(1, 9) * 9""")

# ---------------------------------------------------------------- 5
sec('Potenzen und große Zahlen')
expl('''#### Potenzen

`**` berechnet Potenzen: `2**10` ist 1024. Ganze Zahlen werden in Python beliebig groß, man kann also auch `2**100` exakt ausrechnen.

Bei **negativen Exponenten** entsteht ein Bruch: 2⁻³ = 1/8. Mit Python-Zahlen kommt dabei eine Kommazahl heraus.
Für das exakte Ergebnis schreibt man die Basis als sympy-Zahl: `Integer(2)**(-3)`.''',
     """display(2**100)
display(2**(-3))
display(Integer(2)**(-3))
Rational(2, 3)**4""")
expl('''#### Normdarstellung

Sehr große oder sehr kleine Zahlen schreibt man in **Normdarstellung** (wissenschaftliche Schreibweise) als a · 10ⁿ mit 1 ≤ a < 10.
`N(zahl, 3)` rundet auf 3 gültige Ziffern und zeigt große und kleine Zahlen automatisch so an.''',
     """display(N(149600000000, 3))
display(N(Integer(1) / 4000, 2))
N(6.02214076 * 10**23, 4)""")

t('Berechne 3¹⁵.', body='3**15')
t('Berechne 2⁻⁵ exakt.', body='Integer(2)**(-5)')
t('Berechne 10⁻³ exakt.', body='Integer(10)**(-3)')
t('Berechne `2⁻⁵ + 4⁻²` exakt.', body='Integer(2)**(-5) + Integer(4)**(-2)')
t('Berechne (2/3)⁴ exakt.', body='Rational(2, 3)**4')
t('Prüfe das Potenzgesetz 3⁴ · 3² = 3⁶.', body='3**4 * 3**2 == 3**6')
t('Gib die Quadratzahlen von 11² bis 20² als Liste aus.', body='[n**2 for n in range(11, 21)]')
t('Wie viele Stellen hat 2¹⁰⁰⁰? Verwende `len(str(...))`.', body='len(str(2**1000))')
t('Gib die Lichtgeschwindigkeit 299792458 m/s in Normdarstellung mit 3 gültigen Ziffern aus.', body='N(299792458, 3)')
t('Ein Lichtjahr ist 9460730472580800 m lang. Gib die Länge in Normdarstellung mit 4 gültigen Ziffern aus.', body='N(9460730472580800, 4)')
t('Der Durchmesser eines Wasserstoffatoms beträgt etwa 0,000000000106 m. Gib ihn in Normdarstellung mit 3 gültigen Ziffern aus.',
  body="N(Rational('0.000000000106'), 3)")
t('''Ein Reiskorn auf dem ersten Feld eines Schachbretts, 2 auf dem zweiten, 4 auf dem dritten, ... Wie viele Körner liegen auf allen 64 Feldern?
Gib die exakte Zahl und darunter die Normdarstellung mit 3 Ziffern aus.''',
  body='koerner = sum(2**k for k in range(64))\ndisplay(koerner)\nN(koerner, 3)')
predict("""display(Integer(5)**0)
display(Integer(-2)**3)
display(Rational(1, 2)**(-2))
N(1000000, 2)""")

# ---------------------------------------------------------------- 6
sec('Wurzeln und irrationale Zahlen')
expl('''#### Wurzeln exakt

`sqrt(x)` ist die Quadratwurzel, `root(x, 3)` die dritte Wurzel. sympy lässt Wurzeln, die nicht aufgehen, **exakt** stehen
und zieht automatisch teilweise die Wurzel: √72 = √(36 · 2) = 6√2.

Gleichartige Wurzeln fasst sympy zusammen (√12 + √27 = 2√3 + 3√3 = 5√3), Produkte auch (√2 · √8 = 4).
Achtung: √(a + b) ist im Allgemeinen **nicht** √a + √b.''',
     """display(sqrt(49))
display(sqrt(72))
display(root(54, 3))
display(sqrt(12) + sqrt(27))
display(sqrt(2) * sqrt(8))
display(sqrt(9 + 16), sqrt(9) + sqrt(16))""")
expl('''#### Irrationale Zahlen und Näherungen

√2 ist **irrational**: Es gibt keinen Bruch, der genau √2 ist, und die Dezimaldarstellung bricht nie ab und ist nicht periodisch.
sympy kann das prüfen: `sqrt(2).is_rational` ist `False`. Mit `N(sqrt(2), 50)` siehst du 50 Ziffern.

Steht eine Wurzel im **Nenner**, macht `radsimp()` den Nenner wurzelfrei (Nenner rational machen).''',
     """display(sqrt(2).is_rational)
display(N(sqrt(2), 50))
display(radsimp(1 / (sqrt(3) - 1)))""")

t('Vereinfache √500.', body='sqrt(500)')
t('Vereinfache √(4/9).', body='sqrt(Rational(4, 9))')
t('Berechne die dritte Wurzel von 216.', body='root(216, 3)')
t('Vereinfache die dritte Wurzel von 54.', body='root(54, 3)')
t('Berechne √2 · √18.', body='sqrt(2) * sqrt(18)')
t('Berechne √50 + √18 − √8.', body='sqrt(50) + sqrt(18) - sqrt(8)')
t('Berechne √(16 + 9) und √16 + √9 und gib beides mit `display()` aus.', body='display(sqrt(16 + 9), sqrt(16) + sqrt(9))')
t('Berechne (√3)² und (2√5)².', body='display(sqrt(3)**2, (2 * sqrt(5))**2)')
t('Gib √3 mit 30 gültigen Ziffern aus.', body='N(sqrt(3), 30)')
t('Prüfe für die Zahlen 36, 37 und 2.25, ob ihre Wurzel rational ist. Gib die Ergebnisse als Liste aus.',
  body="[sqrt(36).is_rational, sqrt(37).is_rational, sqrt(Rational('2.25')).is_rational]")
t('Mache den Nenner von `1 / (1 + √2)` rational.', body='radsimp(1 / (1 + sqrt(2)))')
t('''**Heron-Verfahren:** Eine Näherung `x` für √2 wird besser, wenn man sie durch `(x + 2/x) / 2` ersetzt. Beginne mit `x = Integer(1)`
und gib die ersten vier Näherungen als exakte Brüche aus, jede mit `display()`.''',
  body='x = Integer(1)\nfor i in range(4):\n    x = (x + 2 / x) / 2\n    display(x)')
t('Führe das Heron-Verfahren für √2 fünfmal durch und gib danach den Abstand der letzten Näherung zu √2 mit 5 gültigen Ziffern aus.',
  body='x = Integer(1)\nfor i in range(5):\n    x = (x + 2 / x) / 2\nN(x - sqrt(2), 5)')
predict("""display(sqrt(8))
display(sqrt(2) + sqrt(2))
display(sqrt(2) * sqrt(3))
sqrt(-4)""")

# ---------------------------------------------------------------- 7
sec('Runden und Genauigkeit')
expl('''#### Runden

- `N(x, n)` gibt `x` mit `n` **gültigen Ziffern** aus.
- `round(x, n)` rundet auf `n` **Nachkommastellen**.

Rechnet man mit gerundeten Zwischenergebnissen weiter, werden die Fehler größer. Am genauesten ist es, **exakt** zu rechnen und erst
am Ende zu runden.''',
     """x = Rational(2, 3)
display(N(x, 3))
display(round(N(x), 2))
display(N(pi * 100**2, 8))
3.14 * 100**2""")

t('Runde 22/7 auf 4 Nachkommastellen.', body='round(N(Rational(22, 7)), 4)')
t('Berechne den Flächeninhalt eines Kreises mit Radius 5 cm mit dem Symbol `pi` und danach als Dezimalzahl mit 6 gültigen Ziffern.',
  body='A = pi * 5**2\ndisplay(A)\nN(A, 6)')
t('Wie groß ist der Fehler, wenn man für den Kreis mit Radius 5 cm mit π ≈ 3,14 rechnet? Gib `3.14 * 5**2 - pi * 5**2` mit 4 gültigen Ziffern aus.',
  body='N(3.14 * 5**2 - pi * 5**2, 4)')
t('''Ein Kapital von 1000 € wird 10 Jahre mit 3 % verzinst. Berechne das Endkapital exakt mit `Rational(103, 100)` und gib es auf Cent gerundet aus.''',
  body='K = 1000 * Rational(103, 100)**10\nround(N(K), 2)')
t('''Rechne `1/3 · 3` einmal mit dem gerundeten Wert 0,333 und einmal exakt. Gib beide Ergebnisse aus.''',
  body='display(0.333 * 3)\nRational(1, 3) * 3')

# ---------------------------------------------------------------- 8
sec('Gemischte Übungen')
t('''Berechne den ggT von 1071 und 462 mit dem **Euklidischen Algorithmus**: Solange `b` nicht 0 ist, ersetze `(a, b)` durch `(b, a % b)`.
Gib am Ende `a` aus und darunter zur Kontrolle `gcd(1071, 462)`.''',
  body='a, b = 1071, 462\nwhile b != 0:\n    a, b = b, a % b\ndisplay(a)\ngcd(1071, 462)')
t('''**Goldbach:** Jede gerade Zahl größer als 2 lässt sich als Summe zweier Primzahlen schreiben. Gib für 100 alle Zerlegungen `(p, 100 - p)`
mit `p <= 50` als Liste aus.''',
  body='[(p, 100 - p) for p in primerange(2, 51) if isprime(100 - p)]')
t('''Kürze den Bruch 1071/462 von Hand mit dem ggT: Teile Zähler und Nenner durch `gcd(1071, 462)` und gib beide aus. Vergleiche mit `Rational(1071, 462)`.''',
  body='g = gcd(1071, 462)\ndisplay(1071 // g, 462 // g)\nRational(1071, 462)')
t('''Gib 1/7, 2/7 und 3/7 mit je 20 Ziffern aus. Die Periode besteht immer aus denselben sechs Ziffern in anderer Reihenfolge.''',
  body='display(N(Rational(1, 7), 20), N(Rational(2, 7), 20), N(Rational(3, 7), 20))')
t('''Ein Quadrat hat den Flächeninhalt 50 cm². Berechne die Seitenlänge exakt und als Dezimalzahl mit 4 gültigen Ziffern.''',
  body='a = sqrt(50)\ndisplay(a)\nN(a, 4)')
t('''Die Diagonale eines Quadrats mit der Seite 1 ist √2 lang. Wie lang ist die Diagonale eines Würfels mit der Kante 1 (√3)?
Gib beide Längen exakt aus und darunter ihr Verhältnis `sqrt(3) / sqrt(2)` vereinfacht (`radsimp()`).''',
  body='display(sqrt(2), sqrt(3))\nradsimp(sqrt(3) / sqrt(2))')
t('''Gib alle Zahlen von 1 bis 100 als Liste aus, die genau drei Teiler haben, und darunter die Liste ihrer Quadratwurzeln.''',
  body='zahlen = [n for n in range(1, 101) if divisor_count(n) == 3]\ndisplay(zahlen)\n[sqrt(n) for n in zahlen]')

generate('sympy_zahlen', 'Zahlen exakt: Brüche, Primzahlen, Potenzen und Wurzeln', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
