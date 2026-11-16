param(
    [string]$ProjectRoot = "E:\Projet\PokeStat-Challenge-GitHub"
)

$ErrorActionPreference = "Stop"
$WindowsDir = Join-Path $ProjectRoot "windows"
$VenvPython = Join-Path $ProjectRoot ".venv-windows-build\Scripts\python.exe"
$DistDir = Join-Path $WindowsDir "dist"
$BuildDir = Join-Path $WindowsDir "build"
$ReleaseDir = Join-Path $WindowsDir "release-exe"
$PackageDir = Join-Path $ReleaseDir "Pokestat-Challenge-Windows-Standalone-v1.3.0"
$ZipPath = Join-Path $ReleaseDir "Pokestat-Challenge-Windows-Standalone-v1.3.0.zip"
$HashPath = "$ZipPath.sha256"

if (-not (Test-Path $WindowsDir)) { throw "Dossier introuvable : $WindowsDir" }
if (-not (Test-Path $VenvPython)) { throw "Venv introuvable : $VenvPython" }

$PythonFiles = @(
    "accueil.py", "accueil_pc.py", "affichage_pc.py", "pokemon_categories.py",
    "mode_draft.py", "mode_draft_pc.py", "mode_guesser.py", "mode_guesser_pc.py",
    "mode_stat_rush.py", "mode_stat_rush_pc.py"
)
foreach ($File in $PythonFiles) {
    if (-not (Test-Path (Join-Path $WindowsDir $File))) { throw "Fichier manquant : $File" }
}
if (-not (Test-Path (Join-Path $WindowsDir "assets\pokemon_logo.png"))) {
    throw "Logo manquant : windows\assets\pokemon_logo.png"
}

Set-Location $WindowsDir
Write-Host "[1/6] Verification des dependances..." -ForegroundColor Cyan
& $VenvPython -c "import tkinter; from PIL import Image, ImageTk; import PyInstaller; print('Dependances OK')"
if ($LASTEXITCODE -ne 0) { throw "Dependances incompletes" }

Write-Host "[2/6] Verification de la syntaxe..." -ForegroundColor Cyan
& $VenvPython -m py_compile @PythonFiles
if ($LASTEXITCODE -ne 0) { throw "Erreur de syntaxe" }

Write-Host "[3/6] Nettoyage..." -ForegroundColor Cyan
Remove-Item $BuildDir -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $DistDir -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item $ReleaseDir -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item ".\Pokestat-Challenge-Vertical.spec", ".\Pokestat-Challenge-PC.spec" -Force -ErrorAction SilentlyContinue

Write-Host "[4/6] Compilation verticale..." -ForegroundColor Cyan
& $VenvPython -m PyInstaller --noconfirm --clean --windowed --onedir `
    --name "Pokestat-Challenge-Vertical" `
    --add-data "assets;assets" `
    --hidden-import "pokemon_categories" `
    --hidden-import "mode_stat_rush" `
    "accueil.py"
if ($LASTEXITCODE -ne 0) { throw "Echec compilation verticale" }

Write-Host "[5/6] Compilation PC..." -ForegroundColor Cyan
& $VenvPython -m PyInstaller --noconfirm --clean --windowed --onedir `
    --name "Pokestat-Challenge-PC" `
    --add-data "assets;assets" `
    --hidden-import "pokemon_categories" `
    --hidden-import "mode_stat_rush" `
    --hidden-import "mode_stat_rush_pc" `
    "accueil_pc.py"
if ($LASTEXITCODE -ne 0) { throw "Echec compilation PC" }

Write-Host "[6/6] Creation de l'archive v1.3.0..." -ForegroundColor Cyan
New-Item -ItemType Directory -Path $PackageDir -Force | Out-Null
Copy-Item (Join-Path $DistDir "Pokestat-Challenge-Vertical") (Join-Path $PackageDir "Interface-Verticale") -Recurse -Force
Copy-Item (Join-Path $DistDir "Pokestat-Challenge-PC") (Join-Path $PackageDir "Interface-PC") -Recurse -Force
@'
POKÉSTAT CHALLENGE v1.3.0 - VERSION WINDOWS AUTONOME

Python et Pillow ne sont pas requis.

NOUVEAUTÉS
- Filtres de catégories dans les trois modes
- Légendaires + fabuleux
- Familles de starters
- Fossiles
- Familles pseudo-légendaires
- Bébés Pokémon
- Pokémon sans évolution
- Méga-Évolutions liées à la génération de leur espèce de base

LANCEMENT
Interface-Verticale\Pokestat-Challenge-Vertical.exe
Interface-PC\Pokestat-Challenge-PC.exe

Ne déplacez pas les EXE hors de leurs dossiers _internal.
'@ | Set-Content (Join-Path $PackageDir "LISEZ-MOI.txt") -Encoding UTF8

Compress-Archive -Path $PackageDir -DestinationPath $ZipPath -CompressionLevel Optimal -Force
$Hash = (Get-FileHash $ZipPath -Algorithm SHA256).Hash.ToLower()
"$Hash  Pokestat-Challenge-Windows-Standalone-v1.3.0.zip" | Set-Content $HashPath -Encoding ascii

Write-Host "" 
Write-Host "Compilation v1.3.0 terminee." -ForegroundColor Green
Write-Host $ZipPath -ForegroundColor Yellow
Write-Host $HashPath -ForegroundColor Yellow
Write-Host "SHA-256 : $Hash" -ForegroundColor Yellow
