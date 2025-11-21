import numpy as np
import xarray as xr
from OCEANFILMS_param import global_vars

def read_nc(l, yr, path):
    file_end = f'_regular_grid_interp_vw_{yr}.nc'
    file_names = [f'PCHO_var{file_end}',
                  f'DCAA_var{file_end}',
                  f'PL_var{file_end}']

    variables = ['PCHO', 'DCAA', 'PL']
    file_names_burrows = ['TRUEPOLYC', 'TRUEPROTC', 'TRUELIPC']
    c_total = []
    lat, lon = 0, 0
    for i, fi in enumerate(file_names):
        concentration_fesom = xr.open_dataset(path + fi)[variables[i]].isel(time=l)

        f_dir = global_vars.path_cesm_biom + file_names_burrows[i] + '_res025.nc'
        concentration_burrows = xr.open_dataset(f_dir)[file_names_burrows[i]].isel(time=l)

        if global_vars.exp_biomolecules == "burrows_":
            concentration = concentration_burrows
        elif global_vars.exp_biomolecules == "fesom_burrows_":
            if variables[i] == 'PL':
                concentration = concentration_fesom + concentration_burrows
        else:
            concentration = concentration_fesom

        ice_mask = xr.open_dataset(path + f'mask_ice_var{file_end}')['sic'].isel(time=l)

        concentration_mask = (concentration)*ice_mask
        lat = concentration_mask.lat.values
        lon = concentration_mask.lon.values
        c_total.append(concentration_mask)

    return c_total, lat, lon
