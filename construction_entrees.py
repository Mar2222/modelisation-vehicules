# -*- coding: utf-8 -*-
"""
Created on Wed May 29 10:45:01 2019

@author: mgtpe
"""
import pandas as pd
import numpy as np

import environment
import lane_change
import state

from scipy import arange  

tp=0.1
t_simu_deb=11
t_simu_fin=90



"""
#test une voie infinie avec 2 véhicules:

vehicles = {'vehicle':[1,2], 'classe vehicule':['HD','HD'],'aggressivity 0':[50,50], 'aggressivity':[50,50], 'reaction time':[1,1], 'courtesy':[50,50], 'respect code de la route':[50,50], 'road': [1, 1], 'lane': [1, 1],'road turn':[3,3],'lane turn':[1,1], 'position turn':[100,300]}
vehicles=pd.DataFrame(data=vehicles)
Network={'road':[1],'lane':[1],'vitesse limite':[30]} #vitesse de 110km/h
Network=pd.DataFrame(data=Network)
trajectories0={'vehicle':[1], 'time':[0], 'acceleration':[0], 'vitesse':[28], 'position':[100], 'road':[1], 'lane':[1] }
trajectories0=pd.DataFrame(data=trajectories0)
ego_vehicle=vehicles.loc[vehicles['vehicle']==2]

for i in arange(t_simu_deb-10,t_simu_fin+1,0.1):
    trajectories0 = pd.DataFrame(np.array([[1,round(i,1), 0, 28, 250+i*28, 1, 1]]),columns=["vehicle", "time", "acceleration", "vitesse", "position", "road", "lane" ]).append(trajectories0, ignore_index=True)
    
for j in arange (0,11.1,0.1):
    trajectories0 = pd.DataFrame(np.array([[2,round(j,1), 0, 29, j*29, 1, 1]]),columns=["vehicle", "time", "acceleration", "vitesse", "position", "road", "lane" ]).append(trajectories0, ignore_index=True)
#for k in arange(0.1,10,0.1):
 #   c=round(k,1)
  #  print(c)


#test avec le changement de voie, route infinie avec 2 voies
vehicles = {'vehicle':[1,2,3,4,5,6,7,8], 'classe vehicule':['HD','HD','AV','AV','HD','HD','HD','AV'],'type vehicule':['VL','VL','VL','VL','VL','PL','VL','VL'],'aggressivity 0':[50,50,50,50,50,50,50,50], 'aggressivity':[50,50,50,50,50,50,50,50], 'reaction time':[1,1,0.5,0.5,1,1,1,0.5], 'courtesy':[50,50,50,50,50,50,50,50], 'respect code de la route':[50,50,50,50,50,50,50,50], 'road': [1, 1, 1, 1, 1, 1, 1, 1], 'lane': [1, 2, 1, 2, 1, 2, 2, 2],'road turn':[3,3,3,3,3,3,3,3],'lane turn':[1,1,1,1,1,1,1,1], 'position turn':[1,1,1,1,1,1,1,1]}
vehicles=pd.DataFrame(data=vehicles)
#vitesse limite=110km/h <=> 30m/s
Network={'road':[1,1],'lane':[1,2],'vitesse limite':[30,30]}
Network=pd.DataFrame(data=Network)
trajectories0={'vehicle':[1], 'time':[0], 'acceleration':[0], 'vitesse':[25], 'position':[0], 'road':[1], 'lane':[1] }
trajectories0=pd.DataFrame(data=trajectories0)
position_initiale=[500,750,900,1100,1200,1400,1500]

for i in range(0,6):
    p=position_initiale[i]
    lane=vehicles[vehicles['vehicle']==i+1]
    lane=lane.iloc[0]['lane']
    for j in arange(t_simu_deb-10, t_simu_fin+1, 0.1):
        trajectories0 = pd.DataFrame(np.array([[i+1,round(j,1), 0, 25, p+j*25, 1, lane]]),columns=["vehicle", "time", "acceleration", "vitesse", "position", "road", "lane" ]).append(trajectories0, ignore_index=True)
        
for k in arange (0,11.1,0.1):
    trajectories0 = pd.DataFrame(np.array([[8,round(k,1), 0, 29, 250+k*29, 1, 1]]),columns=["vehicle", "time", "acceleration", "vitesse", "position", "road", "lane" ]).append(trajectories0, ignore_index=True)

ego_vehicle=vehicles.loc[vehicles['vehicle']==8]
t=t_simu_deb
tr_bis= ego_vehicle.iloc[0]['reaction time']
a_max=2

"""

#test avec le changement de voie, route infinie avec 2 voies, avec 2 véhicules
vehicles = {'vehicle':[1,2,3,4,5,6,7,8], 'classe vehicule':['HD','HD','AV','AV','HD','HD','HD','AV'],'type vehicule':['VL','VL','VL','VL','VL','PL','VL','VL'],'aggressivity 0':[50,50,50,50,50,50,50,50], 'aggressivity':[50,50,50,50,50,50,50,50], 'reaction time':[1,1,0.5,0.5,1,1,1,0.5], 'courtesy':[50,50,50,50,50,50,50,50], 'respect code de la route':[50,50,50,50,50,50,50,50], 'road': [1, 1, 1, 1, 1, 1, 1, 1], 'lane': [1, 2, 1, 2, 1, 2, 2, 2],'road turn':[3,3,3,3,3,3,3,3],'lane turn':[1,1,1,1,1,1,1,1], 'position turn':[1,1,1,1,1,1,1,1]}
vehicles=pd.DataFrame(data=vehicles)
#vitesse limite=110km/h <=> 30m/s
Network={'road':[1,1],'lane':[1,2],'vitesse limite':[30,30]}
Network=pd.DataFrame(data=Network)
trajectories0={'vehicle':[1], 'time':[0], 'acceleration':[0], 'vitesse':[25], 'position':[0], 'road':[1], 'lane':[1] }
trajectories0=pd.DataFrame(data=trajectories0)
position_initiale=[500,750,600,1100,1200,1400,1500]


p=position_initiale[2]
lane=vehicles[vehicles['vehicle']==2]
lane=lane.iloc[0]['lane']
for j in arange(t_simu_deb-10, t_simu_fin+1, 0.1):
    trajectories0 = pd.DataFrame(np.array([[2,round(j,1), 0, 25, p+j*25, 1, lane]]),columns=["vehicle", "time", "acceleration", "vitesse", "position", "road", "lane" ]).append(trajectories0, ignore_index=True)
        
for k in arange (0.1,11.1,0.1):
    trajectories0 = pd.DataFrame(np.array([[8,round(k,1), 0, 29, 250+k*29, 1, 1]]),columns=["vehicle", "time", "acceleration", "vitesse", "position", "road", "lane" ]).append(trajectories0, ignore_index=True)

ego_vehicle=vehicles.loc[vehicles['vehicle']==8]
t=t_simu_deb
tr_bis= ego_vehicle.iloc[0]['reaction time']
a_max=10
