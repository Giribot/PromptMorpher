@echo off
:: Vérifie si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas installé sur ce système.
    echo Veuillez installer Python depuis https://www.python.org/downloads/ et réessayez.
    pause
    exit /b
)

echo Python détecté. Vérification des bibliothèques nécessaires...

:: Vérifie et installe les bibliothèques nécessaires
pip install tk >nul 2>&1
if %errorlevel% neq 0 (
    echo Une erreur est survenue lors de l'installation de tkinter.
    echo Vérifiez vos paramètres réseau ou votre installation de Python.
    pause
    exit /b
)

pip install pillow >nul 2>&1
if %errorlevel% neq 0 (
    echo Une erreur est survenue lors de l'installation de Pillow.
    echo Vérifiez vos paramètres réseau ou votre installation de Python.
    pause
    exit /b
)

echo Toutes les bibliothèques nécessaires sont installées.

:: Lance le script Python
echo Lancement du script...
python "promptmorpher.py"
if %errorlevel% neq 0 (
    echo Une erreur est survenue lors de l'exécution du script Python.
    pause
    exit /b
)

pause
exit
