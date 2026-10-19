# Erzeugt ../content/sympy_wachstum.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_wachstum.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_wachstum.py
#
# Bildungsplan BW 2016, Kursstufe, Leitidee Funktionaler Zusammenhang: exponentielles Wachstum und exponentielle Abnahme
# mit f(t) = f(0)·e^(kt), Verdopplungs- und Halbwertszeit, Parameter aus Messwerten, beschränktes Wachstum,
# Zusammenhang zwischen Bestand und Änderungsrate (f' = k·f, f' = k·(S − f)), Differentialgleichungen (Leistungsfach),
# logistisches Wachstum (Zusatz).
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t_(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = ("from sympy import *\ninit_printing()\nimport matplotlib.pyplot as plt\nt = symbols('t', real=True)\n"
         "k = symbols('k', real=True)")

INTRO = '''In diesem Notebook geht es um **Wachstumsmodelle**: exponentielles Wachstum und exponentielle Abnahme, beschränktes Wachstum
und (als Zusatz) logistisches Wachstum. Du bestimmst die Parameter eines Modells aus Messwerten, berechnest Verdopplungs- und Halbwertszeiten
und untersuchst, wie Bestand und Änderungsrate zusammenhängen. Im Leistungsfach löst du die zugehörigen **Differentialgleichungen** mit `dsolve()`.

Die Zeitvariable heißt `t`. Kommazahlen in Modellen schreibst du als `Rational`, damit sympy genau rechnet.

Vorausgesetzt werden die Notebooks *Ableitungsregeln* und *Integrale*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy und matplotlib, schaltet die Formel-Ausgabe ein
und legt die reellen Variablen `t` und `k` an.

**Achtung:** Verwende nicht `S` als eigenen Variablennamen, `S` gehört zu sympy (z. B. `S.Reals`). Die Schranke heißt in den Programmen deshalb `G`.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Exponentielles Wachstum und Abnahme')
expl('''#### f(t) = f(0) · e^(kt)

Bei **exponentiellem Wachstum** wächst der Bestand in gleichen Zeitschritten um denselben **Faktor**. Mit der e-Funktion schreibt man
f(t) = f(0) · e^(kt) mit der **Wachstumskonstante** k: k > 0 Wachstum, k < 0 Abnahme.

Ist der Wachstumsfaktor pro Zeitschritt a (z. B. a = 1,05 bei 5 % Zunahme), dann ist k = ln(a), denn aᵗ = e^(t·ln a).

**Verdopplungszeit** (k > 0): T = ln(2)/k. **Halbwertszeit** (k < 0): T = ln(2)/|k|.

Gleichungen mit e-Funktionen löst du am besten mit `solveset(..., S.Reals)`, das liefert einfachere Logarithmen als `solve`.
Das einzige Element einer Lösungsmenge `l` bekommst du mit `list(l)[0]`.''',
     """f = 500 * exp(log(Rational(105, 100)) * t)
display(f)
display(N(f.subs(t, 10), 5))
l = solveset(Eq(f, 1000), t, S.Reals)
display(l)
N(list(l)[0], 4)""")

t_('Ein Kapital von 2000 € wird mit 3 % pro Jahr verzinst. Gib das Modell f(t) = 2000 · e^(kt) mit k = ln(1,03) aus und den Wert nach 10 Jahren (auf Cent gerundet: `round(N(...), 2)`).',
   body='f = 2000 * exp(log(Rational(103, 100)) * t)\ndisplay(f)\nround(N(f.subs(t, 10)), 2)')
t_('Nach wie vielen Jahren hat sich das Kapital aus der vorigen Aufgabe verdoppelt? Genau und mit 4 Ziffern.',
   body="l = solveset(Eq(2000 * exp(log(Rational(103, 100)) * t), 4000), t, S.Reals)\ndisplay(l)\nN(list(l)[0], 4)")
t_('Berechne die Verdopplungszeit für k = 0,1 mit T = ln(2)/k genau und mit 4 Ziffern.', body='T = log(2) / Rational(1, 10)\ndisplay(T)\nN(T, 4)')
t_('Ein Medikament wird im Körper abgebaut: Jede Stunde nimmt die Menge um 15 % ab. Gib k = ln(0,85) mit 4 Ziffern und die Halbwertszeit mit 4 Ziffern aus.',
   body='k0 = log(Rational(85, 100))\ndisplay(N(k0, 4))\nN(log(2) / Abs(k0), 4)')
t_('''**C-14-Methode:** Kohlenstoff-14 hat eine Halbwertszeit von 5730 Jahren. Bestimme k genau (aus e^(5730k) = 1/2 mit `solveset`) und mit 4 Ziffern.''',
   body="l = solveset(Eq(exp(5730*k), Rational(1, 2)), k, S.Reals)\ndisplay(l)\nN(list(l)[0], 4)")
t_('''Ein Knochen enthält noch 30 % des ursprünglichen C-14. Wie alt ist er (auf ganze Jahre gerundet: `round(N(...))`)? Verwende k = −ln(2)/5730.''',
   body="k0 = -log(2) / 5730\nl = solveset(Eq(exp(k0 * t), Rational(3, 10)), t, S.Reals)\nround(N(list(l)[0]))")
t_('''Schreibe f(t) = 300 · 2^(t/4) (Verdopplung alle 4 Stunden) als e-Funktion: Prüfe mit `simplify`, dass 300 · e^(ln(2)/4 · t) dasselbe ist (Differenz 0).''',
   body='simplify(300 * 2**(t / 4) - 300 * exp(log(2) / 4 * t))')
t_('Zeichne f(t) = 100 · e^(0,2t) und g(t) = 100 · e^(−0,2t) für 0 ≤ t ≤ 10 in ein Diagramm (mit Legende).',
   body='plot(100 * exp(Rational(1, 5) * t), 100 * exp(-Rational(1, 5) * t), (t, 0, 10), legend=True);')
predict("""f = 50 * exp(log(2) * t)
display(f.subs(t, 0))
display(f.subs(t, 1))
display(f.subs(t, 3))
simplify(f)""")

# ---------------------------------------------------------------- 2
sec('Parameter aus Messwerten')
expl('''#### Zwei Messwerte bestimmen das Modell

Für f(t) = c · e^(kt) braucht man zwei Messwerte. Aus f(0) = c folgt c direkt; aus einem zweiten Wert f(t₁) = y₁ folgt k.
Sind beide Werte nicht bei t = 0, teilt man die Gleichungen: f(t₂)/f(t₁) = e^(k(t₂ − t₁)).

Beispiel: Eine Bakterienkultur hat am Anfang 50 und nach 5 Stunden 80 Bakterien.''',
     """l = solveset(Eq(50 * exp(5*k), 80), k, S.Reals)
k0 = list(l)[0]
display(k0, N(k0, 4))
f = 50 * exp(k0 * t)
display(f)
N(f.subs(t, 12), 4)""")

t_('Ein Bestand hat am Anfang 1200 und nach 3 Tagen 1500 Einheiten (exponentielles Wachstum). Bestimme k genau und mit 4 Ziffern.',
   body="k0 = list(solveset(Eq(1200 * exp(3*k), 1500), k, S.Reals))[0]\ndisplay(k0)\nN(k0, 4)")
t_('Mit welchem Bestand ist im Modell der vorigen Aufgabe nach 10 Tagen zu rechnen? (auf eine ganze Zahl gerundet)',
   body="k0 = log(Rational(5, 4)) / 3\nround(N(1200 * exp(k0 * 10)))")
t_('''Eine Tasse Kaffee enthält 100 mg Koffein, nach 2 Stunden sind es noch 76 mg. Bestimme k (4 Ziffern) und die Halbwertszeit (4 Ziffern).''',
   body="k0 = list(solveset(Eq(100 * exp(2*k), 76), k, S.Reals))[0]\ndisplay(N(k0, 4))\nN(log(2) / Abs(k0), 4)")
t_('''Ein Bestand wird nach 2 Stunden mit 300 und nach 6 Stunden mit 1200 gemessen. Bestimme k (aus 1200/300 = e^(4k)) und dann c aus c · e^(2k) = 300.''',
   given="c = symbols('c', positive=True)",
   body="k0 = list(solveset(Eq(exp(4*k), 4), k, S.Reals))[0]\ndisplay(k0)\nsolve(Eq(c * exp(2*k0), 300), c)")
t_('''Löse dieselbe Aufgabe mit einem Gleichungssystem: `solve([Eq(c*exp(2*k), 300), Eq(c*exp(6*k), 1200)], [c, k], dict=True)` (c positiv angelegt).''',
   given="c = symbols('c', positive=True)",
   body="solve([Eq(c * exp(2*k), 300), Eq(c * exp(6*k), 1200)], [c, k], dict=True)")
t_('''**Weltbevölkerung:** 1990 lebten etwa 5,3 Mrd., 2020 etwa 7,8 Mrd. Menschen. Bestimme ein exponentielles Modell (t in Jahren ab 1990) und die Prognose
für 2050 mit 3 Ziffern.''',
   body="k0 = list(solveset(Eq(Rational(53, 10) * exp(30*k), Rational(78, 10)), k, S.Reals))[0]\nf = Rational(53, 10) * exp(k0 * t)\nN(f.subs(t, 60), 3)")

# ---------------------------------------------------------------- 3
sec('Beschränktes Wachstum')
expl('''#### f(t) = S − (S − f(0)) · e^(−kt)

Bei **beschränktem Wachstum** nähert sich der Bestand einer **Schranke** S. Die Änderungsrate ist proportional zum **Sättigungsmanko** S − f(t):
je näher am Ziel, desto langsamer. Beispiele: Abkühlung (S = Raumtemperatur), Lernkurven, Erwärmung, Medikamente bei Dauerinfusion.

f(t) = S − (S − f(0)) · e^(−kt) mit k > 0. Für t → ∞ geht f(t) → S.''',
     """f = 20 + (90 - 20) * exp(-Rational(1, 10) * t)
display(f)
display(N(f.subs(t, 10), 4))
display(limit(f, t, oo))
plot(f, 20, (t, 0, 40), ylim=(0, 100));""")

t_('''**Abkühlung:** Ein Tee hat 85 °C, der Raum 22 °C, k = 0,05 (pro Minute). Gib das Modell aus und die Temperatur nach 15 Minuten (4 Ziffern).''',
   body="f = 22 + (85 - 22) * exp(-Rational(1, 20) * t)\ndisplay(f)\nN(f.subs(t, 15), 4)")
t_('''Wann ist der Tee aus der vorigen Aufgabe auf 50 °C abgekühlt? Genau und mit 4 Ziffern.''',
   body="f = 22 + (85 - 22) * exp(-Rational(1, 20) * t)\nl = solveset(Eq(f, 50), t, S.Reals)\ndisplay(l)\nN(list(l)[0], 4)")
t_('''**Erwärmung:** Eine Flasche hat 6 °C und kommt in einen 24 °C warmen Raum. Nach 20 Minuten hat sie 12 °C. Bestimme k (genau und 4 Ziffern).''',
   body="f = 24 - (24 - 6) * exp(-k * t)\nk0 = list(solveset(Eq(f.subs(t, 20), 12), k, S.Reals))[0]\ndisplay(k0)\nN(k0, 4)")
t_('''**Lernkurve:** Jemand lernt Vokabeln. Höchstens 200 Wörter kann er sich merken, am Anfang kennt er 0, nach 5 Tagen 80. Bestimme das Modell f(t) = 200 − 200 · e^(−kt)
und wann er 180 Wörter kennt (4 Ziffern).''',
   body="k0 = list(solveset(Eq(200 - 200 * exp(-5*k), 80), k, S.Reals))[0]\nf = 200 - 200 * exp(-k0 * t)\ndisplay(f)\nN(list(solveset(Eq(f, 180), t, S.Reals))[0], 4)")
t_('''Prüfe für f(t) = 20 + 70 · e^(−0,1t), dass die Änderungsrate proportional zum Abstand von S = 20 ist: `simplify(f' − (−0,1) · (f − 20))` muss 0 sein.''',
   body="f = 20 + 70 * exp(-Rational(1, 10) * t)\nsimplify(diff(f, t) - (-Rational(1, 10)) * (f - 20))")
t_('''Zeichne die beschränkten Wachstumskurven f(t) = 100 − 100 · e^(−kt) für k = 0,1, 0,3 und 1 in ein Diagramm (0 ≤ t ≤ 20, mit Legende).''',
   body="plot(*[100 - 100 * exp(-w * t) for w in [Rational(1, 10), Rational(3, 10), 1]], (t, 0, 20), legend=True);")
predict("""f = 50 - 30 * exp(-t)
display(f.subs(t, 0))
display(limit(f, t, oo))
diff(f, t).subs(t, 0)""")

# ---------------------------------------------------------------- 4
sec('Bestand und Änderungsrate')
expl('''#### Wachstumsgeschwindigkeit

Die **Änderungsrate** f'(t) gibt an, wie schnell der Bestand gerade wächst.
- Exponentiell: f'(t) = k · f(t) (die Rate ist proportional zum **Bestand**)
- Beschränkt: f'(t) = k · (S − f(t)) (die Rate ist proportional zum **Sättigungsmanko**)

Mit der Integralrechnung bekommt man umgekehrt aus der Änderungsrate die Änderung des Bestands.''',
     """f = 400 * exp(Rational(1, 5) * t)
display(diff(f, t))
display(simplify(diff(f, t) - Rational(1, 5) * f))
display(N(diff(f, t).subs(t, 5), 4))
integrate(diff(f, t), (t, 0, 5)) == f.subs(t, 5) - f.subs(t, 0)""")

t_('''Ein Bestand wächst nach f(t) = 800 · e^(0,04t). Wie groß ist die Wachstumsgeschwindigkeit zu Beginn und nach 10 Zeiteinheiten (4 Ziffern)?''',
   body="f = 800 * exp(Rational(4, 100) * t)\ndisplay(diff(f, t).subs(t, 0))\nN(diff(f, t).subs(t, 10), 4)")
t_('''Wann wächst der Bestand aus der vorigen Aufgabe mit 50 Einheiten pro Zeiteinheit? (4 Ziffern)''',
   body="f = 800 * exp(Rational(4, 100) * t)\nN(list(solveset(Eq(diff(f, t), 50), t, S.Reals))[0], 4)")
t_('''Eine Tablette löst sich mit der Rate r(t) = 20 · e^(−0,5t) mg pro Minute auf. Wie viel mg lösen sich in den ersten 4 Minuten (4 Ziffern), wie viel insgesamt?''',
   body="r = 20 * exp(-Rational(1, 2) * t)\ndisplay(N(integrate(r, (t, 0, 4)), 4))\nintegrate(r, (t, 0, oo))")
t_('''Prüfe: Für welches k erfüllt f(t) = 3 · e^(kt) die Gleichung f'(t) = −0,25 · f(t)? Löse `Eq(diff(f, t), -Rational(1, 4) * f)` nach k.''',
   body="f = 3 * exp(k * t)\nsolve(Eq(diff(f, t), -Rational(1, 4) * f), k)")
