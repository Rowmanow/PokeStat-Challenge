# Ajout du mode « Le plus proche » sur la version stable 1.0

Seuls `pokestat/data.py` et `pokestat/screens.py` sont modifiés.

## Nouveau mode Draft

Le bouton de mode suit désormais ce cycle :

1. Au-dessus / Above
2. En dessous / Below
3. Le plus proche / Closest

En mode « Le plus proche », la victoire est obtenue lorsque l'écart absolu entre le total final et l'objectif est inférieur ou égal à 20.

Exemple pour un objectif de 600 : victoire de 580 à 620 inclus.

Le récapitulatif calcule aussi la répartition des six statistiques qui se rapproche le plus de l'objectif.

Aucun fichier d'accueil, d'API, de Guesser ou de design n'est remplacé.
