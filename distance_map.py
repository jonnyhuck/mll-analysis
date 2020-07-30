"""
This is analysing locations based on village names rather than codes
"""
from geopandas import read_file
from pandas import read_csv, DataFrame
from pyproj import Geod


# set which ellipsoid you would like to use
g = Geod(ellps='WGS84')


def distance(o, d):
    """
    * ellipsoidal distance
    """
    # measure the forward azimuth, back azimuth and distance between two points
    azF, azB, distance = g.inv(o[0], o[1], d[0], d[1])
    return distance


# open datasets
# mll_survey = read_csv("./datasets/limbloss_extract2020apr2.csv")[['parish', 'hlthcare', 'contrib', 'rehabacs']]
mll_survey = read_csv("./datasets/edited MLL dataset_22April2020.csv")[['parish', 'hlthcare2', 'contrib', 'rehabacs']]
parishes = read_file("/Users/jonnyhuck/Dropbox/Manchester/Research/Uganda/1.MLL-MRC-AHRC/data/acholi/parishes.shp")

# There are lots of duplicated parish names
# print(parishes[parishes.PNAME_2010.duplicated()])

''' DATA REPAIR '''

# repair discrpancies (by manual comparison with the parish dataset)
mll_survey.loc[mll_survey['parish'] == 'ALANGO WARD', 'parish'] = 'ALANGO'
mll_survey.loc[mll_survey['parish'] == 'ATIYABAR', 'parish'] = 'ATIABA'
mll_survey.loc[mll_survey['parish'] == 'ATOO', 'parish'] = 'ATO'
mll_survey.loc[mll_survey['parish'] == 'FORGOD', 'parish'] = 'FOR GOD WARD'
mll_survey.loc[mll_survey['parish'] == 'GEM ONYOT', 'parish'] = 'GEM'
mll_survey.loc[mll_survey['parish'] == 'GWENGDIYA', 'parish'] = 'GWENDIYA'
mll_survey.loc[mll_survey['parish'] == 'KAL UMU', 'parish'] = 'KAL-UMU'
mll_survey.loc[mll_survey['parish'] == 'KALUMU', 'parish'] = 'KAL-UMU'
mll_survey.loc[mll_survey['parish'] == 'KASUBI', 'parish'] = 'KASUBI WARD'
mll_survey.loc[mll_survey['parish'] == 'LAROO', 'parish'] = 'LARO'
mll_survey.loc[mll_survey['parish'] == 'LOLIA', 'parish'] = 'LOLIYA'
mll_survey.loc[mll_survey['parish'] == 'LOLWA', 'parish'] = 'LOLWAR'
mll_survey.loc[mll_survey['parish'] == 'LUJORO', 'parish'] = 'LUJORONGOLE'
mll_survey.loc[mll_survey['parish'] == 'LUKWO', 'parish'] = 'LUKWOR'
mll_survey.loc[mll_survey['parish'] == 'MEDDE', 'parish'] = 'MEDE'
mll_survey.loc[mll_survey['parish'] == 'OBBO', 'parish'] = 'OBOO'
mll_survey.loc[mll_survey['parish'] == 'ATOO', 'parish'] = 'ATO'
mll_survey.loc[mll_survey['parish'] == 'ORYANG CENTRAL', 'parish'] = 'ORYANG'
mll_survey.loc[mll_survey['parish'] == 'PABWOR', 'parish'] = 'PABWO'
mll_survey.loc[mll_survey['parish'] == 'PAGAK AMOYOMOMA', 'parish'] = 'PAGAK'
mll_survey.loc[mll_survey['parish'] == 'PAGER', 'parish'] = 'PAGER WARD'
mll_survey.loc[mll_survey['parish'] == 'PAGER A', 'parish'] = 'PAGER WARD'
mll_survey.loc[mll_survey['parish'] == 'PALOGA', 'parish'] = 'PALUGA'
mll_survey.loc[mll_survey['parish'] == 'PARACELLE', 'parish'] = 'PARACELE'
mll_survey.loc[mll_survey['parish'] == 'PARWACA', 'parish'] = 'PARWACHA'
mll_survey.loc[mll_survey['parish'] == 'PECE', 'parish'] = 'PECE PRISONS WARD'
mll_survey.loc[mll_survey['parish'] == 'PONGDWONGO', 'parish'] = 'PONDWONG'
mll_survey.loc[mll_survey['parish'] == 'PUBECH', 'parish'] = 'PUBEC'
mll_survey.loc[mll_survey['parish'] == 'PUGODA', 'parish'] = 'PUGODA EAST'
mll_survey.loc[mll_survey['parish'] == 'TECHO', 'parish'] = 'TECHO WARD'
mll_survey.loc[mll_survey['parish'] == 'TEEGWANA', 'parish'] = 'TEGWANA WARD'
mll_survey.loc[mll_survey['parish'] == 'TOWN PARISH', 'parish'] = 'TOWN BOARD'
mll_survey.loc[mll_survey['parish'] == 'Bwebonam kal', 'parish'] = 'BWOBONAM'
mll_survey.loc[mll_survey['parish'] == 'Bwobonam', 'parish'] = 'BWOBONAM'
mll_survey.loc[mll_survey['parish'] == 'Ongom ward', 'parish'] = 'OGOM'
mll_survey.loc[mll_survey['parish'] == 'Pabali', 'parish'] = 'PABALI'
mll_survey.loc[mll_survey['parish'] == 'Patira', 'parish'] = 'PATIRA'
mll_survey.loc[mll_survey['parish'] == 'Todora', 'parish'] = 'TODORA'
mll_survey.loc[mll_survey['parish'] == 'agonga A', 'parish'] = 'AGONGA'
mll_survey.loc[mll_survey['parish'] == 'pabit', 'parish'] = 'PABIT'

