class Automate_cellulaire:
    """
    Représente un automate cellulaire unidimensionnel.

    Attributs :
        espace_etat (set): Ensemble des états possibles que peut prendre une cellule.
        fonction_transition (dict): Fonction de transition sous forme de dictionnaire.
            Clé : tuple (gauche, centre, droite), Valeur : nouvel état.
        symbol_vide (str): Symbole utilisé pour les cellules hors de la configuration définie.
        configuration (Configuration): Représente l'état courant de l'automate.

    Méthodes :
        prochaine_etat(gauche, centre, droite): Retourne le prochain état selon le triplet donné.
    """

    def __init__(self, espace_etat, fonction_transition, symbol_vide, configuration=None):
        # Ensemble des états possibles (ex : {"0", "1", "2"})
        self.espace_etat = espace_etat

        # Fonction de transition définissant l'évolution locale de chaque cellule
        self.fonction_transition = fonction_transition

        # Symbole utilisé pour les cellules en dehors des bornes de la configuration connue
        self.symbol_vide = symbol_vide

        # Configuration courante de l'automate (objet Configuration)
        self.configuration = configuration

    def prochaine_etat(self, gauche, centre, droite):
        """
        Calcule le prochain état d'une cellule selon les états de ses voisines.

        Args:
            gauche (str): état de la cellule à gauche
            centre (str): état actuel de la cellule
            droite (str): état de la cellule à droite

        Returns:
            str: nouvel état après application de la règle de transition,
                 ou le symbol_vide si le triplet n'est pas défini.
        """
        return self.fonction_transition.get((gauche, centre, droite), self.symbol_vide)


class Configuration:
    """
    Représente une configuration unidimensionnelle de cellules pour un automate cellulaire.

    Attributs :
        cellules (list): Liste des états des cellules.
        symbol_vide (str): Symbole par défaut pour les cellules en dehors de la configuration connue.
        decalage (int): Indice logique de la cellule d'indice 0 dans la liste `cellules`.

    Méthodes :
        get(index): Retourne l'état de la cellule à l'indice donné (même hors des bornes).
        set(index, valeur): Modifie ou étend la configuration pour affecter l'état à l'indice donné.
        __str__(): Retourne une représentation en chaîne des cellules (utile pour l'affichage).
    """

    def __init__(self, état_initiale, symbol_vide):
        # Liste des états des cellules dans la configuration initiale (ex: ["0", "0", "1", "0"])
        self.cellules = list(état_initiale)

        # Symbole par défaut utilisé si on demande une cellule hors des bornes (ex: "0")
        self.symbol_vide = symbol_vide

        # decalage logique : correspond à l'indice réel de la première cellule
        # Utile quand on veut étendre la configuration vers la gauche
        self.decalage = 0

    def get(self, index):
        """
        Retourne l'état de la cellule à une position donnée.

        Si l'index est hors des limites de la configuration actuelle,
        retourne le symbole vide (symbol_vide).

        Args:
            index (int): Position logique de la cellule

        Returns:
            str: État de la cellule
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
            valeur (str): Nouvel état de la cellule
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
        utile pour afficher facilement les états des cellules.

        Returns:
            str: Représentation textuelle de la configuration
        """
        return "".join(str(c) for c in self.cellules)