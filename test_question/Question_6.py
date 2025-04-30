from importation import code
if __name__ == '__main__':
    print("Question 6 : Modifier la fonction précédente pour que, à chaque pas de simulation, la configuration de l’automate s’affiche de manière compréhensible (soit graphiquement, soit sur le terminal).")
    print("\n\n Réponse : \n Voici le code de la fonction simulation : \n")
    print("""Plus précisément : on ajouté 2 print :\n-print (f"00 : {automate.configuration}")\n-print(f"{step:02d} : {nouvelle_configuration}")""")
    print("\n\n Voici le code de la fonction simulation : \n")
    code(6)