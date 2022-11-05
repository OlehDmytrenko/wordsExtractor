#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 11:44:45 2022

@author: dmytrenko.o
"""

import matplotlib.pylab as plt

import pandas as pd
from scipy.spatial import distance_matrix   
    

def euclidianSimilyrity(df):
    # Whole similarity algorithm in one line
    df_euclid = pd.DataFrame(
        1 / (1 + distance_matrix(df.T, df.T)),
        columns=df.columns, index=df.columns
        )
    print (df_euclid)
    return df_euclid

def vizualization(df):
    matrx = df.to_numpy()       
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_aspect('equal')
    plt.imshow(matrx, interpolation='nearest', cmap=plt.cm.ocean)
    plt.colorbar()
    plt.show()
    plt.savefig('general_graphic_.png', format='png', dpi=100)
    