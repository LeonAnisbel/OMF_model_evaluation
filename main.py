##### Import packges
import numpy as np
import pandas as pd
import read_data_functions, interp_func
import glob, os
import general_func
import map_with_loc

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # data paths
    try:
        os.mkdir('plots')
    except OSError:
        pass
    try:
        os.mkdir('plots/Sfc_conc_plots')
    except OSError:
        pass

    plot_dir = './plots/'
    data_dir = (f"/home/manuel/Downloads/Observ_sites_maps/Burows_param/")

    dates, PASCAL, PI_ICE, data_CVAO, data_SVAL_15, data_MH_18 = (
        read_data_functions.read_obs_data_loc())

    print('MaceHead')
    pd_obs_mo_MH_18 = interp_func.interp_omf_stations(data_MH_18,
                                                        'MH',
                                                        data_dir)
    pd_obs_mo_MH_18.to_pickle('tot_omf_MH.pkl')

    print('Pascal, Pice')
    pd_obs_mo_pi_ice = interp_func.assign_loc_ship(PI_ICE[3],
                                                   PI_ICE[1],
                                                   PI_ICE[0],
                                                   'WAP',
                                                   data_dir)
    pd_obs_mo_pascal = interp_func.assign_loc_ship(PASCAL[3],
                                                   PASCAL[1],
                                                   PASCAL[0],
                                                   'NAO',
                                                   data_dir)

    # print('RS')
    # pd_obs_mo_rs = interp_func.interp_omf_stations(data_rs,
    #                                                'RS',
    #                                                data_dir)
    print('CVAO')
    pd_obs_mo_cvao = interp_func.interp_omf_stations(data_CVAO[0],
                                                     'CVAO',
                                                     data_dir)


    print('SVALVARD')

    # pd_obs_mo_sval_14 = interp_func.interp_omf_stations(data_SVAL_14[1],
    #                                                     'SVD14',
    #                                                     data_dir)
    pd_obs_mo_sval_15 = interp_func.interp_omf_stations(data_SVAL_15[0],
                                                        'SVD15',
                                                        data_dir)



    # print(pd_obs_mo_sval_15['OMF_mod_pro'])
    #
    # pd_obs_mo_sval_18 = interp_func.interp_omf_stations(data_SVAL_18[1],
    #                                                     'SVD18',
    #                                                     data_dir)



    # pd_obs_mo_chichi = interp_func.interp_omf_stations(data_Chichi,'Chichi', data_dir)

    # # combine data of poly for all stations and generate box plot with statistics
    # OMF_pd_pol_tot = pd.concat([pd_obs_mo_pascal, pd_obs_mo_cvao, pd_obs_mo_pi_ice])
    # general_func.pd_combine_pol(OMF_pd_pol_tot, plot_dir)
    #
    # # combine data of lip and prot for all stations and generate box plot with statistics
    # OMF_pd_pr_li_tot = pd.concat([pd_obs_mo_cvao, pd_obs_mo_sval_14_15, pd_obs_mo_sval_18_19])  # ,pd_obs_mo_chichi])
    # general_func.pd_combine_pro_lip(OMF_pd_pr_li_tot, plot_dir)
    #
    # # generate box plot for lip and proteins over CVAO

    general_func.pd_combine_pr_li(pd_obs_mo_cvao, plot_dir)

    OMF_all_po = pd.concat([pd_obs_mo_pascal,
                            pd_obs_mo_cvao,
                            pd_obs_mo_pi_ice])
    OMF_all_pr = pd.concat([pd_obs_mo_cvao,
                            # pd_obs_mo_sval_14,
                            pd_obs_mo_sval_15,
                            # pd_obs_mo_sval_18,
                            # pd_obs_mo_rs
                            ])
    OMF_all_li = pd_obs_mo_cvao

    general_func.pd_combine_all(OMF_all_po,
                                OMF_all_pr,
                                OMF_all_li,
                                plot_dir)


