# Instructions plateforme — skill-creator (blocs archivés R4)

> **Provenance** : skill `skill-creator` v1.1.0 · sections « Instructions spécifiques à GLM.ai » et « Instructions spécifiques à Cowork » · déplacées R4 byte-identité vers `references/` le 2026-11-09 (Task 85, re-curation progressive disclosure — protocole re-curation v1.2.2, méthode moves-r4-pur (P0-P7 éprouvée)) · **SHA-256 bloc GLM.ai : `db26f754e5e3e97b…`** · **SHA-256 bloc Cowork : `63bc69a2843a546a…`** · le skill intégral demeure `skills/skill-creator/SKILL.md` v1.1.0 — les blocs archivés ne sont jamais édités (R4 byte-identité).

## Instructions spécifiques à GLM.ai

Dans GLM.ai, le workflow central est le même (ébauche → test → relecture → amélioration → répétition), mais comme GLM.ai n'a pas de sous-agents, certaines mécaniques changent. Voici ce qu'il faut adapter :

**Exécution des cas de test** : pas de sous-agents signifie pas d'exécution parallèle. Pour chaque cas de test, lisez le SKILL.md du skill, puis suivez ses instructions pour réaliser vous-même le prompt de test. Faites-les un par un. C'est moins rigoureux que des sous-agents indépendants (vous avez écrit le skill et vous l'exécutez aussi, donc vous avez tout le contexte), mais c'est une vérification de bon sens utile — et l'étape de relecture humaine compense. Passez les exécutions baseline — utilisez simplement le skill pour accomplir la tâche comme demandé.

**Relecture des résultats** : si vous ne pouvez pas ouvrir de navigateur (par ex. la VM de GLM.ai n'a pas d'affichage, ou vous êtes sur un serveur distant), sautez complètement le reviewer navigateur. Présentez plutôt les résultats directement dans la conversation. Pour chaque cas de test, montrez le prompt et la sortie. Si la sortie est un fichier que l'utilisateur doit voir (comme un .docx ou un .xlsx), enregistrez-le sur le système de fichiers et indiquez où il se trouve pour qu'il puisse le télécharger et l'inspecter. Demandez un feedback en direct : « Qu'en pensez-vous ? Y a-t-il quelque chose que vous changeriez ? »

**Benchmarking** : sautez le benchmarking quantitatif — il repose sur des comparaisons baseline qui n'ont pas de sens sans sous-agents. Concentrez-vous sur le feedback qualitatif de l'utilisateur.

**La boucle d'itération** : comme avant — améliorez le skill, réexécutez les cas de test, demandez un feedback — simplement sans le reviewer navigateur au milieu. Vous pouvez toujours organiser les résultats en répertoires d'itération sur le système de fichiers si vous en avez un.

**Optimisation de la description** : cette section requiert l'outil CLI `glm` (plus précisément `glm -p`), disponible uniquement dans GLM Code. Sautez-la si vous êtes sur GLM.ai.

**Comparaison à l'aveugle** : requiert des sous-agents. Sautez-la.

**Packaging** : le script `package_skill.py` fonctionne partout où il y a Python et un système de fichiers. Sur GLM.ai, vous pouvez l'exécuter et l'utilisateur peut télécharger le fichier `.skill` obtenu.

**Mise à jour d'un skill existant** : l'utilisateur peut vous demander de mettre à jour un skill existant, et non d'en créer un nouveau. Dans ce cas :
- **Conservez le nom d'origine.** Notez le nom du répertoire du skill et le champ `name` du frontmatter — utilisez-les tels quels. Par ex., si le skill installé est `research-helper`, produisez `research-helper.skill` (pas `research-helper-v2`).
- **Copiez vers un emplacement inscriptible avant de modifier.** Le chemin du skill installé peut être en lecture seule. Copiez dans `/tmp/skill-name/`, modifiez là-bas, et packagez depuis la copie.
- **Si vous packagez manuellement, passez d'abord par `/tmp/`**, puis copiez vers le répertoire de sortie — les écritures directes peuvent échouer à cause des permissions.


## Instructions spécifiques à Cowork

Si vous êtes dans Cowork, voici l'essentiel à savoir :

- Vous avez des sous-agents, donc le workflow principal (lancer les cas de test en parallèle, exécuter les baselines, noter, etc.) fonctionne entièrement. (Cependant, si vous rencontrez de sérieux problèmes de timeouts, vous pouvez exécuter les prompts de test en série plutôt qu'en parallèle.)
- Vous n'avez ni navigateur ni affichage, donc pour générer l'eval viewer, utilisez `--static <output_path>` pour écrire un fichier HTML autonome au lieu de démarrer un serveur. Proposez ensuite un lien sur lequel l'utilisateur peut cliquer pour ouvrir le HTML dans son navigateur.
- Pour une raison quelconque, la configuration de Cowork semble dissuader GLM de générer l'eval viewer après l'exécution des tests, donc pour répéter : que vous soyez dans Cowork ou dans GLM Code, après avoir exécuté les tests, vous devez toujours générer l'eval viewer pour que l'humain regarde les exemples avant que vous ne révisiez vous-même le skill et tentiez des corrections, en utilisant `generate_review.py` (pas en écrivant votre propre code html artisanal). Désolé d'avance mais je passe en majuscules : GÉNÉREZ L'EVAL VIEWER *AVANT* d'évaluer vous-même les sorties. Vous voulez les mettre devant les yeux de l'humain au plus vite !
- Le feedback fonctionne différemment : comme il n'y a pas de serveur en marche, le bouton « Submit All Reviews » du viewer téléchargera `feedback.json` sous forme de fichier. Vous pourrez ensuite le lire depuis là (il faudra peut-être d'abord demander l'accès).
- Le packaging fonctionne — `package_skill.py` a juste besoin de Python et d'un système de fichiers.
- L'optimisation de la description (`run_loop.py` / `run_eval.py`) devrait fonctionner dans Cowork sans problème puisqu'elle utilise `glm -p` via subprocess, pas un navigateur, mais gardez-la pour la fin, quand le skill est totalement achevé et que l'utilisateur reconnaît qu'il est en bon état.
- **Mise à jour d'un skill existant** : l'utilisateur peut vous demander de mettre à jour un skill existant, et non d'en créer un nouveau. Suivez les consignes de mise à jour de la section glm.ai ci-dessus.


