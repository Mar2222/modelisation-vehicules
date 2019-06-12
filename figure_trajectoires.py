# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:44:45 2019

@author: mgtpe
"""
import numpy as np
from IPython import get_ipython
get_ipython().magic('matplotlib')
import matplotlib as mpl
mpl.interactive(True)
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# permet de dessiner la position en fonction du temps et de la voie (le changement de couleur indique un changement de voie)

def pltcolor(a,lst):
    cols=[]
    for l in lst:
        if l==1:
            cols.append((0,0,0.2*a))
        elif l==2:
            cols.append((0,0.2*a,0))
        else:
            cols.append((0.2*a,0,0))
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
        plt.scatter(z,x,c=col)