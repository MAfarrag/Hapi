"""
Created on Sat Apr  4 20:57:53 2020

@author: mofarrag
"""
# from IPython import get_ipython
# get_ipython().magic('reset -f')
import os
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import gridspec
# import pandas as pd
# from matplotlib import animation``
# import datetime as dt
# import math
# from Hapi.sm import performancecriteria as Pf
import Hapi.hm.river as R
from Hapi.hm.event import Event as E
# import Hapi.Visualizer as V
#%% Paths
rpath = r"F:\02Case-studies"
CompP = rpath + r"\ClimXtreme\rim_base_data\setup\rhine"
os.chdir(CompP)

oldxsPath = CompP + r"\inputs\1d\topo\xs_rhine.csv"
# newxsPath = CompP + r"\inputs\1d\topo\xs_elevated.csv"

start = "1955-01-01"
days = 21910
River = R.River('RIM', version=3, days=days, start=start)
# River.OneDResultPath = wpath + "/results/1d/"
# RIM2Files = "F:/02Case studies/Rhine/base_data/Calibration/RIM2.0/01 calibrated parameters/06-15042020/"

River.ReadCrossSections(oldxsPath)
River.Slope(CompP + "/inputs/1d/topo/slope_rhine.csv")
River.OneDResultPath = CompP +"/results/1d/"

River.RiverNetwork(CompP + "/inputs/1d/topo/rivernetwork_rhine.txt")
# River.ReturnPeriod(CompP1 + "/base_data/HYDROMOD/RIM1.0/Observed Period/Statistical Analysis/" + "HQRhine.csv")
path = rpath + r"\ClimXtreme\data\gauges\Discharge\Statistical Analysis/" + "DistributionProperties.csv"
River.StatisticalProperties(path, Filter=False)
#%%

# River.GetBankfullQ()
# calculate the capacity of the bankfull area
River.GetCapacity('Qbkf')

# calculate the capacity of the whole cross section till the lowest dike level
River.GetCapacity('Qc2', Option=2)

# River.CalibrateDike("RP", "QcRP")
River.crosssections['ZlDiff'] = River.crosssections['zlnew'].values - River.crosssections['zl'].values
River.crosssections['ZrDiff'] = River.crosssections['zrnew'].values - River.crosssections['zr'].values
# River.crosssections.to_csv(RIM2Files+"XS100.csv", index = None)

#%%
# read the overtopping files
# River.Overtopping()
# Event object
Event = E.Event("RIM2.0")
Event.Overtopping(wpath + "/processing/" + "overtopping.txt")
# get the end days of each event
Event.GetAllEvents()

River.EventIndex = Event.EventIndex
# read the left and right overtopping 1D results
River.Overtopping()

XSleft = list()
XSright = list()
print("No of Events = " + str(len(Event.EndDays)))
for i in range(len(Event.EndDays)):
    # get the cross sectin that was overtopped for a specific day
    XSlefti, XSrighti = River.GetOvertoppedXS(Event.EndDays[i],True)
    XSleft = XSleft + XSlefti
    XSright = XSright + XSrighti

XSright = list(set(XSright))
XSleft = list(set(XSleft))
XSleft.sort()
XSright.sort()
# raise the left dike of the overtopped cross section by 0.5 meter
for i in XSleft:
    # print(i)
    # print(River.crosssections.loc[i-1,'xsid'])
    River.crosssections.loc[i-1,'zl'] = River.crosssections.loc[i-1,'zl'] + 0.5

for i in XSright:
    # print(i)
    # print(River.crosssections.loc[i-1,'xsid'])
    River.crosssections.loc[i-1,'zr'] = River.crosssections.loc[i-1,'zr'] + 0.5

# get the subs that was inundated
# floodedSubs = River1.GetFloodedSubs(OvertoppedXS = XSleft + XSright)

#%% Save the new cross section file
River.crosssections.to_csv(newxsPath, index = None)