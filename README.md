# Présentation du projet modelisation-vehicules

Ce projet vise à coder le comportement d'un véhicule dans un réseau. Ce comportement est défini par la loi de poursuite HDM et un changement de voie particulier. Ce modèle intègre notamment des différences entre les vehicules autonomes et les conducteurs humains. Le but est ensuite de pouvoir intégrer ce modèle dans un simulateur pour voir l'évolution de nombreux véhicules dans un réseau complexe. 

# Utilisation

Les scripts sont plutôt longs mais c'est parce qu'avant chaque fonction je spécifie les variables d'entrée, de sortie et les paramètres.
Le script *general.py* permet de lancer la fonction donnant l'évolution d'un véhicule dans un réseau en connaissant l'évolution du reste du trafic. Ce script fait appel aux scripts *environment.py*, *state.py* et *lane_change.py*. Les scripts *construction_entrées_AV* et *construction_entrées_HD* permettent de créer les variables d'entrée de la fonction *general.py* pour 2 scénarios très simples. 

__POUR TESTER LE CODE__ il faut donc lancer le script *construction_entrées_AV* (ou *construction_entrées_HD*). Ensuite il faut appeler la fonction *general.py*: trajectories=general(ego_vehicle, Network, vehicles, t_simu_deb, t_simu_fin,tp, trajectories0). Il faut ensuite attendre un peu avant que le code retourne *trajectories* qui contient les états des véhicules à chaque instant de la simulation. Pour visualiser ces résultats on peut utiliser le script *figure_animation* qui montre l'évolution de ego_vehicle en fonction du temps ou le script *figure_trajectoires* qui trace le diagrammme espace-temps des véhicules. Ces scripts pour la visualisation ne marchent peut-être pas (la dernière fois que j'ai pu les tester ça marchait mais maintenant je n'arrive plus à utiliser matplotlib...).

# Description des variables, explication des fonctions et du modèle

Je vais expliquer dans cette section (pour ne pas surcharger les scripts), comment sont construites certaines variables et comment/pourquoi j'ai créée mes fonctions.


## Variables de *ego_vehicle*:

* Vehicle : (float : compris entre 1 et le nombre de véhicules simulés) numéro du véhicule dans la simulation (id)

* classe vehicle :(string= ‘HD’ ou ‘AV’ pour l’instant ) type de véhicule avec ‘HD’ pour Human Driver et ‘AV’ pour Autonomous Vehicle

* type vehicle : (string = ‘VL’, ‘Bus’ ou ‘PL’ pour l’instant) type de véhicule avec ‘VL’ pour un véhicule léger, ‘Bus’ pour… un bus et ‘PL’ pour un poids lourd

* agressivity 0 : (float = 50 pour les véhicules autonomes et compris entre 0 et 100 pour les conducteurs humains) représente l’aggressivité du véhicule. Plus ce nombre est élevé, plus le véhicule est aggressif dans sa façon de conduire. Plus il est faible, plus il est « timide ». Un véhicule possédant une agressivité de 50 conduira de manière « neutre » (i.e respectant les distance de sécurité idéales, les limites de vitesses...). L’aggressivité d’un véhicule détermine les paramètres de conduite suivants : la distance minimale avec le leader, la vitesse, l’accélération maximale et le time headway désirés par le véhicule. Plus un véhicule est aggressif (aggressivity > 50) plus sa distance minimale et son time headway sont faibles et plus sa vitesse désirée et son accélération maximale sont élevées. Et l’inverse pour un véhicule « timide ».

* reaction time : (float : = 0.5 pour un véhicule autonome et normalement distribué N(1.2 ;0.3) pour les conducteurs humains): temps de réaction en seconde du véhicule

* courtesy : (float : =50 pour un véhicule autonome et distribué sur 0-100 pour un conducteur humain) : paramètre utilisé dans la fonction *utility_courtesy*. Plus ce paramètre est élevé, plus le véhicule est « courtois », plus il considèrera l’impact de son changement de voie sur les autres utilisateurs : si le changement de voie fait « trop » ralentir les autres véhicules en comparaison à son gain personnel, le véhicule ne changera pas de voie. Un véhicule présentant un coefficient de courtoisie de 100 ne voudra pas faire ralentir les autres véhicules et ne changera pas de voie si c’est le cas. A l’inverse, un véhicule ayant 0 ne regardera pas du tout l’impact d’un changement de voie sur les autres véhicules.

* respect code de la route: (float : =100 pour un véhicule autonome et distribué sur 0-100 pour un conducteur humain): paramètre utilisé dans *utility_overtaking*. Il représente le désir de suivre la règle de non dépassement par la droite. Un véhicule dont le coefficient est 100 évitera le plus possible de doubler par la droite même si cela implique de ralentir. A l’inverse avec le coefficient 0, le conducteur doublera par la droite si ça lui permet d’atteindre sa vitesse désirée.

* road : (float : compris entre 1 et le nombre de routes dans le réseau (si il y a un double sens sur une route, ce sera considéré comme deux routes) : route sur laquelle se trouve le véhicule à l’instant t

* lane : (float: compris entre 1 et le nombre de voies sur la route): voie sur laquelle se trouve le véhicule à l’instant t. J’ai considéré que les voies étaient numérotées par ordre croissant de la gauche vers la droite (1= voie de gauche, 3= voie de droite)

* road turn : (float: compris entre 1 et le nombre de routes dans le réseau) : route sur laquelle le véhicule devra effectuer un tournant (pour suivre son itinéraire). Pour l’instant mon code ne gère pas le changement de route donc cette variable est inutile

* position turn : (float: compris entre 1 et le nombre de voies sur cette route): voie sur laquelle le véhicule devra effectuer un tournant (pour suivre son itinéraire). Pour l’instant mon code ne gère pas le changement de route donc cette variable est inutile

## Variables de *vehicles*

Les variables de *vehicles* sont exactement les mêmes que celles de *ego_vehicle*, en fait *ego_vehicle* est une ligne du tableau *vehicles*.

## Variables de *Network*

* road : (float: compris entre 1 et le nombre de routes du réseau) : numéro de la route (id)

* lane : (float: compris entre 1 et le nombre de voies sur la route considérée): numéro de la voie dans la route (j'ai considéré que les voies étaient numérotées par ordre croissant de la gauche vers la droite)

* vitesse limite : (float: compris entre 0 et 37) : vitesse limite (d'après la régulation) sur la voie en m/s.

## Autres variables d'entrée

* t_simu_deb/t_simu_fin (float: avec  5 < t_simu_deb < t_simu_fin) : temps de début/fin de la simulation en s. J'ai mis supérieur à 5 pour qu'au début de la simulation on puisse avoir des avoir des données sur les véhicules au temps t_simu_deb-temps de réaction

* tp (float: dans l'idéal compris entre 0.1 et 0.5) : pas de temps de la simulation en s

* trajectories (dataframe): contient les états (position, vitesse, accélération, road, lane) des véhicules à chaque instant entre 0 et t_simu_deb

# Explication du modèle

## Structure générale du modèle

