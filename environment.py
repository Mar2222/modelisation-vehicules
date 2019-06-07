# -*- coding: utf-8 -*-
"""
Created on Fri May 24 10:34:49 2019

@author: mgtpe
"""

import numpy as np
import pandas as pd


"""
fonction permettant de déterminer les voies possibles (sur lesquelles le véhicule peut aller)
depuis une voie considérée (i.e sur laquelle se trouve le véhicule)

ENTREES: 
    road (float)= numéro de la route considérée 
    lane (float)= numéro de la voie considérée
    Network (Dataframe)= description du réseau (contient pour l'instant: 'road', 'lane', 'vitesse limite')

SORTIE:
    adjoining (liste)= liste des voies sur lesquelles le véhicule peut aller 
    (la voie sur laquelle se trouve le véhicule est le dernier élément de la liste)
"""



def adjoining_road(road, lane, Network):
    route=Network.loc[Network['road']==road,:]
    droite=route.loc[route['lane']== lane+1, 'lane'] 
    gauche= route.loc[route['lane']== lane-1, 'lane']
    
    if droite.empty:
        d=0
    else:
        d=1  

    if gauche.empty:
        g=0
    else:
        g=1 
    
    if d==1 and g==1:
        adjoining=[lane-1, lane+1, lane]
    if d==0 and g==1:
        adjoining=[lane-1, lane]
    if d==1 and g==0:
        adjoining=[lane+1, lane]
    if d==0 and g==0 :
        adjoining=[lane]
        
    return adjoining

"""
permet de déterminer le véhicule follower dans la voie considérée, à l'instant donné

ENTREES:
    xv (float)= position de ego_vehicle au temps t
    road (float)= numéro de la route considérée (i.e sur laquelle se trouve ego_vehicle)
    lane (float)= numéro de la voie considérée (pas forcément celle sur laquelle se trouve ego_vehicle)
    trajectories (DataFrame)= contient les états de tous les véhicules à chaque instant (contient: 'vehicle',
     'time', 'acceleration', 'vitesse', 'position', 'road', 'lane')
    t (float)= instant considéré

SORTIE :
    follower (list): liste retournant le follower sur la voie considérée
"""


def following_vehicle(xv, road, lane, vehicles, trajectories,t):
    follower1=trajectories[(trajectories['road']==road)&(trajectories['lane']==lane)]
    follower1=follower1[(follower1['position']<xv)&(follower1['time']==t)]
    follower1=follower1.sort_values(by = 'position')
    follower=[]
    if follower1.empty:
        return follower
        
    else:
        follower.append(follower1.iloc[0]['vehicle'])
    return follower

"""
fonction qui permet de déterminer les véhicules leaders considérés dans le calcul de l'accélération de la loi HDM

ENTREES: 
    xv (float): position de ego_vehicle au temps t
    road (float): numéro de la route sur laquelle se trouve ego_vehicle
    lane float): numéro de la voie considérée (pas forcément la voie où se trouvae ego_vehicle) 
    cv (string): classe de ego_vehicle (AV, HD)
    vehicles (DataFrame): description des véhicules présant sur le réseau (contient:'vehicle', 'classe vehicule',
             'type vehicule','aggressivity 0','reaction time', 'courtesy', 'respect code de la route', 'road', 
             'lane','road turn','lane turn','position turn') 
    trajectories (DataFrame): contient les états de tous les véhicules à chaque instant (contient: 'vehicle',
                 'time', 'acceleration', 'vitesse', 'position', 'road', 'lane')
    t (float): instant considéré

PARAMETRES :
    Dh: distance jusqu'à laquelle le véhicule autonome perçoit un véhicule leader (peut-être à faire dépendant de la vitesse)
    Da: distance jusqu'à laquelle le conducteur humain perçoit un véhicule leader (peut-être à faire dépendant de la vitesse)
    nHD: nombre max de véhicules considérés par un conducteur humain

SORTIE :
    leaders (list): liste des véhicules leaders d ego_vehicle dans la voie considérée
"""


def leading_vehicles(xv, road, lane, cv, vehicles, trajectories,t):
    
    Dh= 200 
    Da= 200 
    nHD= 3
    
    leaders1=trajectories[(trajectories['road']==road)&(trajectories['lane']==lane)&(trajectories['time']==round(t,1))]
    leaders=[]
    
    if cv is 'HD':
        leaders1=leaders1.loc[leaders1['position']>xv] #on prend les véhicules devant ego_véhicule...
        leaders1=leaders1.loc[leaders1['position']<Dh+xv] # ... mais aussi ceux qui ne sont pas trop loin
        leaders1=leaders1.sort_values(by = 'position')
        nb_vehicles=min(nHD,len(leaders1))
        leaders=[]

        
        if nb_vehicles==0:
            leaders=[]
        
        if nb_vehicles==1: # on choisit pas plus des trois premiers (mais il faut trier par distance avant ça)
            leads=vehicles.loc[vehicles['vehicle']==leaders1.iloc[0]['vehicle']]
            leaders.append(leads.iloc[0]['vehicle'])
           
    
        if nb_vehicles==2:
            leads2=vehicles.loc[vehicles['vehicle']==leaders1.iloc[0]['vehicle']]
            leads3=vehicles.loc[vehicles['vehicle']==leaders1.iloc[1]['vehicle']]
            leaders.append(leads2.iloc[0]['vehicle'])
            leaders.append(leads3.iloc[0]['vehicle'])
            

        if nb_vehicles==3:
            leads2=vehicles.loc[vehicles['vehicle']==leaders1.iloc[0]['vehicle']]
            leads3=vehicles.loc[vehicles['vehicle']==leaders1.iloc[1]['vehicle']]
            leads4=vehicles.loc[vehicles['vehicle']==leaders1.iloc[2]['vehicle']]
            leaders.append(leads2.iloc[0]['vehicle'])
            leaders.append(leads3.iloc[0]['vehicle'])
            leaders.append(leads4.iloc[0]['vehicle'])
          
        
    cv='AV'    
    if cv is 'AV':
        leaders=[]
        leads=leaders1.loc[leaders1['position']>xv]
        leads=leads.loc[leads['position']< Da+xv]
        leads=leads.sort_values(by='position') # on choisit seulement le premier véhicule
        if leads.empty:
            leaders=[]
        else:
            leaders.append(leads.iloc[0]['vehicle'])
    return leaders
