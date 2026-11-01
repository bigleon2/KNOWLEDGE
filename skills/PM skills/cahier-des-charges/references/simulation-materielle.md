# Simulation matérielle — patrons Python stdlib pour les tests TH (M7 TESTER)

> Compatibilité : skill `cahier-des-charges` v2.0.1 → v2.0.2 (résorption réserve S3 — élargissement de la description ; contenu de cette référence inchangé, R2).


> Skill cahier-des-charges v2.0.0 — reference des patrons de tests matériels SIMULÉS. Un test
> matériel simulé (TH-xx) construit un modèle discret exécutable du sous-système physique et
> vérifie sur ce modèle les exigences qui lui sont allouées. Règles absolues : **stdlib Python
> uniquement**, **déterminisme** (graine fixe, pas d'horloge murale dans le calcul), **verdicts
> mécaniques** (assertions à seuils), **journal JSON** persistant — le même test rejoué deux fois
> produit le même verdict et le même journal (idempotence R1).

## §1 — Cadre général d'un TH

```python
#!/usr/bin/env python3
"""TH-xx : <ce que le test simule et vérifie> — vérifie <EF/ENF-…>.
Patron : <réf. §3-§6> · Graine : <n> · stdlib uniquement."""
import json, math, random, time
from pathlib import Path

SEED = 42                      # graine fixe — le modèle est reproductible
DT = 0.01                      # pas de temps discret (s) — adapté au phénomène
T_END = 10.0                   # durée simulée (s)
JOURNAL = Path(__file__).parent.parent / "journal" / "th_xx.json"

def simuler():
    rng = random.Random(SEED)  # RNG local seedé — JAMAIS random.global
    etat = {...}               # état du modèle physique
    trace = []                 # échantillonnage pour le journal
    t = 0.0
    while t < T_END:
        # 1. commande (actionneur) → 2. physique (modèle discret) → 3. capteur (mesure bruitée)
        ...
        trace.append({"t": round(t, 3), **etat})
        t += DT
    return trace

def verifier(trace):
    """Retourne [(nom_check, bool, détail)] — chaque check cite son exigence."""
    return [("EF-01 : <critère>", bool(...), f"valeur={...}")]

def main():
    trace = simuler()
    checks = verifier(trace)
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL.write_text(json.dumps({
        "test": "TH-xx", "graine": SEED, "dt": DT, "verdict": "PASS" if all(ok for _, ok, _ in checks) else "ECHEC",
        "checks": [{"nom": n, "ok": ok, "detail": d} for n, ok, d in checks],
    }, indent=2, sort_keys=True), encoding="utf-8")
    for nom, ok, detail in checks:
        print(("PASS " if ok else "ECHEC") + f" {nom} — {detail}")
    raise SystemExit(0 if all(ok for _, ok, _ in checks) else 1)

if __name__ == "__main__":
    main()
```

Discipline : chaque check cite l'exigence vérifiée (EF/ENF-xx) ; les tolérances sont des
constantes nommées au sommet du fichier (pas des nombres enfouis) ; le journal est écrit même en
échec ; le code retour est 0/1 — `run_all.py` l'agrège.

## §2 — Modèle discret : la règle d'Euler appliquée à bon escient

Un système continu se simule par intégration explicite à pas fixe : `x[t+1] = x[t] + dt * f(x[t], u[t])`.
Le pas doit être au moins 20× plus petit que la constante de temps la plus rapide simulée
(ex : thermique τ=60 s → dt ≤ 3 s ; asservissement électrique τ=5 ms → dt ≤ 0,25 ms). Un pas trop
grand produit une divergence numérique qui n'est PAS un échec du système — c'est un bug du test.

## §3 — Patron : système du 1er/2nd ordre (thermique, mécanique, RC)

```python
# 1er ordre : dX/dt = (K*u - X) / TAU           (thermique, filtre, attitude lente)
# 2nd ordre (masse-ressort-amortisseur) :
#   dx'' = (F(u) - c*dx - k*x) / m
x += dt * v; v += dt * (F(u) - c*v - k*x) / m   # Euler explicite, dt strict
```
Usage : serre (température d'ambiance), suspension, actionneur à lissage, réseau RC.
Vérifications types : dépassement (overshoot) < seuil, temps d'établissement à ±x % < seuil,
erreur statique < seuil (ENF de performance).

## §4 — Patron : capteur virtuel (bruit, biais, quantification, échantillonnage)

```python
def mesurer(vraie_valeur):
    bruit = rng.gauss(0.0, SIGMA)              # gaussienne seedée
    biais  = BIAS                              # dérive systématique
    brut   = vraie_valeur + bruit + biais
    return round(brut / QUANT) * QUANT          # quantification du CAN
```
Usage : tout sous-système instrumenté. Vérifications types : la commande tolère le bruit de
sigma connu (ENF robustesse), la précision mesurée reste dans la tolérance exigée, la chaîne
ne diverge pas avec le pire biais admissible.

## §5 — Patron : actionneur virtuel (saturation, dead-zone, pente limitée)

```python
def commander(u):
    u = max(U_MIN, min(U_MAX, u))              # saturation
    if abs(u) < DEADZONE: u = 0.0              # dead-zone
    return u                                   # (variante : limiteur de pente du/dt)
```
Usage : moteur, vanne, résistance chauffante. Vérifications types : le régulateur converge
malgré la saturation (pas de windup non géré), le temps de montée respecte l'ENF.

## §6 — Patron : boucle PID complète (le modèle mécatronique canonique)

```python
err = consigne - y; integ += err*dt; deriv = (err - err_prec)/dt
u = Kp*err + Ki*integ + Kd*deriv
integ = max(I_MIN, min(I_MAX, integ))          # anti-windup par bornage
```
Chaîne complète : consigne → PID → actionneur §5 → physique §3 → capteur §4 → comparaison.
Vérifications types : dépassement < X %, temps d'établissement < T s à ±Y %, erreur statique < Z,
rejet de perturbation (échelon de charge à t connu) revenant dans la tolérance < T' s.
C'est LE test TH par défaut d'un sous-système asservi (serre, robot, drone, CNC).

## §7 — Autres patrons rapides

- **Système à événements / réseau** : file d'événements discrète, retards tirés d'une loi seedée —
  vérifier la cadence, la perte admissible, la latence de bout en bout (IoT, pipeline vidéo).
- **Chaîne d'échantillonnage audio** : signal test (sine/balayage) → échantillonnage Fs →
  quantification b bits → filtrage — vérifier latence, dynamique, repliement (audio).
- **Bilan de puissance / énergie** : intégrer P(t)=U·I sur la mission type — vérifier autonomie
  et dimensionnement (énergie, batterie).
- **Charge mécanique statique** : somme des efforts, marge au seuil du matériau — vérifier
  dimensionnement (mécanique, CAO).

## §8 — Harness `run_all.py` et orchestration

- `run_all.py` (généré par le scaffold) découvre `tf_*.py` et `th_*.py`, les exécute en
  sous-processus, agrège les code-retours et écrit `journal/synthese.json` (verdict global
  PASS/ECHEC + détail par test + durées). Aucune dépendance à un framework de test.
- Lorsque la batterie grandit ou que des tests deviennent des nœuds concurrents (simulations
  longues), les enregistrer au registre **inter-scripts** et laisser son orchestrateur faire le
  fan-out par niveau — les journaux restent identiques (idempotence).
- Un test INCONCLUSANT (modèle incapable de prouver l'exigence) est déclaré NON VÉRIFIABLE dans
  le rapport de couverture avec la raison — jamais PASS par défaut d'assertion (R3).
