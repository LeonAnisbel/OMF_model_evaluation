import plot_functions
import pandas as pd


def pd_combine_pol(OMF_pd, plot_dir):
    """
    Combines and cleans data of Polysaccharides and total OMF creating a dataframe and box plots of model vs. obs
    :var OMF_pd: dataframe of OMF data
    :param plot_dir: directory to save plot to
    :return: None
    """
    # combining all omf obs and model into a datframe (new_OMF_pol) for box plot
    obs_omf_pol = (OMF_pd['OMF_mod_poly'].to_list() +
                   OMF_pd['OMF_obs_poly_sub'].to_list())

    obs_omf_all = (OMF_pd['OMF_mod_tot'].to_list() +
                   OMF_pd['OMF_obs_tot_sub'].to_list())

    ID_all = (OMF_pd['ID'].to_list() +
              OMF_pd['ID'].to_list())

    mod_obs = (len(OMF_pd['ID'].values) * ['Mdel'] +
               len(OMF_pd['ID'].values) * ['Measurements'])

    new_OMF_pd = pd.DataFrame({'Aerosol OMF': obs_omf_pol,
                               'Measurement': ID_all,
                               '': mod_obs,
                               'Total aerosol OMF': obs_omf_all})

    new_OMF_pd_tot_nan = new_OMF_pd.dropna(subset=['Total aerosol OMF'])
    new_OMF_pd_pol_nan = new_OMF_pd.dropna(subset=['Aerosol OMF'])

    plot_functions.box_plot(new_OMF_pd_tot_nan, plot_dir,
                            "Total aerosol OMF",
                            "",
                            'tot_omf_box')
    plot_functions.box_plot(new_OMF_pd_pol_nan, plot_dir,
                            "Aerosol OMF",
                            "PCHO",
                            'CCHO_omf_box')

    # Plotting box plots with statistics
    names = ['NAO', 'CVAO', 'WAP']
    dict_comp = dict((name, {
        'pol_mod': OMF_pd[OMF_pd['ID'] == name].dropna(subset=['OMF_obs_poly_sub'])['OMF_mod_poly'].to_list(),
        'pol_obs': OMF_pd[OMF_pd['ID'] == name].dropna(subset=['OMF_obs_poly_sub'])['OMF_obs_poly_sub'].to_list(),
        'tot_mod': OMF_pd[OMF_pd['ID'] == name].dropna(subset=['OMF_obs_tot_sub'])['OMF_mod_tot'].to_list(),
        'tot_obs': OMF_pd[OMF_pd['ID'] == name].dropna(subset=['OMF_obs_tot_sub'])['OMF_obs_tot_sub'].to_list()
        }) for name in names)
    # print(dict_comp)

    plot_functions.box_plot_stat(new_OMF_pd_pol_nan, dict_comp,
                                 'pol',
                                 'pcho_stat',
                                 [1e-5, 1e0],
                                 "Aerosol OMF",
                                 plot_dir,
                                 0.5,
                                 0.05)
    plot_functions.box_plot_stat(new_OMF_pd_tot_nan, dict_comp,
                                 'tot',
                                 'total_stat',
                                 [1e-3, 1e1],
                                 "Total aerosol OMF",
                                 plot_dir,
                                 5,
                                 0.05)


def pd_combine_pr_li(pd_obs_mo_cvao, plot_dir):
    """
    Combines and cleans data of lipids and protein OMF creating a dataframe and box plots of model vs. obs
    :var OMF_pd: dataframe of OMF data for CVAO
    :param plot_dir: directory to save plot to
    :return: None
    """
    # Compiling all omf obs and model into a datframe (new_OMF_pro_lip) for box plot
    obs_omf_pro_lip = pd_obs_mo_cvao['OMF_mod_pro'].to_list() + pd_obs_mo_cvao['OMF_mod_lip'].to_list() + \
                      pd_obs_mo_cvao['OMF_obs_prot_sub'].to_list() + pd_obs_mo_cvao['OMF_obs_lipi_sub'].to_list()

    ID_all = (pd_obs_mo_cvao['Name_pro'].to_list() + pd_obs_mo_cvao['Name_lip'].to_list() +
              pd_obs_mo_cvao['Name_pro'].to_list() + pd_obs_mo_cvao['Name_lip'].to_list())  # Prot or lip

    mod_obs = len(pd_obs_mo_cvao['Name_pro'].values) * ['Mdel'] + len(pd_obs_mo_cvao['Name_pro'].values) * ['Mdel'] + \
              len(pd_obs_mo_cvao['Name_pro'].values) * ['Measurements'] + len(pd_obs_mo_cvao['Name_pro'].values) * [
                  'Measurements']

    new_OMF_pd_pl = pd.DataFrame({'Aerosol OMF': obs_omf_pro_lip, 'Species': ID_all, '': mod_obs})

    plot_functions.box_plot_lip(new_OMF_pd_pl, plot_dir)


