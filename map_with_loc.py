import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import os
import read_data_functions
import itertools

def get_list(var_list,names):
    """
    Creates list with lat, lon locations of campaigns ID indicated in names
    :var var_list: dataframe containing lat and lon metadata for each campaign
    :param names: list of names of campaigns IDs
    :return var_list: list of lists containing lat and lon for each campaign
    """
    loc_list = []

    for i,loc in enumerate(var_list):
        if names[i] == 'NAO' or names[i] == 'WAP':
            l_list = [[loc['Latitude'].values[m], loc['Longitude'].values[m]] for m in
                      range(len(loc['Longitude'].values))]
        else:
            l_list = [[loc['Start Latitude'].values[m], loc['Start Longitude'].values[m]] for m in
                      range(len(loc['Start Longitude'].values))]
        loc_list.append(l_list)

    return loc_list


def loc_map_plot(mo, yr, PASCAL, PI_ICE, CVAO, plot_dir):
    """
    Groups data and calls the function to plot station or campaign location for a certain biomolecule
    """
    exp = 'ac3_arctic'
    data_dir = f"/scratch/b/b381361/{exp}/"
    if mo < 10:
        mo_str = f'0{mo}'
    else:
        mo_str = f'{mo}'

    names = ['NAO', 'CVAO']#, 'WAP']
    var_list = [PASCAL, CVAO]#, WAP]

    loc_list = get_list(var_list,names)

    file = f'{data_dir}{exp}_{yr}{mo_str}.01_ham.nc'

    if os.path.exists(file):
        data = read_data_functions.read_model_spec_data(file)

    loc_list[0].sort()
    loc_list[1].sort()

    m1_new = list(k for k,_ in itertools.groupby(loc_list[0]))

    m2_new = list(k for k,_ in itertools.groupby(loc_list[1]))

    loc_list = [m1_new] + [m2_new]

    plot_map_loc(data['OMF_POL'].mean(dim= 'time'), 'OMF_POL',loc_list , names,plot_dir)



# defining function 1 column plot, 3 rows
def plot_map_loc(C, name, location, names,plot_dir):
    """
    Creates map with campaign locations
    :var C: dataArray containing lat and lon
    :var names: name of biomolecule
    :var location: list containing lat and lon metadata for each campaign and biomolecule
    :var names: list of names of campaigns IDs
    :var plot_dir: directory to save plots
    :return : None
    """
    fig, ax = plt.subplots(1, 1,  # define figure with cartopy
                             subplot_kw={'projection': ccrs.NorthPolarStereo()},
                           figsize=(5, 6))
    ax.set_extent([-180, 180, 50, 90],
                  ccrs.PlateCarree())

    plt.subplots_adjust(left=0,
                        right=1,
                        top=0.9,
                        bottom=0)
    fig.suptitle(name,
                 fontsize=20)

    im = ax.pcolormesh(C.lon,
                       C.lat,
                       C,
                       cmap="Blues",
                       transform=ccrs.PlateCarree())
    # ax.set_title(names, fontsize='14')
    ax.coastlines()
    loc_plot(location,
             names,
             ax,
             fig)

    fig.colorbar(im,
                 orientation="horizontal",
                 label="$mmol C m^{-3}$")
    plt.tight_layout()
    plt.savefig(plot_dir + 'Sfc_conc_plots/' + name + '_sfc_map_loc.png',
                dpi=300,
                bbox_inches="tight")


def loc_plot(location, names, ax, fig):
    """
    Plots dots in map to indicate station or campaign locations
    :var location: list containing lat and lon metadata for each campaign
    :var names: list of names of campaigns IDs corresponding to each [lat, lon]
    :var ax: matplotlib axes
    :return :None
    """
    ind = 0
    for loc, n in zip(location, names):

        if len(loc) == 2:
            ax.scatter(x=loc[1], y=loc[0],
                       color='m', marker='X',
                       transform=ccrs.PlateCarree())
            ax.text(loc[1] + 6, loc[0] - 3, n,
                    horizontalalignment='right',
                    transform=ccrs.Geodetic(),
                    bbox={'facecolor': 'lightgray', 'boxstyle': 'round', 'pad': 0.2})
        else:
            ind = 1
            for l in loc:
                ax.scatter(x=l[1], y=l[0],
                           color='m', marker='X',
                           transform=ccrs.PlateCarree())

            ax.text(l[1] + 6, l[0] - 3, n,
                    horizontalalignment='left',
                    transform=ccrs.Geodetic(),
                    bbox={'facecolor': 'lightgray', 'boxstyle': 'round', 'pad': 0.2})