t_('''Ein beschränktes Wachstum hat die Schranke 500 und f(0) = 100, k = 0,2. Gib die Änderungsrate zu Beginn und zum Zeitpunkt, an dem f = 400 ist, aus (über f' = k(S − f)).''',
   body="kk = Rational(1, 5)\ndisplay(kk * (500 - 100))\nkk * (500 - 400)")

# ---------------------------------------------------------------- 5
sec('Differentialgleichungen (Leistungsfach)')
expl('''#### `dsolve()`

Eine **Differentialgleichung** ist eine Gleichung, in der eine Funktion und ihre Ableitung vorkommen, z. B. f'(t) = 0,3 · f(t).
Gesucht ist **die Funktion** f. In sympy legst du dafür ein Funktionssymbol mit `Function('f')` an; f(t) ist dann die
unbekannte Funktion und `f(t).diff(t)` ihre Ableitung.

- `dsolve(gleichung, f(t))` liefert die **allgemeine Lösung** mit einer Konstanten C1.
- Mit `ics={f(0): 100}` (Anfangswert) wird die Konstante bestimmt.
- `.rhs` (right hand side) ist die rechte Seite der Lösung, also der Funktionsterm.
- `checkodesol(gleichung, loesung)` prüft die Lösung: `(True, 0)` bedeutet richtig.''',
     """f = Function('f')
dgl = Eq(f(t).diff(t), Rational(3, 10) * f(t))
display(dgl)
display(dsolve(dgl, f(t)))
loesung = dsolve(dgl, f(t), ics={f(0): 100})
display(loesung)
display(loesung.rhs.subs(t, 2))
checkodesol(dgl, loesung)""")

