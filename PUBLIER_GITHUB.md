# Publication GitHub

## 1. Créer le dépôt

Crée un dépôt nommé `PokeStat-Challenge`. Pour une première vérification, choisis **Private**. Ne préremplis pas le README, le `.gitignore` ou la licence.

## 2. Envoyer les fichiers

Depuis WSL, dans ce dossier :

```bash
git init
git branch -M main
git add .
git commit -m "PokeStat Challenge v1.0.0"
git remote add origin https://github.com/TON_COMPTE/PokeStat-Challenge.git
git push -u origin main
```

## 3. Créer la release

Sur GitHub :

1. Ouvre **Releases**.
2. Clique sur **Draft a new release**.
3. Crée le tag `v1.0.0`.
4. Titre : `PokeStat Challenge Android v1.0.0`.
5. Copie le contenu de `RELEASE_NOTES_v1.0.0.md`.
6. Ajoute `release/PokeStat-Challenge-Android-v1.0.0.apk`.
7. Coche **This is a pre-release** pour la première bêta publique.
8. Enregistre d'abord en brouillon, vérifie, puis publie.
