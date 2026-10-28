# Sonde P4 — impacts Gironde (généré)

Généré par `python -m etl.probe.p4` le 28/10/2026 18:21 UTC. Aucun indicateur calculé.

## 1. Dates de vendanges

Second passage : la première lecture découpait les lignes aux blancs et décalait les colonnes.

### Base Daux et al. 2012 (NOAA Paleo), colonne Bordeaux

`https://www.ncei.noaa.gov/pub/data/paleo/historical/europe/europe2012ghd.txt` → **200**

```
2118 lignes
lignes brutes (repr) :
'Year              Als                  Auv                  Aux                  Bea                  Bor                  Bur                 Cha1                 Cha2                  Gai'
'1354                                                                                                                      15.3'
'1355                                                                                                                      13.4'
'Year            Germany         High Loire Valley      Ile de France            Jura               Languedoc        Low Loire Valley        Luxembourg          Maritime alps       Northern Italy'
'1354              Ger                  HLV                  IdF                  Jur                  Lan                  LLV                  Lux                  Mar                  NIt'
'1355'
'1976             21.7                                                            6.0                 11.7                  8.8                                       1.0'
'2003              8.0                                                                                -4.3                 -10.1                                     -4.0'
'2006                                                                                                 16.1                 16.0                                      16.0'
'1976                                                       28.0                 29.0                 24.9                 39.0'
'2003                                                                                                 20.8                 34.4'
'2006                                                                                                 20.4                 24.0'
table ligne 137 : colonnes ['Year', 'Als', 'Auv', 'Aux', 'Bea', 'Bor', 'Bur', 'Cha1', 'Cha2', 'Gai'] ; Bor entre les caractères 84 et 106
cellules illisibles (lecture à largeur fixe) : 0
colonne Bor : 327 valeurs, [1449] à [2006]
1800s : 1800:23.8, 1801:14.3, 1802:22, 1803:25.2, 1804:14.2, 1805:22.2, 1806:20.2, 1807:11.3, 1808:13, 1809:28.7
1810s : 1810:19.3, 1811:13.2, 1812:21.3, 1813:34.2, 1814:29.2, 1815:25.2, 1816:57.2, 1817:33.2, 1818:16.2, 1819:21.2
1820s : 1820:27.2, 1821:33.2, 1822:-5.8, 1823:36.6, 1824:33.6, 1825:9.7, 1826:18.5, 1827:18.5, 1828:15.3, 1829:25.3
1830s : 1830:15.6, 1831:13.4, 1832:20.5, 1833:20.7, 1834:9, 1835:24, 1836:23.8, 1837:25.8, 1838:29.3, 1839:26.3
1840s : 1840:18.6, 1841:19.3, 1842:21.8, 1843:36.3, 1844:14.8, 1845:38.1, 1846:14.3, 1847:25.3, 1848:19.8, 1849:21
1850s : 1850:29.2, 1851:26.9, 1852:24.3, 1853:39.2, 1854:35, 1855:36.8, 1856:29.9, 1857:19, 1858:20, 1859:22
1860s : 1860:28, 1861:21.8, 1862:19, 1863:23.1, 1864:17.2, 1865:6.2, 1866:20.8, 1867:18.3, 1868:6.4, 1869:14.9
1870s : 1870:10.2, 1871:22.2, 1872:25.8, 1873:22.8, 1874:15, 1875:23.2, 1876:29, 1877:26, 1878:24, 1879:44.2
1880s : 1880:22.6, 1881:21.1, 1882:25.1, 1883:29.6, 1884:25.1, 1885:26.1, 1886:24.6, 1887:24.6, 1888:32.1, 1889:35.6
1890s : 1890:31.1, 1891:34.6, 1892:17.6, 1893:-12.4, 1894:28.1, 1895:21.1, 1896:16.1, 1897:15.6, 1898:20.1, 1899:21.1
1900s : 1900:18.1, 1901:10.6, 1902:20.6, 1903:22.1, 1904:15.1, 1905:13.6, 1906:11.6, 1907:22.1, 1908:14.1, 1909:22.1
1910s : 1910:36.4, 1911:14.4, 1912:19.4, 1913:22.9, 1914:19.1, 1915:19.1, 1916:24.1, 1917:16.1, 1918:22.1, 1919:19.1
1920s : 1920:18.9, 1921:13.1, 1922:10.9, 1923:26.1, 1924:15.9, 1925:28.9, 1926:23.4, 1927:19.4, 1928:17.4, 1929:22.1
1930s : 1930:26.4, 1931:20.1, 1932:39.9, 1933:20.1, 1934:16.1, 1935:24.1, 1936:31.1, 1937:19.1, 1938:24.7, 1939:26.2
1940s : 1940:24.4, 1941:24.9, 1942:21.1, 1943:14.7, 1944:20.9, 1945:8.9, 1946:29.8, 1947:13.1, 1948:20.8, 1949:26.1
1950s : 1950:17.1, 1951:34.1, 1952:16.1, 1953:28.8, 1954:35.4, 1955:25.1, 1956:39.2, 1957:29.1, 1958:35.4, 1959:20.6
1960s : 1960:13.4, 1961:14.6, 1962:30.7, 1963:33.1, 1964:25.1, 1965:30.6, 1966:22.5, 1967:22.2, 1968:24.3, 1969:23.5
1970s : 1970:26.5, 1971:26.6, 1972:36.1, 1973:24.9, 1974:26.6, 1975:24.1, 1976:11.7, 1977:34.4, 1978:35.2, 1979:29.7
1980s : 1980:34.7, 1981:24.2, 1982:14.7, 1983:27.2, 1984:27.2, 1985:23.7, 1986:27.7, 1987:28.7, 1988:27.2, 1989:1.2
1990s : 1990:9.2, 1991:25.7, 1992:19.7, 1993:17.2, 1994:13.2, 1995:13.2, 1996:17.7, 1997:12.7, 1998:15.7, 1999:4.2
2000s : 2000:15.7, 2001:18.7, 2002:26.7, 2003:-4.3, 2004:11.1, 2005:-4.9, 2006:16.1
années manquantes 1900-2006 : []
```

