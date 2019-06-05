# -*- coding: utf-8 -*-
"""
Created on Tue May 28 13:49:17 2019

@author: mgtpe
"""

"""
pour observer les trajectoires
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



# permet de dessiner la position en fonction du temps et de la voie (le changement de couleur indique un changement de voie)

def pltcolor(a,lst):
    cols=[]
    for l in lst:
        if l==1:
            cols.append((0,0,0.1*a))
        elif l==2:
            cols.append((0,0.1*a,0))
        else:
            cols.append((0.1*a,0,0))
    return cols
# Create the colors list using the function above


def traj(trajectories, vehicles):
    for i in range(len(vehicles)):
        x=trajectories[trajectories['vehicle']==i+1]['position']
        x=x.values
        y=trajectories[trajectories['vehicle']==i+1]['lane']
        y=y.values
        col=pltcolor(i+1,y)
        z=trajectories[trajectories['vehicle']==i+1]['time']
        z=z.values
       # cm = plt.cm.get_cmap('RdYlBu')
        plt.scatter(z,x,c=col) #,cmap=cm)
    #plt.colorbar(sc)
    

"""
col=['b','b','b','b','b','b','b','r']


# en 3D, pour l'instant c'est pas plus clair...

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def traj3D(trajectories, vehicles):
    fig = figure()
    ax = Axes3D(fig)
    for i in range(len(vehicles)):
        x=trajectories[trajectories['vehicle']==i+1]['position']
        x=x.values
        y=trajectories[trajectories['vehicle']==i+1]['lane']
        y=y.values
        z=trajectories[trajectories['vehicle']==i+1]['time']
        z=z.values
        ax.scatter(x, y, z, c=col[i])
      
        
fig = figure()
ax = Axes3D(fig)


ax.scatter(y, x, z)
show()
Axes3D.scatter(x, y, z)

"""