t_('''Löse die Differentialgleichung f'(t) = −0,5 · f(t) allgemein.''',
   given="f = Function('f')", body="dsolve(Eq(f(t).diff(t), -Rational(1, 2) * f(t)), f(t))")
t_('''Löse f'(t) = −0,5 · f(t) mit dem Anfangswert f(0) = 80.''',
   given="f = Function('f')", body="dsolve(Eq(f(t).diff(t), -Rational(1, 2) * f(t)), f(t), ics={f(0): 80})")
t_('''Löse die Differentialgleichung des beschränkten Wachstums f'(t) = 0,1 · (50 − f(t)) mit f(0) = 10.''',
   given="f = Function('f')", body="dsolve(Eq(f(t).diff(t), Rational(1, 10) * (50 - f(t))), f(t), ics={f(0): 10})")
t_('''Löse f'(t) = k · (G − f(t)) mit f(0) = 0 allgemein (k und die Schranke G positiv anlegen).''',
   given="f = Function('f')\nk, G = symbols('k G', positive=True)",
   body="dsolve(Eq(f(t).diff(t), k * (G - f(t))), f(t), ics={f(0): 0})")
t_('''Prüfe mit `checkodesol`, ob f(t) = 50 − 40 · e^(−t/10) die Differentialgleichung f'(t) = 0,1 · (50 − f(t)) löst.''',
   given="f = Function('f')",
   body="dgl = Eq(f(t).diff(t), Rational(1, 10) * (50 - f(t)))\ncheckodesol(dgl, Eq(f(t), 50 - 40 * exp(-t / 10)))")
