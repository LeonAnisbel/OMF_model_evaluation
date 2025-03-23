import pandas as pd
import numpy as np
import utils_func


# save all lat, lon and date/Time in locations files between start and end in omf files

def assign_loc_ship(ds_lim, ds_sub, ds_btw, ID, data_dir):
    def datetime_to_integer(dt_time):
        return pd.to_datetime(dt_time).astype(int) / 10 ** 9  # 10000*dt_time.year + 100*dt_time.month + dt_time.day

    time_loc = datetime_to_integer(ds_btw['Date/Time'])  # convert datetime to int
    mo_loc = ds_btw['Date/Time'].dt.month.values  # list with months

    time_var_start = datetime_to_integer(ds_lim['Start Date/Time'])  # convert datetime to int
    mo_start = ds_lim['Start Date/Time'].dt.month.values  # list with months
    yr_start = ds_lim['Start Date/Time'].dt.year.values  # list with months

    time_var_end = datetime_to_integer(ds_lim['End Date/Time'])  # convert datetime to int
    mo_end = ds_lim['End Date/Time'].dt.month.values  # list with months

    start_4_mod, end_4_mod = [], []
    omf_model_pol, omf_model_pro, omf_model_lip, omf_model_tot = [], [], [], []
    omf_obs_pol_sub, omf_obs_tot_sub = [], []
    omf_obs_pol_sup, omf_obs_tot_sup = [], []

    omf_obs_pol, omf_obs_pro, omf_obs_lip, omf_obs_tot = [], [], [], []
    name_lip, name_pro = [], []
    id_camp = []

    for i, (start, end) in enumerate(zip(time_var_start, time_var_end)):

        # times, lats and lons between start and end
        omf_mod_pol, omf_mod_pro, omf_mod_lip = [], [], []
        interp_btw = []
        interp_btw_pol = []
        interp_btw_pro = []
        interp_btw_lip = []

        # saving lats, longs and months between start and end into a list
        lat_btw, lon_btw, mo_btw = [], [], []
        for l, loc in enumerate(time_loc):
            if loc >= start and loc <= end:  # and \
                #             ds_btw['Latitude'].values[l] >= ds_lim['Start Latitude'].values[i] and \
                #             ds_btw['Latitude'].values[l] <= ds_lim['End Latitude'].values[i]:
                lat_btw.append(ds_btw['Latitude'].values[l])
                lon_btw.append(ds_btw['Longitude'].values[l])

        mod_data = utils_func.read_model(mo_start[i], yr_start[i], data_dir)


        if len(lat_btw) > 1:
            print('interpolation data in process for ship trajectories')
            # lon_btw = [lon180 % 360 for lon180 in lon_btw]
            mi_ma_lat = [min(lat_btw), max(lat_btw)]
            mi_ma_lon = [min(lon_btw), max(lon_btw)]
            # for la, lo in zip(lat_btw, lon_btw):
            f_interp_pol = utils_func.interp_func(mod_data, 'OMF_POL', lon_btw, lat_btw, mi_ma_lon, mi_ma_lat)
            f_interp_pro = utils_func.interp_func(mod_data, 'OMF_PRO', lon_btw, lat_btw, mi_ma_lon, mi_ma_lat)
            f_interp_lip = utils_func.interp_func(mod_data, 'OMF_LIP', lon_btw, lat_btw, mi_ma_lon, mi_ma_lat)

            interp_btw_pol.append(f_interp_pol)
            interp_btw_pro.append(f_interp_pro)
            interp_btw_lip.append(f_interp_lip)

            print(float(np.nanmean(interp_btw_pol)))
            omf_mod_pol.append(np.nanmean(interp_btw_pol))
            omf_mod_pro.append(np.nanmean(interp_btw_pro))
            omf_mod_lip.append(np.nanmean(interp_btw_lip))

        else:
            start_lo = ds_lim['Start Longitude'].values[i]
            start_la = ds_lim['Start Latitude'].values[i]
            mi_ma_lon, mi_ma_lat = [start_lo, start_lo], [start_la, start_la]

            f_interp_pol = utils_func.interp_func(mod_data, 'OMF_POL', start_lo, start_la, mi_ma_lon, mi_ma_lat)
            f_interp_pro = utils_func.interp_func(mod_data, 'OMF_PRO', start_lo, start_la, mi_ma_lon, mi_ma_lat)
            f_interp_lip = utils_func.interp_func(mod_data, 'OMF_LIP', start_lo, start_la, mi_ma_lon, mi_ma_lat)

            interp_lim_start = f_interp_pol[0][0]
            interp_lim_start_pr = f_interp_pro[0][0]
            interp_lim_start_li = f_interp_lip[0][0]
            print(type(interp_lim_start), 'start')

            end_lo = ds_lim['End Longitude'].values[i]
            end_la = ds_lim['End Latitude'].values[i]
            mi_ma_lon, mi_ma_lat = [end_lo, end_lo], [end_la, end_la]

            f_interp_pol = utils_func.interp_func(mod_data, 'OMF_POL', end_lo, end_la, mi_ma_lon, mi_ma_lat)
            f_interp_pro = utils_func.interp_func(mod_data, 'OMF_PRO', end_lo, end_la, mi_ma_lon, mi_ma_lat)
            f_interp_lip = utils_func.interp_func(mod_data, 'OMF_LIP', end_lo, end_la, mi_ma_lon, mi_ma_lat)

            interp_lim_end = f_interp_pol[0][0]
            interp_lim_end_pr = f_interp_pro[0][0]
            interp_lim_end_li = f_interp_lip[0][0]

            omf_mod_pol.append(np.nanmean([interp_lim_start, interp_lim_end]))
            omf_mod_pro.append(np.nanmean([interp_lim_start_pr, interp_lim_end_pr]))
            omf_mod_lip.append(np.nanmean([interp_lim_start_li + interp_lim_end_li]))

        # if ds_lim['OMF_pol'].values[i] > 0.:
        start_4_mod.append(ds_lim['Start Date/Time'].values[i])
        end_4_mod.append(ds_lim['End Date/Time'].values[i])

        omf_obs_pol_sub.append(ds_sub['OMF_pol'].values[i])
        omf_obs_tot_sub.append(ds_sub['OMF_tot'].values[i])
        omf_obs_pro.append(ds_sub['OMF_CAA'].values[i])
        omf_obs_lip.append(ds_sub['OMF_PG'].values[i])

        interp_lim_start_pol = np.nanmean(omf_mod_pol)
        interp_lim_start_pro = np.nanmean(omf_mod_pro)
        interp_lim_start_lip = np.nanmean(omf_mod_lip)

        omf_model_pol.append(interp_lim_start_pol)
        omf_model_pro.append(interp_lim_start_pro)
        omf_model_lip.append(interp_lim_start_lip)

        omf_model_tot.append(interp_lim_start_pol +
                             interp_lim_start_pro +
                             interp_lim_start_lip)

        name_pro.append('DCAA CAA')
        name_lip.append('Lipids PG')

        id_camp.append(ID)

    # create new dataframe to store the data after filtering all lat, lons and Date/Time

    pd_da = pd.DataFrame({'ID': id_camp, 'Start Date/Time': start_4_mod, 'End Date/Time': end_4_mod,
                          'OMF_mod_poly': omf_model_pol, 'OMF_mod_pro': omf_model_pro, 'OMF_mod_lip': omf_model_lip,
                          'OMF_obs_poly_sub': omf_obs_pol_sub, 'OMF_obs_prot_sub': omf_obs_pro,
                          'OMF_obs_lipi_sub': omf_obs_lip,
                          'OMF_obs_tot_sub': omf_obs_tot_sub, 'OMF_mod_tot': omf_model_tot,
                          'Name_pro': name_pro, 'Name_lip': name_lip})

    pd_da['Start Date/Time'] = pd_da['Start Date/Time'].apply(pd.to_datetime)
    pd_da['End Date/Time'] = pd_da['End Date/Time'].apply(pd.to_datetime)

    return pd_da


