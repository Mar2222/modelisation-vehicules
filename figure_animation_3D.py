# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:42:00 2019

@author: mgtpe
"""

import numpy as np
from IPython import get_ipython
get_ipython().magic('matplotlib')
import matplotlib as mpl
mpl.interactive(True)
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


"""
animation avec une voiture
"""
x=trajectories[trajectories['vehicle']==2]['position']
x=x.values
y=trajectories[trajectories['vehicle']==2]['lane']*(-100)
y=y.values
t=trajectories[trajectories['vehicle']==2]['time']
t=t.values


fig, ax = plt.subplots(figsize=(4, 3))
ax.set(xlim=(0,3000 ), ylim=(-220, -80))
scat = ax.scatter(x[0], y[0],s=1000)

def animate(i):
    scat.set_offsets(np.c_[x[-i], y[-i]])
        

anim = FuncAnimation(fig, animate, interval=100, frames=len(t)-1, repeat=True)
fig.show()
