# -*- coding: utf-8 -*-
"""
Created on Fri May 24 10:34:49 2019

@author: mgtpe
"""
import numpy as np
import pandas as pd


"""
fonction permettant de déterminer les voies adjacentes à la voie sur laquelle se trouve le véhicule
"""



def adjoining_road(road, lane, Network):
    route=Network.loc[Network['road']==road,:]
    droite=route.loc[route['lane']== lane+1, 'lane']   
    if droite.empty:
        d=0
    else:
        d=1
    
    gauche= route.loc[route['lane']== lane-1, 'lane']
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
permet de déterminer le véhicule follower dans la voie considérée
"""


def following_vehicle(xv, road, lane, vehicles, trajectories,t):
    follower1=trajectories[(trajectories['road']==road)&(trajectories['lane']==lane)]
    follower1=follower1[(follower1['position']<xv)&(follower1['time']==t)]
 #le -0.1 a été rajouté parce que sinon des fois ego_vehicule est considéré comme son propre follower
    follower1=follower1.sort_values(by = 'position')
    follower=[]
    if follower1.empty:
        return follower
        
    else:
        follower.append(follower1.iloc[0]['vehicle'])
    return follower

"""
fonction qui permet de déterminer les véhicules leaders considérés dans le calcul de l'accélération 

entrées: 
xv= position vehicule dans sa voie (longitudinale); Lane= voie dans laquelle on le considère; 
road= route sur laquelle il est; cv= classe du véhicule (AV, CAV, HD CHD); vehicles= liste des véhicles se trouvant 
avec les informations sur leur position (sur quelle route et dans quelle voie) et leur classe

Parametres : distances (pour le VA et le HD) pour lesquelles on prend en compte des véhicules; nombre de véhicules max 
 
"""

#en ne considérant que t je me retrouve avec mon ego_véhicule dans les véhicules leaders (il est son propre leader) 
def leading_vehicles(xv, road, lane, cv, vehicles, trajectories,t):
    
    leaders1=trajectories[(trajectories['road']==road)&(trajectories['lane']==lane)&(trajectories['time']==round(t,1))]
    #considérée (par forcément dans la voie où se trouve notre véhicule)
    Dh= 200 #distance considérée par un conducteur humain, peut-être une distance dépendant de la vitesse du véhicule
    Da= 200 #distance considérée par un véhicule autonome
    Dc= 500 # distance considérée pour la communication
    nHD= 3  #nombre maximum de véhicules considérés par HD
    
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
"""        
   # revoir je pense que c'est un peu n'importe quoi  
    if cv is 'CAV':
        leaders1=leaders1.loc[leaders1['position']>xv]
        leaders1=leaders1.loc[leaders1['position']< Da+xv]
        leaders1=leaders1.sort_values(by='position')
        leaders1=vehicles.loc[vehicles['vehicle']==leaders1.iloc[0]['vehicle']]
        leaders2=leaders1.loc[leaders1['position']>xv]
        leaders2=leaders2.loc[leaders2['position']<Dc+xv]
        leaders2=leaders2.loc[leaders2['communication']==True]
        leaders3=pd.concact([leaders1,leaders2],ignore_index=True)
        leaders=vehicles.loc[vehicles['vehicle']==leaders3['vehicle']]
        return leaders
    
    else:
        print('error class')
"""