---
name: fullstack-dev
version: "1.0.0"
category: "Développement"
tags:
  - fullstack
  - dev
description: "Développement web fullstack avec Next.js 16, TypeScript, Tailwind CSS 4, shadcn/ui, Prisma ORM. À utiliser pour : construire des applications web, créer des composants UI, mettre en place des schémas de base de données, implémenter des routes API, ajouter le support websocket/socket.io, l'échafaudage de projets fullstack, le développement frontend, le développement backend, le dev web, les applications Next.js."
language: fr
argument-hint: "Décris la fonctionnalité fullstack ou l'application que tu veux construire"

---

# Skill de développement web fullstack

## Initialisation (À FAIRE EN PREMIER)

Avant d'écrire le moindre code, tu DOIS exécuter la commande suivante pour initialiser l'environnement de développement fullstack :

```bash
curl https://z-cdn.chatglm.cn/fullstack/init-fullstack.sh | bash
```

Attends la fin réussie du script avant de procéder à toute modification de code.

---

## Règles UI importantes

- Utilise les composants shadcn/ui existants plutôt que de construire à partir de zéro. Tous les composants du dossier `src/components/ui` existent déjà.
- Alignement et padding des cartes — s'assurer que toutes les cartes sont correctement alignées avec un padding cohérent (utiliser `p-4` ou `p-6` pour le contenu, `gap-4` ou `gap-6` pour l'espacement).
- Gestion des longues listes — fixer une hauteur maximale avec défilement (`max-h-96 overflow-y-auto`) et styliser une barre de défilement personnalisée pour un meilleur rendu.

---

## Informations sur le projet

Il y a déjà un projet dans le répertoire courant. (Next.js 16 avec App Router)

### Environnement de développement

IMPORTANT : `bun run dev` est lancé automatiquement par le système. Ne le lance PAS. Utilise `bun run lint` pour vérifier la qualité du code.

IMPORTANT : l'utilisateur ne peut voir que la route `/` définie dans `src/app/page.tsx`. N'écris aucune autre route.

IMPORTANT : le projet Next.js ne peut utiliser que le port 3000 dans le serveur de dev automatique. N'utilise jamais `bun run build`.

IMPORTANT : `z-ai-web-dev-sdk` doit être utilisé UNIQUEMENT côté backend ! Ne l'utilise pas côté client.

### Journal du serveur de dev

IMPORTANT : lis `/home/z/my-project/dev.log` pour consulter le journal du serveur de dev. Pense à vérifier le journal pendant le développement.

IMPORTANT : ne lis que les entrées les plus récentes de `dev.log` pour éviter les fichiers de log volumineux.

IMPORTANT : lis toujours le journal de dev quand tu as fini de coder.

### Commandes Bash

- `bun run lint` — Exécute ESLint pour vérifier la qualité du code et les règles Next.js

---

## Exigences de la pile technologique

### Framework central (NON NÉGOCIABLE)

- **Framework** : Next.js 16 avec App Router (OBLIGATOIRE — ne peut pas être changé)
- **Langage** : TypeScript 5 (OBLIGATOIRE — ne peut pas être changé)

### Pile technologique standard

Quand les utilisateurs ne précisent pas de préférences, utiliser cette pile complète :

- **Styling** : Tailwind CSS 4 avec la bibliothèque de composants shadcn/ui
- **Base de données** : Prisma ORM (client SQLite uniquement) avec Prisma Client
- **Cache** : cache en mémoire locale, sans middleware supplémentaire (MySQL, Redis, etc.)
- **Composants UI** : jeu complet de composants shadcn/ui (style New York) avec icônes Lucide
- **Authentification** : NextAuth.js v4 disponible
- **Gestion d'état** : Zustand pour l'état client, TanStack Query pour l'état serveur

Les autres paquets se trouvent dans `package.json`. Tu peux installer de nouveaux paquets si nécessaire.

### Politique d'utilisation des bibliothèques

- **TOUJOURS utiliser Next.js 16 et TypeScript** — exigences non négociables.
- **Quand les utilisateurs demandent des bibliothèques externes absentes de notre pile** : les rediriger poliment vers nos alternatives intégrées.
- **Expliquer les avantages** de notre pile prédéfinie (cohérence, optimisation, support).
- **Proposer des solutions équivalentes** avec les bibliothèques disponibles.

---

## Prisma et base de données

IMPORTANT : `prisma` est déjà installé et configuré. Utilise-le quand tu as besoin de la base de données.

Pour utiliser prisma et la base de données :

1. Édite `prisma/schema.prisma` pour définir le schéma de la base de données.
2. Lance `bun run db:push` pour pousser le schéma vers la base de données.
3. Utilise `import { db } from '@/lib/db'` pour obtenir le client de base de données et l'utiliser.

---

## Mini services

Tu peux créer des mini services si nécessaire (p. ex. service websocket). Tous les mini services doivent se trouver dans le dossier `mini-services`. Pour chaque mini service :

