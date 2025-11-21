import xarray as xr
import os
import codecs
import pandas as pd
import itertools

def read_obs_data_loc():
    """
    Read observational data from various campaigns
    :returns dates: list of dates
             PASCAL: PASCAL campaign data list (len=4) of dataframes
                    [ship location, sub-micron size, super-micron size, total size]
             PI_ICE: PI_ICE campaign data list (len=4) of dataframes
                    [ship location, sub-micron size, super-micron size, total size]
             CVAO: CVAO data list (len=2)  of dataframes [sub-micron size, total size]
             SVAL_15: Svalbard data list (len=2) of dataframes [sub-micron size, total size]
             data_MH_18: Mace Head data sub-micron size dataframes
             data_AI_02_09: Amsterdam Island data sub-micron size dataframes
    """

    #### Reading station locations
    main_dir = '../Observation_data/'
    loc_dir = 'Aerosol_sample_coordinates/'
    files = ['PASCAL_lat_lon_aer.csv', 'PI_ICE_lat_lon_aer.csv']
    pol_data = 'AER_OMF_pol_lip_pro_all_sizes.csv'

    doc = codecs.open(main_dir + loc_dir + files[0], 'r', 'UTF-8')  # open for reading with "universal" type set
    PASCAL_loc = pd.read_csv(doc, sep=',')

    doc = codecs.open(main_dir + loc_dir + files[1], 'r', 'UTF-8')  # open for reading with "universal" type set
    PI_ICE_loc = pd.read_csv(doc, sep=',')

    # converting 'Date/Time' column to datetime data type
    print(PASCAL_loc['Date/Time'].values)
    PASCAL_loc['Date/Time'] = [pd.Timestamp(row).to_pydatetime() for row in PASCAL_loc['Date/Time'].values]
    PI_ICE_loc['Date/Time'] = [pd.Timestamp(row).to_pydatetime() for row in PI_ICE_loc['Date/Time'].values]

    print(PI_ICE_loc['Date/Time'])

    doc = codecs.open(main_dir + pol_data, 'r', 'UTF-8')  # open for reading with "universal" type set
    data = pd.read_csv(doc, sep=',')

    # converting 'Date/Time' column to datetime data type
    data['Start Date/Time'] = data['Start Date/Time'].apply(pd.to_datetime)
    data['End Date/Time'] = data['End Date/Time'].apply(pd.to_datetime)
    print(data['Event'])
    # Save data for PI_ICE
    data_PI_ICE_subm_1 = data[data['Station_sizes'] == 'PI-ICE_0.05_1.2']  # data for submicron aerosol size
    data_PI_ICE_subm_2 = data[data['Station_sizes'] == 'PI-ICE_0.14_1.2']  # data for submicron aerosol size
    data_PI_ICE_super = data[data['Station_sizes'] == 'PI-ICE_1.2_10']  # data for supermicron aerosol size
    data_PI_ICE_tot = data[data['Station_sizes'] == 'PI-ICE_0.05_10']  # data for all aerosol sizes

    # Save data for PASCAL
    # data_PASCAL = data[24:33]
    data_PASCAL_subm_1 = data[data['Station_sizes'] == 'PASCAL_0.05_1.2']  # data for submicron aerosol size
    data_PASCAL_subm_2 = data[data['Station_sizes'] == 'PASCAL_0.14_1.2']  # data for submicron aerosol size
    data_PASCAL_super = data[data['Station_sizes'] == 'PASCAL_1.2_10']  # data for supermicron aerosol size
    data_PASCAL_tot = data[data['Station_sizes'] == 'PASCAL_0.05_10']  # data for all aerosol sizes

    data_CVAO_subm_1 = data[data['Station_sizes'] == 'CVAO_0.05-1.2 µm']
    data_CVAO_subm_2 = data[data['Station_sizes'] == 'CVAO_PM1']

    # data_CVAO_super = data_CVAO[28:36]
    data_CVAO_tot = data[data['Station_sizes'] == 'CVAO_0.05-10 µm']

    data_SVAL_15_subm_1 = data[data['Station_sizes'] == 'Sval_0-1.5µm_15']
    data_SVAL_15_subm_2 = data[data['Station_sizes'] == 'Sval_<0.49_0.95µm_15']
    data_SVAL_15_tot = data[data['Station_sizes'] == 'Sval_0-10µm_15']

    data_MH_18 = data[data['Station_sizes'] == 'MH_submicron']
    data_AI_02_09 = data[data['Station_sizes'] == 'AI']


    dates = []
    for i, d in enumerate(data['Start Date/Time'].dt.month):
        dates.append([d, data['Start Date/Time'].dt.year[i]])
        dates.append([data['End Date/Time'].dt.month[i], data['End Date/Time'].dt.year[i]])
    dates.sort()
    dates = list(k for k, _ in itertools.groupby(dates))

    PI_ICE = [PI_ICE_loc, data_PI_ICE_subm_2, data_PI_ICE_super, data_PI_ICE_tot]
    PASCAL = [PASCAL_loc, data_PASCAL_subm_2, data_PASCAL_super, data_PASCAL_tot]
    CVAO = [data_CVAO_subm_2, data_CVAO_tot]
    SVAL_15 = [data_SVAL_15_subm_2, data_SVAL_15_tot]

    return dates, PASCAL, PI_ICE, CVAO, SVAL_15, data_MH_18, data_AI_02_09

