"""DEM related functions."""
from typing import Dict
import numpy as np
from pyramids.dataset import Dataset


class DEM(Dataset):
    """DEM."""

    def __init__(self, src):
        super().__init__(src)

    def flow_direction_index(self) -> np.ndarray:
        """flow_direction_index.

            flow_direction_index takes flow direction raster and converts codes for the 8 directions
            (1,2,4,8,16,32,64,128) into indices of the Downstream cell.

        flow_direct:
            [gdal.dataset] flow direction raster obtained from catchment delineation
            it only contains values [1,2,4,8,16,32,64,128]

        Returns
        -------
        [numpy array]:
            with the same dimensions of the raster and 2 layers
            first layer for rows index and second rows for column index
        """
        # check flow direction input raster
        no_val = self.no_data_value[0]
        cols = self.columns
        rows = self.rows

        fd = self.read_array(band=0)
        fd_val = np.unique(fd[~np.isclose(fd, no_val, rtol=0.00001)])
        fd_should = [1, 2, 4, 8, 16, 32, 64, 128]
        if not all(fd_val[i] in fd_should for i in range(len(fd_val))):
            raise ValueError(
                "flow direction raster should contain values 1,2,4,8,16,32,64,128 only "
            )

        fd_cell = np.ones((rows, cols, 2)) * np.nan

        for i in range(rows):
            for j in range(cols):
                if fd[i, j] == 1:
                    # index of the rows
                    fd_cell[i, j, 0] = i
                    # index of the column
                    fd_cell[i, j, 1] = j + 1
                elif fd[i, j] == 128:
                    fd_cell[i, j, 0] = i - 1
                    fd_cell[i, j, 1] = j + 1
                elif fd[i, j] == 64:
                    fd_cell[i, j, 0] = i - 1
                    fd_cell[i, j, 1] = j
                elif fd[i, j] == 32:
                    fd_cell[i, j, 0] = i - 1
                    fd_cell[i, j, 1] = j - 1
                elif fd[i, j] == 16:
                    fd_cell[i, j, 0] = i
                    fd_cell[i, j, 1] = j - 1
                elif fd[i, j] == 8:
                    fd_cell[i, j, 0] = i + 1
                    fd_cell[i, j, 1] = j - 1
                elif fd[i, j] == 4:
                    fd_cell[i, j, 0] = i + 1
                    fd_cell[i, j, 1] = j
                elif fd[i, j] == 2:
                    fd_cell[i, j, 0] = i + 1
                    fd_cell[i, j, 1] = j + 1

        return fd_cell

    def flow_direction_table(self) -> Dict:
        """Flow Direction Table.

            - flow_direction_table takes flow direction indices created by FlowDirectِِIndex function and creates a
            dictionary with the cells' indices as a key and indices of directly upstream cells as values
            (list of tuples).


            flow_direct:
                [gdal.dataset] flow direction raster obtained from catchment delineation
                it only contains values [1,2,4,8,16,32,64,128]

        Returns
        -------
        flowAccTable:
            [Dict] dictionary with the cells indices as a key and indices of directly
            upstream cells as values (list of tuples)
        """
        flow_direction_index = self.flow_direction_index()

        rows = self.rows
        cols = self.columns

        cell_i = []
        cell_j = []
        celli_content = []
        cellj_content = []
        for i in range(rows):
            for j in range(cols):
                if not np.isnan(flow_direction_index[i, j, 0]):
                    # store the indexes of not empty cells and the indexes stored inside these cells
                    cell_i.append(i)
                    cell_j.append(j)
                    # store the index of the receiving cells
                    celli_content.append(flow_direction_index[i, j, 0])
                    cellj_content.append(flow_direction_index[i, j, 1])

        flow_acc_table = {}
        # for each cell store the directly giving cells
        for i in range(rows):
            for j in range(cols):
                if not np.isnan(flow_direction_index[i, j, 0]):
                    # get the indexes of the cell and use it as a key in a dictionary
                    name = str(i) + "," + str(j)
                    flow_acc_table[name] = []
                    for k in range(len(celli_content)):
                        # search if any cell are giving this cell
                        if i == celli_content[k] and j == cellj_content[k]:
                            flow_acc_table[name].append((cell_i[k], cell_j[k]))

        return flow_acc_table