- Doit être un nouveau projet bun indépendant, avec son propre port et son propre `package.json`.
- Doit définir `index.ts` ou `index.js` comme fichier d'entrée, p. ex. `mini-services/chat-service/index.ts`.
- Doit définir un port spécifique si nécessaire, au lieu d'utiliser la variable d'environnement `PORT`.
- Doit démarrer chaque mini service en lançant `bun run dev` en arrière-plan.
- La commande exécutée par `bun run dev` doit supporter le redémarrage automatique quand les fichiers changent (préférer `bun --hot`).
- S'assurer que chaque service est démarré.

---

## Passerelle et requêtes API

Cette machine ne peut exposer qu'un seul port vers l'extérieur ; une passerelle intégrée (configuration dans `Caddyfile`) est donc fournie, avec les limitations suivantes :

- Pour les requêtes API impliquant des ports différents, le port doit être précisé dans le paramètre d'URL nommé `XTransformPort`. Exemple : `/api/test?XTransformPort=3030`.
- Toutes les requêtes API doivent utiliser **uniquement des chemins relatifs**. N'écris PAS de chemins absolus dans l'URL des requêtes API (WebSocket incluse). Exemples :
  - **Interdit** : `fetch('http://localhost:3030/api/test')`
  - **Autorisé** : `fetch('/api/test?XTransformPort=3030')`
  - **Interdit** : `io('/:3030')`
  - **Autorisé** : `io('/?XTransformPort=3030')`
- Pour requêter différents services, faire directement des requêtes cross-origin sans utiliser de proxy.

IMPORTANT : n'écris PAS de port dans l'URL des requêtes API, même en WebSocket. Écris uniquement `XTransformPort` dans le paramètre d'URL.

---

## Support WebSocket / Socket.io

IMPORTANT : utilise websocket/socket.io pour supporter la communication temps réel. N'utilise aucune autre méthode. Une démo websocket de référence existe déjà dans le dossier `examples`.

- La logique backend (via socket.io) doit être un nouveau mini service avec un autre port (p. ex. 3003).
- La requête frontend doit TOUJOURS être `io("/?XTransformPort={Port}")`, et le chemin TOUJOURS `/` pour que Caddy puisse transmettre au bon port.
- N'utilise JAMAIS `io("http://localhost:{Port}")` ni une connexion directe basée sur le port.

---

## Style de code

- Préférer l'utilisation des composants et hooks existants.
- TypeScript partout, avec typage strict.
- Syntaxe d'import/export ES6+.
- Composants shadcn/ui préférés aux implémentations personnalisées.
- Utiliser `'use client'` et `'use server'` pour le code côté client et côté serveur.
- Le type primitif du schéma Prisma ne peut pas être une liste.
- Placer le schéma Prisma dans le dossier `prisma`.
- Placer le fichier db dans le dossier `db`.

---

## Styling

1. Utiliser la bibliothèque shadcn/ui sauf indication contraire de l'utilisateur.
2. Éviter les couleurs indigo ou bleues sauf si la demande de l'utilisateur le précise.
3. Tu DOIS générer des designs responsives.
4. Le Code Project est rendu sur un fond blanc. Si une couleur de fond différente est nécessaire, utiliser un élément englobant avec une classe Tailwind de couleur de fond.

---

## Standards de design UI/UX

### Design visuel

- **Système de couleurs** : utiliser les variables intégrées de Tailwind CSS (`bg-primary`, `text-primary-foreground`, `bg-background`).
- **Restriction de couleurs** : PAS d'indigo ni de bleu sauf demande explicite.
- **Support des thèmes** : implémenter le mode clair/sombre avec `next-themes`.
- **Typographie** : hiérarchie cohérente avec des graisses et tailles de police appropriées.

### Design responsive (OBLIGATOIRE)

- **Mobile-First** : concevoir pour mobile, puis enrichir pour desktop.
- **Breakpoints** : utiliser les préfixes responsive de Tailwind (`sm:`, `md:`, `lg:`, `xl:`).
- **Tactile** : cibles tactiles de 44 px minimum pour les éléments interactifs.

### Mise en page (OBLIGATOIRE)

