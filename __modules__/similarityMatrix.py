#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 11:44:45 2022

@author: dmytrenko.o
"""
import networkx as nx
import numpy as np
import matplotlib.pylab as plt

import pandas as pd
from scipy.spatial.distance import euclidean, pdist, squareform
    
    
def similarity_func(u, v):
    return 1/(1+euclidean(u,v))

def euclidianSimilyrity(df):
    dists = pdist(df.T, similarity_func)
    DF_euclid = pd.DataFrame(squareform(dists), columns=df.columns, index=df.columns)
    print (DF_euclid)
    return DF_euclid

def vizualization(matrx):
            
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_aspect('equal')
    plt.imshow(matrx, interpolation='nearest', cmap=plt.cm.ocean)
    plt.colorbar()
    plt.show()
    plt.savefig('general_graphic_.png', format='png', dpi=100)
    