# report matches
# print(len(mll_survey.parish.unique()))
# print(sum(el in list(mll_survey.parish.unique()) for el in list(parishes.PNAME_2010.unique())))
# print()

# report missing
# missing = []
# for i in mll_survey.parish.unique():
#     if i not in list(parishes.PNAME_2010.unique()):
#         missing.append(i)
# print(sorted(missing))
# print()
# print(sorted(list(parishes.PNAME_2010.unique())))
# exit()

# transform health parameters to y/n (not required)
# mll_survey.loc[mll_survey['hlthcare'] == 'No', 'hlthcare'] = 'False'
# mll_survey.loc[mll_survey['hlthcare'] != 'No', 'hlthcare'] = 'True'
#
# # device (e.g. prosthetic)
# mll_survey.loc[mll_survey['contrib'] == 'Never', 'contrib'] = 'False'
# mll_survey.loc[mll_survey['contrib'] != 'Never', 'contrib'] = 'True'
#
# # rehabilitation services
# mll_survey.loc[mll_survey['rehabacs'] == 'Never', 'rehabacs'] = 'False'
# mll_survey.loc[mll_survey['rehabacs'] != 'Never', 'rehabacs'] = 'True'

''' DISTANCE CALCULATION '''

# calculate distance to GROW for each parish
parishes['distance'] = parishes.geometry.apply(lambda x: distance(x.centroid.coords[0], [32.299807, 2.778360]))

''' COUNT INCIDENCES '''

# count mll per parish
mll = mll_survey.parish.value_counts(dropna=False)
mll_counts = DataFrame(data={'name': list(mll.index), 'mll': list(mll)})
print(f"MLL Sufferers: {mll.sum()}")

# count never accessed healthcare per parish
healthcare = mll_survey.loc[mll_survey['hlthcare2'] == 'Never'].parish.value_counts(dropna=False)
healthcare_counts = DataFrame(data={'name': list(healthcare.index), 'healthcare': list(healthcare)})
print(f"never accessed healthcare (6 months): {healthcare.sum()} / {mll_survey['hlthcare2'].count()} ({healthcare.sum() / mll_survey['hlthcare2'].count() * 100:.1f}%)")

# count never accessed assistive device per parish
device = mll_survey.loc[mll_survey['contrib'] == 'Never'].parish.value_counts(dropna=False)
device_counts = DataFrame(data={'name': list(device.index), 'device': list(device)})
print(f"never accessed assistive device (6 months): {device.sum()} / {mll_survey['contrib'].count()} ({device.sum() / mll_survey['contrib'].count() * 100:.1f}%)")

# # count never accessed rehab services per parish
rehab = mll_survey.loc[mll_survey['rehabacs'] == 'Never'].parish.value_counts(dropna=False)
rehab_counts = DataFrame(data={'name': list(rehab.index), 'rehab': list(rehab)})
print(f"never accessed rehab (6 months): {rehab.sum()} / {mll_survey['rehabacs'].count()} ({rehab.sum() / mll_survey['rehabacs'].count() * 100:.1f}%)")

# join count results to parish dataset (bodge to get around index problem)
parishes1 = parishes.merge(mll_counts, how='left', left_on=parishes.PNAME_2010, right_on=mll_counts.name)
parishes2 = parishes.merge(healthcare_counts, how='left', left_on=parishes.PNAME_2010, right_on=healthcare_counts.name)
parishes3 = parishes.merge(device_counts, how='left', left_on=parishes.PNAME_2010, right_on=device_counts.name)
parishes4 = parishes.merge(rehab_counts, how='left', left_on=parishes.PNAME_2010, right_on=rehab_counts.name)

# add all columns back into parishes dataset (part of the same bodge)
parishes['mll'] = parishes1['mll']
parishes['healthcare'] = parishes2['healthcare']
parishes['device'] = parishes3['device']
parishes['rehab'] = parishes4['rehab']

print(f"located MLL sufferers: {parishes['mll'].sum()} / {mll.sum()} ({parishes['mll'].sum() / mll.sum() * 100:.1f}%)")

# swap na for 0 in the count columns
parishes.fillna(value={'mll':0, 'healthcare':0, 'device':0, 'rehab':0}, inplace=True)

# output parish dataset
parishes.to_file("../distance-analysis/parishes_mll.shp")
print("done")
