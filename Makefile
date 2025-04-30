# Partie 1 : Définition des paramètres par défaut pour l'exécution de main.py
fichier ?= MA_machine.txt
mot ?= 010
vide ?= 0
max ?= 10
transi ?= None
stable ?= True

# Partie 2 : Règle par défaut pour exécuter main.py avec un fichier .txt (fichier par défaut = MA_machine.txt)
.PHONY: run_default

run_default:
	@echo "==> Lancement avec $(fichier)"
	@echo "  Mot         : $(mot)"
	@echo "  Vide        : $(vide)"
	@echo "  Pas max     : $(max)"
	@echo "  Stop sur    : $(transi)"
	@echo "  Stable      : $(stable)"
	@python3 main.py $(fichier) $(mot) $(vide) $(max) $(transi) $(stable)

# Partie 3 : Exécution de main.py avec un fichier .txt personnalisé
.PHONY: run_txt

run_txt:
	@echo "Utilise : make fichier.txt mot=... vide=... etc."

# Si on veut exécuter avec un fichier .txt, on utilise %.txt
%.txt: run_txt
	@echo "==> Lancement avec $(fichier)"
	@echo "  Mot         : $(mot)"
	@echo "  Vide        : $(vide)"
	@echo "  Pas max     : $(max)"
	@echo "  Stop sur    : $(transi)"
	@echo "  Stable      : $(stable)"
	@python3 main.py $(fichier) $(mot) $(vide) $(max) $(transi) $(stable)

# Partie 4 : exécution des Question_x.py
QNUMBERS := $(shell seq 1 14)
.PHONY: $(addprefix q, $(QNUMBERS))

$(addprefix q, $(QNUMBERS)):
	@QNUM=$(patsubst q%,%,$@); \
	FILE=./test_question/Question_$$QNUM.py; \
	if [ -f $$FILE ]; then \
		echo "==> Exécution de $$FILE"; \
		python3 $$FILE; \
	else \
		echo "Fichier $$FILE introuvable."; \
		exit 1; \
	fi
