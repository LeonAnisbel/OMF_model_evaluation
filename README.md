# Evaluate OMF of submicron marine aerosol
> The scripts in this project interpolates the model results of organic mass fraction (OMF) to observation sites and dates.
> 
> OMF values are computed following Burrows et al. 2014 (OCEANFILMS) based on FESOM-REcoM-derived biomolecule groups (PCHO, DCAA and PL). See more information in [Leon-Marcos et al. 2025](https://doi.org/10.5194/egusphere-2025-2829). The data to reproduce the results are publicly accessible on Zenodo (https://doi.org/10.5281/zenodo.15172565) under oceanfilms_omf_experiments_res025_1990_2019.zip.
> 
> Run "conda activate environment.yml" to set up the environment for this project.
> 
> Additionally, it allows for the sensitivity analysis presented in CHAPTER 5 of Leon-Marcos et al. 2026 Doctoral Thesis (see "exp_biomolecules" in global_vars.py)
> 

* Run main.py to perform the interpolation of modelled OMF across all biomolecule and station locations. \
This will create several pickle files with the output. It will also create a multipanel box plot with the comparison of modelled and observed OMF values.
