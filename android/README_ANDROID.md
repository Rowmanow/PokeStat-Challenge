# PokeStat Challenge Mobile - V0.1

Cette premiere base contient l'accueil bilingue et un Stat Guesser jouable. Le Draft est affiche comme prochaine etape.

## Test sur PC
```bash
python -m pip install -r requirements.txt
python main.py
```

## Compiler sous Windows avec WSL2
Dans Ubuntu/WSL, place le projet dans le systeme Linux (par exemple `~/PokeStat-Mobile`) puis :
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip python3-venv autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev cmake libffi-dev libssl-dev
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install buildozer cython
buildozer android debug
```
L'APK apparait dans `bin/`. Le premier build peut etre long car les outils Android sont telecharges.

## Notes
- Internet est requis pour charger un Pokemon la premiere fois.
- Les reponses PokeAPI sont mises en cache dans le dossier prive de l'application.
- Les valeurs hors des bornes deja connues sont bloquees.
