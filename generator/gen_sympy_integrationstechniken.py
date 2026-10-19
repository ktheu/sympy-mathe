# Erzeugt ../content/sympy_integrationstechniken.ipynb (siehe nbgen.py und sympy_ausgabe.py).
#
#     py -3.13 -W error generator/gen_sympy_integrationstechniken.py
#     py -3.13 generator/pyodide_check/pruefen.py generator/gen_sympy_integrationstechniken.py
#
# Vertiefungskurs Mathematik BW: weiterführende Integralrechnung (partielle Integration, Substitution, Partialbruchzerlegung als Zusatz).
# Differentialgleichungen stehen im Notebook sympy_dmw_dgl (Wahlfach Digitale Mathematische Werkzeuge). Baut auf sympy_integrale auf.
from nbgen import sec, expl, task, predict, generate, setup
from sympy_ausgabe import sympy_ausfuehrung


def t(text, given='', body='', kind='normal'):
    """Aufgabe, deren Lösung aus dem vorgegebenen Code plus body besteht."""
    task(text, given=given, solution=(given + '\n' + body) if given else body, kind=kind)


SETUP = "from sympy import *\ninit_printing()\nx, u = symbols('x u', real=True)"

INTRO = '''In diesem Notebook (Vertiefungskurs) geht es um **Integrationstechniken**. Mit **partieller Integration** und **Substitution** findest du
Stammfunktionen, die man nicht einfach „ablesen“ kann; als Zusatz zerlegst du Brüche in **Partialbrüche**.

`integrate()` liefert das Ergebnis sofort. Hier geht es aber um den **Rechenweg**: Du führst die Schritte einzeln mit sympy aus
und vergleichst am Ende mit dem fertigen Ergebnis.

Vorausgesetzt wird das Notebook *Integrale*.

Jeder Abschnitt beginnt mit kurzen Erklärungen und Beispielen. Führe die Beispiele aus und probiere sie ruhig ein wenig aus.
Danach folgen viele kleine Übungen. Unter den meisten Aufgaben steht das **erwartete Ergebnis**.'''

setup('''#### sympy laden

**Führe diese Zelle zuerst aus** (und nach jedem Neustart des Kernels wieder). Sie lädt sympy, schaltet die Formel-Ausgabe ein
und legt die reellen Variablen `x` und `u` an.''',
      SETUP)

# ---------------------------------------------------------------- 1
sec('Partielle Integration')
expl('''#### ∫ u · v' dx = u · v − ∫ u' · v dx

Die **partielle Integration** kommt aus der Produktregel. Man zerlegt den Integranden in einen Faktor u, der beim Ableiten einfacher wird,
und einen Faktor v', den man integrieren kann.

Beispiel ∫ x · eˣ dx: u = x (u' = 1), v' = eˣ (v = eˣ). Dann ist ∫ x · eˣ dx = x · eˣ − ∫ 1 · eˣ dx = (x − 1) · eˣ.''',
     """uu = x
vs = exp(x)
v = integrate(vs, x)
F = uu * v - integrate(diff(uu, x) * v, x)
display(factor(F))
display(integrate(x * exp(x), x))
simplify(diff(F, x) - x * exp(x))""")

PI = "F = uu * v - integrate(diff(uu, x) * v, x)\n"
t('Berechne ∫ x · sin(x) dx mit partieller Integration (u = x, v\' = sin x) wie im Beispiel und vergleiche mit `integrate`.',
  body="uu, vs = x, sin(x)\nv = integrate(vs, x)\n" + PI + "display(F)\nintegrate(x * sin(x), x)")
t('Berechne ∫ x · e^(−x) dx mit partieller Integration.', body="uu, vs = x, exp(-x)\nv = integrate(vs, x)\n" + PI + "factor(F)")
t('''Berechne ∫ ln(x) dx mit dem Trick ln(x) = 1 · ln(x): u = ln(x), v' = 1.''', body="uu, vs = log(x), 1\nv = integrate(vs, x)\n" + PI + "F")
t('''Berechne ∫ x · ln(x) dx (u = ln x, v' = x).''', body="uu, vs = log(x), x\nv = integrate(vs, x)\n" + PI + "expand(F)")
t('''∫ x² · eˣ dx braucht **zweimal** partielle Integration. Gib zuerst u · v − ∫ u'·v **ohne** das letzte Integral auszurechnen aus
(`Integral(...)` statt `integrate`), dann das Endergebnis mit `integrate` (ausgeklammert).''',
  body="display(x**2 * exp(x) - Integral(2*x * exp(x), x))\nfactor(integrate(x**2 * exp(x), x))")
