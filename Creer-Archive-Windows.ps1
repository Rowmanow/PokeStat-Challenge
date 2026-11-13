param(
    [string]$ProjectRoot = (Split-Path -Parent $MyInvocation.MyCommand.Path)
)

$ErrorActionPreference = "Stop"

$WindowsDir = Join-Path $ProjectRoot "windows"
$ReleaseDir = Join-Path $ProjectRoot "release"
$PackageRoot = Join-Path $ReleaseDir "Pokestat-Challenge-Windows"
$ZipPath = Join-Path $ReleaseDir "Pokestat-Challenge-Windows.zip"

$RequiredFiles = @(
    "accueil.py",
    "accueil_pc.py",
    "affichage_pc.py",
    "mode_draft.py",
    "mode_draft_pc.py",
    "mode_guesser.py",
    "mode_guesser_pc.py",
    "Pokestat-Challenge-Vertical.vbs",
    "Pokestat-Challenge-PC.vbs"
)

Write-Host "Verification du dossier Windows..." -ForegroundColor Cyan

if (-not (Test-Path $WindowsDir)) {
    throw "Le dossier windows est introuvable : $WindowsDir"
}

foreach ($File in $RequiredFiles) {
    $Path = Join-Path $WindowsDir $File
    if (-not (Test-Path $Path)) {
        throw "Fichier obligatoire manquant : $Path"
    }
}

$LogoPath = Join-Path $WindowsDir "assets\pokemon_logo.png"
if (-not (Test-Path $LogoPath)) {
    throw "Logo obligatoire manquant : $LogoPath"
}

Write-Host "Verification de la syntaxe Python..." -ForegroundColor Cyan
$PythonFiles = $RequiredFiles | Where-Object { $_ -like "*.py" } | ForEach-Object {
    Join-Path $WindowsDir $_
}

& py -3 -m py_compile @PythonFiles
if ($LASTEXITCODE -ne 0) {
    throw "La verification Python a echoue. L'archive n'a pas ete creee."
}

Write-Host "Preparation de l'archive..." -ForegroundColor Cyan

if (Test-Path $PackageRoot) {
    Remove-Item $PackageRoot -Recurse -Force
}
if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
}

New-Item -ItemType Directory -Path $PackageRoot -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $PackageRoot "assets") -Force | Out-Null

foreach ($File in $RequiredFiles) {
    Copy-Item (Join-Path $WindowsDir $File) (Join-Path $PackageRoot $File) -Force
}

Copy-Item $LogoPath (Join-Path $PackageRoot "assets\pokemon_logo.png") -Force

@'
Pillow>=10.0
'@ | Set-Content -Path (Join-Path $PackageRoot "requirements.txt") -Encoding UTF8

@'
POKESTAT CHALLENGE - VERSION WINDOWS

Cette archive contient deux interfaces :

1. Pokestat-Challenge-Vertical.vbs
   Interface verticale adaptee aux ecrans etroits, TikTok et YouTube Shorts.

2. Pokestat-Challenge-PC.vbs
   Interface horizontale 1280 x 720 adaptee a YouTube et OBS Studio.
   La zone webcam peut etre affichee en 4:3 ou en 16:9.

PRE-REQUIS
- Windows 10 ou Windows 11
- Python 3
- Pillow

INSTALLATION DE PILLOW
Ouvrez PowerShell dans ce dossier puis executez :

py -3 -m pip install -r requirements.txt

LANCEMENT
Double-cliquez sur le lanceur souhaite :
- Pokestat-Challenge-Vertical.vbs
- Pokestat-Challenge-PC.vbs

PREMIER DEMARRAGE
Une connexion Internet est requise pour recuperer les donnees et illustrations Pokemon.
Le dossier cache sera cree automatiquement et restera local.

INTERFACE PC
- F11 : activer ou quitter le plein ecran
- Echap : quitter le plein ecran
- Emplacement webcam fixe en haut a droite
- Formats webcam 4:3 et 16:9

PROJET NON OFFICIEL
PokeStat Challenge est un projet de fan gratuit et non officiel.
Pokemon et les noms associes appartiennent a leurs proprietaires respectifs.
Les donnees utilisees proviennent de PokeAPI.
'@ | Set-Content -Path (Join-Path $PackageRoot "LISEZ-MOI.txt") -Encoding UTF8

Write-Host "Creation du fichier ZIP..." -ForegroundColor Cyan
Compress-Archive -Path $PackageRoot -DestinationPath $ZipPath -CompressionLevel Optimal -Force

Write-Host "Verification du contenu..." -ForegroundColor Cyan
Add-Type -AssemblyName System.IO.Compression.FileSystem
$Zip = [System.IO.Compression.ZipFile]::OpenRead($ZipPath)
try {
    $EntryNames = $Zip.Entries | ForEach-Object { $_.FullName.Replace('\','/') }

    foreach ($File in $RequiredFiles) {
        $Expected = "Pokestat-Challenge-Windows/$File"
        if ($EntryNames -notcontains $Expected) {
            throw "Fichier absent de l'archive : $Expected"
        }
    }

    $Forbidden = @("__pycache__", "/cache/", "/save/", "erreur_lancement")
    foreach ($Entry in $EntryNames) {
        foreach ($Pattern in $Forbidden) {
            if ($Entry -like "*$Pattern*") {
                throw "Element local interdit dans l'archive : $Entry"
            }
        }
    }
}
finally {
    $Zip.Dispose()
}

$SizeMB = [Math]::Round((Get-Item $ZipPath).Length / 1MB, 2)
Write-Host "" 
Write-Host "Archive creee avec succes :" -ForegroundColor Green
Write-Host $ZipPath -ForegroundColor Yellow
Write-Host "Taille : $SizeMB Mo"
Write-Host "" 
Write-Host "Cette archive peut maintenant etre jointe a une GitHub Release." -ForegroundColor Green
