
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy as cart
import numpy as np
from mpl_toolkits.basemap import addcyclic
from Reading_nc import Cape_Verde



def function_plot(lat,lon,C,name,month):
    print(len(C),len(C[0]))
    z, loni = \
        addcyclic(C, lon)
    x, y = np.meshgrid(loni, lat)
    fig = plt.figure(figsize=(8, 6))
    # ax = fig.add_subplot(1,1, 1,projection=ccrs.Robinson(0))

    projection = ccrs.PlateCarree(central_longitude=180)
    ax = plt.axes(projection=projection)
    clevs = np.array([0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5,0.6])

    colors = (
        '#3000e2', '#2548ff', '#27a7ff', '#70e4ff', '#cbfdff',
        '#fdf9d2', '#fec783', '#ff5d46', '#fe0229', '#b40018')

    # clevs = np.array([ 0,1,2, 4,6,8,10, 15,17, 20])
    # clevs = np.array([0, 0.05, 0.1,0.15, 0.2,0.25, 0.3, 0.4, 0.5, 0.6])
    cmap1 = mcolors.ListedColormap(colors)
    norm1 = mcolors.BoundaryNorm(clevs, cmap1.N)
    # cs = m.colorbar(cs, location='right', size='3.5%', pad="4%", ticks=bar, boundaries=bar, extend='max', extendfrac='auto',spacing='proportional')

    # print(x)
    # print(len(y),len(z[0]))
    m = ax.pcolormesh(x, y,z[:, :], norm = norm1, cmap = cmap1,
                        transform=ccrs.PlateCarree())


    # im = ax.contourf(x, y, z[:,:], transform=ccrs.PlateCarree())
    #
    cbar = plt.colorbar(m, norm=norm1, cmap=cmap1, ticks=clevs, boundaries=clevs, extend='max', extendfrac='auto', shrink=0.6,orientation='vertical')
    # cbar.set_label('${uMol C/ L}$')
    ax.add_feature(cart.feature.LAND, zorder=100, edgecolor='k')

    # indice_lat, indice_lon = Cape_Verde(lat, lon)
    # ax.scatter(y[indice_lat], x[indice_lon], color='m',
    #            transform=ccrs.PlateCarree()
    #            )

    ax.coastlines(resolution='110m')
    gl = ax.gridlines()
    plt.title(name+' '+month)
    plt.savefig(name+'_'+month+'.png', dpi = 300)
    plt.close()
    # plt.show()