t('''Berechne das bestimmte Integral ∫₀^π x · sin(x) dx: [u · v]₀^π − ∫₀^π u' · v dx.''',
  body="uu, vs = x, sin(x)\nv = integrate(vs, x)\n(uu * v).subs(x, pi) - (uu * v).subs(x, 0) - integrate(diff(uu, x) * v, (x, 0, pi))")
t('''**Phönix-Trick:** Bei I = ∫ eˣ · sin(x) dx kommt nach zweimaliger partieller Integration I wieder vor: I = eˣ sin x − eˣ cos x − I. Löse diese Gleichung nach I
(mit `solve(..., simplify=False)`, sonst schreibt sympy das Ergebnis mit einem verschobenen Kosinus) und vergleiche mit `integrate`.''',
  given="I_ = symbols('I_')",
  body="display(solve(Eq(I_, exp(x) * sin(x) - exp(x) * cos(x) - I_), I_, simplify=False))\nintegrate(exp(x) * sin(x), x)")
t('''Prüfe das Ergebnis von ∫ x² · cos(x) dx durch Ableiten (`simplify` der Differenz).''',
  body="F = integrate(x**2 * cos(x), x)\ndisplay(F)\nsimplify(diff(F, x) - x**2 * cos(x))")

# ---------------------------------------------------------------- 2
sec('Integration durch Substitution')
expl('''#### ∫ f(g(x)) · g'(x) dx = F(g(x))

Steht im Integranden eine verkettete Funktion **und** die Ableitung der inneren Funktion, ersetzt man die innere Funktion durch u = g(x).
Dann ist du = g'(x) dx, und das Integral wird einfacher.

Beispiel ∫ 2x · cos(x²) dx: u = x², du = 2x dx, also ∫ cos(u) du = sin(u) = sin(x²).

Mit sympy: Integrand durch g'(x) teilen, g(x) durch u ersetzen (`subs`), nach u integrieren, dann u = g(x) zurücksetzen.''',
     """g = x**2
integrand = 2*x * cos(x**2)
in_u = simplify(integrand / diff(g, x)).subs(g, u)
display(in_u)
Fu = integrate(in_u, u)
display(Fu.subs(u, g))
integrate(integrand, x)""")

t('Berechne ∫ 3x² · e^(x³) dx mit der Substitution u = x³ wie im Beispiel.',
  body="g = x**3\nin_u = simplify(3*x**2 * exp(x**3) / diff(g, x)).subs(g, u)\ndisplay(in_u)\nintegrate(in_u, u).subs(u, g)")
t('Berechne ∫ x · (x² + 1)⁵ dx mit u = x² + 1 (hier bleibt ein Faktor 1/2).',
  body="g = x**2 + 1\nin_u = simplify(x * (x**2 + 1)**5 / diff(g, x)).subs(g, u)\ndisplay(in_u)\nintegrate(in_u, u).subs(u, g)")
t('Berechne ∫ cos(x) · sin³(x) dx mit u = sin(x).',
  body="g = sin(x)\nin_u = simplify(cos(x) * sin(x)**3 / diff(g, x)).subs(g, u)\ndisplay(in_u)\nintegrate(in_u, u).subs(u, g)")
t('''Berechne ∫ x/(x² + 4) dx mit u = x² + 4 (ein Logarithmus entsteht).''',
  body="g = x**2 + 4\nin_u = simplify(x / (x**2 + 4) / diff(g, x)).subs(g, u)\ndisplay(in_u)\nintegrate(in_u, u).subs(u, g)")
t('''**Logarithmische Integration:** ∫ g'(x)/g(x) dx = ln|g(x)|. Berechne ∫ (2x + 3)/(x² + 3x + 1) dx und ∫ tan(x) dx = ∫ sin(x)/cos(x) dx mit `integrate`.''',
  body="display(integrate((2*x + 3) / (x**2 + 3*x + 1), x))\nintegrate(sin(x) / cos(x), x)")
t('''Berechne ∫₀² x · e^(x²) dx mit Substitution: Die Grenzen werden mit u = x² zu 0 und 4. Rechne ∫₀⁴ (1/2) eᵘ du und vergleiche mit `integrate`.''',
  body="display(integrate(exp(u) / 2, (u, 0, 4)))\nintegrate(x * exp(x**2), (x, 0, 2))")
t('''Prüfe durch Ableiten, dass F(x) = −(1/3)·(1 − x²)^(3/2) eine Stammfunktion von x · √(1 − x²) ist.''',
  body="F = -Rational(1, 3) * (1 - x**2)**Rational(3, 2)\nsimplify(diff(F, x) - x * sqrt(1 - x**2))")