def pd_combine_pro_lip(OMF_pd, plot_dir):
    """
    Combines and cleans data of lipids and protein OMF creating a dataframe and box plots of model vs. obs
    :var OMF_pd: dataframe of OMF data
    :param plot_dir: directory to save plot to
    :return: None
    """
    # combining all omf obs and model into a datframe (new_OMF_pol) for box plot
    OMF_pd_pro = OMF_pd.dropna(subset=['OMF_obs_prot_sub'])
    OMF_pd_lip = OMF_pd.dropna(subset=['OMF_obs_lipi_sub'])

    obs_omf_pro = (OMF_pd_pro['OMF_mod_pro'].to_list() +
                   OMF_pd_pro['OMF_obs_prot_sub'].to_list())

    obs_omf_lip = (OMF_pd_lip['OMF_mod_lip'].to_list() +
                   OMF_pd_lip['OMF_obs_lipi_sub'].to_list())

    ID_pro = (OMF_pd_pro['ID'].to_list() +
              OMF_pd_pro['ID'].to_list())

    ID_lip = (OMF_pd_lip['ID'].to_list() +
              OMF_pd_lip['ID'].to_list())

    mod_obs_pro = (len(OMF_pd_pro['ID'].values) * ['Mdel'] +
                   len(OMF_pd_pro['ID'].values) * ['Measurements'])

    mod_obs_lip = (len(OMF_pd_lip['ID'].values) * ['Mdel'] +
                   len(OMF_pd_lip['ID'].values) * ['Measurements'])

    new_OMF_pd_pro = pd.DataFrame({'OMF Proteins': obs_omf_pro,
                                   'Measurement': ID_pro,
                                   '': mod_obs_pro,
                                   })

    new_OMF_pd_lip = pd.DataFrame({'OMF Lipids': obs_omf_lip,
                                   'Measurement': ID_lip,
                                   '': mod_obs_lip,
                                   })

    new_OMF_pd_lip_nan = new_OMF_pd_lip.dropna(subset=['OMF Lipids'])
    new_OMF_pd_pro_nan = new_OMF_pd_pro.dropna(subset=['OMF Proteins'])

    # Plotting box plots with statistics
    names = ['CVAO', 'SVD14', 'SVD15', 'SVD18', 'RS']
    dict_comp_pro = dict((name, {'pro_mod': OMF_pd[OMF_pd['ID'] == name].dropna(subset=['OMF_obs_prot_sub'])[
                                    'OMF_mod_pro'].to_list(),
                                 'pro_obs': OMF_pd[OMF_pd['ID'] == name].dropna(subset=['OMF_obs_prot_sub'])[
                                     'OMF_obs_prot_sub'].to_list(), }) for name in names)
    # print(new_OMF_pd_lip_nan)
    # name = ['CVAO'],#'Chichi'
    name = 'CVAO'
    dict_comp_lip = {
        name: {'lip_mod': OMF_pd[OMF_pd['ID'] == name].dropna(subset=['OMF_obs_lipi_sub'])[
                    'OMF_mod_lip'].to_list(),
               'lip_obs': OMF_pd[OMF_pd['ID'] == name].dropna(subset=['OMF_obs_lipi_sub'])[
                   'OMF_obs_lipi_sub'].to_list()}}

    # print(dict_comp_lip)
    plot_functions.box_plot_stat(new_OMF_pd_pro_nan,
                                 dict_comp_pro,
                                 'pro',
                                 'proteins_stat',
                                 [1e-4, 1e-1],
                                 "OMF Proteins",
                                 plot_dir,
                                 0.05,
                                 -0.15)
    plot_functions.box_plot_stat(new_OMF_pd_lip_nan,
                                 dict_comp_lip,
                                 'lip',
                                 'lipids_stat',
                                 [1e-3, 1e0],
                                 "OMF Lipids",
                                 plot_dir,
                                 0.7,
                                 -0.4)