t_('''Prüfe genauso, ob f(t) = 50 + 40 · e^(−t/10) eine Lösung ist, und ob f(t) = 50 − 40 · e^(t/10) eine ist (zwei Ausgaben).''',
   given="f = Function('f')",
   body="dgl = Eq(f(t).diff(t), Rational(1, 10) * (50 - f(t)))\ndisplay(checkodesol(dgl, Eq(f(t), 50 + 40 * exp(-t / 10))))\ncheckodesol(dgl, Eq(f(t), 50 - 40 * exp(t / 10)))")
t_('''**Abkühlung:** Eine Suppe mit 90 °C kühlt in einem 20 °C warmen Raum nach T'(t) = −0,08 · (T(t) − 20) ab. Löse die Differentialgleichung und gib die Temperatur
nach 10 Minuten mit 4 Ziffern aus.''',
   given="T = Function('T')",
   body="l = dsolve(Eq(T(t).diff(t), -Rational(8, 100) * (T(t) - 20)), T(t), ics={T(0): 90})\ndisplay(l)\nN(l.rhs.subs(t, 10), 4)")
t_('''**Zufluss:** In einen Teich fließen pro Tag 100 m³ Wasser, gleichzeitig verdunsten 2 % des Wasservolumens V pro Tag: V'(t) = 100 − 0,02 · V(t), V(0) = 1000.
Löse die Differentialgleichung und gib den Grenzwert für t → ∞ aus.''',
   given="V = Function('V')",
   body="l = dsolve(Eq(V(t).diff(t), 100 - Rational(2, 100) * V(t)), V(t), ics={V(0): 1000})\ndisplay(l)\nlimit(l.rhs, t, oo)")

