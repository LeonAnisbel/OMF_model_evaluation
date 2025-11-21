from OCEANFILMS_param import global_vars
from Reading_nc import read_nc
import numpy as np
from compute_omf import calc_funct
import generate_nc

if __name__ == '__main__':
    path = global_vars.path_fesom_biom
    # month_list = np.arange(10)
    years = np.arange(1990, 2020)
    for y in years:
        print(y)
        MF_pol, MF_pro, MF_lip = [], [], []
        C_m = []
        yr = 'res025_' + str(y)
        for o in range(12):
            C, lat, lon = read_nc(o, yr, path)
            Conc = np.array(C)

            MF = calc_funct(Conc)

            MF_pol.append(MF[0])
            MF_pro.append(MF[1])
            MF_lip.append(MF[2])

            C_m.append(Conc)

            min_color = MF.min()
            max_color = MF.max()

        MF_all = [MF_pol, MF_pro, MF_lip]
        names = ['Polysaccharides', 'Proteins', 'Lipids']

        # initializing 3D array
        pol = np.zeros((12, len(lat), len(lon)))
        pro = np.zeros((12, len(lat), len(lon)))
        lip = np.zeros((12, len(lat), len(lon)))

        # Defining 3D array
        for i in range(len(MF_pol)):
            pol[i, :, :] = MF_pol[i]
            pro[i, :, :] = MF_pro[i]
            lip[i, :, :] = MF_lip[i]

        ds = generate_nc.create_dataset(pol, pro, lip, y, lon, lat)
        # new_filename_1 = f'./{global_vars.exp_biomolecules}oceanfilms_omf_{yr}.nc'
        # ds.to_netcdf(path=new_filename_1)
