"""
Make sure the working directory is set to the examples folder in the Hapi repo"
currunt_work_directory = Hapi/example

install and use earth2observe package https://github.com/MAfarrag/earth2observe
"""
from earth2observe.chirps import CHIRPS
from earth2observe.ecmwf import ECMWF, Variables

root_path = "C:/MyComputer/01Algorithms/Hydrology/Hapi/"
# %% Basin data
StartDate = "2009-01-01"
EndDate = "2009-02-01"
time = "daily"
latlim = [4.190755, 4.643963]
lonlim = [-75.649243, -74.727286]
# make sure to provide a full path not relative path
# please replace the following root_path to the repo main directory in your machine
path = root_path + "examples/data/satellite_data/"
# %%
"""
check the ECMWF variable names that you have to provide to the RemoteSensing object
"""
Vars = Variables("daily")
Vars.__str__()
# %% ECMWF
"""
provide the time period, temporal resolution, extent and variables of your interest
"""
start = "2009-01-01"
end = "2009-01-10"
ts = "daily"
latlim = [4.190755, 4.643963]
lonlim = [-75.649243, -74.727286]
# Temperature, Evapotranspiration
variables = ["T", "E"]

Coello = ECMWF(
    time=time,
    start=start,
    end=end,
    lat_lim=latlim,
    lon_lim=lonlim,
    path=path,
    variables=variables,
)

Coello.download()
# %% CHRIPS
Coello = CHIRPS(
    StartDate=StartDate,
    EndDate=EndDate,
    Time=time,
    latlim=latlim,
    lonlim=lonlim,
    Path=path,
)
Coello.Download()
# %%
"""
if you want to use parallel downloads using multi cores, enter the number of
cores you want to use

PS. the multi-coredownload does not have an indication bar
"""
cores = 4

Coello = CHIRPS(
    StartDate=StartDate,
    EndDate=EndDate,
    Time=time,
    latlim=latlim,
    lonlim=lonlim,
    Path=path,
)
Coello.Download(cores=cores)