# Sonde P6 — sources mondiales (généré)

Généré par `python -m etl.probe.p6` le 31/10/2026 20:49 UTC. Aucun indicateur calculé.

## Puits de carbone : fichiers CSV openclimatedata (Global Carbon Budget 2025)

### `https://openclimatedata.github.io/global-carbon-budget/data/global-carbon-budget-2025-ocean-sink-gcb.csv` → **200**

```
102 lignes
# Global Carbon Budget 2025 — Global_Carbon_Budget_2025_v1.0.xlsx  — Ocean Sink
#
# Ocean CO2 sink (positive values represent a flux from the atmosphere to the ocean)
# All values in billion tonnes of carbon per year (GtC/yr), for the globe. For values in billion tonnes of carbon dioxide per year (GtCO2/yr), multiply the numbers below by 3.664.
# 1 billion tonnes C = 1 petagram of carbon (10^15 gC) = 1 gigatonne C = 3.664 billion tonnes of CO2
# Methods: The ocean sink (uncertainty of ±0.4 GtC/yr on average) is estimated from the average of 10 global ocean biogeochemistry models and 9 fCO2-products that reproduce the observed mean ocean sink of the 1990s. Cite as: Friedlingstein et al 2025 (see summary tab). The GCB adjusted column includ
# Prior to 1990, the GCB ocean sink estimate is calculated from the GOBM multi-model mean with an offset applied. The offset is calculated as the half of the difference between GOBMs and data products in the period 1990-1999 (inclusive). This ensures no artificial jumps occur in 1990 when the data p
# Note: the surface ocean fCO2-products are adjusted for a pre-industrial steady state source of CO2 from rivers (of 0.65 GtC/yr) to be comparable with the ocean model results and to satisfy the definition of the ocean carbon sink used in the Global Carbon Budget.
# Cite individual estimates as:
# Global ocean biogeochemical models:
# ACCESS (CSIRO)	Law, R. M., Ziehn, T., Matear, R. J., Lenton, A., Chamberlain, M. A., Stevens, L. E., Wang, Y.-P., Srbinovsky, J., Bi, D., Yan, H., and Vohralik, P. F.: The carbon cycle in the Australian Community Climate and Earth System Simulator (ACCESS-ESM1) - Part 1: Model description and pre-
# CESM-ETHZ	Doney, S. C., Lima, I., Feely, R. A., Glover, D. M., Lindsay, K., Mahowald, N., Moore, J. K., and Wanninkhof, R.: Mechanisms governing interannual variability in upper-ocean inorganic carbon system and air-sea CO2 fluxes: Physical climate and atmospheric dust, Deep-Sea Res. Pt. II, 56, 6
…
2021,3.14461483961061,2.94242080690918
2022,3.12045088068765,2.91759282450711
2023,3.27543128208379,3.06793569525405
2024,3.38894731727194,3.17499250428639
```

### `https://openclimatedata.github.io/global-carbon-budget/data/global-carbon-budget-2025-terrestrial-sink-gcb.csv` → **200**

```
102 lignes
# Global Carbon Budget 2025 — Global_Carbon_Budget_2025_v1.0.xlsx  — Terrestrial Sink
#
# Terrestrial CO2 sink (positive values represent a flux from the atmosphere to the land)
# All values in billion tonnes of carbon per year (GtC/yr), for the globe. For values in billion tonnes of carbon dioxide per year (GtCO2/yr), multiply the numbers below by 3.664.
# 1 billion tonnes C = 1 petagram of carbon (10^15 gC) = 1 gigatonne C = 3.664 billion tonnes of CO2
# Methods: The terrestrial sink (uncertainty of ±0.5 GtC/yr on average) is estimated from the average of 22 Dynamic Global Vegetation Models (calculated from simulation S2; see Supplementary S4.1 in Friedlingstein et al. 2025) that reproduce the observed mean total land uptake of the 1990s. GCB adju
# Cite individual estimates as:
# CABLE-POP	Haverd, V., Smith, B., Nieradzik, L., Briggs, P. R., Woodgate, W., Trudinger, C. M., Canadell, J. G., and Cuntz, M.: A new version of the CABLE land surface model (Subversion revision r4601) incorporating land use and land cover change, woody vegetation demography, and a novel optimisati
# CLASSIC	Melton, J. R., Arora, V. K., Wisernig-cojoc, E., Seiler, C., Fortier, M. and Chan, E.: CLASSIC v1 . 0 : the open-source community successor to the Canadian Land Surface Scheme ( CLASS ) and the Canadian Terrestrial Ecosystem Model ( CTEM ) - Part 1 : Model framework and site-level performa
# CLM6.0	Lawrence, D. M., Fisher, R. A., Koven,C. D., Oleson, K. W., Swenson, S. C.,Bonan, G., et al.: The Community Land Model version 5: Description of new features, benchmarking, and impact of forcing
# CLM-FATES	uncertainty. Journal of Advances in Modeling Earth Systems, 11, 4245-4287. https://doi.org/10.1029/2018MS001583, 2019.
# DLEM	Tian, H., G. Chen, C. Lu, X. Xu, D. J. Hayes, W. Ren, S. Pan, D.N. Huntzinger, S.C. Wofsy: North American terrestrial CO2 uptake largely offset by CH4 and N2O emissions: Toward a full accounting of the greenhouse gas budget, Climatic Change, 129:423-426, https://doi.org/10.1007/s10584-014-107
…
2021,2.59562956218391,3.29090069405422
2022,3.1061842407254,3.92121511200666
2023,2.01670466921629,2.57617860397072
2024,1.94215497985298,2.48414195043578
```

