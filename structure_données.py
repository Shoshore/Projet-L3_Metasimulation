class Automate_cellulaire:
    """
    Représente un automate cellulaire unidimensionnel.

    Attributs :
        espace_etat (set): Ensemble des etats possibles que peut prendre une cellule.
        fonction_transition (dict): Fonction de transition sous forme de dictionnaire.
            Clé : tuple (gauche, centre, droite), Valeur : nouvel etat.
        symbol_vide (str): Symbole utilisé pour les cellules hors de la configuration définie.
        configuration (Configuration): Représente l'etat courant de l'automate.

    Méthodes :
        prochaine_etat(gauche, centre, droite): Retourne le prochain etat selon le triplet donné.
    """

    def __init__(self, espace_etat, fonction_transition, symbol_vide, configuration=None):
        # Ensemble des etats possibles (ex : {"0", "1", "2"})
        self.espace_etat = espace_etat

        # Fonction de transition définissant l'évolution locale de chaque cellule
        self.fonction_transition = fonction_transition

        # Symbole utilisé pour les cellules en dehors des bornes de la configuration connue
        self.symbol_vide = symbol_vide

        # Configuration courante de l'automate (objet Configuration)
        self.configuration = configuration

    def prochaine_etat(self, gauche, centre, droite):
        """
        Retourne le nouvel état de la cellule au centre en fonction des voisins
        et de la règle de transition de l'automate cellulaire.
        """
        # Recherche si une transition est définie pour la combinaison (gauche, centre, droite)
        if (gauche, centre, droite) in self.fonction_transition:
            return self.fonction_transition[(gauche, centre, droite)]
        return centre  # Si aucune règle définie, on ne change pas le centre (évolution par défaut)


class Configuration:
    """
    Représente une configuration unidimensionnelle de cellules pour un automate cellulaire.

    Attributs :
        cellules (list): Liste des etats des cellules.
        symbol_vide (str): Symbole par défaut pour les cellules en dehors de la configuration connue.
        decalage (int): Indice logique de la cellule d'indice 0 dans la liste `cellules`.

    Méthodes :
        get(index): Retourne l'etat de la cellule à l'indice donné (même hors des bornes).
        set(index, valeur): Modifie ou étend la configuration pour affecter l'etat à l'indice donné.
        __str__(): Retourne une représentation en chaîne des cellules (utile pour l'affichage).
    """

    def __init__(self, etat_initiale, symbol_vide):
        # Liste des etats des cellules dans la configuration initiale (ex: ["0", "0", "1", "0"])
        self.cellules = list(etat_initiale)

        # Symbole par défaut utilisé si on demande une cellule hors des bornes (ex: "0")
        self.symbol_vide = symbol_vide

        # decalage logique : correspond à l'indice réel de la première cellule
        # Utile quand on veut étendre la configuration vers la gauche
        self.decalage = 0

    def get(self, index):
        """
        Retourne l'etat de la cellule à une position donnée.

        Si l'index est hors des limites de la configuration actuelle,
        retourne le symbole vide (symbol_vide).

        Args:
            index (int): Position logique de la cellule

        Returns:
            str: etat de la cellule
        """
        i = index - self.decalage
        if 0 <= i < len(self.cellules):
            return self.cellules[i]
        else:
            return self.symbol_vide

    def set(self, index, valeur):
        """
        Modifie la valeur de la cellule à l'indice donné.
        Étend la configuration à gauche ou à droite si besoin.

        Args:
            index (int): Position logique de la cellule
            valeur (str): Nouvel etat de la cellule
        """
        i = index - self.decalage

        if i < 0:
            # Extension vers la gauche (ajout de symbol_vide en début)
            self.cellules = [self.symbol_vide] * (-i) + self.cellules
            self.decalage += i
            i = 0
        elif i >= len(self.cellules):
            # Extension vers la droite
            self.cellules += [self.symbol_vide] * (i - len(self.cellules) + 1)

        self.cellules[i] = valeur

    def __str__(self):
        """
        Représente la configuration sous forme de chaîne de caractères,
        utile pour afficher facilement les etats des cellules.

        Returns:
            str: Représentation textuelle de la configuration
        """
        return "".join(str(c) for c in self.cellules)


class MachineTuring:
    """
    Représente une machine de Turing déterministe à un seul ruban.

    Attributs :
        etats (set of str) : L'ensemble des etats possibles de la machine.
        symboles (set of str) : L'alphabet de travail utilisé par la machine (ex: {'0', '1', '□'}).
        etat_initial (str) : L'etat de départ de la machine.
        etats_acceptation (set of str) : L'ensemble des etats d'acceptation.
        transitions (dict) : Fonction de transition de la machine.
                             Clé : tuple (etat_actuel, symbole_lu)
                             Valeur : tuple (etat_suivant, symbole_écrit, direction)
                             La direction est soit 'G' (gauche) soit 'D' (droite).
        configuration (ConfigurationTuring) : La configuration courante (bande, tete, etat).

    Exemple de transition :
        transitions = {
            ('q0', '1'): ('q1', '□', 'D'),
            ('q1', '0'): ('q_accept', '1', 'D')
        }
    """
    def __init__(self, etats, symboles, etat_initial, etats_acceptation, transitions, configuration):
        self.etats = etats
        self.symboles = symboles
        self.etat_initial = etat_initial
        self.etats_acceptation = etats_acceptation
        self.transitions = transitions
        self.configuration = configuration


class ConfigurationTuring:
    """
    Représente une configuration (instantané) de la machine de Turing.

    Attributs :
        bande (list of str) : La bande de la machine représentée comme une liste de symboles.
                              Elle peut être étendue dynamiquement à gauche ou à droite.
        tete (int) : Position actuelle de la tete de lecture/écriture sur la bande.
        etat (str) : etat courant de la machine.

    Exemple :
        Pour une configuration avec bande = ['0', '1', '□'], tete = 1, etat = 'q0',
        cela signifie que la tete lit le symbole '1' et que la machine est dans l'etat 'q0'.
    """
    def __init__(self, bande, tete, etat):
        self.bande = bande
        self.tete = tete
        self.etat = etat
