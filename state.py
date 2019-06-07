# -*- coding: utf-8 -*-
"""
Created on Fri May 24 10:45:43 2019

@author: mgtpe
"""
import numpy as np
import pandas as pd

"""
fonction permettant de calculer l'accélération d'un véhicule d'après la loi de poursuite HDM

ENTREES :
  ego_vehicle (DataFrame): description du véhicule considéré (ego_vehicle) (contient: (contient:'vehicle', 'classe vehicule',
             'type vehicule','aggressivity 0','reaction time', 'courtesy', 'respect code de la route', 'road', 
             'lane','road turn','lane turn','position turn')
  leaders (liste) : liste des ID des véhicules leaders de ego_vehicle
  Network (DataFrame) : description du réseau (contient: 'road','lane','vitesse limite')
  trajectories (DataFrame) : donne les états de tous les véhicules à chaque instant (contient: 'vehicle','time','position'
              ,'vitesse','acceleration'road','lane')
  to (float): instant considéré
  Ag (float): aggressivité de ego_vehicle


PARAMETRES:
    delta : parametre de la loi HDM, s0 : minimum gap, a_max: accélération max, T: time headway, b: comfortable deceleration

"""


def HDM(ego_vehicle, leaders, Network, trajectories, t0, Ag):
    # innitialisation des paramètres
    delta=4
    s0=2 #minimum gap
    a_max=2.2 #accélération max
    c=0
    T=2 # time headway
    b=2 # comfortable deceleration
    
    #on cherche les états du véhicules et de la route
    v0=Network.loc[Network['road']== ego_vehicle.iloc[0]['road']] # on trouve la limitation de vitesse sur la route sur laquelle se trouve  la voiture
    v0=v0.iloc[0]['vitesse limite']
    ve=trajectories[(trajectories['vehicle']== ego_vehicle.iloc[0]['vehicle'])&(trajectories['time']==round(t0,1))]
    ve=ve.iloc[0]['vitesse'] # on récupère la vitesse en t0 (=t-Tr par exemple)
    xe=trajectories[(trajectories['vehicle']==ego_vehicle.iloc[0]['vehicle'])&(trajectories['time']==round(t0,1))]
    xe=xe.iloc[0]['position']
    
    #impact de l'aggressivité sur les paramètres
    s0=s0*(1+0.1*(Ag-50)/50) 
    v0=v0*(1+0.25*(Ag-50)/50)
    a_max=a_max*(1+0.1*(Ag-50)/50)
    T=T*(1+0.1*(Ag-50)/50)
    
    #calcul de l'accélération idéale en free flow
    a_free= a_max*(1-(ve/v0)**delta)
    a_int=0
    
    if len(leaders)==0: # si il n'y a pas de véhicule leader (i.e. free flow)
      a_mic=a_free
      return a_mic

    else:  # si il y a des véhicules leader
      for i in range(0,len(leaders)): #calul du coefficient qui va pondérer l'impact des véhicules leaders sur la loi de poursuite. len(l) représente le nombre de leaders
        c=c+1/((i+1)**2)
      c=1/c
      for j in range(0,len(leaders)):
        # on cherche les vitesses et positions des véhicules leaders
        vl=trajectories[(trajectories['vehicle']==leaders[j])&(trajectories['time']==round(t0,1))]
        vl=vl.iloc[0]['vitesse']
        xl=trajectories[(trajectories['vehicle']==leaders[j])&(trajectories['time']==round(t0,1))]
        xl=xl.iloc[0]['position']
        # on calcule l'accélération due à la présence de chaque véhicule leader considéré
        s1=s0 + max(0,ve*T+ve*(vl-ve)/(2*(a_max*b)**0.5))
        a_int=a_int - a_max*(s1/abs(xe-xl))**2
      a_mic=a_free + c*a_int
      return a_mic

"""
fonction basique de calcul de vitesse où on suppose l'accélération constante entre deux pas de temps 

ENTREES:
  a_prece/v_prece (float): accélération/vitesse observée au pas de temps précédent
  tp: pas de temps
"""

def vitesse(a_prece,v_prece,tp):
    return a_prece*tp+v_prece

"""
fonction basique de calcul de la position où on suppose la vitesse constante entre deux pas de temps

ENTREES:
  v_prece/x_prece (float): vitesse/position observée au pas de temps précédent
  tp (float): pas de temps
"""

def position(v_prece,x_prece,tp):
    return v_prece*tp+x_prece

"""
fonction donnant la nouvelle accélération en considérant le seuil de perception

ENTREES :
  a_precedent (float): l'accélération que le véhicule avait au pas de temps précédent
  a_mic (float): l'accélération calculée par la loi de car-following pour le véhicule

PARAMETRES : at= seuil de perception
"""

def perception_threshold(a_precedent, a_mic):
    at=0.1
    if abs(a_precedent-a_mic)>at: #si on dépasse le seuil fixé
        return a_mic
    else:
        return a_precedent

"""
fonction permettant d'ajouter un bruit à l'accélération (due aux erreurs de controle de la part de HD)

ENTREES:
  a (float): accélération que choisit d'implémenter le véhicule
  cv (string): classe du véhicule

PARAMETRES:
  distribution aléatoire pour le bruit

SORTIE: 
  a (float): accélération réllement implémentée par le véhicule
"""
def a_bruit(a,cv):
    if cv is 'AV' or cv is 'CAV':
        return a
    else:
        a_b=0.1*np.random.randn(1) #nombre aléatoire de loi normale centrée réduite 
        #(choisir autre distribution aléatoire là ça impacte trop)
        a=(a+1)*a_b[0]
        return a
    