# ---------------------------------------------------------------- 6
sec('Logistisches Wachstum (Zusatz)')
expl('''#### f(t) = S / (1 + a · e^(−k·S·t))

Beim **logistischen Wachstum** ist die Änderungsrate proportional zum Bestand **und** zum Sättigungsmanko: f'(t) = k · f(t) · (S − f(t)).
Am Anfang wächst der Bestand fast exponentiell, später fast beschränkt. Am **Wendepunkt** (bei f = S/2) ist das Wachstum am schnellsten.

Eine Lösung ist f(t) = S / (1 + a · e^(−k·S·t)) mit a = S/f(0) − 1.''',
     """G, a = 1000, 99
kk = Rational(1, 5000)
f = G / (1 + a * exp(-kk * G * t))
display(f, f.subs(t, 0))
display(simplify(diff(f, t) - kk * f * (G - f)))
tw = solve(diff(f, t, 2), t)[0]
display(tw, N(tw, 4), f.subs(t, tw))
plot(f, (t, 0, 50));""")

t_('''Eine Grippe breitet sich in einer Schule mit 800 Schülern logistisch aus: f(t) = 800 / (1 + 79 · e^(−0,4t)) (t in Tagen). Wie viele sind am Anfang krank, wie viele
nach 10 Tagen (gerundet)?''',
   body="f = 800 / (1 + 79 * exp(-Rational(2, 5) * t))\ndisplay(f.subs(t, 0))\nround(N(f.subs(t, 10)))")
