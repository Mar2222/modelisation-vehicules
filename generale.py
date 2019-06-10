# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

import environment
import lane_change
import state

"""
fonction permettant de déterminer l'évolution d'un véhicule dans un réseau 

ENTREES:
    ego_vehicle (DataFrame): description du véhicule étudié (contient: 'vehicle', 'classe vehicule','type vehicule','aggressivity 0',
                    'reaction time', 'courtesy', 'respect code de la route', 'road','lane','road turn','lane turn','position turn')
    Network (DataFrame): description du réseau (contient: 'road', 'lane', 'vitesse limite')
    vehicles (DataFrame): description de tous les véhicules dans le réseau (contient la même chose que ego_vehicle)
    t_simu_deb/t_simu_fin/tp (float): temps de début/fin de simulation et pas de temps
    trajectories (DataFrame): donne les états des autres véhicules à chaque instant et de ego_vehicle pour l'initialistion (quelques pas de temps)
                    (contient: 'vehicle','time','position','vitesse','acceleration'road','lane')
SORTIE:
trajectories (DataFrame): donne les états de tous les véhicules à chaque instant

"""

def general(ego_vehicle, Network, vehicles, t_simu_deb, t_simu_fin,tp, trajectories) :   
    
    t=t_simu_deb
    tr_bis= (ego_vehicle.iloc[0]['reaction time']//tp)*tp #pour avoir un nombre entier de pas de temps dans tr_bis
    a_max=2 
    mAg=50 # aggressivité moyenne des véhicules , c'est l'aggressivité que les condcteurs attribuent aux autres véhicules? (cf af_sans et af_avec)
    
    while t<t_simu_fin:
        
        t=round(t,1) # étape obligatoire parce que python ne parvenait pas à trouver t dans les dataframes à cause de la façon dont il stock les nombres
        
###### recherche des états (position, vitesse, accélération) précédents (en t-tp) de ego_vehicle    

            
        a_prece=trajectories[(trajectories['vehicle']==ego_vehicle.iloc[0]['vehicle'])&(trajectories['time']==round(t,1))]
        a_prece=a_prece.iloc[0]['acceleration']
        v_prece=trajectories[(trajectories['vehicle']==ego_vehicle.iloc[0]['vehicle'])&(trajectories['time']==round(t,1))]
        v_prece=v_prece.iloc[0]['vitesse']
        x_prece=trajectories[(trajectories['vehicle']==ego_vehicle.iloc[0]['vehicle'])&(trajectories['time']==round(t,1))]
        x_prece=x_prece.iloc[0]['position']
        
####### recherche des caractérisitiques (classe de véhicule, route, voie, aggressivité...)de ego_vehicle:
        
        road=ego_vehicle.iloc[0]['road']
        lane=ego_vehicle.iloc[0]['lane']
        cv=ego_vehicle.iloc[0]['classe vehicule']
        Ag0=ego_vehicle.iloc[0]['aggressivity 0']
        R=ego_vehicle.iloc[0]['respect code de la route']
        ID_vehicle=ego_vehicle.iloc[0]['vehicle']
        
        
###### estimation des voies possibles (i.e sur lesquelles ego_vehicle peut aller) dans la route sur laquelle se trouve ego_vehicle    
        
        A=environment.adjoining_road(road,lane,Network)
      

####### premier cas: ego_vehicle peut seulement rester dans sa voie (il n'y a qu'une voie sur la route, ou il y a des restrictions de circulation sur les autres voies)
        
        if len(A)==1:
            leads=environment.leading_vehicles(x_prece, road, lane, cv, vehicles, trajectories, t) # on trouve les véhicules leaders de ego_vehicle
            a=state.HDM(ego_vehicle, leads, Network,trajectories, t-tr_bis, Ag0) # on calcule la nouvelle accélération donnée par la loi de poursuite HDM
          
####### deuxième cas: ego_vehicle a le choix entre plusieurs voies:
            
        else:
            # initialisation de variables
            Af_sans=[]
            Af_avec=[]
            Ae=[]
            Leaders=[]
            Followers=[]
            # calcul de l'aggresivité de ego_vehicle qui sera utilisée plus loin
            Ag=lane_change.aggressivity(Ag0, cv,x_prece, road, ego_vehicle.iloc[0]['position turn'],ego_vehicle.iloc[0]['road turn'], v_prece)# on récupère l'aggréssivité du véhicule

    #### pour chaque voie on va calculer les différentes accélérations (accélérations du vehicule follower avec et sans la présence de ego_vehicle dans la voie et accélération de ego_vehicle ) 
            for i in range(len(A)):
                #### dans chaque voie on cherche les véhicules leaders et le véhicule follower de ego_vehicle
                follow=environment.following_vehicle(x_prece, road, A[i], vehicles, trajectories,t)
                leads=environment.leading_vehicles(x_prece,road,A[i],cv,vehicles,trajectories, t) 

                #### on calcule les accélérations du véhicule follower dans la voie considérée avec et sans la présence de ego_vehicle dans la voie
                if follow==[]: #si il n'y a pas de follower (i.e. il n'y a pas d'impact sur le véhicule follower si ego_vehicle change de voie ou reste dans la voie)
                    af_sans=0
                    af_avec=0
                else: #si il y a un vehicule follower, on va calculer les accélérations des véhicules followers avec et sans la présence de ego_vehicle dans la voie
                    af_sans=state.HDM(vehicles[vehicles['vehicle']==follow],leads,Network, trajectories, t-tr_bis, mAg)# (dans la loi HDM on ne considère que l'impact d'un leader parce qu'on va dire que mon conducteur ne va pas anticiper avec plusieurs véhicules pour changer de voie)
                    af_avec=state.HDM(vehicles[vehicles['vehicle']==follow],[ID_vehicle], Network,trajectories, t-tr_bis, mAg) #le leader de follower devient ego_vehicle quand ego_vehicle est dans la voie
                
                #### on calcule ensuite l'accélération de ego_vehicle dans la voie considérée
                ae=state.HDM(ego_vehicle,leads, Network, trajectories, t-tr_bis, Ag)

                #### on garde en mémoire ces accélérations calculées et les véhicules followers/leaders trouvés
                Af_sans.append(af_sans)
                Af_avec.append(af_avec)
                Ae.append(ae)
                Leaders.append(leads)
                Followers.append(follow)  

        
    ##### pour chaque voie on va ensuite évaluer le safety criterion (grace aux accélérations calculées précédemment) et déterminer les voies dans lesquelles le véhicule peut aller:
            Possible_lane=[]
            sc=[]
            # on regarde tout d'abord si c'est sûr de rester dans la voie actuelle
            safe_stay=lane_change.safety_criterion(Ag,Ae[-1], Af_avec[-1])


            if cv=='HD' or (cv=='AV' and safe_stay==True): #si on a un HD ou on a un AV pour lequel le critère de sécurité est respecté si on reste dans la même voie:
                # on va juste regarder le critère de sécurité des autres voies 
                for j in range(len(A)-1):
                    safe=lane_change.safety_criterion(Ag,Ae[j],Af_avec[j])
         
                    if safe==True : # si c'est pas dangereux d'aller dans la voie j, on rajoute cette voie dans les voies possibles
                        Possible_lane.append(A[j])
                    else: # si c'est dangereux d'aller dans la voie j, on enlève cette voie des voies possibles et on l'enlève des listes qu'on va utiliser plus tard 
                        del Leaders[j]
                        del Followers[j]
                        del Ae[j]
                Possible_lane.append(A[-1]) #on rajoute dans les voies possibles la voie dans laquelle se trouve le véhicule
            
            else: # si le véhicule est autonome et qu'il ne peut pas rester dans sa voie, il faut comparer les dangers des autres voies à la voie actuelle
                for i in range(len(A)-1):
                    safe=lane_change.safety_criterion(Ag,Ae[i],Af_avec[i])
                    if safe== True:
                        Possible_lane.append(A[i])
                    else:
                        sc.append(Ae[i]+Af_avec[i])
                        del Leaders[j]
                        del Followers[j]
                        del Ae[j]

    ##### parmi les voies possibles (i.e. voies "safe") on choisit et on attribue sa nouvelle voie à ego_vehicle            
            if len(Possible_lane) == 0: # si aucune voie n'est "safe" pour le véhicule autonome (cas très rare), ego_vehicle va choisir la voie la "moins dangereuse"
                sc.append(Ae[-1]+Af_avec[-1])
                ind=sc.index(max(sc))
                lanea=sc[ind]
                a=Ae[ind] 
           
                
            elif len(Possible_lane)==1 : # si il n'y a qu'une seule voie "safe", ego_vehicle choisit cette voie
                lanea=Possible_lane[0]
                a=Ae[0] # on détermine la nouvelle accélération de ego_vehicle avec les accélérations calculées précedemment

                
            else: # si il y a plus d'une voie "safe", ego_vehicle choisit sa voie en fonction du calcul d'utilité sur toutes les voies
                l1=Leaders[-1]
                U=[]
                

                ### on définit les variables caractérisant le véhicule leader dans la voie d'ego_vehicle (ces variables sont ensuite utilisées dans le calcul d'utilité)
                if l1==[]: # ce qui est le cas si il y a aucun véhicule visible devant ego_vehicle sur la voie où il se trouve
                    xl1=10000
                    tv1='VL'
                else:   # si il y avait effectivement un véhicule leader sur la voie de ego_vehicle     
                    xl1=trajectories[(trajectories['vehicle']==l1)&(trajectories['time']==round(t,1))]
                    xl1=xl1.iloc[0]['position']
                    veh1=vehicles[vehicles['vehicle']==l1]
                    tv1=veh1.iloc[0]['type vehicule']
                    
                ### on va calculer pour chaque voie la fonction d'utilité    
                for k in range(len(Possible_lane)-1):
                    #on définit les variables caractérisant le leader dans la voie où ego_vehicle considère aller
                    l2=Leaders[k]
                    if l2==[]:
                        xl2=10000
                        lane2=lane
                        tv2='VL' 
                    else:
                        xl2=trajectories[(trajectories['vehicle']==l2)&(trajectories['time']==round(t,1))]
                        xl2=xl2.iloc[0]['position']
                        veh2=vehicles[vehicles['vehicle']==l2]
                        lane2=veh2.iloc[0]['lane']
                        tv2=veh2.iloc[0]['type vehicule']
                        
                    ### c'est ici qu'on calcule enfin les utilités marginales    
                    O=lane_change.utility_overtaking(xl1,xl2,lane,lane2,x_prece, R) #utilité marginale due aux règles pour doubler
                    T=lane_change.utility_truck(tv1,tv2, cv) #utilité marginale due à la présence de camion devant ego_vehicle
                    C=lane_change.utility_courtesy(Af_sans[k],Af_avec[k],Af_sans[-1], Af_avec[-1], ego_vehicle.iloc[0]['courtesy']) #U M due au fait que les conducteurs ne veulent pas forcément trop impacter le traffic
                    Tu=lane_change.utility_turn(x_prece, ego_vehicle.iloc[0]['position turn'],lane, ego_vehicle.iloc[0]['lane turn'], Possible_lane[k], ego_vehicle.iloc[0]['road turn'], road, cv, v_prece) # U M due à l'approche d'un tournant obligatoire
                    Bo=0.1 # bother_factor représente le fait qu'à deux utilités égales, le véhicules préférera rester dans sa voie et ne pas effectuer de manoeuvre supplémentaire
                    u=Ae[k]-Ae[-1]-C-T-O-Tu-Bo
                    U.append(u)
                U.append(0) # il faut rajouter l'utilité marginale pour rester dans la voie, qui est nulle
                rang_max=U.index(max(U))#parmi les choix de voies possibles, on choisit celle dont l'utilité marginale est maximale
                lanea=Possible_lane[rang_max] # on attribue la nouvelle voie 
                a=Ae[rang_max] # on a la nouvelle accélération (calculée précédemment)

###### une fois qu'on a la nouvelle voie, on majore l'acceleration par l'impact du seuil de perception (HD n'est pas capable de percevoir un changement infime dans l'accélération)                
       a=state.perception_threshold(a_prece,a)
                
####### on ajoute ensuite du bruit à l'accélération (dû à l'erreur de contrôle de la part de HD)
        a_fin=state.a_bruit(a,cv)
        
####### on majore cette nouvelle accélération par l'accélération max du véhicule        
        if a_fin>a_max:
            a_fin=a_max
        if a_fin<-a_max:
            a_fin=-a_max

###### on majore aussi par le jerk (qui représente la différence max d'accélération entre deux pas de temps)
        J=1.5*tp
        if abs(a_fin-a_prece)>J:
            a_fin=a_prece + np.sign(a_fin-a_prece)*J
        
            
###### on obtient ensuite les nouvelles variables d'état de ego_vehicle           
        v=state.vitesse(a_prece, v_prece,tp) 
        x=state.position(v_prece,x_prece,tp)
        
        t=t+tp #on passe au pas de temps suivant
        t=round(t,1)
        # on met à jour la table trajectories
        trajectories = pd.DataFrame(np.array([[ego_vehicle.iloc[0]['vehicle'],t, a_fin, v, x, ego_vehicle.iloc[0]['road'], lanea]]),columns=["vehicle", "time", "acceleration", "vitesse", "position", "road", "lane" ]).append(trajectories, ignore_index=True)

    return trajectories
