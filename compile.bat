@echo off

set NOM=%~1 

if not "%~1" == "" (
    python made_stock.py %NOM%
    echo recuperation des images de %NOM%
)
echo entrainement...
python made_train.py

echo reconnaissance faciale en cours...
python reconnaissance_faciale.py