# Format .agent — Spécification

## Objectif

Ce fichier définit le format YAML utilisé pour stocker l'État Long d'un agent autonome. Le fichier `.agent` est la mémoire persistante qui permet à un agent de retrouver son contexte entre deux sessions.

## Schéma YAML

```yaml
agent:
  nom: string                    # Nom unique de l'agent (kebab-case)
  objectif: string               # Objectif principal en 1 phrase
  version: string                # Version semver de l'agent
  modes:
    - analyse                    # Mode M1
    - synthese                   # Mode M2
    - pipeline                   # Mode M3
    - simulation                 # Mode M4
  regles:
    - string                     # Règles strictes de l'agent
  inputs:
    - string                     # Types d'entrées acceptées
  outputs:
    - string                     # Types de sorties produites
  memoire:
    court:
      description: string       # Description de la structure EC
      max_entries: integer       # Nombre max d'entrées (défaut: 20)
      ttl: string                 # Durée de vie (ex: "session")
    long:
      description: string       # Description de la structure EL
      persistence: string        # Mode de persistance ("file", "clone-chat", "kb")
      path: string                # Chemin du fichier de persistance
  formats:
    standard: boolean            # Format 4 sections obligatoire
    pipeline: boolean             # Format A-F obligatoire
  pipeline:
    steps:
      - code: string             # Code de l'étape (A-H)
        nom: string              # Nom de l'étape
        description: string      # Description
        module: string           # Module responsable
    verification: boolean         # Vérification à chaque étape
  securite:
    no_hallucination: boolean     # Ne jamais inventer de données
    no_rule_modification: boolean # Ne jamais modifier les règles EL
    no_sensitive_data: boolean    # Pas de données sensibles
    max_token_output: integer     # Plafond tokens en sortie (défaut: 4000)
```

## Exemple minimal

```yaml
agent:
  nom: research-assistant
  objectif: "Analyser et synthétiser des documents de recherche"
  version: "1.0.0"
  modes: [analyse, synthese, pipeline, simulation]
  regles:
    - "Toujours citer les sources"
    - "Ne jamais inventer de données"
    - "Format de réponse standard obligatoire"
  inputs: ["document", "question", "query"]
  outputs: ["analyse", "synthese", "rapport"]
  memoire:
    court:
      description: "Derniers messages et intentions locales"
      max_entries: 20
      ttl: "session"
    long:
      description: "Préférences utilisateur et historique"
      persistence: "file"
      path: "research-assistant.agent"
  formats:
    standard: true
    pipeline: true
  pipeline:
    steps:
      - code: A
        nom: "Analyse du message"
        description: "Segmenter et classifier l'entrée"
        module: "Analyse"
      - code: B
        nom: "Mise à jour État Court"
        description: "Intégrer le message dans le contexte"
        module: "Mémoire"
      - code: C
        nom: "Consultation État Long"
        description: "Récupérer règles et préférences"
        module: "Mémoire"
      - code: D
        nom: "Détermination du mode"
        description: "Choisir M1-M4"
        module: "Analyse"
      - code: E
        nom: "Exécution du mode"
        description: "Traiter selon le mode sélectionné"
        module: "Synthèse"
      - code: F
        nom: "Synthèse structurée"
        description: "Produire la réponse formatée"
        module: "Synthèse"
      - code: G
        nom: "Vérification"
        description: "Valider cohérence et conformité"
        module: "Règles"
      - code: H
        nom: "Mise à jour mémoire"
        description: "Persister les nouvelles informations"
        module: "Mémoire"
    verification: true
  securite:
    no_hallucination: true
    no_rule_modification: true
    no_sensitive_data: true
    max_token_output: 4000
```

## Règles de persistance

1. L'État Court n'est **jamais** persisté — il est reconstruit à chaque session
2. L'État Long est persisté dans le fichier `.agent` à la fin de chaque pipeline
3. Si clone-chat est disponible, l'État Long peut être intégré dans le clone
4. Le fichier `.agent` suit la convention kebab-case (SHARED §1.2)
5. Les chemins dans le fichier sont **relatifs** (SHARED §3.2)

## Compatibilité

- Compatible avec le format YAML frontmatter des SKILL.md
- Compatible avec le Protocole de Découverte KB (SHARED §2.3)
- Compatible avec le format worklog (SHARED §1.4)