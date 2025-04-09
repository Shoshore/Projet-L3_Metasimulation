from structure_données import Automate_cellulaire, Configuration

def extension_paterne(paterne, espace_etat):
    """
    Développe un modèle de transition (paterne) en remplaçant les caractères '*' 
    par tous les symboles possibles dans l'ensemble d'états (espace_etat).
    
    Cette fonction génère toutes les combinaisons possibles où '*' est remplacé 
    par tous les éléments de `espace_etat`.

    Args:
        paterne (tuple): Le modèle de transition contenant des symboles (ex : ('*', '0', '*'))
        espace_etat (set): Ensemble des symboles possibles dans les états (ex : {'0', '1', '2'})

    Returns:
        list: Une liste de tuples représentant toutes les combinaisons possibles du modèle après expansion.
    """
    from itertools import product

    # Crée une liste de sous-listes où '*' est remplacé par une liste contenant tous les symboles de espace_etat
    slots = [
        [x] if x != '*' else list(espace_etat)
        for x in paterne
    ]

    # Retourne toutes les combinaisons possibles des sous-listes en utilisant `itertools.product`
    return list(product(*slots))


def lecture_automate(chemin_acces, mot_entre, symbol_vide):
    """
    Lit un fichier de définition d'un automate cellulaire et construit l'automate 
    correspondant avec une configuration initiale donnée.

    Le fichier doit contenir des transitions sous la forme 'gauche centre droite -> nouvel état'.
    Chaque transition est ajoutée à une fonction de transition pour l'automate.
    
    Args:
        chemin_acces (str): Chemin vers le fichier contenant la définition des transitions de l'automate.
        mot_entre (str): Mot d'entrée initial représentant l'état de l'automate sous forme de chaîne de caractères.
        symbol_vide (str): Symbole représentant les cellules vides (par défaut, en dehors de la configuration définie).

    Returns:
        Automate_cellulaire: Un objet représentant l'automate avec sa fonction de transition et sa configuration initiale.
    """
    fonction_transition = {}  # Dictionnaire pour stocker la fonction de transition
    espace_etat = set()       # Ensemble des états possibles dans l'automate

    # Ouverture et lecture du fichier de définitions de transitions
    with open(chemin_acces, 'r') as fichier:
        for ligne in fichier:
            if '->' not in ligne:
                continue  # Ignore les lignes qui ne définissent pas de transition

            # Séparation de la ligne en un modèle de transition et un résultat
            lhs, rhs = ligne.strip().split('->')
            paterne = tuple(s.strip() for s in lhs.strip().split())  # Modèle (gauche, centre, droite)
            resultat = rhs.strip()  # Résultat de la transition (nouvel état)

            # Mise à jour de l'ensemble des états possibles en fonction du modèle
            espace_etat.update(s for s in paterne if s != '*')
            espace_etat.add(resultat)  # On ajoute aussi le résultat à l'ensemble des états possibles

            # Expansion si `*` est présent dans le modèle
            for extension in extension_paterne(paterne, espace_etat):
                fonction_transition[extension] = resultat  # On ajoute la transition au dictionnaire

    # Création de l'automate avec la fonction de transition et la configuration initiale
    automate = Automate_cellulaire(
        espace_etat=espace_etat,
        fonction_transition=fonction_transition,
        symbol_vide=symbol_vide
    )

    # Initialisation de la configuration de l'automate avec le mot d'entrée
    config = Configuration(list(mot_entre), symbol_vide=symbol_vide)
    automate.configuration = config  # On garde la configuration dans l'automate

    return automate  # Retourne l'automate complet