def create_dataframe(omf_pd_nan, mod, obs, mac_na):
    """
    Combines all omf obs and model into a dataframe (new_omf_pol)
    :var omf_pd_nan: dataframe with omf
    :param mod: argument name for model interpolated results
    :param obs: argument name for obs values
    :param mac_na: campaign Id
    :return: new dataframe
    """
    # combining all omf obs and model into a datframe (new_omf_pol) for box plot
    if mac_na != 'RS':
        omf_pd = omf_pd_nan.dropna(subset=[obs])
    else:
        omf_pd = omf_pd_nan


    obs_omf_pol = (list(omf_pd[mod].values) +
                   list(omf_pd[obs].values))

    id_all = (omf_pd['ID'].to_list() +
              omf_pd['ID'].to_list())

    mod_obs = (len(omf_pd['ID'].values) * ['Model'] +
               len(omf_pd['ID'].values) * ['Observation'])

    mac = len(mod_obs) * [mac_na]

    new_omf_po = pd.DataFrame({'Aerosol OMF': obs_omf_pol,
                               'Measurements': id_all,
                               '': mod_obs,
                               'Macromolecules': mac})

    # new_omf_pd_tot_nan = new_omf_pd.dropna(subset=['Aerosol omf'])
    # new_omf_pd_po_nan = new_omf_po.dropna(subset=['Aerosol OMF'])

    return new_omf_po

def rename_func(data_pd, na, new_na):
    """
    Renames columns of the data_pd data frame from the old name "na" to "new_na"
    :var data_pd: dataframe
    :param na: argument name to replace
    :var new_na: new name to fill with updated "na" name
    :return: new dataframe
    """
    pd_new = data_pd
    list_col = data_pd['Measurements'].to_list()
    for i in range(len(list_col)):
        if list_col[i] == na:
            list_col[i] = new_na
    pd_new = pd_new.drop(columns='Measurements')
    pd_new['Measurements'] = list_col
    return pd_new

def pd_combine_all(dicc_po_to, dicc_pr, dicc_li):
    """
    Combines all omf obs and model into a dataframe, call the plot box function and saves omf values for each species
    in individual pickle files
    :var dicc_po_to: dataframe with polysaccharide-like omf values
    :var dicc_pr: dataframe with protein-like omf values
    :var dicc_li: dataframe with lipid-like omf values
    :return: None
    """
    mac_names = ['PCHO|CCHO', 'DCAA|AA', 'PL|PG','(PCHO+DCAA+PL)|OM']
    omf_pd_po = create_dataframe(dicc_po_to,
                                 'OMF_mod_poly',
                                 'OMF_obs_poly_sub',
                                 mac_names[0])
    omf_pd_pr = create_dataframe(dicc_pr,
                                 'OMF_mod_pro',
                                 'OMF_obs_prot_sub',
                                 mac_names[1] )
    omf_pd_li = create_dataframe(dicc_li,
                                 'OMF_mod_lip',
                                 'OMF_obs_lipi_sub',
                                 mac_names[2])
    omf_pd_to = create_dataframe(dicc_po_to,
                                 'OMF_mod_tot',
                                 'OMF_obs_tot_sub',
                                 mac_names[3])

    omf_pd_li_new = rename_func(omf_pd_li,
                                'CVAO',
                                'CVAO ')
    omf_pd_pr_new = rename_func(omf_pd_pr,
                                'CVAO',
                                'CVAO  ')
    omf_pd_to1 = rename_func(omf_pd_to,
                             'CVAO',
                             'CVAO   ')
    omf_pd_to2 = rename_func(omf_pd_to1,
                             'NAO',
                             'NAO ')
    omf_pd_to_new = rename_func(omf_pd_to2,
                                'WAP',
                                'WAP ')

    plot_functions.box_plot_vert(pd.concat([omf_pd_po, omf_pd_pr_new, omf_pd_li_new, omf_pd_to_new]),
                                 mac_names,
                                 ['pol', 'pro', 'lip'],
            'All_groups',
                                 [1e-5, 1e1])

    omf_pd_po.to_pickle('./pkl_files/poly_omf.pkl')
    omf_pd_pr_new.to_pickle('./pkl_files/prot_omf.pkl')
    omf_pd_li_new.to_pickle('./pkl_files/lipi_omf.pkl')
    omf_pd_to_new.to_pickle('./pkl_files/tot_omf.pkl')

