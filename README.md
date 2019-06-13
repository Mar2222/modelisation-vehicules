# Présentation du projet modelisation-vehicules

Ce projet vise à coder le comportement d'un véhicule (appelé ego_vehicle) dans un réseau. Ce comportement est défini par la loi de poursuite HDM (Human Driving Model) et un changement de voie particulier. Ce modèle intègre notamment des différences entre les vehicules autonomes et les conducteurs humains. J'ai créée cet algorithme de façon à ce qu'on puisse enlever/ajouter facilement des parties du modèle (d'où le nombre important de petites fonctions qui sont appelées). Le but est ensuite de pouvoir intégrer ce modèle dans un simulateur pour voir l'évolution de nombreux véhicules dans un réseau complexe. 


# Utilisation

Les scripts sont plutôt longs mais c'est parce qu'avant chaque fonction je spécifie les variables d'entrée, de sortie et les paramètres.
Le script *general.py* permet de lancer la fonction donnant l'évolution d'un véhicule dans un réseau en connaissant l'évolution du reste du trafic. Ce script fait appel aux scripts *environment.py*, *state.py* et *lane_change.py*. Les scripts *construction_entrées_AV* et *construction_entrées_HD* permettent de créer les variables d'entrée de la fonction *general.py* pour 2 scénarios très simples. 

__POUR TESTER LE CODE__ il faut donc lancer le script *construction_entrées_AV* (ou *construction_entrées_HD*). Ensuite il faut appeler la fonction *general.py*: trajectories=general(ego_vehicle, Network, vehicles, t_simu_deb, t_simu_fin,tp, trajectories0). Il faut ensuite attendre un peu avant que le code retourne *trajectories* qui contient les états des véhicules à chaque instant de la simulation. Pour visualiser ces résultats on peut utiliser le script *figure_animation* qui montre l'évolution de ego_vehicle en fonction du temps ou le script *figure_trajectoires* qui trace le diagrammme espace-temps des véhicules. Ces scripts pour la visualisation ne marchent peut-être pas (la dernière fois que j'ai pu les tester ça marchait mais maintenant je n'arrive plus à utiliser matplotlib...).


# Explication du modèle et de l'algorithme

L'algorithme détermine à chaque pas de temps le nouvel état de ego_vehicule. Pour cela il détermine d'abord si ego_vehicule peut changer de voie (safety criterion) et si c'est le cas si il veut changer de voie (utility criterion). Avec ces informations l'algorithme fournit la nouvelle voie de ego_vehicle. Une fois qu'on a la nouvelle voie de ego_vehicle l'algorithme calcule sa nouvelle accélération grâce à la loi de poursuite HDM. On détermine ensuite sa nouvelle position et vitesse grâce aux états précedents.

## Modèle de changement de voie

