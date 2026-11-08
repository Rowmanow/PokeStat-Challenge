# PokéStat Challenge

PokéStat Challenge est un jeu de statistiques Pokémon disponible sur **Android** et **Windows**.

Deux modes de jeu sont inclus :

- **Stat Draft**
- **Stat Guesser**

L’application est disponible en français et en anglais.

---

## Télécharger PokéStat Challenge

### Android, version 1.0.3

**[Télécharger PokéStat Challenge pour Android](https://github.com/Rowmanow/PokeStat-Challenge/releases/tag/v1.0.3)**

Fichier à télécharger :

```text
PokeStat-Challenge-1.0.3.apk
```

La version Android 1.0.3 utilise la même signature que la version 1.0.0. Elle peut être installée directement par-dessus l’ancienne version, sans désinstallation.

### Windows

**[Télécharger la dernière version Windows](https://github.com/Rowmanow/PokeStat-Challenge/releases/latest)**

Fichier à télécharger :

```text
Pokestat-Challenge-Windows.zip
```

L’archive Windows contient deux interfaces utilisant les mêmes modes de jeu :

- une interface verticale, adaptée aux écrans étroits, à TikTok et aux YouTube Shorts ;
- une interface PC horizontale, adaptée aux écrans classiques, à YouTube et à OBS Studio.

> N’utilisez pas les archives automatiques `Source code (zip)` et `Source code (tar.gz)` pour installer le jeu. Elles contiennent le code source du dépôt et non l’archive Windows préparée pour le lancement.

---

## Installation sur Android

1. Ouvrez la [page de téléchargement Android 1.0.3](https://github.com/Rowmanow/PokeStat-Challenge/releases/tag/v1.0.3).
2. Téléchargez `PokeStat-Challenge-1.0.3.apk`.
3. Ouvrez le fichier APK sur votre téléphone.
4. Si Android le demande, autorisez temporairement l’installation depuis votre navigateur ou votre gestionnaire de fichiers.
5. Appuyez sur **Mettre à jour** si une ancienne version est déjà installée.
6. Appuyez sur **Installer** si aucune version précédente n’est présente.
7. Lancez PokéStat Challenge depuis l’écran d’accueil.

Une connexion Internet est nécessaire pour récupérer certaines données et illustrations Pokémon.

Les données déjà téléchargées sont conservées dans le cache local afin d’accélérer les chargements suivants.

---

## Installation sur Windows

### Prérequis

- Windows 10 ou Windows 11
- Python 3.10 ou une version plus récente
- Une connexion Internet lors du premier chargement de certaines données

### Télécharger et extraire le jeu

1. Ouvrez la [page de la dernière version Windows](https://github.com/Rowmanow/PokeStat-Challenge/releases/latest).
2. Téléchargez `Pokestat-Challenge-Windows.zip`.
3. Faites un clic droit sur l’archive.
4. Sélectionnez **Extraire tout**.
5. Ouvrez le dossier `Pokestat-Challenge-Windows` obtenu après extraction.

> Ne lancez pas le jeu directement depuis l’archive ZIP. Tous les fichiers doivent d’abord être extraits.

### Installer les dépendances

Dans le dossier extrait :

1. Cliquez dans la barre d’adresse de l’Explorateur de fichiers.
2. Saisissez `powershell`.
3. Appuyez sur Entrée.
4. Exécutez :

```powershell
py -3 -m pip install -r requirements.txt
```

### Choisir une interface

#### Interface verticale

Double-cliquez sur :

```text
Pokestat-Challenge-Vertical.vbs
```

Cette interface est adaptée :

- aux écrans verticaux ;
- aux petits écrans ;
- à TikTok ;
- aux YouTube Shorts ;
- à une utilisation sur un écran secondaire.

#### Interface PC

Double-cliquez sur :

```text
Pokestat-Challenge-PC.vbs
```

Cette interface est adaptée :

- aux écrans classiques ;
- au format 1280 × 720 ;
- au format 1920 × 1080 ;
- aux vidéos YouTube ;
- à OBS Studio ;
- à l’utilisation d’une webcam.

### Raccourcis de l’interface PC

```text
F11     Activer ou quitter le plein écran
Échap   Quitter le plein écran
```

### Zone webcam

L’interface PC réserve une zone fixe en haut à droite de chaque écran.

Deux formats sont disponibles :

- **4:3**
- **16:9**

La zone reste au même emplacement sur :

- l’accueil ;
- le Stat Draft ;
- le Stat Guesser ;
- le récapitulatif du Draft.

Vous pouvez placer une source webcam par-dessus cette zone dans OBS Studio sans devoir la déplacer lors d’un changement d’écran.

### Journaux d’erreur

Si le lancement échoue, un fichier de diagnostic est créé dans le dossier du jeu :

```text
erreur_lancement.txt
```

ou :

```text
erreur_lancement_pc.txt
```

---

## Modes de jeu

### Stat Draft

Composez une équipe de six Pokémon en attribuant une statistique différente à chacun.

Les valeurs sont masquées avant votre choix. Chaque catégorie ne peut être utilisée qu’une seule fois pendant la partie.

Les six statistiques disponibles sont :

- PV
- Attaque
- Défense
- Attaque Spéciale
- Défense Spéciale
- Vitesse

### Objectif du Draft

La valeur de l’objectif peut être saisie manuellement.

Un bouton **ALÉA** permet également de générer un nombre entier aléatoire entre :

```text
250 et 750
```

Le résultat peut ensuite être modifié manuellement.

### Modes du Draft

Trois modes sont disponibles.

#### Au-dessus

Le score final doit être supérieur ou égal à l’objectif.

#### En dessous

Le score final doit être inférieur ou égal à l’objectif.

#### Au plus proche de

Le but est de terminer aussi près que possible de l’objectif.

La victoire est accordée lorsque l’écart entre le score final et l’objectif est inférieur ou égal à 20.

Exemple avec un objectif de 600 :

```text
De 580 à 620 inclus : victoire
579 ou moins : défaite
621 ou plus : défaite
```

### Récapitulatif du Draft

À la fin de la partie, un récapitulatif compare votre équipe à la meilleure répartition possible :

- meilleur total en mode **Au-dessus** ;
- total minimum en mode **En dessous** ;
- total le plus proche de l’objectif en mode **Au plus proche de**.

Le calcul teste toutes les répartitions valides des six statistiques entre les six Pokémon.

### Stat Guesser

Retrouvez les six statistiques de base du Pokémon en un nombre limité de tentatives.

Après chaque essai :

- une proposition trop basse met à jour la borne basse ;
- une proposition trop haute met à jour la borne haute ;
- une valeur exacte verrouille la statistique.

Les statistiques à retrouver sont :

- PV
- Attaque
- Attaque Spéciale
- Défense
- Défense Spéciale
- Vitesse

Le nombre de tentatives peut être personnalisé avant le début de la partie.

La victoire ou la défaite est affichée directement dans l’interface.

---

## Filtres

Les filtres permettent de personnaliser les Pokémon pouvant apparaître dans une partie.

### Types

Vous pouvez sélectionner un ou plusieurs types Pokémon.

Lorsque plusieurs types sont sélectionnés, les Pokémon correspondant à au moins l’un des types autorisés peuvent apparaître.

### Générations

Vous pouvez sélectionner une ou plusieurs générations.

### Formes sur Windows

Les interfaces Windows proposent les choix suivants :

- **Formes standards uniquement**
- **Méga-Évolutions uniquement**
- **Standard + Méga-Évolutions**

Les filtres de types, de générations et de formes peuvent être combinés.

Exemple :

```text
Type : Spectre
Générations : Toutes
Formes : Méga uniquement
```

### Formes sur Android

La version Android propose trois catégories :

- **Standards**
- **Méga**
- **Régionales**

Le filtre Régionales regroupe :

- les formes d’Alola ;
- les formes de Galar ;
- les formes de Hisui ;
- les formes de Paldea.

Les catégories peuvent être combinées librement.

---

## Fonctionnalités principales

### Fonctionnalités communes

- Interface en français et en anglais
- Stat Draft
- Stat Guesser
- Filtres par type
- Filtres par génération
- Pokémon standards
- Méga-Évolutions
- Nombre de tentatives personnalisable dans le Guesser
- Calcul de la composition optimale dans le Draft
- Cache local des données et illustrations
- Illustrations Pokémon haute définition

### Fonctionnalités du Draft

- Mode Au-dessus
- Mode En dessous
- Mode Au plus proche de
- Victoire à 20 points ou moins de l’objectif
- Objectif saisissable manuellement
- Objectif aléatoire entre 250 et 750
- Filtre Standard et Méga
- Récapitulatif détaillé

### Fonctionnalités Windows

- Interface verticale
- Interface PC horizontale
- Résolution PC adaptée au 1280 × 720
- Fenêtre redimensionnable
- Plein écran
- Zone webcam fixe
- Formats webcam 4:3 et 16:9
- Emplacement webcam identique sur tous les écrans
- Lanceurs silencieux Windows

### Fonctionnalités Android

- Interface tactile
- APK signé
- Mise à jour directe depuis une ancienne version compatible
- Filtre de formes régionales
- Formes d’Alola, de Galar, de Hisui et de Paldea

---

## Vérifier l’archive Windows

GitHub affiche automatiquement un condensat SHA-256 à côté de l’archive de la Release.

Lorsqu’un fichier `.sha256` est également fourni, vous pouvez vérifier l’intégrité de l’archive avec PowerShell :

```powershell
$expected = (
    Get-Content ".\Pokestat-Challenge-Windows.zip.sha256"
).Split()[0]

$actual = (
    Get-FileHash ".\Pokestat-Challenge-Windows.zip" -Algorithm SHA256
).Hash.ToLower()

$actual -eq $expected
```

Le résultat attendu est :

```text
True
```

---

## English

PokéStat Challenge is a Pokémon statistics game available on **Android** and **Windows**.

The application includes two game modes:

- **Stat Draft**
- **Stat Guesser**

The interface is available in French and English.

### Download for Android

**[Download PokéStat Challenge for Android](https://github.com/Rowmanow/PokeStat-Challenge/releases/tag/v1.0.3)**

Download:

```text
PokeStat-Challenge-1.0.3.apk
```

### Download for Windows

**[Download the latest Windows release](https://github.com/Rowmanow/PokeStat-Challenge/releases/latest)**

Download:

```text
Pokestat-Challenge-Windows.zip
```

> Do not use the automatic `Source code (zip)` or `Source code (tar.gz)` archives to install the Windows version.

### Windows interfaces

The Windows archive contains two interfaces.

#### Vertical interface

Launch:

```text
Pokestat-Challenge-Vertical.vbs
```

Designed for vertical screens, TikTok and YouTube Shorts.

#### PC interface

Launch:

```text
Pokestat-Challenge-PC.vbs
```

Designed for conventional displays, YouTube recording and OBS Studio.

The PC interface includes:

- a 1280 × 720 layout;
- resizable windows;
- fullscreen support;
- a fixed webcam area;
- 4:3 and 16:9 webcam formats;
- the same webcam position on every screen.

### Windows installation

1. Download `Pokestat-Challenge-Windows.zip`.
2. Extract the archive completely.
3. Open PowerShell in the extracted folder.
4. Run:

```powershell
py -3 -m pip install -r requirements.txt
```

5. Launch the preferred VBS file.

### Stat Draft

Assign one different stat to each of six Pokémon.

Three modes are available:

- **Above**
- **Below**
- **Closest to**

In Closest mode, victory is awarded when the final total is within 20 points of the target.

A **RANDOM** button generates any integer target between 250 and 750.

The target can still be edited manually.

At the end of the game, the recap compares the player’s choices with the optimal assignment.

### Stat Guesser

Find all six Base Stats using the lower and upper bounds.

The number of attempts can be customized before starting a game.

Filters are available for:

- types;
- generations;
- standard forms;
- Mega Evolutions.

---

## Aperçu Android

<p align="center">
  <img src="screenshots/Android-Accueil.jpg" alt="Accueil Android" width="23%">
  <img src="screenshots/Android-Draft.jpg" alt="Stat Draft Android" width="23%">
  <img src="screenshots/Android-Recapitulatif.jpg" alt="Récapitulatif Android" width="23%">
  <img src="screenshots/Android-Guesser.jpg" alt="Stat Guesser Android" width="23%">
</p>

## Aperçu Windows

<p align="center">
  <img src="screenshots/Windows-Accueil.png" alt="Accueil Windows" width="23%">
  <img src="screenshots/Windows-Draft.png" alt="Stat Draft Windows" width="23%">
  <img src="screenshots/Windows-Recapitulatif.png" alt="Récapitulatif Windows" width="23%">
  <img src="screenshots/Windows-Guesser.png" alt="Stat Guesser Windows" width="23%">
</p>

> Les captures Windows peuvent être complétées ultérieurement avec des images séparées de l’interface verticale et de l’interface PC.

---

## Signaler un problème

Utilisez l’onglet Issues du dépôt :

**https://github.com/Rowmanow/PokeStat-Challenge/issues/new/choose**

Merci de préciser :

- le modèle du téléphone ou de l’ordinateur ;
- le système d’exploitation ;
- la version Android ou Windows ;
- la langue utilisée ;
- l’interface Windows utilisée, verticale ou PC ;
- le mode de jeu concerné ;
- les filtres sélectionnés ;
- les étapes permettant de reproduire le problème ;
- une capture d’écran si possible.

---

## Confidentialité

PokéStat Challenge ne demande pas de compte utilisateur et ne collecte pas volontairement de données personnelles.

Certaines données et illustrations nécessaires au jeu sont téléchargées puis conservées dans le cache local de l’application.

Consultez la [politique de confidentialité](PRIVACY.md).

---

## Avertissement

PokéStat Challenge est un projet communautaire gratuit et non officiel.

Pokémon et les noms associés appartiennent à leurs ayants droit respectifs.

Ce projet n’est ni affilié, ni approuvé, ni sponsorisé par Nintendo, Game Freak ou The Pokémon Company.

---

## Licence

Aucune licence open source n’est accordée pour le moment.

Le code est visible à des fins de test et d’évaluation.

Consultez [LICENSE.md](LICENSE.md).
