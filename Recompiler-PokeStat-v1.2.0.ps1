param(
    [string]$ProjectRoot = "E:\Projet\PokeStat-Challenge-GitHub"
)

$ErrorActionPreference = "Stop"

$WindowsDir = Join-Path $ProjectRoot "windows"
$VenvPython = Join-Path $ProjectRoot ".venv-windows-build\Scripts\python.exe"
$DistDir = Join-Path $WindowsDir "dist"
$BuildDir = Join-Path $WindowsDir "build"
$ReleaseDir = Join-Path $WindowsDir "release-exe"
$PackageDir = Join-Path $ReleaseDir "Pokestat-Challenge-Windows-Standalone-v1.2.0"
$ZipPath = Join-Path $ReleaseDir "Pokestat-Challenge-Windows-Standalone-v1.2.0.zip"
$HashPath = "$ZipPath.sha256"

Write-Host "=== PokeStat Challenge Windows v1.2.0 ===" -ForegroundColor Cyan

if (-not (Test-Path $WindowsDir)) {
    throw "Dossier Windows introuvable : $WindowsDir"
}
if (-not (Test-Path $VenvPython)) {
    throw "Python du venv introuvable : $VenvPython"
}

$RequiredFiles = @(
    "accueil.py",
    "accueil_pc.py",
    "affichage_pc.py",
    "mode_draft.py",
    "mode_draft_pc.py",
    "mode_guesser.py",
    "mode_guesser_pc.py",
    "mode_stat_rush.py",
    "mode_stat_rush_pc.py",
    "assets\pokemon_logo.png"
)

foreach ($File in $RequiredFiles) {
    $FullPath = Join-Path $WindowsDir $File
    if (-not (Test-Path $FullPath)) {
        throw "Fichier obligatoire manquant : $FullPath"
    }
}

Set-Location $WindowsDir

Write-Host "[1/7] Verification de Python, Pillow et PyInstaller..." -ForegroundColor Cyan
& $VenvPython -c "import sys, tkinter; from PIL import Image, ImageTk; import PyInstaller; print(sys.version); print('Dependances OK')"
if ($LASTEXITCODE -ne 0) { throw "Dependances Python incompletes." }

Write-Host "[2/7] Verification de la syntaxe des neuf modules..." -ForegroundColor Cyan
$PythonFiles = @(
    "accueil.py",
    "accueil_pc.py",
    "affichage_pc.py",
    "mode_draft.py",
    "mode_draft_pc.py",
    "mode_guesser.py",
    "mode_guesser_pc.py",
    "mode_stat_rush.py",
    "mode_stat_rush_pc.py"
)
& $VenvPython -m py_compile @PythonFiles
if ($LASTEXITCODE -ne 0) { throw "Erreur de syntaxe Python. Compilation annulee." }

Write-Host "[3/7] Nettoyage des anciens builds..." -ForegroundColor Cyan
Remove-Item $BuildDir -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $DistDir -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $ReleaseDir -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item ".\Pokestat-Challenge-Vertical.spec" -Force -ErrorAction SilentlyContinue
Remove-Item ".\Pokestat-Challenge-PC.spec" -Force -ErrorAction SilentlyContinue

Write-Host "[4/7] Compilation de l'interface verticale..." -ForegroundColor Cyan
& $VenvPython -m PyInstaller `
    --noconfirm `
    --clean `
    --windowed `
    --onedir `
    --name "Pokestat-Challenge-Vertical" `
    --add-data "assets;assets" `
    --hidden-import "mode_stat_rush" `
    "accueil.py"
if ($LASTEXITCODE -ne 0) { throw "Echec de la compilation verticale." }

Write-Host "[5/7] Compilation de l'interface PC..." -ForegroundColor Cyan
& $VenvPython -m PyInstaller `
    --noconfirm `
    --clean `
    --windowed `
    --onedir `
    --name "Pokestat-Challenge-PC" `
    --add-data "assets;assets" `
    --hidden-import "mode_stat_rush" `
    --hidden-import "mode_stat_rush_pc" `
    "accueil_pc.py"
if ($LASTEXITCODE -ne 0) { throw "Echec de la compilation PC." }

$VerticalExe = Join-Path $DistDir "Pokestat-Challenge-Vertical\Pokestat-Challenge-Vertical.exe"
$PcExe = Join-Path $DistDir "Pokestat-Challenge-PC\Pokestat-Challenge-PC.exe"
if (-not (Test-Path $VerticalExe)) { throw "EXE vertical absent : $VerticalExe" }
if (-not (Test-Path $PcExe)) { throw "EXE PC absent : $PcExe" }

Write-Host "[6/7] Preparation du paquet autonome v1.2.0..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path $PackageDir -Force | Out-Null
Copy-Item (Join-Path $DistDir "Pokestat-Challenge-Vertical") `
          (Join-Path $PackageDir "Interface-Verticale") -Recurse -Force
Copy-Item (Join-Path $DistDir "Pokestat-Challenge-PC") `
          (Join-Path $PackageDir "Interface-PC") -Recurse -Force

@'
POKESTAT CHALLENGE v1.2.0
VERSION WINDOWS AUTONOME

Python et Pillow ne sont pas requis.

NOUVEAUTE PRINCIPALE
- Ajout du mode Stat Rush dans les interfaces verticale et PC.

INTERFACE VERTICALE
Ouvrez Interface-Verticale puis lancez :
Pokestat-Challenge-Vertical.exe

INTERFACE PC
Ouvrez Interface-PC puis lancez :
Pokestat-Challenge-PC.exe

IMPORTANT
Ne déplacez pas uniquement les fichiers EXE.
Chaque EXE doit rester avec son dossier _internal.

Une connexion Internet est nécessaire lors du premier chargement de certaines donnees et illustrations Pokemon.
'@ | Set-Content (Join-Path $PackageDir "LISEZ-MOI.txt") -Encoding UTF8

Write-Host "[7/7] Creation du ZIP et du SHA-256..." -ForegroundColor Cyan
Compress-Archive -Path $PackageDir -DestinationPath $ZipPath -CompressionLevel Optimal -Force
$Hash = (Get-FileHash $ZipPath -Algorithm SHA256).Hash.ToLower()
"$Hash  Pokestat-Challenge-Windows-Standalone-v1.2.0.zip" |
    Set-Content $HashPath -Encoding ascii

Write-Host "" 
Write-Host "Compilation terminee avec succes." -ForegroundColor Green
Write-Host "EXE vertical : $VerticalExe" -ForegroundColor Yellow
Write-Host "EXE PC       : $PcExe" -ForegroundColor Yellow
Write-Host "Archive      : $ZipPath" -ForegroundColor Yellow
Write-Host "SHA-256      : $HashPath" -ForegroundColor Yellow
Write-Host "Hash         : $Hash" -ForegroundColor Yellow
Write-Host ""
Write-Host "Testez maintenant les deux EXE depuis le dossier release-exe avant publication." -ForegroundColor Cyan
