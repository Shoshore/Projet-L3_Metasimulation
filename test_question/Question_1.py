import sys
import os
import inspect
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from structure_données import Automate_cellulaire
print("Question 1 : Proposer une structure de données qui permet de représenter un automate cellulaire. Attention, l’espace d’états des cellules doit être préciser (ça n’est pas forcément {0, 1} comme dans l’exemple oule jeu de la vie).")
print("\nRéponse :\nNous avons fais sous forme d'objet.\n\nVoici le code de la classe Automate_cellulaire :")
print(inspect.getsource(Automate_cellulaire))
