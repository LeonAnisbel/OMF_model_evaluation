import numpy as np

def location(lats,lons,CV_location):

    indice_lat, indice_lon= np.searchsorted(lats,CV_location[0]), \
                            np.searchsorted(lons,CV_location[1])

    return indice_lat, indice_lon


def OMF_comp(lat,lon,MF):
    observation = {'CVAO':{'coord':[14.99, 335.114],'m':[9,10],'OMF':{'poly':[0,0]},'pro':[0.1173,0.108],
                           'lip':[0.309,0.147]}, 'PI_ICE':{'coord':[-67.78,291.5],'m':[1,2],'OMF':{'poly':[0.085,
                                                                                                           0.02]}},
                   'PASCAL': {'coord':[-67.78,291.5],'m':[1,2]}}
    #lon (-lon%360)
    model = {'CVAO':{'poly':[],'pro':[],'lip':[], 'tot':[]},'PI_ICE':{'poly':[],'pro':[],'lip':[], 'tot':[]},'PASCAL':{'poly':[],'pro':[],'lip':[], 'tot':[]} }

    key = list(observation.keys())
    for i in range(len(key)):
        for m in range(len(observation[key[i]]['m'])):
            mo_loc = location(lat, lon, observation[key[i]]['coord'])

            model[key[i]]['poly'].append(MF[m-1][0][mo_loc[0]][mo_loc[1]])
            model[key[i]]['pro'].append(MF[m-1][1][mo_loc[0]][mo_loc[1]])
            model[key[i]]['lip'].append(MF[m-1][2][mo_loc[0]][mo_loc[1]])

    print(model)


