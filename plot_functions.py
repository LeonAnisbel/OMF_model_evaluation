import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy as cart
import numpy as np
from matplotlib.ticker import FuncFormatter
import seaborn as sns
from sklearn.metrics import mean_squared_error

def plot_map(C, name, id_var, step, ma,outdir_polts, factor,unit,cmap,poles = True,total = True):
    if poles:
        fig, axes = plt.subplots(4, 1,  # define figure with cartopy
                                 subplot_kw={'projection': ccrs.NorthPolarStereo()}, figsize=(5, 12))
        for i in range(len(axes)):
            axes[i].set_extent([-180, 180, 50, 90], ccrs.PlateCarree())
    else:
        fig, axes = plt.subplots(4, 1,  # define figure with cartopy
                                 subplot_kw={'projection': ccrs.Robinson()}, figsize=(5, 12))

    axflat = axes.flatten()

    plt.subplots_adjust(left=0, right=1, top=0.9, bottom=0)

    fig.suptitle(name, fontsize=20)
    months = [1, 4, 7, 10]
    titles = ['February', 'May', 'August', 'November']


    for idx, var in enumerate(months):
        if total:
            Z = (C[var][id_var[0]] + C[var][id_var[1]]+ C[var][id_var[2]])/ factor
            id_var_a = id_var[0][:3]
        else:
            Z = C[var][id_var]/factor
            id_var_a = id_var


        Z_da = np.ma.masked_where(Z <= 0, Z)

        levels = np.linspace(0.0, ma, 20)
        im = axflat[idx].contourf(Z.lon, Z.lat,Z_da,levels = levels,extend = 'max',
                                  cmap = cmap, transform=ccrs.PlateCarree())  # , levels=np.arange(-10,10.1, 0.1))
        axflat[idx].set_title(titles[idx], fontsize='14')
        axflat[idx].add_feature(
            cart.feature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='face', facecolor='lightgray'))
        axflat[idx].coastlines()
        axflat[idx].gridlines()

    cbar_ax = fig.add_axes([0.1, -0.05, 0.8, 0.03])

    if ma >= 6 :
        fmt = lambda x, pos: '{:.0f}'.format(x)
    if ma < 6 and ma >= 1:
        fmt = lambda x, pos: '{:.1f}'.format(x)
    if ma < 0.05:
        fmt = lambda x, pos: '{:.4f}'.format(x)

    if ma >= 0.05 and ma <= 0.9: fmt = lambda x, pos: '{:.2f}'.format(x)

    cbar = fig.colorbar(im ,format=FuncFormatter(fmt), cax=cbar_ax, orientation="horizontal", label=unit)
    cbar.set_label(unit,fontsize = '16')
    cbar.ax.tick_params(rotation = 45)

    plt.savefig(outdir_polts + name + '.png', dpi=300, bbox_inches="tight")
    plt.close()



def box_plot(data_pd,plot_dir,yaxis,title,name):
    """
    Creates figure with box plot of model and observation data using seaborn
    :var data_pd: pandas.DataFrame with model and observation for certain biomolecule
    :var plot_dir: path to save figure
    :param yaxis: y-axis label
    :param title: biomolecule name
    :var name: figure name
    :return: None
    """
    # box plot using seaborn
    fig, ax = plt.subplots(1, 1,
                           figsize=(9, 8))  # creating figure

    # The box shows the quartiles of the dataset while the whiskers extend to show the rest of the distribution,
    # except for points that are determined to be “outliers” using a method that is a function of the inter-quartile
    # range.
    sns.boxplot(data=data_pd,
                x="Measurement",
                y=yaxis,
                hue="")

    # Customizing axes
    ax.tick_params(axis='both',
                   labelsize='14')
    ax.yaxis.get_label().set_fontsize(14)
    ax.set_xlabel('')
    ax.set_yscale('log')
    ax.set_title(title,
                 fontsize='16')
    ax.grid(linestyle='--',
            linewidth=0.4)
    ax.set_ylim([1e-5, 1e1])

    plt.savefig(f'{plot_dir}{name}.png',
                dpi=300)
    plt.close()


