from simulation import simulation
from lecture_fichier import lecture_automate
from sys import argv

if __name__ == "__main__":
    condition = True
    # Lecture de l'automate et initialisation de la configuration
    nom_fichier = argv[1]
    vide = argv[2]
    mot = argv[3] if argv[3] else "010"
    automaton = lecture_automate(nom_fichier, mot, symbol_vide=vide)

    # Simulation de l'automate avec 10 étapes ou arrêt si configuration stable
    result = simulation(automaton, pas_maximale=10, arret_sur_la_transition=None,
                        arret_sur_un_stable=True)

    print("\nÉvolution de l'automate :")
    for step, conf in enumerate(result):
        print(f"{step:02d} : {conf}")
