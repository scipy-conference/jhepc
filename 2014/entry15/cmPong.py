'''
PONG colormaps.
'''

import numpy as np
from matplotlib import cm, colors
import matplotlib.pyplot as plt

def salinity(cmap='YlGnBu_r', levels=(37-np.exp(np.linspace(0,np.log(36.), 10)))[::-1]-1):
    '''
    Colormap for salinity for river plumes, with bigger chunks of salinity per color
    section at lower salinity than higher.
    Help from http://wiki.scipy.org/Cookbook/Matplotlib/Show_colormaps

    Kristen Thyng, Feb 2014

    Inputs:
        cmap        Colormap name to use, e.g. 'YlGnBu'
        levels      edges of colors, as in contourf, to stretch 
                    colormap. e.g. for salinity
                    levels = (37-exp(linspace(0,log(36.), 10)))[::-1]-1

    Outputs:
        my_cmap     colormap instance
    '''

    N = levels.size

    # Colors on either side of the edges
    rgb0 = cm.get_cmap(cmap)(np.linspace(0.0, 1.0, N))[:,0:3]

    red = np.vstack((levels/levels.max(), 
                    rgb0[:,0], 
                    rgb0[:,0])).T
    red = tuple(map(tuple, red))

    green = np.vstack((levels/levels.max(), 
                    rgb0[:,1], 
                    rgb0[:,1])).T
    green = tuple(map(tuple, green))

    blue = np.vstack((levels/levels.max(), 
                    rgb0[:,2], 
                    rgb0[:,2])).T
    blue = tuple(map(tuple, blue))

    cdict = {'red':red, 'green':green, 'blue':blue}

    my_cmap = colors.LinearSegmentedColormap('my_colormap', cdict, 256)

    return my_cmap


def test(cmap):
    '''
    Test colormap.
    '''

    plt.figure()
    plt.pcolor(np.random.rand(10,10), cmap=cmap)
    cb = plt.colorbar()
