import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
# from mpl_toolkits.basemap import addcyclic
import cartopy as cart
import cartopy



def function_plot_chl(x,y,z,name,month,ID,proj):
    fig = plt.figure(figsize=(8, 6))
    # ax = fig.add_subplot(1,1, 1,projection=ccrs.Robinson(0))
    print(z.max(),'maxxx')
    ax = plt.axes(projection=proj)
    clevs = [0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 6,7]
    # colors = (
    #     '#1316ff', '#016eff', '#04b0ff', '#63e5fe', '#b4ffff',
    #     '#fcffc0', '#ffe47a', '#ffaf25', '#ff6602', '#ff0202')
    #
    # cmap1 = mcolors.ListedColormap(colors)
    # norm1 = mcolors.BoundaryNorm(clevs, cmap1.N)
    # m = ax.pcolormesh(x, y,z[:, :], norm = norm1, cmap = cmap1,
    #                     transform=ccrs.PlateCarree())
    # cbar = plt.colorbar(m, norm=norm1, cmap=cmap1, ticks=clevs, boundaries=clevs, extend='max', extendfrac='auto', shrink=0.9,orientation='horizontal')

    # m = ax.pcolormesh(x, y,z[:, :], cmap = 'BuGn', vmin=min, vmax=0.25,
    #                     transform=ccrs.PlateCarree())
    # cbar = plt.colorbar(m, extend='max', extendfrac='auto', shrink=0.9,orientation='horizontal')

    cmap = plt.get_cmap('rainbow')
    norm = mcolors.BoundaryNorm(clevs, ncolors=cmap.N, clip=True)
    m = ax.pcolormesh(x, y, z[:, :], cmap=cmap, norm=norm,
                      transform=ccrs.PlateCarree())

    # CV_location = [16.8880556,335.04306780703126]
    # # # NOTE: longitude before latitude!!
    # plt.plot(CV_location[1], CV_location[0], color='m', linewidth=20,  transform=ccrs.Geodetic())
    #

    # cbar = plt.colorbar(m, extend='max', cmap=cmap, norm=norm, extendfrac='auto', shrink=0.9,orientation='horizontal')
    cbar = plt.colorbar(m, extend='max', cmap=cmap, norm=norm, extendfrac='auto', shrink=0.6,orientation='vertical')

    cbar.set_label('${mg m^{-3}}$')
    ax.add_feature(cart.feature.LAND, zorder=100, edgecolor='k')

    ax.coastlines(resolution='10m')
    gl = ax.gridlines()
    plt.title('Ocean Chl-a conc ' +' '+month)
    plt.savefig(name+ID+month+'.png', dpi = 300)
    plt.close()



def function_plot_2(x,y,z,name,month,clevs):

    plt.figure(figsize=(9, 9))
    ax = plt.axes(projection=cartopy.crs.Robinson(0))
    ax.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=1)

    ax.coastlines(resolution='10m')
    ax.add_feature(cartopy.feature.OCEAN, facecolor=(0.5, 0.5, 0.5))
    ax.add_feature(cart.feature.LAND, zorder=100, edgecolor='k')
    ax.gridlines()
    # ax.set_extent((-7.5, 50, 34, 69), cartopy.crs.PlateCarree())


    colors = (
        '#3000e2', '#2548ff', '#27a7ff', '#70e4ff', '#cbfdff',
        '#fdf9d2', '#fec783', '#ff5d46', '#fe0229', '#b40018')

    cmap1 = mcolors.ListedColormap(colors)
    norm1 = mcolors.BoundaryNorm(clevs, cmap1.N)
    m = ax.pcolormesh(x, y, z[:, :], norm=norm1, cmap=cmap1,
                      transform=cartopy.crs.PlateCarree())

    cbar = plt.colorbar(m, norm=norm1, cmap=cmap1, ticks=clevs, boundaries=clevs, extend='max', extendfrac='auto',
                        shrink=0.6, orientation='vertical')
    cbar.set_label('${uMol C/ L}$')


    plt.title('Ocean Sfc Concentration ' + name+' '+month)
    plt.savefig(name+'_new_'+month+'.png', dpi = 300)
    plt.close()




if __name__=="__main__":
    path = './'
    # temp_global_CapeVerde

    names = ['POLY','PROT','LIP','HUM','PROC']

    clevs = [np.array([0, 3, 6, 9, 12, 15, 18, 21, 24, 27]),
             np.array([0, 10, 20, 30, 40, 50,60,70, 80,90]),
             np.array([0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2,5 ,8]),
             np.array([0, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20,50, 70]),
             np.array([0, 10, 20, 30, 40, 50, 60, 70])]
    vars = ['TRUEPROTC','TRUEPOLYC','TRUELIPC','TRUEHUMC','TRUEPROCC']
    file_name = []
    [file_name.append(vars[i]+'.nc') for i in range(len(vars))]


    # for j in range(len(month)):
    #     Chl = np.array(nc.variables['CHL1'][month[j]][:])
    #     Chl_1, loni = \
    #         addcyclic(Chl, lon)
    #     x, y = np.meshgrid(loni, lat)
    #     lll = Chl_1.min()
    #     function_plot_chl(x, y, Chl_1, 'chl-a', months[j], '_global_',ccrs.Robinson(central_longitude=180))

    C_old = 0
    for i in range(3):
        l = 1
        nc = Dataset(path + file_name[i], mode='r')


        lat = np.array(nc.variables['lat'][:])
        lon = np.array(nc.variables['lon'][:])

        C = np.array(nc.variables[vars[i]][1])
        # C = np.array(nc.variables[vars[i]][0][-1][:])
        #
        print(C.shape)
        C_old = C



        C1, loni = C, lon
        units = "uMol C / L"
        month = 'FEB'
        print(vars[i],C.max(),C.min())
        x, y = np.meshgrid(loni, lat)
        # function_plot_2(x,y,C1,vars[i],month,clevs[i])



    nc = Dataset(path + 'macromolecules_all.nc', mode='r')

    lat = np.array(nc.variables['lat'][:])
    lon = np.array(nc.variables['lon'][:])

    clevs = np.array([0, 0.05, 0.1, 0.5, 1,2,2.5,3,3.5,4, 5])
    C = np.array(nc.variables[vars[0]][1])
    C_old = C

    C1, loni = C, lon
    units = "uMol C / L"
    month = 'orig_FEB_scale'
    x, y = np.meshgrid(loni, lat)
    function_plot_2(x,y,C1,vars[0],month,clevs)




    nc = Dataset('/Users/leon/Desktop/Burrows_param/DATA_Biochem_model/Moritz_data/2015/Macromolecules_FESON_RECOM.nc', mode='r')

    lat = np.array(nc.variables['lat'][:])
    lon = np.array(nc.variables['lon'][:])

    clevs = np.array([0, 0.05, 0.1, 0.5, 1,2,2.5,3,3.5,4, 5])

    mm = [1,8]
    for m in mm:
        for i in range(3):
            C = np.array(nc.variables[vars[i]][m])
            C_old = C

            C1, loni = C, lon
            units = "uMol C / L"
            month = 'FESON_RECOM_' + str(m+1)
            x, y = np.meshgrid(loni, lat)
            function_plot_2(x,y,C1,vars[i],month,clevs)
