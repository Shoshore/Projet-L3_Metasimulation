Pour accéder aux questions 1 à 14, il suffit de taper dans le terminal (∀ x ∈ [1, 14]) :
make qx

Pour exécuter le code :
Exécute le fichier MA_machine.txt :
make
Exécute un fichier spécifique, ce fichier doit commencer par :

- AC pour un automate cellulaire

- MT pour une machine de Turing

- MA pour simuler un automate cellulaire à partir d’une machine de Turing

La commande :
make fichier=nom_du_fichier.txt

Pour les commandes make et make fichier=nom_du_fichier.txt, on peut ajouter les arguments suivants :
fichier = MA_machine.txt
mot = 010
vide = 0
max = 10
transi = None
stable = True

Les valeurs données sont les valeurs par défaut, sauf si elles sont modifiées via l’entrée make.
Les machines de Turing fonctionnent uniquement avec l’alphabet Σ = {0, 1, □}.

mot : le mot d’entrée (str ou int selon l’alphabet de travail).

Utile uniquement pour les automates cellulaires :

vide : le caractère vide de l’alphabet de travail.

max : un entier pour savoir au bout de combien de cycles on arrête l’automate cellulaire.

transi : 3 caractères ou None qui s’arrêtera sur la transition correspondante.

stable : s’arrête si l’automate devient stable (True ou False).

exemple pour un automate cellulaire :
make fichier=AC_interessant_1.txt mot=0001000 vide=0 max=20 transi=111 stable=False