### ONERC, page « agriculture et forêt » (série Saint-Émilion)

`https://www.ecologie.gouv.fr/politiques-publiques/impacts-du-changement-climatique-agriculture-foret` → **200**

```
102155 caractères, 103 liens
/sites/default/files/styles/default_mobile/public/images/19_Graph_indicateur_date_vendanges_Saint-Emilion.png?itok=HLn-yxaI
/sites/default/files/styles/default_mobile/public/images/21_Visuel_1_Graph_indicateur_Dates_recolte_ble_Mirecourt.png?itok=m4kK2B80
/sites/default/files/styles/default_mobile/public/images/21_Visuel_2_Graph_indicateur_Dates_recolte_ble_Breteniere.png?itok=RDUfWhR6
/sites/default/files/styles/default_mobile/public/images/21_Visuel_3_Graph_indicateur_Dates_recolte_ble_Auzeville.png?itok=tRSCspi9
/sites/default/files/styles/default_mobile/public/images/22_Graph_indicateur_dates_d%C3%A9bu_vendanges_C%C3%B4tes_d_Rh%C3%B4ne_m%C3%A9ridionales.png?itok=DILKfX2V
/sites/default/files/styles/default_mobile/public/images/23_Graph_indicateur_date_floraison_vendanges_en_Champagne.png?itok=tecxbMum
/sites/default/files/styles/default_mobile/public/images/Onerc_Date%20des%20vendanges_1901_2016.png?itok=7x5hqSnk
— contexte —
dernières années (95 jours d'écart en 1951-1961 contre 86 en 2015-2025).&nbsp;</p></div><div class="paragraph paragraph--type--accordion-group paragraph--view-mode--default"><h2 > Date de vendanges à Saint-Emilion (Gironde)</h2><div class="paragraph paragraph--type--accordion-group paragraph--view-mode--default fr-accordions-group" data-component-id="customer:accordion_group" data-fr-group="false"><div class="paragraph paragraph--type--accordion-element paragraph--view-mode--default"> <section d
ion"><h3 class="fr-accordion__title"> <button class="fr-accordion__btn" aria-expanded="false" aria-controls="accordion-587886023" type="button"> Définition de l&#039;indicateur de date de vendanges à Saint-Emilion (Gironde) </button></h3><div class="fr-collapse" id="accordion-587886023"><p>Cet indicateur rend compte de la date de début des vendanges dans une propriété de l’appellation Saint-Émilion depuis 1900.</p></div> </section></div><div class="paragraph paragraph--type--accordion-element pa
dion__title"> <button class="fr-accordion__btn" aria-expanded="false" aria-controls="accordion-265263275" type="button"> Responsable et origine des données de l&#039;indicateur de date de vendanges à Saint-Emilion (Gironde) </button></h3><div class="fr-collapse" id="accordion-265263275"><p>Responsable de l’indicateur&nbsp;: Pr. Cornelis (Kees) VAN&nbsp;LEEUWEN, INRAE et Bordeaux Sciences Agro</p><p>Organisme propriétaire des données&nbsp;: INRAE et Bordeaux Sciences Agro</p><p>Date de dernière a
dion"><h3 class="fr-accordion__title"> <button class="fr-accordion__btn" aria-expanded="false" aria-controls="accordion-221818234" type="button"> Fiabilité de l&#039;indicateur de date de vendanges à Saint-Emilion (Gironde) </button></h3><div class="fr-collapse" id="accordion-221818234"><p>La date des vendanges est un indicateur pertinent du régime thermique de l’année. La phénologie de la vigne est corrélée à la somme des températures moyennes journalières supérieures à 10&nbsp;°C. En effet, la
— scripts —
```

### Recherche Data Gouv : jeux de données « vendanges »

`https://entrepot.recherche.data.gouv.fr/api/search?q=vendanges&type=dataset&per_page=30` → **200**

```
```

### INRAE Colmar (indicateur ONERC Alsace), fichiers

`https://entrepot.recherche.data.gouv.fr/api/datasets/:persistentId/?persistentId=doi%3A10.15454/GYSGNR` → **200**

```
ReadMe_PhenoRiesling_INRA_Bergheim_2024.rtf (10693 o)
RieslingPhenology_Bergheim_68_1958_2026.tab (5753 o)
```
