import numpy as np
from osgeo import gdal
from Hapi.dem import DEM


def test_flowDirectionIndex(coello_df_4000: gdal.Dataset):
    dem = DEM(coello_df_4000)
    fd_cell = dem.flow_direction_index()
    assert isinstance(fd_cell, np.ndarray)
    assert fd_cell.shape == (dem.rows, dem.columns, 2)


def test_flowDirectionTable(coello_df_4000: gdal.Dataset):
    dem = DEM(coello_df_4000)
    fd_cell = dem.flow_direction_table()
    assert isinstance(fd_cell, np.ndarray)
    assert fd_cell.shape == (dem.rows, dem.columns, 2)


def test_flowDirectionTable(coello_df_4000: gdal.Dataset, coello_fdt):
    dem = DEM(coello_df_4000)
    fd_table = dem.flow_direction_table()
    assert fd_table == coello_fdt
