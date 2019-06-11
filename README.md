# Présentation du projet modelisation-vehicules

Ce projet vise à coder le comportement d'un véhicule dans un réseau. Ce comportement est défini par la loi de poursuite HDM et un changement de voie particulier. Ce modèle intègre notamment des différences entre les vehicules autonomes et les conducteurs humains. Le but est ensuite de pouvoir intégrer ce modèle dans un simulateur pour voir l'évolution de nombreux véhicules dans un réseau complexe. 

# Utilisation

Les scripts sont plutôt longs mais c'est parce qu'avant chaque fonction je spécifie les variables d'entrée,de sortie et les paramètres.
Le script general.py permet de lancer la fonction donnant l'évolution d'un véhicule dans un réseau en connaissant l'évolution du reste du trafic. Ce script fait appel aux scripts environment.py, state.py et lane_change.py. Le script construction_entrées permet de créer les variables d'entrée de la fonction general.py pour quelques scénarios très simples. Il suffit donc de lancer construction_entrées puis de lancer general pour avoir un résultat. Le script figures trajectoires.py permet (ou en tout cas permettra) ensuite de visualiser quelques trajectoires.

# Description des variables, explication des fonctions et du modèle

Je vais expliquer dans cette section (pour ne pas surcharger les scripts), comment sont construites certaines variables et comment/pourquoi j'ai créée mes fonctions.



