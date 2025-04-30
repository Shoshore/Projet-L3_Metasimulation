import sys
import os
import inspect
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from structure_données import Automate_cellulaire, Configuration, MachineTuring, ConfigurationTuring
from lecture_fichier import lecture_automate, lire_machine_turing, construire_automate_depuis_turing
from simulation import simulation, simuler, pas_de_calcul, calcule_prochaine_configuration
reponse_question_14 = ""
fonction_question = {
    1: Automate_cellulaire,
    2: Configuration,
    3: lecture_automate,
    4: calcule_prochaine_configuration,
    5: simulation,
    6: simulation,
    7: ("AC_cycler.txt", "AC_grandir.txt", "AC_interessant_1.txt", "AC_interessant_2.txt"),
    8: MachineTuring,
    9: ConfigurationTuring,
    10: lire_machine_turing,
    11: pas_de_calcul,
    12: simuler,
    13: construire_automate_depuis_turing,
    14: reponse_question_14
}
def code(numero_question: int):
    """
    Affiche dynamiquement le code ou contenu lié à la question spécifiée.
    
    Args:
        numero_question (int): Le numéro de la question dont on veut afficher le code.
    """
    element = fonction_question.get(numero_question)
    if numero_question == 7:
        dossier_racine = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        for nom_fichier in element:
            chemin = os.path.join(dossier_racine, nom_fichier)
            print(f"\n--- Contenu de {nom_fichier} ---")
            try:
                with open(chemin, 'r') as fichier:
                    print(fichier.read())
            except FileNotFoundError:
                print(f"[Erreur] Fichier {nom_fichier} introuvable à {chemin}")

    elif numero_question == 14:
        print(element)
    else:
        try:
            print(inspect.getsource(element))
        except TypeError:
            print(f"Impossible d’afficher le code source de l’élément pour la question {numero_question}")
