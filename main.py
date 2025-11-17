##### Import packges
import pandas as pd
import global_vars
import read_data_functions, interp_func
import os
import general_func

if __name__ == '__main__':
    try:
        os.mkdir('plots_experiments')
    except OSError:
        pass
    try:
        os.mkdir('pkl_files')
    except OSError:
        pass
    try:
        os.mkdir('plots_experiments/Sfc_conc_plots')
    except OSError:
        pass

    plot_dir = global_vars.plot_dir
    data_dir = (global_vars.data_dir)
    exp_biom = global_vars.exp_biomolecules

    # Read all observational data (station or ship trajectory and aerosol concentration)
    dates, PASCAL, PI_ICE, data_CVAO, data_SVAL_15, data_MH_18, data_MH_02_09 = (
        read_data_functions.read_obs_data_loc())

    print('MaceHead')
    # Interpolate model results to Mace Head location and dates (2002-2009, total )
    pd_obs_mo_MH_02_09 = interp_func.interp_omf_stations(data_MH_02_09,
                                                        'MH0209',
                                                        data_dir,
                                                        filter_exposition=True)
    pd_obs_mo_MH_02_09.to_pickle(f'./pkl_files/{exp_biom}tot_omf_MH_Rinaldi.pkl')

    # Interpolate model results to Mace Head location and dates (2018)
    pd_obs_mo_MH_18 = interp_func.interp_omf_stations(data_MH_18,
                                                        'MH',
                                                        data_dir)
    pd_obs_mo_MH_18.to_pickle(f'./pkl_files/{exp_biom}tot_omf_MH.pkl')


    print('Pascal, Pice')
    # Interpolate model results to PI_ICE campaign locations and dates (submicron poly)
    pd_obs_mo_pi_ice = interp_func.assign_loc_ship(PI_ICE[3],
                                                   PI_ICE[1],
                                                   PI_ICE[0],
                                                   'WAP',
                                                   data_dir)
    # Interpolate model results to PASCAL campaign locations and dates (submicron poly)
    pd_obs_mo_pascal = interp_func.assign_loc_ship(PASCAL[3],
                                                   PASCAL[1],
                                                   PASCAL[0],
                                                   'NAO',
                                                   data_dir)


    print('CVAO')
    # Interpolate model results to CVAO campaign locations and dates (submicron lip, poly, prot)
    pd_obs_mo_cvao = interp_func.interp_omf_stations(data_CVAO[0],
                                                     'CVAO',
                                                     data_dir)


    print('SVALVARD')
    # Interpolate model results to Svalbard campaign locations and dates (submicron DCAA)
    pd_obs_mo_sval_15 = interp_func.interp_omf_stations(data_SVAL_15[0],
                                                        'SVD15',
                                                        data_dir)


    # combine and concatenate all data
    general_func.pd_combine_pr_li(pd_obs_mo_cvao, plot_dir)

    OMF_all_po = pd.concat([pd_obs_mo_pascal,
                            pd_obs_mo_cvao,
                            pd_obs_mo_pi_ice])
    OMF_all_pr = pd.concat([pd_obs_mo_cvao,
                            pd_obs_mo_sval_15,
                            ])
    OMF_all_li = pd_obs_mo_cvao

    # create box plot of omf from observations and interpolated model values
    # save dataframes in pickle files
    general_func.pd_combine_all(OMF_all_po,
                                OMF_all_pr,
                                OMF_all_li
                                )