def box_plot_lip(new_OMF_pd_pl,plot_dir):
    """
    Creates figure with box plot of model and observation data using seaborn
    :var new_OMF_pd_pl: pandas.DataFrame with model and observation for lipids
    :var plot_dir: path to save figure
    :return: None
    """

    fig, ax = plt.subplots(figsize=(9, 8))
    bx = sns.boxplot(data=new_OMF_pd_pl, x="Species", y="Aerosol OMF", hue="",
                     showfliers=False)  # The box shows the quartiles of the
    # dataset while the whiskers extend to
    # show the rest of the distribution,
    # except for points that are determined
    # to be “outliers” using a method that
    # is a function of the inter-quartile range.
    #

    # Customizing axes
    ax.tick_params(axis='both', labelsize='14')
    ax.yaxis.get_label().set_fontsize(14)
    ax.set_xlabel('', fontsize=14)
    ax.set_yscale('log')
    ax.set_ylim([1e-5, 1e1])
    ax.grid(linestyle='--', linewidth=0.4)
    ax.set_title('OMF (Proteins and Lipids) over CVAO', fontsize='16')
    plt.savefig(plot_dir + 'Pro_Lip_omf_box.png', dpi=300)

# Statistical indicators
def equat_stat(model, observ):
    """
    Function to compute statistics
    :var model: list of interpolated model values
    :var observ: list of observation values
    :return: statistics rmse, pearsons_coeff, nmb, nmsd
    """
    # Root Mean Squared Error
    rmse = np.sqrt(mean_squared_error(model, observ))

    # Correlation coefficient (R)
    corrcoef = np.corrcoef(model, observ)[0][1]

    # Normalised Mean Bias (NMB)
    obs_mean = sum(observ) / len(observ)
    mod_mean = sum(model) / len(model)
    bias = mod_mean - obs_mean
    nmb = bias / obs_mean

    # Normalised Mean Standard Deviation (NMSD)
    std_obs = np.std(observ)
    std_mod = np.std(model)
    nmsd = (std_mod - std_obs) / std_obs

    return rmse, corrcoef, nmb, nmsd

def stat(da, id_mod, id_obs):
    """
    Calls function to compute statistics of each station and biomolecule
    :var da: pandas DataFrame with model and observation for certain biomolecule
    :var id_mod: model attribute name in dataframe ID
    :var id_obs: observation attribute name in dataframe ID
    :return: None
    """
    rmse_val = []
    corrcoef = []
    nmb_val = []
    nmsd_val = []

    mod_all = []
    obs_all = []
    for na, _ in da.items():
        if len(da[na][id_mod]) > 0:  # this won't be necessary when the data is complete

            model = da[na][id_mod]
            observ = da[na][id_obs]

            for i, m in enumerate(model):  # For global statistics
                mod_all.append(m)  # appending values to a list of modeled data
                obs_all.append(observ[i])  # appending values to a list of observed data

            rmse, corr, nmb, nmsd = equat_stat(model, observ)

            rmse_val.append(rmse)
            corrcoef.append(corr)
            nmb_val.append(nmb)
            nmsd_val.append(nmsd)

    rmse_tot, corr_tot, nmb_tot, nmsd_tot = equat_stat(mod_all, obs_all)

    stat_all = [rmse_tot, corr_tot, nmb_tot, nmsd_tot]

    return rmse_val, corrcoef, nmb_val, nmsd_val, stat_all



