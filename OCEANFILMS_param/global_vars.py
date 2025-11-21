path_fesom_biom = '/Users/Leon/Desktop/Folder_from_linux/Downloads/ocean_data/yearly_data/'
path_cesm_biom = 'CESM_BGC/' # this data refers to the macromolecule carbon concentration from CESM model
                            # (Burrows et al. 2014). It is not publicly available.
                            # Contact leon@tropos.de or heinold@tropos.de to request access to it.
exp_biomolecules = "" # three experiments available for the sensitivity analysis presented in CHAPTER 5 of Leon-Marcos et al. 2026 Doctoral Thesis
                      # "" no ID uses only FESOM-REcoM model-derived biomolecules
                      # "burrows_" uses only burrows CESM model-derived macromolecules
                      # "fesom_burrows_" uses FESOM-REcoM model-derived poly and prot and assume for lipids
                      # the sum of FESOM-REcoM computed polar lipids and CESM model-derived lipid-like mixture