# interpolation function
def interp_omf_stations(obs, ID, data_dir):
    from scipy.interpolate import interp2d

    start_4_mod, end_4_mod = [], []
    id_camp = []
    omf_model_pol, omf_model_pro, omf_model_lip, omf_model_tot = [], [], [], []
    omf_obs_pol, omf_obs_pro, omf_obs_lip, omf_obs_tot = [], [], [], []
    name_lip, name_pro = [], []
    months = obs['Start Date/Time'].dt.month.values
    years = obs['Start Date/Time'].dt.year.values

    for m, mo in enumerate(months):
        # lat, lon = 16.86361111, -24.86722223 % 360
        lat, lon = obs['Start Latitude'].values[0], obs['Start Longitude'].values[0]  # for 0.25x0.25 grid only
        # interpolation function
        mod_data = utils_func.read_model(mo, years[m], data_dir)

        mi_ma_lon, mi_ma_lat = [lon, lon], [lat, lat]

        f_interp_pol = utils_func.interp_func(mod_data, 'OMF_POL', lon, lat, mi_ma_lon, mi_ma_lat)
        f_interp_pro = utils_func.interp_func(mod_data, 'OMF_PRO', lon, lat, mi_ma_lon, mi_ma_lat)
        f_interp_lip = utils_func.interp_func(mod_data, 'OMF_LIP', lon, lat, mi_ma_lon, mi_ma_lat)

        # interpolate obs coordinates
        interp_lim_start_pol = f_interp_pol[0][0]
        interp_lim_start_pro = f_interp_pro[0][0]
        interp_lim_start_lip = f_interp_lip[0][0]

        start_4_mod.append(obs['Start Date/Time'].values[m])
        end_4_mod.append(obs['End Date/Time'].values[m])

        omf_model_pol.append(interp_lim_start_pol)
        omf_model_pro.append(interp_lim_start_pro)
        omf_model_lip.append(interp_lim_start_lip)
        omf_model_tot.append(interp_lim_start_pol +
                             interp_lim_start_pro +
                             interp_lim_start_lip)

        omf_obs_pol.append(obs['OMF_pol'].values[m])
        omf_obs_tot.append(obs['OMF_tot'].values[m])
        omf_obs_pro.append(obs['OMF_CAA'].values[m])
        omf_obs_lip.append(obs['OMF_PG'].values[m])

        name_pro.append('DCAA CAA')
        name_lip.append('Lipids PG')

        id_camp.append(ID)

    # create new dataframe to store the model data after interpolation together with obs.
    pd_da = pd.DataFrame({'ID': id_camp, 'Start Date/Time': start_4_mod, 'End Date/Time': end_4_mod,
                          'OMF_mod_poly': omf_model_pol, 'OMF_mod_pro': omf_model_pro, 'OMF_mod_lip': omf_model_lip,
                          'OMF_obs_poly_sub': omf_obs_pol, 'OMF_obs_prot_sub': omf_obs_pro,
                          'OMF_obs_lipi_sub': omf_obs_lip,
                          'OMF_obs_tot_sub': omf_obs_tot, 'OMF_mod_tot': omf_model_tot,
                          'Name_pro': name_pro, 'Name_lip': name_lip})

    pd_da['Start Date/Time'] = pd_da['Start Date/Time'].apply(pd.to_datetime)
    pd_da['End Date/Time'] = pd_da['End Date/Time'].apply(pd.to_datetime)

    return pd_da
