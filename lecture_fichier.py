from structure_données import Automate_cellulaire, Configuration, MachineTuring, ConfigurationTuring


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


def lire_machine_turing(fichier: str, mot: str) -> MachineTuring:
    """
    Lit une machine de Turing depuis un fichier et initialise la configuration
    avec le mot donné.

    Le fichier peut contenir des commentaires commençant par #, pour spécifier :
    - # initial: q0
    - # accept: q_accept
    - # reject: q_reject

    Chaque transition est décrite sous la forme :
    état_courant symbole_lu -> nouvel_état symbole_écrit direction
    Exemple : q0 1 -> q1 0 R
    """
    transitions = {}
    etat_initial = None
    etats_accept = set()
    etats_reject = set()

    with open(fichier, "r") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne or ligne.startswith("#"):
                # Gérer les commentaires pour les infos supplémentaires
                if "initial:" in ligne:
                    etat_initial = ligne.split("initial:")[1].strip()
                elif "accept:" in ligne:
                    etats_accept.update(ligne.split("accept:")[1].strip().split())
                elif "reject:" in ligne:
                    etats_reject.update(ligne.split("reject:")[1].strip().split())
                continue

            # Parser une transition
            if "->" in ligne:
                gauche, droite = ligne.split("->")
                etat_courant, symbole_lu = gauche.strip().split()
                nouvel_etat, symbole_ecrit, direction = droite.strip().split()
                transitions[(etat_courant, symbole_lu)] = (nouvel_etat, symbole_ecrit, direction)

    if etat_initial is None:
        raise ValueError("État initial non défini dans le fichier (ligne avec '# initial: ...')")

    # Récupération de tous les états et symboles vus dans les transitions
    etats = set()
    symboles = set()
    for (etat_courant, symbole_lu), (etat_suivant, symbole_ecrit, _) in transitions.items():
        etats.add(etat_courant)
        etats.add(etat_suivant)
        symboles.add(symbole_lu)
        symboles.add(symbole_ecrit)

    # Ajouter le symbole blanc si pas déjà dedans
    symboles.add('□')

    # Créer la configuration initiale
    config_init = ConfigurationTuring(
        bande=list(mot) + ['□'],  # Ajout d'un symbole blanc à la fin de la bande
        tete=0,
        etat=etat_initial
    )

    # Créer la machine de Turing
    machine = MachineTuring(
        etats=etats,
        symboles=symboles,
        etat_initial=etat_initial,
        etats_acceptation=etats_accept,
        transitions=transitions,
        configuration=config_init
    )

    return machine


def construire_automate_depuis_turing(machine_turing):
    """
    Cette fonction construit un automate cellulaire à partir d'une machine de Turing donnée.
    L'automate cellulaire simule le comportement de la machine de Turing en suivant les règles 
    de transition définies pour cette machine.

    Args:
        machine_turing (MachineTuring): Une instance de la machine de Turing à simuler.
    
    Returns:
        Automate_cellulaire: Une instance d'un automate cellulaire simulant la machine de Turing.
    """

    # Initialisation de l'espace d'états et de la fonction de transition
    espace_etat = set()  # Ensemble pour stocker les états des cellules (symbole_etat)
    fonction_transition = {}  # Dictionnaire pour les règles de transition
    symbol_vide = '□'  # Le symbole vide de la bande de la machine de Turing

    # Ajout des états de cellules possibles dans l'espace d'état
    # Chaque cellule peut être dans un état "symbole_état" où "état" est l'état de la machine de Turing
    for symbole in machine_turing.symboles:
        espace_etat.add(symbole)  # Ajout du symbole seul (par exemple '0', '1', etc.)
        for etat in machine_turing.etats:
            espace_etat.add(f"{symbole}_{etat}")  # Ajout des cellules combinées avec un état (par exemple '0_q0')

    # Construction des règles de transition de la machine de Turing
    for (etat, symbole_lu), (etat_suiv, symbole_ecrit, direction) in machine_turing.transitions.items():
        # Si l'état actuel est un état d'acceptation, on ignore les transitions pour cet état
        if etat in machine_turing.etats_acceptation:
            continue  # On ne traite pas les transitions des états d'acceptation

        # On parcourt toutes les configurations possibles pour les cellules voisines (gauche, centre, droite)
        for gauche in espace_etat:
            for centre in espace_etat:
                for droite in espace_etat:
                    if centre == f"{symbole_lu}_{etat}":  # Si la cellule du centre correspond au symbole lu et à l'état
                        if direction == 'D':  # Si la direction de la tête est à droite
                            nouvelle_centre = symbole_ecrit  # Le symbole écrit dans la cellule centrale
                            # La cellule droite devient l'état suivant (en fonction de l'état et du symbole)
                            nouvelle_droite = f"{droite}_{etat_suiv}" if droite in machine_turing.symboles else f"{symbol_vide}_{etat_suiv}"
                            fonction_transition[(gauche, centre, droite)] = nouvelle_centre  # Enregistrement de la transition
                        elif direction == 'G':  # Si la direction de la tête est à gauche
                            nouvelle_centre = symbole_ecrit  # Le symbole écrit dans la cellule centrale
                            # La cellule gauche devient l'état suivant (en fonction de l'état et du symbole)
                            nouvelle_gauche = f"{gauche}_{etat_suiv}" if gauche in machine_turing.symboles else f"{symbol_vide}_{etat_suiv}"
                            fonction_transition[(gauche, centre, droite)] = nouvelle_centre  # Enregistrement de la transition

    # Stabilisation des états d'acceptation : lorsqu'un état d'acceptation est atteint,
    # la machine de Turing reste dans cet état et écrit le même symbole
    for etat_terminal in machine_turing.etats_acceptation:
        for symbole in list(machine_turing.symboles) + [symbol_vide]:  # On parcourt les symboles possibles
            etat_cellule = f"{symbole}_{etat_terminal}"  # Définition de l'état final
            for g in espace_etat:
                for d in espace_etat:
                    fonction_transition[(g, etat_cellule, d)] = symbole  # Les transitions sont stabilisées

    # Initialisation de la configuration de l'automate à partir de la configuration de la machine de Turing
    cellule_etats = []  # Liste pour stocker les états des cellules de l'automate
    for i, symbole in enumerate(machine_turing.configuration.bande):
        # Si la position de la tête correspond à l'indice, on associe l'état de la machine
        if i == machine_turing.configuration.tete:
            cellule_etats.append(f"{symbole}_{machine_turing.configuration.etat}")
        else:
            cellule_etats.append(symbole)  # Sinon, on ajoute simplement le symbole de la bande

    # Création de la configuration initiale de l'automate
    configuration_initiale = Configuration(cellule_etats, symbol_vide)

    # Retour de l'automate cellulaire avec l'espace d'état, la fonction de transition et la configuration initiale
    return Automate_cellulaire(
        espace_etat=espace_etat,
        fonction_transition=fonction_transition,
        symbol_vide=symbol_vide,
        configuration=configuration_initiale
    )
