# Présentation du projet modelisation-vehicules

Ce projet vise à coder le comportement d'un véhicule dans un réseau. Ce comportement est défini par la loi de poursuite HDM et un changement de voie particulier. Ce modèle intègre notamment des différences entre les vehicules autonomes et les conducteurs humains. Le but est ensuite de pouvoir intégrer ce modèle dans un simulateur pour voir l'évolution de nombreux véhicules dans un réseau complexe. 

# Utilisation

Les scripts sont plutôt longs mais c'est parce qu'avant chaque fonction je spécifie les variables d'entrée,de sortie et les paramètres.
Le script general.py permet de lancer la fonction donnant l'évolution d'un véhicule dans un réseau en connaissant l'évolution du reste du trafic. Ce script fait appel aux scripts environment.py, state.py et lane_change.py. Le script construction_entrées permet de créer les variables d'entrée de la fonction general.py pour quelques scénarios très simples. Il suffit donc de lancer construction_entrées puis de lancer general pour avoir un résultat. Le script figures trajectoires.py permet (ou en tout cas permettra) ensuite de visualiser quelques trajectoires.

# Description des variables, explication des fonctions et du modèle

Je vais expliquer dans cette section (pour ne pas surcharger les scripts), comment sont construites certaines variables et comment/pourquoi j'ai créée mes fonctions.


## les variables de ego_vehicle:

Vehicle (float : compris entre 1 et le nombre de véhicules simulés): numéro du véhicule dans la simulation (id)

classe vehicle (string= ‘HD’ ou ‘AV’ pour l’instant ):  type de véhicule avec ‘HD’ pour Human Driver et ‘AV’ pour véhicule autonome

type vehicle: (string = ‘VL’, ‘Bus’ ou ‘PL’ pour l’instant): type de véhicule avec ‘VL’ por véhicule léger, ‘Bus’ pour… bus et ‘PL’ pour poids lourd

agressivity 0: (float = 50 pour véhicule autonome et compris entre 0 et 100 pour conducteur humain): représente l’aggressivité du véhicule. Plus ce nombre est élevé, plus le véhicule est aggressif dans sa façon de conduire. Plus il est faible, plus il est « timide ». Un véhicule possédant une agressivité de 50 conduira de manière « neutre ». L’aggressivité d’un véhicule détermine les paramètres de conduite suivants : la distance minimale avec le leader, la vitesse, l’accélération maximale et le time headway désirés par le véhicule. Un véhicule aggressif (aggressivity > 50) aura une distance minimale et un time headway plus faibles mais une vitesse désirée et une accélération maximale plus élevées qu’un véhicule neutre. Et l’inverse pour un véhicule « timide ».

reaction time (float : = 0.5 pour un véhicule autonome et normalement distribué N(1.2 ;0.3) pour un conducteur humain): est le temps de réaction en seconde du véhicule

courtesy: (float : compris entre 0 et 100) : est le paramètre utilisé dans la fonction utility_courtesy. Plus ce paramètre est élevé, plus le véhicule est « courtois », plus il considèrera l’impact de son changement de voie sur les autres utilisateurs : si le changement de voie fait « trop » ralentir les autres véhicules en comparaison à son gain espéré, le véhicule ne changera pas voie. Un véhicule présentant un coefficient de courtoisie de 100 ne voudra pas faire ralentir les autres véhicules et ne changera pas de voie si c’est le cas. A l’inverse, un véhicule ayant 0 ne regardera pas du tout l’impact d’un changement de voie sur les autres véhicules.
resspect code de la route: (float compris entre 0 et 100). est le paramètre utilisé dans utility_overtaking. Il représente le désir de suivre la règle de non dépassement par la droite. Un véhicule dont le coefficient est 100 évitera le plus possible de doubler par la droite même si cela implique de ralentir. A l’inverse avec le coefficient 0, le conducteur doublera par la droite si ça lui permet d’atteindre sa vitesse désirée.

road: (float : compris entre 1 et le nombre de routes dans le réseau (si il y a un double sens sur une route, ce sera considéré comme deux routes) : est la route sur laquelle se trouve le véhicule à l’instant t

lane: (float: compris entre 1 et le nombre de voies sur la route): est la voie sur laquelle se trouve le véhicule à l’instant t. J’ai considéré que les voies étaient numérotées par ordre croissant de la gauche vers la droite (1= voie de gauche, 3= voie de droite)

road turn: (float: compris entre 1 et le nombre de routes dans le réseau) : représente la route sur laquelle le véhicule devra effectuer un tournant (pour suivre son itinéraire). Pour l’instant mon code ne gère pas le changement de route donc cette variable est inutile

position turn (float: compris entre 1 et le nombre de voies sur cette route): représente la voie sur laquelle le véhicule devra effectuer un tournant (pour suivre son itinéraire). Pour l’instant mon code ne gère pas le changement de route donc cette variable est inutile