def file_var(ds, var):
    """
    Get dataArrays from dataset
    :var ds: dataset
    :param var: variable name
    :return: dataArray
    """
    fi_va = [f[var] for f in ds]
    return fi_va

def read_model_data(data_dir, dates, exp):
    """
    Read OMF from model
    :param data_dir: data directory
    :param dates: list containing months
    :param exp: experiment name
    :return: list of OMF data of biomolecules
    """
    omf_files = []
    emi_files = []
    wind_files = []
    for d in dates:
        if d[0] < 10:
            mo_str = f'0{d[0]}'
        else:
            mo_str = f'{d[0]}'

        if os.path.exists(f'{data_dir}{exp}_{d[1]}{mo_str}.01_ham.nc'):
            da = xr.open_mfdataset(f'{data_dir}{exp}_{d[1]}{mo_str}.01_ham.nc',
                                   concat_dim='time',
                                   combine='nested')
            omf_files.append(da)
            da = xr.open_mfdataset(f'{data_dir}{exp}_{d[1]}{mo_str}.01_emi.nc',
                                   concat_dim='time',
                                   combine='nested')
            emi_files.append(da)
            da = xr.open_mfdataset(f'{data_dir}{exp}_{d[1]}{mo_str}.01_echam.nc',
                                   concat_dim='time',
                                   combine='nested')
            wind_files.append(da)


    omf_pol = xr.concat(file_var(omf_files, 'OMF_POL'),
                        dim='time')
    omf_pro = xr.concat(file_var(omf_files, 'OMF_PRO'),
                        dim='time')
    omf_lip = xr.concat(file_var(omf_files, 'OMF_LIP'),
                        dim='time')

    omf = [omf_pol, omf_pro, omf_lip]

    return omf


def read_model_spec_data(file):
    """
    This function reads (with dask) the data from a certain file type group
    :param file: files to read
    :return: dataset
    """
    return xr.open_mfdataset(file,
                             concat_dim='time',
                             combine='nested')


# reading data
def read_nc_ds(files, path):
    """
    Reading model data from netCDF files
    :param files: list of files to read
    :param path: path to netCDF file
    :return: dataset
    """
    data_model = []
    data_month = [[] for i in range(12)]
    da_month_mean = [[] for i in range(12)]

    pp = len(path)

    for fi in files:
        if int(fi[pp + 11:pp + 15]) == 2015 or int(
                fi[pp + 11:pp + 15]) == 2010:  # or int(fi[-16:-12]) == 2015:# or int(fi[-16:-12]) == 2019:
            da = xr.open_mfdataset(fi)
            data = da.mean(dim='time')
            data_model.append(data)
            for i in range(12):
                if int(fi[pp + 15:pp + 17]) - 1 == i:
                    data_month[i].append(data)

    for l, da in enumerate(data_month):
        if len(da) > 0:
            dada = xr.concat(da, dim='time')
            da_month_mean[l] = dada.mean(dim='time')

    return xr.concat(data_model, dim='time'), data_month, da_month_mean



