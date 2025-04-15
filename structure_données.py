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
        transition = self.fonction_transition.get((gauche, centre, droite))
        if transition is None:
            return self.symbol_vide  # Retourne symbol_vide si la transition n'est pas définie
        return transition



class MachineTuring:
    """
    Représente une machine de Turing à un ruban.

    Attributs :
        états (set) : Ensemble des états possibles.
        symboles (set) : Alphabet de travail (ex: {'0', '1', '□'}).
        état_initial (str) : État de départ.
        états_acceptation (set) : États d'acceptation.
        transitions (dict) : Dictionnaire des transitions.
            Clé : (état, symbole), Valeur : (nouvel état, symbole à écrire, direction 'G' ou 'D')
        configuration (ConfigurationTuring) : Configuration actuelle (bande, tête, état).
    """

    def __init__(self, états, symboles, état_initial, états_acceptation, transitions, configuration):
        self.états = états
        self.symboles = symboles
        self.état_initial = état_initial
        self.états_acceptation = états_acceptation
        self.transitions = transitions  # { (etat, symbole): (etat_suivant, symbole_écrit, direction) }
        self.configuration = configuration  # instance de ConfigurationTuring

    

class MachineTuring:
    """
    Représente une machine de Turing à une bande.

    Attributs :
        états (set) : Ensemble des états possibles (ex: {"q0", "q1", "qf"}).
        alphabet (set) : Alphabet de travail (ex: {"0", "1", "□"}).
        état_initial (str) : État de départ de la machine (ex: "q0").
        état_final (str) : État d’acceptation/halting (ex: "qf").
        transitions (dict) : Fonction de transition :
            clé : (état, symbole_lu)
            valeur : (nouvel_état, symbole_écrit, direction)
        bande (list) : Contenu actuel de la bande.
        tête (int) : Position actuelle de la tête de lecture/écriture.
        état_courant (str) : État actuel de la machine.
    """

    def __init__(self, états, alphabet, état_initial, état_final, transitions, bande_initiale):
        self.états = états
        self.alphabet = alphabet
        self.état_initial = état_initial
        self.état_final = état_final
        self.transitions = transitions  # Dictionnaire : (état, symbole_lu) → (nouvel_état, symbole_écrit, direction)
        self.bande = list(bande_initiale)  # Bande initiale sous forme de liste de symboles
        self.tête = 0  # Position de départ
        self.état_courant = état_initial

    def symbole_lu(self):
        if self.tête < 0:
            # Extension vers la gauche
            self.bande = ['□'] * (-self.tête) + self.bande
            self.tête = 0
        elif self.tête >= len(self.bande):
            # Extension vers la droite
            self.bande += ['□'] * (self.tête - len(self.bande) + 1)

        return self.bande[self.tête]