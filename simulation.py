from structure_données import Configuration


def calcule_prochaine_configuration(automate):
    """
    Calcule la prochaine configuration de l'automate en appliquant les règles de transition
    sur chaque cellule de l'automate, en tenant compte des cellules voisines (gauche et droite).

    Pour chaque cellule de la configuration actuelle, l'automate applique la fonction de transition
    basée sur son état actuel et ceux de ses voisins immédiats (gauche, centre et droite). Une nouvelle
    configuration est générée et l'automate met à jour son état.

    Args:
        automate (Automate_cellulaire): L'automate dont on doit calculer la prochaine configuration.

    Returns:
        Configuration: La nouvelle configuration calculée de l'automate.
    """
    ancienne_configuration = automate.configuration  # Récupère la configuration actuelle
    nouvelle_configuration = Configuration([], automate.symbol_vide)  # Crée une nouvelle configuration vide

    # Étendre de 1 cellule à gauche et à droite pour couvrir les bords
    for i in range(ancienne_configuration.decalage - 1, ancienne_configuration.decalage + len(ancienne_configuration.cellules) + 1):
        gauche = ancienne_configuration.get(i - 1)  # État de la cellule à gauche
        centre = ancienne_configuration.get(i)    # État de la cellule actuelle
        droite = ancienne_configuration.get(i + 1) # État de la cellule à droite
        nouvelle_etat = automate.prochaine_etat(gauche, centre, droite)  # Calcul du nouvel état basé sur la transition
        nouvelle_configuration.set(i, nouvelle_etat)  # Mise à jour de la nouvelle configuration avec le nouvel état

    # Met à jour la configuration de l'automate avec la nouvelle configuration calculée
    automate.configuration = nouvelle_configuration
    return nouvelle_configuration  # Retourne la nouvelle configuration



def simulation(automate, pas_maximale=None, arret_sur_la_transition=None, arret_sur_un_stable=False):
    """
    Simule le comportement de l'automate cellulaire pendant un nombre défini d'étapes, 
    ou jusqu'à ce que certaines conditions d'arrêt soient remplies (transition spécifique ou configuration stable).

    À chaque étape, l'automate calcule la prochaine configuration et l'ajoute à l'historique. 
    Si l'option `arret_sur_un_stable` est activée, la simulation s'arrête lorsque la configuration devient stable (c'est-à-dire qu'elle ne change plus). 
    Si l'option `arret_sur_la_transition` est spécifiée, la simulation s'arrête dès qu'une transition spécifique est détectée.

    Args:
        automate (Automate_cellulaire): L'automate à simuler.
        pas_maximale (int, optional): Nombre maximal d'étapes avant d'arrêter la simulation. Si None, la simulation continue indéfiniment.
        arret_sur_la_transition (tuple, optional): Si une transition spécifique est détectée, la simulation s'arrête. Le format de la transition est une triplette (gauche, centre, droite).
        arret_sur_un_stable (bool, optional): Si True, la simulation s'arrête lorsque la configuration devient stable.

    Returns:
        list: Une liste contenant l'historique des configurations à chaque étape de la simulation.
    """
    historique = [automate.configuration]  # Liste pour stocker l'historique des configurations

    # On boucle jusqu'à atteindre le nombre d'étapes ou une condition d'arrêt
    for step in range(1, pas_maximale + 1 if pas_maximale is not None else float('inf')):
        prev_config = automate.configuration  # Configuration précédente
        nouvelle_configuration = calcule_prochaine_configuration(automate)  # Calcule la prochaine configuration
        historique.append(nouvelle_configuration)  # Ajoute la nouvelle configuration à l'historique

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