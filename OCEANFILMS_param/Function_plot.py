import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy as cart
import numpy as np
import cartopy


# from mpl_toolkits.basemap import addcyclic


def function_plot(lat, lon, C, name):
    z, loni = C, lon
    x, y = np.meshgrid(loni, lat)

    fig, axes = plt.subplots(4, 1,  # define figure with cartopy
                             subplot_kw={'projection': ccrs.Robinson()}, figsize=(5, 12))
    plt.subplots_adjust(left=0, right=1, top=0.9, bottom=0)

    axflat = axes.flatten()
    print(axflat)
    fig.suptitle(name, fontsize=20)
    months = [1, 4, 8, 10]
    titles = ['February', 'May', 'September', 'November']
    for idx, var in enumerate(months):
        print(idx, var)
        axflat[idx].set_title(titles[idx], fontsize='14')
        axflat[idx].coastlines()

        if name[:3] == 'OMF':
            im = axflat[idx].contourf(x, y, C[months[idx]], 18, vmin=0, vmax=0.16, cmap="jet",
                                      transform=ccrs.PlateCarree())  # , levels=np.arange(-10,10.1, 0.1))
        else:
            im = axflat[idx].contourf(x, y, C[months[idx]], 20, cmap="jet",
                                      transform=ccrs.PlateCarree())  # , levels=np.arange(-10,10.1, 0.1))

        axflat[idx].add_feature(cartopy.feature.OCEAN, facecolor=(0.5, 0.5, 0.5))
        axflat[idx].add_feature(cart.feature.LAND, zorder=100, edgecolor='k')
        axflat[idx].coastlines(resolution='10m')
        axflat[idx].gridlines()

    cbar_ax = fig.add_axes([0.1, -0.05, 0.8, 0.03])

    cbar = fig.colorbar(im, cax=cbar_ax, orientation="horizontal")
    cbar.ax.tick_params(rotation=45)

    plt.savefig('OMF_plots/' + name + '_omf.png', dpi=300, bbox_inches="tight")

    # colors = (
    #     '#3000e2', '#2548ff', '#27a7ff', '#70e4ff', '#cbfdff',
    #     '#fdf9d2', '#fec783', '#ff5d46', '#fe0229', '#b40018')
    #
    # cmap1 = mcolors.ListedColormap(colors)
    # norm1 = mcolors.BoundaryNorm(clevs, cmap1.N)
    # m = ax.pcolormesh(x, y, z[:, :], norm=norm1, cmap=cmap1,
    #                   transform=cartopy.crs.PlateCarree())
    #
    # cbar = plt.colorbar(m, norm=norm1, cmap=cmap1, ticks=clevs, boundaries=clevs, extend='max', extendfrac='auto',
    #                     shrink=1.0, orientation='horizontal')

    # plt.title(name+' '+month)
    #
    # plt.savefig(name+ID+month+'.png', dpi = 300)
    plt.close()