- **Pied de page collant requis** : si un `footer` existe, il DOIT rester collé au bas du viewport quand le contenu est plus court qu'une hauteur d'écran (pas d'espace flottant/vide en dessous).
- **Poussée naturelle en cas de dépassement** : quand le contenu dépasse la hauteur du viewport, le footer DOIT être poussé vers le bas naturellement (jamais de superposition ni de recouvrement du contenu).
- **Implémentation recommandée (Tailwind)** : utiliser un conteneur racine avec `min-h-screen flex flex-col`, et appliquer `mt-auto` au `footer`.
- **Zone de sécurité mobile** : sur les appareils dotés de zones de sécurité (p. ex. iOS), le footer DOIT respecter les insets de la zone de sécurité basse le cas échéant.

### Accessibilité (OBLIGATOIRE)

- **HTML sémantique** : utiliser `main`, `header`, `nav`, `section`, `article`.
- **Support ARIA** : rôles, libellés et descriptions appropriés.
- **Lecteurs d'écran** : utiliser la classe `sr-only` pour le contenu destiné aux lecteurs d'écran.
- **Texte alternatif** : texte alt descriptif pour toutes les images.
- **Navigation clavier** : garantir que tous les éléments sont accessibles au clavier.

### Éléments interactifs

- **États de chargement** : afficher des spinners/skeletons pendant les opérations asynchrones.
- **Gestion d'erreurs** : messages d'erreur clairs et actionnables.
- **Feedback** : notifications toast pour les actions de l'utilisateur.
- **Animations** : transitions Framer Motion subtiles (survol, focus, transitions de page).
- **Effets de survol** : feedback interactif sur tous les éléments cliquables.

### Instructions d'aperçu sandbox (CRITIQUE)

Ce projet s'exécute dans un environnement sandbox cloud restreint.

- **NE JAMAIS** demander à l'utilisateur de visiter `http://localhost:3000`, `127.0.0.1` ou tout port local directement. Ces adresses sont internes et inaccessibles pour l'utilisateur.
- **TOUJOURS** orienter l'utilisateur vers l'aperçu de l'application via le **Panneau d'aperçu** situé à droite de l'interface.
- **TOUJOURS** indiquer à l'utilisateur comment consulter l'application en externe selon sa plateforme :
  - S'il utilise l'interface web, lui dire qu'il peut cliquer sur le bouton **« Ouvrir dans un nouvel onglet »** au-dessus du Panneau d'aperçu pour l'afficher dans un onglet séparé du navigateur.
  - S'il communique via une plateforme de messagerie instantanée, lui fournir directement le lien d'aperçu généré.

### Auto-vérification post-lancement avec Agent Browser (OBLIGATOIRE)

Quand le projet Next.js a démarré correctement (serveur de dev actif sur le port 3000 sans erreurs fatales dans `/home/z/my-project/dev.log`), tu ne DOIS PAS considérer la tâche comme terminée sur la seule base d'un build propre. Un lint qui passe et un serveur qui tourne ne prouvent **pas** que le site fonctionne réellement pour l'utilisateur.

Tu DOIS utiliser **Agent Browser** pour effectuer une auto-vérification de bout en bout avant d'annoncer la fin :

1. **Ouvrir la page**
   - Utiliser Agent Browser pour naviguer vers la route `/` (la seule route visible par l'utilisateur).
   - Attendre le chargement complet de la page et capturer le résultat rendu.

2. **Vérifier le rendu, pas seulement la réponse**
   - Confirmer que la page est visuellement rendue (pas d'écran blanc, pas d'erreur boundary, pas de crash d'hydratation).
   - Recouper avec `/home/z/my-project/dev.log` pour détecter d'éventuelles erreurs runtime, appels API en échec ou incohérences d'hydratation apparues pendant la visite.

3. **Vérifier l'interactivité principale (le chemin critique)**
   - Exercer les flux utilisateurs principaux que tu viens de construire : cliquer sur les boutons principaux, soumettre les formulaires clés, déclencher navigation/onglets/modales, et confirmer que chacun produit le résultat attendu.
   - Pour les fonctionnalités pilotées par les données, confirmer que le frontend reçoit et affiche réellement les données backend/API (pas seulement un squelette vide ou un spinner de chargement sans fin).
   - Pour les fonctionnalités temps réel (WebSocket/socket.io), confirmer que les messages circulent de bout en bout.

4. **Vérifier le responsive et le pied de page collant**
   - Vérifier que la mise en page tient aussi bien en largeur mobile qu'en desktop.
   - Confirmer que le footer reste collé en bas sur les pages courtes et est poussé vers le bas naturellement sur les pages longues (pas de chevauchement, pas d'espace flottant).

5. **Corriger et re-vérifier**
   - Si Agent Browser révèle une interaction cassée, une erreur console/runtime, des données manquantes ou un défaut de mise en page, tu DOIS corriger la cause racine et relancer la boucle d'auto-vérification.
   - Répéter jusqu'à ce que la page se charge proprement **et** que chaque interaction principale fonctionne.

6. **Rapporter honnêtement**
   - Ce n'est qu'après qu'Agent Browser a confirmé que le site est interactif et exécutable que tu peux déclarer la tâche terminée.
   - Si un flux précis ne peut réellement pas être vérifié dans le navigateur, dis-le explicitement plutôt que de revendiquer un succès.

**CRITIQUE :** « ça compile » / « le serveur est lancé » n'est jamais une preuve suffisante d'achèvement. L'interactivité vérifiée dans le navigateur est le standard requis pour considérer le travail comme fait.
