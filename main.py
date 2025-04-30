from simulation import simulation, simuler
from lecture_fichier import lecture_automate, lire_machine_turing, construire_automate_depuis_turing
from sys import argv

if __name__ == "__main__":
    if len(argv) < 2:
        exit(1)

    nom_fichier = argv[1]
    mode = argv[1][0:2]
    mot = argv[2] if len(argv) > 2 else "010"
    vide = argv[3] if len(argv) > 3 else "0"
    pas_maximale = int(argv[4]) if len(argv) > 4 else 10
    arret_sur_la_transition = argv[5] if len(argv) > 5 else None
    arret_sur_un_stable = argv[6].lower() != "false" if len(argv) > 6 else True

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

    elif mode == "AC_MT":
        machine = lire_machine_turing(nom_fichier, mot)
        automate = construire_automate_depuis_turing(machine)
        print("\nÉvolution de la MT :")
        historique = simuler(machine)
        print("\nÉvolution de l'automate simulant la MT :")
        resultat_automate = simulation(automate, pas_maximale, arret_sur_la_transition, arret_sur_un_stable)
        
        print("\n--- Comparaison ---")
        print("Bande finale (Turing) :", ''.join(historique[-1].bande))
        print("Dernière configuration (Automate) :", resultat_automate[-1])
        

