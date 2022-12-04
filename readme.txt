
Pré requis :
python3 -m pip install click
pip install requests
pip install csv
pip install bs4
pip install datetime

Exemples de ligne de commande : 
python3 Click2.py --url='www.aforp.fr' --error404=True --export=True
python3 Click2.py --url='www.aforp.fr' --auth=True --export=True

python3 Click2.py --help

Vous ne pouvez pas demander la liste des pages 404 et des pages 401 puisque les 2 sont incompatibles.
Cependant vous n'aurez pas d'erreur, le script scannera alors les 404 et non les 401. 