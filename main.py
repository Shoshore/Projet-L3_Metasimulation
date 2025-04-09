from simulation import simulation
from lecture_fichier import lecture_automate

if __name__ == "__main__":
    # Lecture de l'automate et initialisation de la configuration
    automaton = lecture_automate("cycler.txt", "0001000", blank_symbol="0")

    # Simulation de l'automate avec 10 étapes ou arrêt si configuration stable
    result = simulation(automaton, max_steps=10, stop_on_stable=True)

    print("\nÉvolution de l'automate :")
    for step, conf in enumerate(result):
        print(f"{step:02d} : {conf}")