### `https://openclimatedata.github.io/global-carbon-budget/data/global-carbon-budget-2025-fossil-emissions.csv` → **200**

```
188 lignes
# Global Carbon Budget 2025 — Global_Carbon_Budget_2025_v1.0.xlsx  — Fossil Emissions by Category
#
# Fossil fuel and cement production emissions by fuel type
# All values in billion tonnes of carbon per year (GtC/yr), except the per capita emissions which are in tonnes of carbon per person per year (tC/person/yr). For values in billion tonnes of CO2 per year, multiply the values below by 3.664
# 1 billion tonnes C = 1 petagram of carbon (10^15 gC) = 1 gigatonne C = 3.664 billion tonnes of CO2
# Methods: Full details of the method are described in Friedlingstein et al (2025) and Andrew and Peters (2025). Full country and fuel data can be found at https://zenodo.org/records/17417124
# The uncertainty for the global estimates is about ±5 % for a ± 1 sigma confidence level.
# Cite as: Friedlingstein et al (2025; see summary tab)
#
# GtC/yr
# Generated with openclimatedata 0.40.1 from the GCB Excel file 'Global_Carbon_Budget_2025_v1.0.xlsx' from https://doi.org/10.18160/gcp-2025
# http://openclimatedata.net - https://github.com/openclimatedata/global-carbon-budget
…
2021,10.061916972685,4.0854938283004,3.14223973707289,2.15029972921194,0.454935869338336,0.109775162301751,0.119172646459688,1.2649421403084955
2022,10.2422957637073,4.21647843671564,3.25188651438613,2.11756152743731,0.430878642879053,0.108862209965357,0.116628432323809,1.2768701947860548
2023,10.3968461161941,4.26756914241784,3.35104842956972,2.12959751910326,0.420383790354005,0.112266023548422,0.115981211200814,1.2848723056470746
2024,10.5345464062896,4.31366106774629,3.40354681135657,2.18608834226212,0.401969831482778,0.113457329801199,0.115823023640606,1.2906863277669887
```

### `https://openclimatedata.github.io/global-carbon-budget/data/global-carbon-budget-2025-land-use-change-emissions-gcb.csv` → **200**

```
109 lignes
# Global Carbon Budget 2025 — Global_Carbon_Budget_2025_v1.0.xlsx  — Land-Use Change Emissions
#
# Land-use change emissions
# All values in billion tonnes of carbon per year (GtC/yr), for the globe. For values in billion tonnes of carbon dioxide per year (GtCO2/yr), multiply the numbers below by 3.664.
# 1 billion tonnes C = 1 petagram of carbon (10^15 gC) = 1 gigatonne C = 3.664 billion tonnes of CO2
# Methods: The GCB estimate is the average of three bookkeeping models BLUE, OSCAR, and LUCE (uncertainty of ±0.7 GtC/yr). Individual results from dynamic global vegetation models (calculated as S2-S3; see Supplementary S2.2 in Friedlingstein et al. 2025) are also provided but not used for the GCB e
# Data below represents the net flux of land-use change, based on the net balance between deforestation and forest regrowth along with other land-use changes
# Cite individual estimates as:
# BLUE	Hansis, E., Davis, S. J., and Pongratz, J.: Relevance of methodological choices for accounting of land use change carbon fluxes, Global Biogeochemical Cycles, 29, 1230-1246, https://doi.org/10.1002/2014GB004997, 2015.
# OSCAR	Gasser, T., Crepin, L., Quilcaille, Y., Houghton, R. A., Ciais, P., and Obersteiner, M.: Historical CO 2 emissions from land use and land cover change and their uncertainty, Biogeosciences, 17, 4075–4101, https://doi.org/10.5194/bg-17-4075-2020, 2020.
# LUCE	Qin, Z., Zhu, Y., Canadell, J. G., Chen, M., Li, T., Mishra, U., and Yuan, W.: Global spatially explicit carbon emissions from land-use change over the past six decades (1961-2020), One Earth, 7, 835-847, https://doi.org/10.1016/j.oneear.2024.04.002, 2024
#
…
2021,1.27104333333333,1.87347333333333,-1.30807666666667,0.08702,0.19655,0.422076666666667
2022,1.30605666666667,1.90669666666667,-1.31074666666667,0.0782633333333333,0.20541,0.42643
2023,1.29518333333333,1.87733,-1.32096666666667,0.0778566666666667,0.236016666666667,0.424946666666667
2024,1.25150333333333,1.87181666666667,-1.32628,0.0765333333333333,0.210456666666667,0.418973333333333
```