t('''**Fläche des Einheitskreises:** Berechne 4 · ∫₀¹ √(1 − x²) dx (Viertelkreis). Von Hand mit x = sin(u); hier mit `integrate`.''',
  body="4 * integrate(sqrt(1 - x**2), (x, 0, 1))")
predict("""display(integrate(2*x * exp(x**2), x))
display(integrate(cos(3*x), x))
integrate(1 / (2*x + 1), x)""")

# ---------------------------------------------------------------- 3
sec('Partialbruchzerlegung (Zusatz)')
expl('''#### Brüche zerlegen, dann integrieren

Gebrochenrationale Funktionen zerlegt man in eine Summe einfacher Brüche (**Partialbrüche**), die man einzeln integrieren kann.
`apart(term, x)` zerlegt, z. B. (3x + 1)/(x² − 1) = 2/(x − 1) + 1/(x + 1).

Von Hand: Ansatz A/(x − 1) + B/(x + 1), mit dem Nenner (x − 1)(x + 1) multiplizieren: 3x + 1 = A(x + 1) + B(x − 1).
Setzt man die Nullstellen x = 1 und x = −1 ein, erhält man A und B.''',
     """display(apart((3*x + 1) / (x**2 - 1), x))
A_, B_ = symbols('A_ B_')
gl = Eq(3*x + 1, A_ * (x + 1) + B_ * (x - 1))
display(solve([gl.subs(x, 1), gl.subs(x, -1)], [A_, B_]))
integrate((3*x + 1) / (x**2 - 1), x)""")

t('Zerlege 1/(x² − 4) in Partialbrüche und integriere.', body="display(apart(1 / (x**2 - 4), x))\nintegrate(1 / (x**2 - 4), x)")
t('Zerlege (x + 5)/(x² + x − 2) in Partialbrüche und integriere.', body="display(apart((x + 5) / (x**2 + x - 2), x))\nintegrate((x + 5) / (x**2 + x - 2), x)")
t('Zerlege x²/(x² − 1) (erst Polynomdivision, `apart` macht beides).', body="apart(x**2 / (x**2 - 1), x)")
t('Berechne ∫₂³ 1/(x² − 1) dx genau und fasse die Logarithmen mit `logcombine` zusammen.', body="logcombine(integrate(1 / (x**2 - 1), (x, 2, 3)), force=True)")

# ---------------------------------------------------------------- 4
sec('Gemischte Übungen')
t('''Berechne ∫ x³ · e^(x²) dx mit sympy und prüfe das Ergebnis durch Ableiten. (Von Hand: erst u = x², dann partiell.)''',
  body="F = integrate(x**3 * exp(x**2), x)\ndisplay(F)\nsimplify(diff(F, x) - x**3 * exp(x**2))")
t('''Berechne ∫₁^e x² · ln(x) dx genau.''', body="integrate(x**2 * log(x), (x, 1, E))")
t('''Berechne ∫ sin(x) · cos(x) dx auf zwei Arten: mit der Substitution u = sin(x) und mit u = cos(x). Gib beide Ergebnisse aus und ihre Differenz
(vereinfacht). Ist die Differenz eine Konstante, sind beide Stammfunktionen.''',
  body="F1 = integrate(u, u).subs(u, sin(x))\nF2 = integrate(-u, u).subs(u, cos(x))\ndisplay(F1, F2)\nsimplify(F1 - F2)")
t('''Berechne ∫₀^(π/2) x² · sin(x) dx genau (zweimal partiell; mit `integrate` prüfen).''', body="integrate(x**2 * sin(x), (x, 0, pi/2))")
t('''Berechne ∫ (2x + 1)/(x² + x − 6) dx: Erkenne, dass der Zähler die Ableitung des Nenners ist (logarithmische Integration), und prüfe mit `integrate`.''',
  body="display(simplify(diff(x**2 + x - 6, x) - (2*x + 1)))\nintegrate((2*x + 1) / (x**2 + x - 6), x)")
t('''Berechne den Flächeninhalt zwischen dem Graphen von f(x) = x · e^(−x) und der x-Achse über [0, ∞) (partielle Integration, uneigentliches Integral).''',
  body="integrate(x * exp(-x), (x, 0, oo))")

generate('sympy_integrationstechniken', 'Integrationstechniken: partielle Integration, Substitution, Partialbrüche', INTRO,
         sprache='sympy', ausfuehren=sympy_ausfuehrung(SETUP))
