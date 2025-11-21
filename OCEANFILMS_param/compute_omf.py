import numpy as np


def constants():
    '''Parameters of OCEANFILMS scheme for polysaccharides, proteins and lipids
     following Burrows et al. 2014.
     All parameters were taken from Burrows et al. 2014 or provided
    through personal communication with Dr. Susannah Burrows 
    (Scientist at Pacific Northwest National Laboratory)'''

    ro = 1.025E6  # seawater density kg/L to g/m3
    s = 0.035  # ocean salinity kg/kg
    nbu = 2   # the coverage of the interior and exterior films of the bubble
    lbu = 0.1E-6  # mean film thickness (micromters) to m
    mm = [250000,  # Molar mass of polysaccharides (g/mol)
          66463,  # proteins
          284]  # lipids

    c1_2 = [0.1,  # Half saturation concentration of polysaccharides (molC/L)
            1.E-4,  # proteins
            1.E-6]  # lipids

    # ! OM to OC ratio
    # ! Scott's numbers
    om_oc = [2.3,
             2.2,
             1.3]

    # ! Carbon gamma_max from Scott [(atoms C) A-2]
    gamma_max = [30.,  # Soluble starch: 10-100; Alginate: 50-100; Pectin: "Close packing"; Gum arabic: 50
                 0.5,  # Lysozyme: 1.0; albumin, casein: 0.5
                 1.0]  # SDS: 0.2; Oleic and Stearic: 1.0; Cholesterol: 0.7

    # ! Conversion mol_C to mol_OM
    # ! [(g OM) (g C)-1] [(g/mol C) (g/mol OM)]  ==> [(mol OM) (mol C)-1]
    carbon_mm = 12
    c_to_om = []
    [c_to_om.append(om_oc[i] * carbon_mm / mm[i]) for i in range(len(om_oc))]

    # ! Langmuir parameter [m3 mol-1]
    # ! 1 / ([mol C per L] * [1e3 L per m3] * [mol OM per mol C])
    lang = []
    [lang.append(1 / (c1_2[i] * 1.e3 * c_to_om[i])) for i in range(len(c1_2))]

    c1_2_om = []
    [c1_2_om.append(c1_2[i] * 1.e3 * c_to_om[i]) for i in range(len(c1_2))]

    # ! Specific area [m2 (mol OM)-1]]
    # ! [(atoms C) A-2] / 6.022e23 [(atom C) per (mol C)] * [(1e20 A2) m-2] * [(mol OM) (mol C)-1] ==> [(mol OM) m-2]
    avogadro = 6.022e23
    a = []
    [a.append(1 / ((gamma_max[i] / avogadro) * 1e20 * c_to_om[i])) for i in range(len(c_to_om))]

    ma = []
    [ma.append(mm[i] / a[i]) for i in range(len(mm))]

    return c_to_om, lang, nbu, ma, ro, s, lbu


def start_MF_EF(Lang, C):
    Obub = []
    LangC = 0.
    C_Tot = 0.
    for m in range(3):
        LangC = LangC + Lang[m] * C[m]
        C_Tot = C_Tot + C[m]

    for m in range(3):
        Obub.append((Lang[m] * C[m]) / (1 + LangC))

    return Obub


def mass_fracc_in_aer(Lang, C, nbub, Ma, ro, lbub, s):
    Obub = start_MF_EF(Lang, C)
    MF = []

    for m in range(3):
        MF.append((nbub * Obub[m] * Ma[m]) / (nbub * Obub[m] * Ma[m] + ro * lbub * s))

    return MF

def calc_funct(new_C):
    a = len(new_C)
    b = len(new_C[0])
    c = len(new_C[0][0])
    C_to_OM, lang, nbub, Ma, ro, s, lbub = constants()

    for l in range(a):
        for i in range(b):
            for j in range(c):
                new_C[l][i][j] = new_C[l][i][j] * C_to_OM[l] * 1.E-3


    C_total = []
    MF = np.zeros((a, b, c))

    for i in range(b):
        for j in range(c):
            for l in range(a):
                C_total.append(new_C[l][i][j])

            MF[:, i, j] = mass_fracc_in_aer(lang, C_total, nbub,
                                            Ma, ro, lbub, s)

            C_total = []
    return MF
