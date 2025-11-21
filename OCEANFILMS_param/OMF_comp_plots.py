import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np


observation = {'CVAO': {'coord': [14.99, 335.114], 'm': [9, 10], 'OMF': {'poly': [0, 0]}, 'pro': [0.1173, 0.108],
                        'lip': [0.309, 0.147]},
               'PI_ICE': {'coord': [-62.66, 299.61], 'm': [1, 2], 'OMF': {'poly': [0.085,
                                                                                  0.02]}},
               'PASCAL': {'coord': [-67.78, 291.5], 'm': [1, 2],'OMF': {'poly': []}}}

model = {'CVAO': {'poly': [0.028304927697334042, 0.023031158082041557], 'pro': [0.12227937304296652,
                    0.10132205631544758], 'lip': [0.08295851253408788, 0.08136487134831707], 'tot': []},
         'PI_ICE': {'poly': [0.0007583549458685605, 0.0007583549458685605], 'pro': [], 'lip': [], 'tot': []},
         'PASCAL': {'poly': [], 'pro': [], 'lip': [], 'tot': []}}

obs = {'CVAO': {'poly': [0.0295], 'pro': [0.11265], 'lip': [0.228], 'tot': [0.37015]},
         'PI_ICE': {'poly': [0.0525], 'pro': [0], 'lip': [0], 'tot': [0]},
         'PASCAL': {'poly': [0], 'pro': [0], 'lip': [0], 'tot': [0]}}

mod = {'CVAO': {'poly': [0.0257], 'pro': [0.1118], 'lip': [0.082], 'tot': [0.2195]},
         'PI_ICE': {'poly': [0.00825], 'pro': [0], 'lip': [0], 'tot': [0]},
         'PASCAL': {'poly': [0], 'pro': [0], 'lip': [0], 'tot': [0]}}

species_n = ['Polysacc.','Proteins','Lipids', 'MOA']
species = [3*[1], 3*[2],3*[3], 3*[4]]

stations = list(observation.keys())
spec = list(mod['CVAO'].keys())
lista_mo = [[],[],[],[]]
lista_obs = [[],[],[],[]]


for m in range(len(spec)):
    for i in range(len(stations)):
        lista_mo[m].append(mod[stations[i]][spec[m]][0])
        lista_obs[m].append(obs[stations[i]][spec[m]][0])

l_mo = lista_mo[0]
l_ob = lista_obs[0]
name = species[0]
for l in range(1,len(lista_mo)):
    l_mo = l_mo + lista_mo[l]
    l_ob = l_ob + lista_obs[l]
    name = name + species[l]

np.random.seed(19680801)
print(name)
fig, ax = plt.subplots()
# for color in ['tab:blue', 'tab:orange', 'tab:green']:

N = 12
# c = np.random.randint(1, 5, size=N)
c = ['b','b','b','r','r','r','g','g','g','k','k','k']
scatter = ax.scatter(name, l_mo,marker ='o', c=c, label=stations,
           alpha=0.3, edgecolors='none')
scatter1 = ax.scatter(name, l_ob,marker ='x', c=c, label=stations,
           alpha=0.3, edgecolors='none')

print(*scatter.legend_elements())
legend1 = ax.legend(*scatter.legend_elements(), title="Locations")
ax.add_artist(legend1)
plt.ylabel('OMF')
legend = ax.legend((scatter,scatter1), ('modeled','obs'))


ax.grid(True)
plt.ylim([0, 0.6])
x_pos = [1,2,3,4]
bars = species_n

plt.xticks(x_pos, bars)
plt.show()




#
# month 0 OMF at MC [array([0.00267561]), array([0.01266818]), array([0.00117273])]
# month 1 OMF at MC [ array([0.0020962]), array([0.00994645]), array([0.00108319])]
# month 2 OMF at MC [ array([0.00165891]), array([0.00788445]), array([0.00108168])]
# month 3 OMF at MC [ array([0.00113904]), array([0.00542423]), array([0.00159569])]
# month 4 OMF at MC [  array([0.00094827]), array([0.00451897]), array([0.00876531])]
# month 5 OMF at MC [array([0.00099188]), array([0.00472605]), array([0.22354248])]
# month 6 OMF at MC [array([0.00119139]), array([0.00567237]), array([0.52145515])]
# month 7 OMF at MC [ array([0.00282564]), array([0.01337101]), array([0.48449283])]
# month 8 OMF at MC [ array([0.00624484]), array([0.02917738]), array([0.34238527])]
# month 9 OMF at MC [ array([0.00711807]), array([0.03315035]), array([0.01496774])]
# month 10 OMF at MC [array([0.00505021]), array([0.02370045]), array([0.00374303])]
# month 11 OMF at MC [  array([0.0035169]), array([0.01659915]), array([0.00165596])]
