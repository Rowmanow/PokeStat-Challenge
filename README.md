# PokéStat Challenge

Jeu de statistiques Pokémon disponible sur **Android** et **Windows**, avec deux modes de jeu : **Stat Draft** et **Stat Guesser**.

L’application est disponible en français et en anglais.

## Télécharger PokéStat Challenge

### Android, version 1.0.3

**[Télécharger PokéStat Challenge pour Android](https://github.com/Rowmanow/PokeStat-Challenge/releases/tag/v1.0.3)**

Fichier à télécharger :

```text
PokeStat-Challenge-1.0.3.apk
```

La version Android 1.0.3 peut être installée directement par-dessus la version 1.0.0, sans désinstaller l’application.

### Windows, version 1.0.0

**[Télécharger PokéStat Challenge pour Windows](https://github.com/Rowmanow/PokeStat-Challenge/releases/tag/v1.0.0)**

Fichier à télécharger :

```text
PokeStat-Challenge-Windows-v1.0.0.zip
```

> N’utilisez pas les archives automatiques `Source code (zip)` et `Source code (tar.gz)`. Elles contiennent le code source et ne correspondent pas aux versions prêtes à lancer.

---

## Nouveautés de la version Android 1.0.3

- Ajout du mode Draft **Le plus proche**
- Victoire lorsque le score final se trouve à **20 points ou moins de l’objectif**
- Ajout des Méga-Évolutions de **Pokémon Légendes : Z-A**
- Prise en charge des formes Méga **X, Y et Z**
- Nouveau filtre de formes :
  - Standards
  - Méga
  - Régionales
- Le filtre **Régionales** regroupe les formes d’Alola, de Galar, de Hisui et de Paldea
- Mise à jour du numéro de version affiché sur l’accueil

### Évolutions intégrées depuis la version 1.0.0

- **Version 1.0.1** : ajout de la règle **Le plus proche** dans le mode Draft
- **Version 1.0.2** : ajout des Méga-Évolutions introduites dans Pokémon Légendes : Z-A
- **Version 1.0.3** : regroupement des formes d’Alola, de Galar, de Hisui et de Paldea dans un filtre unique nommé **Régionales**

---

## Installation sur Android

1. Ouvrez la [page de téléchargement de la version Android 1.0.3](https://github.com/Rowmanow/PokeStat-Challenge/releases/tag/v1.0.3).
2. Téléchargez `PokeStat-Challenge-1.0.3.apk`.
3. Ouvrez le fichier APK sur votre téléphone.
4. Si Android le demande, autorisez temporairement l’installation depuis votre navigateur ou votre gestionnaire de fichiers.
5. Appuyez sur **Mettre à jour** si la version 1.0.0 est déjà installée.
6. Appuyez sur **Installer** si aucune version précédente n’est présente.
7. Lancez **PokéStat Challenge** depuis l’écran d’accueil.

La version 1.0.3 utilise la même signature que la version 1.0.0. Elle peut donc être installée directement par-dessus l’ancienne version, sans désinstallation.

Une connexion Internet est nécessaire pour récupérer les données et les illustrations des Pokémon. Les données déjà téléchargées sont conservées dans le cache local afin d’accélérer les chargements suivants.

---

## Installation sur Windows

### Prérequis

- Windows 10 ou Windows 11
- Python 3.10 ou une version plus récente
- Une connexion Internet lors du premier chargement de certaines données

### Installation

1. Ouvrez la [page de téléchargement de la version Windows 1.0.0](https://github.com/Rowmanow/PokeStat-Challenge/releases/tag/v1.0.0).
2. Téléchargez `PokeStat-Challenge-Windows-v1.0.0.zip`.
3. Faites un clic droit sur l’archive téléchargée.
4. Sélectionnez **Extraire tout**.
5. Ouvrez le dossier extrait.

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

### Lancer le jeu

Double-cliquez ensuite sur :

```text
Pokestat-Challenge.vbs
```

Le lanceur démarre le jeu sans conserver de fenêtre de terminal à l’écran.

Vous pouvez également lancer l’application manuellement :

```powershell
py -3 accueil.py
```

Si le lancement échoue, un fichier `erreur_lancement.txt` sera créé dans le dossier du jeu.

---

## Modes de jeu

### Stat Draft

Composez une équipe de six Pokémon en attribuant une statistique différente à chacun.

Les valeurs sont masquées avant votre choix. Chaque catégorie statistique ne peut être utilisée qu’une seule fois pendant la partie.

Les six statistiques disponibles sont :

- PV
- Attaque
- Défense
- Attaque Spéciale
- Défense Spéciale
- Vitesse

Trois objectifs sont disponibles.

#### Au-dessus

Le score final doit être supérieur ou égal à l’objectif.

#### En dessous

Le score final doit être inférieur ou égal à l’objectif.

#### Le plus proche

Le but est de terminer aussi près que possible de l’objectif.

La victoire est accordée lorsque l’écart entre le score final et l’objectif est inférieur ou égal à 20.

Exemple avec un objectif de 600 :

```text
De 580 à 620 inclus : victoire
579 ou moins : défaite
621 ou plus : défaite
```

À la fin de la partie, un récapitulatif compare votre équipe à la meilleure répartition possible :

- meilleur total en mode **Au-dessus**
- total minimum en mode **En dessous**
- total le plus proche de l’objectif en mode **Le plus proche**

### Stat Guesser

Retrouvez les six statistiques de base du Pokémon en un nombre limité de tentatives.

Après chaque essai, les bornes minimales et maximales sont actualisées pour guider les tentatives suivantes.

Le nombre de tentatives peut être personnalisé avant de commencer.

---

## Filtres

Les filtres permettent de personnaliser les Pokémon pouvant apparaître dans une partie.

### Types

Vous pouvez sélectionner un ou plusieurs types Pokémon.

Lorsque plusieurs types sont sélectionnés, les Pokémon correspondant à au moins l’un des types autorisés peuvent apparaître.

### Générations

Vous pouvez sélectionner une ou plusieurs générations.

### Formes

Trois catégories sont disponibles :

- **Standards**
- **Méga**
- **Régionales**

Les catégories peuvent être combinées librement.

### Standards

Cette catégorie contient les formes standards des Pokémon.

### Méga

Cette catégorie comprend notamment :

- les Méga-Évolutions classiques
- les nouvelles Méga-Évolutions de Pokémon Légendes : Z-A
- les variantes Méga X, Y et Z

### Régionales

Cette catégorie regroupe :

- les formes d’Alola
- les formes de Galar
- les formes de Hisui
- les formes de Paldea

Exemple pour un défi uniquement composé de formes régionales :

```text
Standards : désactivé
Méga : désactivé
Régionales : activé
```

Exemple pour autoriser toutes les formes :

```text
Standards : activé
Méga : activé
Régionales : activé
```

---

## Fonctionnalités

- Interface en français et en anglais
- Deux modes de jeu : Stat Draft et Stat Guesser
- Trois objectifs dans le Draft : Au-dessus, En dessous et Le plus proche
- Victoire à 20 points ou moins de l’objectif en mode Le plus proche
- Filtres par types et générations
- Filtres Standards, Méga et Régionales
- Pokémon standards et Méga-Évolutions
- Méga-Évolutions de Pokémon Légendes : Z-A
- Prise en charge des formes Méga X, Y et Z
- Formes d’Alola, de Galar, de Hisui et de Paldea
- Tirage uniforme parmi les candidats autorisés
- Nombre de tentatives personnalisable dans le Guesser
- Calcul du combo optimal parmi les six Pokémon
- Cache local pour accélérer les chargements suivants
- Interface tactile sur Android
- Lanceur silencieux sur Windows
- APK Android signé permettant la mise à jour depuis la version 1.0.0

---

## English

PokéStat Challenge is a Pokémon statistics game available on **Android** and **Windows**.

The application includes two game modes: **Stat Draft** and **Stat Guesser**.

The interface is available in both French and English.

### Download for Android

**[Download PokéStat Challenge Mobile v1.0.3](https://github.com/Rowmanow/PokeStat-Challenge/releases/tag/v1.0.3)**

Download this file:

```text
PokeStat-Challenge-1.0.3.apk
```

### Download for Windows

**[Downloadhub.com/Rowmanow/PokeStat-Challenge/releases/tag/v1.0.0)**

Download this file:

```text
PokeStat-Challenge-Windows-v1.0.0.zip
```

> Do not download the automatic `Source code (zip)` or `Source code (tar.gz)` archives. They contain the source code and are not ready-to-run versions.

### What’s new in Android v1.0.3

- Added the **Closest** Draft mode
- Victory is awarded when the final score is within **20 points of the target**
- Added the new Mega Evolutions introduced in **Pokémon Legends: Z-A**
- Added support for Mega **X, Y and Z** forms
- New form filters:
  - Standard
  - Mega
  - Regional
- The **Regional** filter groups the Alolan, Galarian, Hisuian and Paldean forms
- Updated the version number displayed on the home screen

### Updating from Android v1.0.0

Version 1.0.3 uses the same signing certificate as version 1.0.0.

Version 1.0.3 can therefore be installed directly over version 1.0.0 without uninstalling the application.

### Android installation

1. Open the [Android v1.0.3 download page](https://github.com/Rowmanow/PokeStat-Challenge/releases/tag/v1.0.0).
2. Download `PokeStat-Challenge-1.0.3.apk`.
3. Open the APK file on your Android device.
4. Allow installation from this source if Android asks for permission.
5. Tap **Update** if version 1.0.0 is already installed.
6. Tap **Install** if no previous version is installed.

An Internet connection is required to download Pokémon data and artwork.

Previously downloaded data is stored in the local cache to speed up future loading.

### Draft modes

Three Draft objectives are available:

- **Above**: finish with a score greater than or equal to the target
- **Below**: finish with a score lower than or equal to the target
- **Closest**: finish as close as possible to the target

In Closest mode, victory is awarded when the final difference is 20 points or less.

Example with a target of 600:

```text
580 to 620 included: victory
579 or lower: defeat
621 or higher: defeat
```

### Form filters

Three form categories are available:

- **Standard**
- **Mega**
- **Regional**

The Regional filter groups:

- Alolan forms
- Galarian forms
- Hisuian forms
- Paldean forms

The Mega filter includes the classic Mega Evolutions and the new X, Y and Z forms introduced in Pokémon Legends: Z-A.

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

---

## Signaler un problème

Utilisez l’onglet **Issues** du dépôt :

**https://github.com/Rowmanow/PokeStat-Challenge/issues/new/choose**

Merci de préciser :

- le modèle du téléphone ou de l’ordinateur
- la version Android ou Windows
- la version de PokéStat Challenge
- la langue utilisée
- le mode de jeu concerné
- les filtres sélectionnés
- les étapes permettant de reproduire le problème
- une capture d’écran si possible

---

## Confidentialité

PokéStat Challenge ne demande pas de compte utilisateur et ne collecte pas volontairement de données personnelles.

Certaines données et illustrations nécessaires au jeu sont téléchargées puis conservées dans le cache local de l’application.

Consultez la [politique de confidentialité](PRIVACY.md).

---

## Avertissement

PokéStat Challenge est un projet communautaire non officiel.

Pokémon et les noms associés appartiennent à leurs ayants droit respectifs. Ce projet n’est ni affilié, ni approuvé, ni sponsorisé par Nintendo, Game Freak ou The Pokémon Company.

## Licence

Aucune licence open source n’est accordée pour le moment. Le code est visible à des fins de test et d’évaluation.

Consultez [LICENSE.md](LICENSE.md).
