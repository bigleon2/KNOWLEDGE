# Checklist de validation — bibliothèque multi-IA @processus

Avant de déclarer un livrable terminé sur une plateforme :

- [ ] Le processus invoqué existe dans `core/processus.md` (pas d'invention) ;
- [ ] La sortie est en français ;
- [ ] L'exécution est idempotente (re-jeu = pas de duplication) ;
- [ ] Aucun secret/identifiant dans la sortie (KO-L009) ;
- [ ] Tout script produit est Python stdlib uniquement (N3) ;
- [ ] Le livrable correspond à la spécification du core (pas de variante
      locale non documentée) ;
- [ ] Si l'écosystème KNOWLEDGE est accessible : le processus a délégué au
      skill écosystème correspondant (table du core) plutôt que de réimplémenter.
