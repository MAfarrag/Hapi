# -*- coding: utf-8 -*-
"""
Created on Sun May 16 18:33:09 2021

@author: mofarrag
"""
import numpy as np
import pandas as pd
import datetime as dt

Path = "F:/01Algorithms/Hydrology/HAPI/Examples/"
#%%
def convertdate(date):
    return dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

USBC = pd.read_csv(Path + "/data/hydrodynamic model/USBC.txt")
USBC.index= USBC['time'].apply(convertdate)
USBC = USBC.drop("time",axis=1)

ind = pd.date_range(USBC.index[0], USBC.index[-1], freq='3Min')
MinQ = pd.DataFrame(index=ind, columns=USBC.columns)
MinQ.loc[:,:] = USBC.loc[:,:].resample('1Min').mean().interpolate('linear')
XS = pd.read_csv(Path + "/data/hydrodynamic model/xs.csv")
#%%
dx = 1000
beta = 3/5
dt = 3*60
dtx = dt/dx
b=60
Laterals = False
LateralsQ = 0


#%%


