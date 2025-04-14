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
    transitions_brutes = []  # stocke temporairement les transitions à traiter
    espace_etat = set()      # ensemble des états

    # Première passe : collecter tous les états
    with open(chemin_acces, 'r') as fichier:
        for ligne in fichier:
            if '->' not in ligne:
                continue

            lhs, rhs = ligne.strip().split('->')
            paterne = tuple(s.strip() for s in lhs.strip().split())
            resultat = rhs.strip()

            # Stocke la ligne pour la deuxième passe
            transitions_brutes.append((paterne, resultat))

            # Met à jour l’ensemble des symboles
            espace_etat.update(s for s in paterne if s != '*')
            espace_etat.add(resultat)

    # Deuxième passe : création de la fonction de transition
    fonction_transition = {}
    for paterne, resultat in transitions_brutes:
        for extension in extension_paterne(paterne, espace_etat):
            fonction_transition[extension] = resultat

    # Création de l’automate avec config initiale
    automate = Automate_cellulaire(
        espace_etat=espace_etat,
        fonction_transition=fonction_transition,
        symbol_vide=symbol_vide
    )

    config = Configuration(list(mot_entre), symbol_vide=symbol_vide)
    automate.configuration = config

    return automate