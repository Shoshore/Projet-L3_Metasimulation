from simulation import simulation, simuler
from lecture_fichier import lecture_automate, lire_machine_turing, construire_automate_depuis_turing
from sys import argv

if __name__ == "__main__":
    if len(argv) < 3:
        exit(1)

    nom_fichier = argv[1]
    mode = argv[2]
    mot = argv[3] if len(argv) > 3 else "010"
    vide = argv[4] if len(argv) > 4 else "0"
    pas_maximale = int(argv[5]) if len(argv) > 5 else 10
    arret_sur_la_transition = argv[6] if len(argv) > 6 else None
    arret_sur_un_stable = argv[7].lower() != "false" if len(argv) > 7 else True

    if mode == "MT":
        machine = lire_machine_turing(nom_fichier, mot)
        historique = simuler(machine)
        print("Bande finale (Turing) :", ''.join(historique[-1].bande)) 

    elif mode == "AC":
        automaton = lecture_automate(nom_fichier, mot, vide)
        result = simulation(automaton, pas_maximale, arret_sur_la_transition, arret_sur_un_stable)
        print("\nÉvolution de l'automate :")
        for step, conf in enumerate(result):
            print(f"{step:02d} : {conf}")

    elif mode == "AC_MT":
        machine = lire_machine_turing(nom_fichier, mot)
        automate = construire_automate_depuis_turing(machine)
        historique = simuler(machine)
        resultat_automate = simulation(automate, pas_maximale, arret_sur_la_transition, arret_sur_un_stable)

        print("\nÉvolution de l'automate simulant la machine :")
        for step, conf in enumerate(resultat_automate):
            print(f"{step:02d} : {conf}")

        print("\n--- Comparaison ---")
        print("Bande finale (Turing) :", ''.join(historique[-1].bande))
        print("Dernière configuration (Automate) :", resultat_automate[-1])
        

