import numpy as np
import xarray as xr
import os
import read_data_functions
from scipy.interpolate import griddata


def read_model(mo, yr, data_dir):
    file = f'{data_dir}oceanfilms_omf_res025_{yr}.nc'
    da_list = []
    print(file)
    if os.path.exists(file):
        print('reading ', file, 'for interpolation with data month = ', mo)
        data = xr.open_dataset(file)
        da_m_ds = data.isel(time=mo - 1)
    return da_m_ds


def get_mod_box(C_m, var, lat_obs, lon_obs):
    bx_size = 7
    C_m_bx = C_m.where((C_m.lat < lat_obs[1] + bx_size) & (C_m.lat > lat_obs[0] - bx_size) &
                       (C_m.lon < lon_obs[1] + bx_size) & (C_m.lon > lon_obs[0] - bx_size), drop=True)

    # variables for the interpolation
    lat_mod = C_m_bx.lat.values
    lon_mod = C_m_bx.lon.values
    model_lo_la = []
    model_data = []
    for la in range(len(C_m_bx[var].values)):
        for lo in range(len(C_m_bx[var][0].values)):
            model_lo_la.append([lon_mod[lo], lat_mod[la]])
            model_data.append(float(C_m_bx[var][la][lo].values))

    # clean nans
    model_lo_la_notnan = []
    model_data_notnan = []
    for idx in range(len(model_data)):
        if model_data[idx] > 0:
            model_lo_la_notnan.append(model_lo_la[idx])
            model_data_notnan.append(model_data[idx])

    return model_lo_la_notnan, model_data_notnan


def interp_func(mod_ds, var, obs_lon, obs_lat, obs_lon_mi_ma, obs_lat_mi_ma):
    points, values = get_mod_box(mod_ds, var, obs_lat_mi_ma, obs_lon_mi_ma)

    grid_lon, grid_lat = np.meshgrid(obs_lon, obs_lat)
    f = griddata(points, values, (grid_lon, grid_lat), method='cubic')
    return f