def box_plot_stat(dict_df, dict_macrom, ID, title, lim,yaxis,plot_dir,loc_high,loc_left):
    """
    Creates figure with box plot of model and observation data using seaborn for a specific biomolecules
    :var dict_df: pandas DataFrame with model and observation for certain biomolecules
    :var dict_macrom: dictionary with model and observation for certain biomolecules
    :var ID: biomolecule ID
    :var title: title of figure
    :var lim: lower and upper limit of y-axis box plot
    :var plot_dir: path to save figure
    :var loc_high: y-axis location for text
    :var loc_left: x-axis location for text
    :return: None
    """
    # Create new plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot with seaborn
    bx = sns.boxplot(data=dict_df, x="Measurement", y=yaxis, hue="", palette="vlag")

    rmse, corr, nmb, nmsd, stat_all = stat(dict_macrom, f'{ID}_mod', f'{ID}_obs')

    if ID == '':#ID == 'pro' or ID == 'lip':
        # Correlation is a measure of how well two vectors track with each other as they change.
        # You can't track mutual change when one vector doesn't change
        # (https://stackoverflow.com/questions/45897003/python-numpy-corrcoef-runtimewarning-invalid-value-encountered-in-true-divide).
        formatted_pvalues = (f' NMB= {np.round(stat_all[2], 2)}   '
                             f'NMSD= {np.round(stat_all[3], 2)}')
    else:
        formatted_pvalues = (f'RMSE = {np.round(stat_all[0], 3)}    '
                             f'R= {np.round(stat_all[1], 2)}  '
                             f' NMB= {np.round(stat_all[2], 2)}  '
                             f' NMSD= {np.round(stat_all[3], 2)}')
        print(f'RMSE = {stat_all[0]}')
    ax.text(loc_left, loc_high, formatted_pvalues,
            fontsize='14',
            weight='bold',
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})

    # Customizing axes
    ax.tick_params(axis='both',
                   labelsize='14')
    ax.yaxis.get_label().set_fontsize(14)
    ax.set_xlabel('',
                  fontsize=14)
    ax.set_yscale('log')
    ax.grid(linestyle='--',
            linewidth=0.4)
    ax.set_ylim(lim)

    plt.legend(loc="lower right",
               fontsize='14')  # bbox_to_anchor=(1.04, 1),

    plt.savefig(plot_dir + f'{title}_{ID}_box.png',
                dpi=300)


def plot_text(dict_macrom, ax, ID, l0, l1, h1, mol_name):

    box1 = mol_name
    ax.text(l0, 50, box1, fontsize='14', weight='bold', bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
    # ax.text(l1, h1, box2, fontsize='10')


def box_plot_vert(dict_df, mol_name, ID, title, lim):
    """
    Creates figure with box plot of model and observation data using seaborn for a specific biomolecules
    :var dict_df: pandas DataFrame with model and observation for all biomolecules
    :var mol_name: list of biomolecule name ids
    :var title: title of figure
    :var lim: y-axis lower and upper limit
    :return: None
    """
    # Create new plot
    fig, ax = plt.subplots(figsize=(15, 8))
    # YlGnBu
    states_palette = sns.color_palette("BuPu",
                                       n_colors=2)
    # Plot with seaborn
    bx = sns.boxplot(data=dict_df,
                     x="Measurements",
                     y="Aerosol OMF",
                     hue="",
                     palette=states_palette,
                     width=.7)
    # The box shows the quartiles of the
    # dataset while the whiskers extend to
    # show the rest of the distribution,
    # except for points that are determined
    # to be “outliers” using a method that
    # is a function of the inter-quartile range.

    ax.text(0.1, 4,
            mol_name[0],
            fontsize='14',
            weight='bold',
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
    ax.text(3.2, 4,
            mol_name[1],
            fontsize='14',
            weight='bold',
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
    ax.text(5.7, 4,
            mol_name[2],
            fontsize='14',
            weight='bold',
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
    ax.text(7, 4,
            mol_name[3],
            fontsize='14',
            weight='bold',
            bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})


    # Customizing axes
    ax.tick_params(axis='both',
                   labelsize='14')
    ax.yaxis.get_label().set_fontsize(14)
    ax.set_xlabel('',
                  fontsize=14)
    ax.set_yscale('log')
    ax.grid(linestyle='--',
            linewidth=0.4)
    ax.set_ylim(lim)

    # dotted lines to separate groups
    ax.axvline(2.5,
               color=".3",
               dashes=(2, 2))
    ax.axvline(5.5,
               color=".3",
               dashes=(2, 2))
    ax.axvline(6.5,
               color=".3",
               dashes=(2, 2))

    plt.legend(loc="lower left",
               fontsize='14')  # bbox_to_anchor=(1.04, 1),

    plt.savefig( f'plots/all_test_{title}_box.png',
                 dpi=300,
                 bbox_inches="tight")