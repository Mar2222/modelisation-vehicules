# -*- coding: utf-8 -*-
"""
Created on Fri May 24 10:45:43 2019

@author: mgtpe
"""
import numpy as np
import pandas as pd

"""
les variables d'entrées sont: 
ego_vehicle:contient la vitesse en t-Tr, la position en t-Tr (longitudinale dans sa voie), la classe du véhicule (autonome ou pas),
l'agressivité du véhicule,... 
Network : décrit les voies et routes avec les vitesses max autorisées
leaders: "liste" des véhicules leaders qui seront considérés dans la loi de poursuite avec les informations suivantes:
vitesses en t-Tr, positions en t-Tr

les paramères sont:
  les paramètres de la loi HDM: a= acceleration max; delta (exposant); 
  les para de HDM dépendant du véhicule: b=comfortable deceleration (peut-être les mêmes pour tous...),T=time headway,
    s0=minimum gap
"""
#pour l'instant pas de projection prise en compte

# renvoie l'accélération calculée par le HDM 

def HDM(ego_vehicle, leaders, Network, trajectories, t, tr_bis):
    # paramètres
    delta=4
    s0=2
    a=2.2
    c=0
    T=2
    b=2
    #Ag= ego_vehicle.iloc[0]['aggressivity']
    #s0=s0*(1+0.1*(Ag-50)/50) # revoir les paramètres propres...
    v0=Network.loc[Network['road']== ego_vehicle.iloc[0]['road']] # on trouve la limitation de vitesse sur la route sur laquelle se trouve  la voiture
    v0=v0.iloc[0]['vitesse limite']
    ve=trajectories[(trajectories['vehicle']== ego_vehicle.iloc[0]['vehicle'])&(trajectories['time']==round(t-tr_bis,1))]
    ve=ve.iloc[0]['vitesse'] # on récupère la vitesse en t-Tr (Tr est celui de ego_vehicle)
    xe=trajectories[(trajectories['vehicle']==ego_vehicle.iloc[0]['vehicle'])&(trajectories['time']==round(t-tr_bis,1))]
    xe=xe.iloc[0]['position']
    a_free= a*(1-(ve/v0)**delta)
    a_int=0
    if leaders is None:
        print('leaders is none')
        a_mic=0
        return a_mic
    else:
        if len(leaders)==0: # si il n'y a pas de véhicule leader (i.e. free flow)
            a_mic=a*(1-(ve/v0)**delta)
            return a_mic

        else:  
            for i in range(0,len(leaders)): #calul du coefficient qui va pondérer l'impact des véhicules leaders sur la loi de poursuite. len(l) représente le nombre de leaders
                c=c+1/((i+1)**2)
            c=1/c
            for j in range(0,len(leaders)):
                vl=trajectories[(trajectories['vehicle']==leaders[j])&(trajectories['time']==round(t-tr_bis,1))]
                vl=vl.iloc[0]['vitesse']
                xl=trajectories[(trajectories['vehicle']==leaders[j])&(trajectories['time']==round(t-tr_bis,1))]
                xl=xl.iloc[0]['position']
                s1=s0 + max(0,ve*T+ve*(vl-ve)/(2*(a*b)**0.5))
                a_int=a_int - a*(s1/abs(xe-xl))**2
    
            a_mic=a_free + c*a_int
            return a_mic

"""
fonction basique de vitesse où on suppose l'accélération constante entre deux pas de temps 
"""

def vitesse(a_prece,v_prece,tp):
    return a_prece*tp+v_prece

"""
fonction basique de vitesse où on suppose l'accélération constante entre deux pas de temps 
"""

def position(v_prece,x_prece,tp):
    return v_prece*tp+x_prece

"""
entrées : a_precedent: l'accélération que le véhicule avait au pas de temps précédent
a_mic : l'accélération calculée par la loi de car-following pour le véhicule

paramètre : at= seuil de perception
"""

def perception_threshold(a_precedent, a_mic):
    at=0.1
    if abs(a_precedent-a_mic)>at: #si on dépasse le seuil fixé
        return a_mic
    else:
        return a_precedent

"""
entrées: a: l'accélération que choisit d'implémenter le véhicule, cv= la classe du véhicule
sortie: l'accélération finale (avec le bruit)

paramètre: limportance du bruit dans l'acceleration
"""
def a_bruit(a,cv):
    if cv is 'AV' or cv is 'CAV':
        return a
    else:
        a_b=0.1*np.random.randn(1) #nombre aléatoire de loi normale centrée réduite 
        #(choisir autre distribution aléatoire là ça impacte trop)
        a=(a+1)*a_b[0]
        return a
    