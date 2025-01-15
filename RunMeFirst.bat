@echo off
REM Vérification de l'installation de Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python n'est pas installé sur ce système.
    echo Veuillez installer Python depuis https://www.python.org/downloads/ et réessayer.
    pause
    exit /b
)

echo Python est installé.

REM Bibliothèques nécessaires pour ce projet
set LIBS=os,string,tkinter

for %%L in (%LIBS%) do (
    python -c "import %%L" >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo La bibliothèque %%L n'est pas installée. Installation en cours...
        python -m pip install %%L
        if %ERRORLEVEL% NEQ 0 (
            echo Erreur lors de l'installation de la bibliothèque %%L. Vérifiez votre connexion Internet ou pip.
            pause
            exit /b
        )
    )
)

echo Toutes les bibliothèques nécessaires sont installées.

REM Lancement du script Python
python promptmorpher.py
if %ERRORLEVEL% NEQ 0 (
    echo Une erreur s'est produite lors de l'exécution du script.
    pause
    exit /b
)

echo Script exécuté avec succès.
pause
