# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:06:34 2019

@author: mgtpe
"""

import pandas as pd
import numpy as np
from scipy import arange  

tp=0.1
t_simu_deb=11
t_simu_fin=100


#### test avec le changement de voie, route infinie avec 2 voies, avec 2 véhicules avec un véhicule autonome

vehicles = {'vehicle':[1,2], 'classe vehicule':['HD','HD'],'type vehicule':['VL','VL'],'aggressivity 0':[50,50],'reaction time':[1,0.5], 'courtesy':[50,50], 'respect code de la route':[50,100], 'road': [1, 1], 'lane': [2, 2],'road turn':[3,3],'lane turn':[1,1], 'position turn':[1,1]}
vehicles=pd.DataFrame(data=vehicles)
Network={'road':[1,1],'lane':[1,2],'vitesse limite':[30,30]}
Network=pd.DataFrame(data=Network)
trajectories0={'vehicle':[1], 'time':[0], 'acceleration':[0], 'vitesse':[25], 'position':[0], 'road':[1], 'lane':[2] }
trajectories0=pd.DataFrame(data=trajectories0)
for j in arange(t_simu_deb-10, t_simu_fin+1, 0.1):
    trajectories0 = pd.DataFrame(np.array([[1,round(j,1), 0, 25, 300+j*25, 1, 2]]),columns=["vehicle", "time", "acceleration", "vitesse", "position", "road", "lane" ]).append(trajectories0, ignore_index=True)
        
for k in arange (0.1,11.1,0.1):
    trajectories0 = pd.DataFrame(np.array([[2,round(k,1), 0, 29, k*29, 1, 1]]),columns=["vehicle", "time", "acceleration", "vitesse", "position", "road", "lane" ]).append(trajectories0, ignore_index=True)
ego_vehicle=vehicles.loc[vehicles['vehicle']==2]