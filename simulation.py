from structure_données import Configuration


def calcule_prochaine_configuration(automate):
    """
    Calcule la prochaine configuration de l'automate en appliquant les règles de transition
    sur chaque cellule de l'automate, en tenant compte des cellules voisines (gauche et droite).
    """
    ancienne_configuration = automate.configuration  # Récupère la configuration actuelle
    nouvelle_configuration = Configuration([], automate.symbol_vide)  # Crée une nouvelle configuration vide
    
    # Parcours des cellules de la configuration actuelle
    for i in range(ancienne_configuration.decalage - 1, ancienne_configuration.decalage + len(ancienne_configuration.cellules) + 1):
        # Récupère les cellules gauche, centre, droite
        gauche = ancienne_configuration.get(i - 1) if i > 0 else automate.symbol_vide
        centre = ancienne_configuration.get(i)
        droite = ancienne_configuration.get(i + 1) if i < len(ancienne_configuration.cellules) - 1 else automate.symbol_vide
        
        # Calcule le nouvel état de la cellule en fonction de la transition
        nouvelle_etat = automate.prochaine_etat(gauche, centre, droite)
        nouvelle_configuration.set(i, nouvelle_etat)  # Mise à jour de la nouvelle configuration avec le nouvel état

    # Met à jour la configuration de l'automate avec la nouvelle configuration calculée
    automate.configuration = nouvelle_configuration
    return nouvelle_configuration  # Retourne la nouvelle configuration


def simulation(automate, pas_maximale=None, arret_sur_la_transition=None, arret_sur_un_stable=False):
    """
    Simule le comportement de l'automate cellulaire pendant un nombre défini d'étapes, 
    ou jusqu'à ce que certaines conditions d'arrêt soient remplies (transition spécifique ou configuration stable).

    Args:
        automate (Automate_cellulaire): L'automate à simuler.
        pas_maximale (int, optional): Nombre maximal d'étapes avant d'arrêter la simulation. Si None, la simulation continue indéfiniment.
        arret_sur_la_transition (tuple, optional): Si une transition spécifique est détectée, la simulation s'arrête.
        arret_sur_un_stable (bool, optional): Si True, la simulation s'arrête lorsque la configuration devient stable.

    Returns:
        list: Une liste contenant l'historique des configurations à chaque étape de la simulation.
    """
    historique = [automate.configuration]  # Liste pour stocker l'historique des configurations
    print(f"00 : {automate.configuration}")  # Affiche la configuration initiale
    for step in range(1, pas_maximale + 1 if pas_maximale is not None else float('inf')):
        prev_config = automate.configuration  # Configuration précédente
        nouvelle_configuration = calcule_prochaine_configuration(automate)  # Calcule la prochaine configuration
        historique.append(nouvelle_configuration)  # Ajoute la nouvelle configuration à l'historique
        print(f"{step:02d} : {nouvelle_configuration}")

        # Vérifie si la configuration est stable (si elle ne change pas)
        if arret_sur_un_stable and str(prev_config) == str(nouvelle_configuration):
            print(f"Arrêt : configuration stable atteinte à l'étape {step}")
            break  # Arrêt si la configuration est stable

        # Vérifie si une transition spécifique a eu lieu et arrête la simulation
        if arret_sur_la_transition:
            for i in range(prev_config.decalage - 1, prev_config.decalage + len(prev_config.cellules) + 1):
                t = (prev_config.get(i - 1), prev_config.get(i), prev_config.get(i + 1))  # Transition courante
                if t == arret_sur_la_transition:  # Si la transition correspond à celle recherchée
                    print(f"Arrêt : transition {t} détectée à l'étape {step}")
                    return historique  # Retourne l'historique jusqu'à ce point

    return historique  # Retourne l'historique des configurations si la simulation ne s'arrête pas avant


def pas_de_calcul(machine):
    """
    Effectue un pas de calcul de la machine de Turing.

    Args:
        machine (MachineTuring): La machine de Turing avec sa configuration actuelle.

    Returns:
        ConfigurationTuring or None: La nouvelle configuration après un pas de calcul,
        ou None si aucune transition n'est possible.
    """
    config = machine.configuration
    tete = config.tete
    symbole_lu = config.bande[tete] if 0 <= tete < len(config.bande) else '□'
    transition = machine.transitions.get((config.etat, symbole_lu))

    if transition is None:
        return None  # Pas de transition définie, arrêt

    nouvel_etat, symbole_ecrit, direction = transition

    # Écriture sur la bande
    config.bande[tete] = symbole_ecrit

    # Déplacement de la tête
    if direction == 'D':
        config.tete += 1
        if config.tete >= len(config.bande):
            config.bande.append('□')  # Étendre la bande à droite si besoin
    elif direction == 'G':
        if config.tete <= 0:
            config.bande.insert(0, '□')  # Étendre la bande à gauche
        else:
            config.tete -= 1

    # Changement d'état
    config.etat = nouvel_etat

    return config


def simuler(machine):
    """
    Simule l'exécution d'une machine de Turing jusqu'à acceptation ou rejet.
    """
    etapes = 0
    historique = []  # Crée une liste pour stocker les étapes de la simulation
    while True:
        config = machine.configuration
        historique.append(config)  # Ajoute la configuration actuelle à l'historique

        print(f"{etapes:02d} : état={config.etat}, tête={config.tete}, bande={''.join(config.bande)}")

        if config.etat in machine.etats_acceptation:
            print("→ Mot accepté.")
            return historique  # Retourne l'historique des configurations jusqu'à ce point

        transition = machine.transitions.get((config.etat, config.bande[config.tete] if 0 <= config.tete < len(config.bande) else '□'))
        if transition is None:
            print(f"→ Aucune transition trouvée pour (état={config.etat}, symbole={config.bande[config.tete]})")
            print("→ Mot rejeté.")
            return historique  # Retourne l'historique des configurations si aucun transition n'est trouvé

        pas_de_calcul(machine)
        etapes += 1