t_('''Wann breitet sich die Grippe aus der vorigen Aufgabe am schnellsten aus (Wendestelle, genau und mit 4 Ziffern)? Wie viele sind dann krank?''',
   body="f = 800 / (1 + 79 * exp(-Rational(2, 5) * t))\ntw = solve(diff(f, t, 2), t)[0]\ndisplay(tw, N(tw, 4))\nf.subs(t, tw)")
t_('''Prüfe, dass f(t) = 800 / (1 + 79 · e^(−0,4t)) die Gleichung f'(t) = 0,0005 · f(t) · (800 − f(t)) erfüllt (Differenz mit `simplify`).''',
   body="f = 800 / (1 + 79 * exp(-Rational(2, 5) * t))\nsimplify(diff(f, t) - Rational(5, 10000) * f * (800 - f))")
t_('''Zeichne die logistische Kurve der Grippe-Aufgabe und ihre Ableitung (Ausbreitungsgeschwindigkeit) für 0 ≤ t ≤ 25 in zwei Diagramme.''',
   body="f = 800 / (1 + 79 * exp(-Rational(2, 5) * t))\nplot(f, (t, 0, 25));\nplot(diff(f, t), (t, 0, 25));")

# ---------------------------------------------------------------- 7
sec('Gemischte Übungen')
t_('''Ein radioaktives Präparat hat eine Halbwertszeit von 8 Tagen. Wie viel Prozent sind nach 30 Tagen noch vorhanden (3 Ziffern)?''',
   body="N(100 * Rational(1, 2)**Rational(30, 8), 3)")
t_('''Ein Auto verliert pro Jahr 15 % an Wert, Neupreis 30 000 €. Nach wie vielen Jahren ist es weniger als 10 000 € wert? Gib die genaue Lösung mit 4 Ziffern
und die nächste ganze Zahl (`ceiling`) aus.''',
   body="l = solveset(Eq(30000 * Rational(85, 100)**t, 10000), t, S.Reals)\nw = list(l)[0]\ndisplay(N(w, 4))\nceiling(w)")
t_('''Ein Ball wird aus dem Kühlschrank (4 °C) in einen 20 °C warmen Raum gelegt. Nach 10 Minuten hat er 10 °C. Wann hat er 18 °C? (beschränktes Wachstum, 4 Ziffern)''',
   body="f = 20 - 16 * exp(-k * t)\nk0 = list(solveset(Eq(f.subs(t, 10), 10), k, S.Reals))[0]\nN(list(solveset(Eq(f.subs(k, k0), 18), t, S.Reals))[0], 4)")
t_('''Vergleiche zwei Angebote: A wächst exponentiell mit f(t) = 1000 · e^(0,05t), B linear mit g(t) = 1000 + 80t. Ab wann ist A größer? (`nsolve` mit Startwert 20, 4 Ziffern)''',
   body="N(nsolve(1000 * exp(Rational(5, 100) * t) - (1000 + 80*t), t, 20), 4)")
t_('''Zeichne die beiden Angebote aus der vorigen Aufgabe für 0 ≤ t ≤ 30 (mit Legende).''',
   body="plot(1000 * exp(Rational(5, 100) * t), 1000 + 80*t, (t, 0, 30), legend=True);")

generate('sympy_wachstum', 'Wachstum: exponentiell, beschränkt, logistisch, Differentialgleichungen', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