Pour déterminer la nouvelle voie de ego_vehicle, l'algorithme va tout d'abord regarder si il y a des voies adjacentes à la voie actuelle (à l'aide de la fonction *adjoining_road*) sur lesquelles ego_vehicle peut aller. Si ce n'est pas le cas, ego_vehicle reste sur sa voie et on passe tout de suite à l'évaluation de son accélération. Sinon on va évaluer la "dangerosité" des différentes voies possibles.

### Changement de voie : Safety criterion

L'algorithme va ensuite regarder dans chaque voie possible le critère de sécurité. Pour qu'une voie soit sûre il faut que les accélérations, de ego_vehicle et de son véhicule follower (trouvé à l'aide de la fonction *following_vehicle*) dans cette voie, soient supérieures à une décélération limite (bsafe). Si une des accélérations est inférieure à bsafe ça veut dire que, si ego_vehicle se trouvait dans cette voie, un des deux véhicule devrait freiner trop brusquement pour éviter une collision et donc que la voie est dangereuse. Les accélérations des véhicules dans les différentes voies sont calculées à l'aide de la loi de poursuite HDM. 

Une fois qu'on a regardé la "dangerosité" de chaque voie, il y a trois cas possibles: 
  * Premier cas (cas extrèmement rare): toutes les voies sont dangereuses. Dans ce cas, j'ai décidé de différencier le comportement du véhicule autonome de celui du conducteur humain. J'ai considéré qu'un conducteur humain n'aurait pas le temps de réfléchir dans ce cas et, par reflexe, braquerait en restant dans sa voie. Sa nouvelle voie est donc sa voie actuelle. J'ai considéré en revanche qu'un véhicule autonome comparerait les "niveaux de dangerosité" et irait dans la voie la moins dangereuse. Dans ce cas, une fois qu'on a déterminé la nouvelle voie, on passe au calcule de l'accélération de ego_vehicle d'après la loi HDM.
  * Deuxième cas (cas rare): une seule voie est sûre. Dans ce cas cette voie devient la nouvelle voie de ego_vehicle et on passe directement au calcul de son accélération.
  * Troisième cas (cas le plus courant): il y a plusieurs voies sûres. Pour choisir la nouvelle voie, on va déterminer la voie présentant le plus "grand gain" avec le critère d'utilité (utility criterion).

### Changement de voie : Utility criterion

Pour déterminer la nouvelle voie parmi les voies sûres, on va regarder l'utilité marginale de chaque voie possible. Ce modèle peut se comprendre de la manière suivante : un véhicule va changer de voie si il "gagne" plus qu'en restant dans la voie actuelle. L'utilité marginale représente la différence entre les gains de la voie actuelle et de la voie considérée. J'ai considéré que cette utilité marginale était égale à : (l'accélération de ego_vehicle dans la voie cosidérée) - (l'accélération de véhicule dans la voie actuelle) - (les contraintes liées au changement de voie). Le calcul des accélération se fait encore une fois à l'aide de la loi de poursuite HDM.

Pour les contraintes liées au changement de voie, j'ai choisi de considéré les éléments suivants (attention les "contraintes" peuvent être positives ou négatives):
  * courtoisie (calculé avec *utility_courtoisie*): un véhicule regardera (plus ou moins, en fonction de son coefficient de courtoisie) si changer de voie fera trop ralentir les autres véhicules dans le réseaux
  * les règles de dépassement (i.e en Europe on ne peut pas doubler par la droite) (calculé avec *utility_overtaking*) : un véhicule essaiera (plus ou moins, en focntion de son coefficient de respect du code de la route) de respecter cette règle de dépassement
  * la présence d'un poids lourd/bus comme véhicule leader (calculé avec *utility_truck*) : j'ai considéré qu'un véhicule autonome ne se préoccupera pas du type de véhicule de son véhicule leader. En revanche, j'ai considéré qu'un conducteur humain préférera avoir un véhicule léger devant lui pour avoir une meilleure visibilité.
  * la distance à un tournant obligatoire (calculé par *utility_turn*) : à l'approche d'un tournant obligatoire, le véhicule va essayer de plus en plus de se placer sur la voie lui permettant de tourner/de changer de route/de prendre la sortie qu'il souhaite et va éviter les voies qui l'éloigne de ce tournant. J'ai considéré que le véhicule autonome pouvait prendre en compte le tournant un peu plus tôt que le conducteur humain.
  * l'"énergie demandée pour tournée" (représenté par le coefficient *Bo*): ce coefficient représente le fait qu'à utilités égales le véhicule évitera d'effectuer une manoeuvre inutile est préfèrera rester dans sa voie. Ce coefficient permet d'éviter d'avoir des changements de voie trop fréquents.
  
Une fois qu'on a les utilités marginales de chaque voie (l'utilité marginale de la voie actuelle étant 0), on choisit l'utilité marginale maximale qui nous donne donc la nouvelle voie de ego_vehicle.

## Loi de poursuite HDM

La loi de poursuite considérée est la loi de poursuite HDM. Cette loi de poursuite calcule l'accélération de ego_vehicle à l'aide d'une équation différentielle différée qui prend en compte le temps de réaction de ego_vehicle. Cette loi de poursuite prend aussi en compte l'aggressivité de ego_vehicle (calculée avec la fonction *aggressivity*). Enfin cete loi considère les différents leaders de ego_vehicle. Les leaders de ego_vehicle sont trouvés à l'aide de la fonction *leading_vehicles* et dépendent de la classe du véhicule. Pour l'instant j'ai considéré qu'un véhicule autonome ne pouvait détecter (grâce à sa caméra) que le véhicule juste devant lui alors qu'un conducteur humain peut voir et prendre en compte jusqu'à 3 véhicules leaders. (Dans un prochain temps j'ajouterai la communication V2V et le véhicule autonome pourra prendre en compte plus de véhicules). 

La loi de poursuite HDM utilise les états (position, vitesse) des véhicules (ego_vehicle et véhicules leaders) à l'instant t-Tr et l'aggressivité de ego_vehicule pour déterminer l'accélération au temps t de ego_vehicle.

## Autres fonctions

Une fois qu'on a l'accélération de ego_vehicle calculée avec la loi de poursuite, j'ai considéré deux facteurs humains qui modifiaient un peu l'accélération:
  * le seuil de perception (fonction *perception_threshold*) : j'ai considéré que le conducteur humain ne pouvait pas remarquer une différence infime d'accélération. Donc si l'accélération de ego_vehicle au pas de temps précédent est trop proche de celle calculée par la loi HDM, le conducteur va garder l'accélération précédente.
  * l'erreur de contrôle (fonction *a_bruit*) : j'ai considéré qu'étant donné une accélération désirée, l'être humain ne pourra jamais appliquer un contrôle parfait sur le véhicule permettant d'atteindre cette accélération. J'ajoute donc un bruit à l'accélération.
  
L'algorithme ajoute une autre contrainte à l'accélération calculée qui est une contrainte physique du véhicule. Cette contrainte (calculée par la fonction *a_jerk*) exprime le fait que le véhicule a une dérivée de l'accélération bornée (i.e. ne peut pas avoir une différence d'accélération trop importante en un pas de temps).

Tout ceci nous donne l'accélération finale de ego_vehicle à l'instant t.

Ensuite, l'algorithme calcule la vitesse et la position au temps t grâce à l'état du véhicule à l'instant t-tp (avec les fonctions *vitesse* et *position*).

Enfin l'algorithme mets à jour la table des trajectoires et passe au pas de temps t+tp.

## Commentaire

Si vous avez bien suivi la structure de l'algorithme, bien que je présente d'abord le changement de voie puis le calcul de l'accélération, dans l'algorithme les calculs des accélérations se font d'abord parce que ceux-ci sont nécessaires pour déterminer la nouvelle voie. Une fois qu'on a la nouvelle voie on attribue à ego_vehicle l'accélération déjà calculée précedemment dans cette voie. 

# Description des variables

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
