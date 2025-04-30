from simulation import simulation, simuler
from lecture_fichier import lecture_automate, lire_machine_turing, construire_automate_depuis_turing
from sys import argv

if __name__ == "__main__":
    nom_fichier = argv[1]
    mode = argv[1][0:2]
    mot = argv[2]
    vide = argv[3]
    pas_maximale = int(argv[4])
    if len(argv[5]) != 3 or argv[5] == "None":
        arret_sur_la_transition = None
    else:
        arret_sur_la_transition = (argv[5][0], argv[5][1], argv[5][2])
    arret_sur_un_stable = bool(argv[6])

    if mode == "MT":
        machine = lire_machine_turing(nom_fichier, mot)
        print("\nÉvolution de la MT :")
        historique = simuler(machine)
        print("Bande finale (Turing) :", ''.join(historique[-1].bande)) 

    elif mode == "AC":
        automaton = lecture_automate(nom_fichier, mot, vide)
        print("\nÉvolution de l'automate :")
        result = simulation(automaton, pas_maximale, arret_sur_la_transition, arret_sur_un_stable)
        print("Dernière configuration :", result[-1])

    elif mode == "MA":
        machine = lire_machine_turing(nom_fichier, mot)
        automate = construire_automate_depuis_turing(machine)
        print("\nÉvolution de la MT :")
        historique = simuler(machine)
        print("\nÉvolution de l'automate simulant la MT :")
        resultat_automate = simulation(automate, pas_maximale, arret_sur_la_transition, arret_sur_un_stable)
        
        print("\n--- Comparaison ---")
        print("Bande finale (Turing) :", ''.join(historique[-1].bande))
        print("Dernière configuration (Automate) :", resultat_automate[-1])
        

