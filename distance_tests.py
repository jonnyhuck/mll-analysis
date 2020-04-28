"""
This is just comparing the locations in the two datasets (neither are complete
 and there isn;t much agreement between them)
"""

from pandas import read_csv, DataFrame, IntervalIndex, cut, value_counts
from geopandas import read_file

# open data points
samples = read_file('../distance-analysis/clusters_d.shp')

# load HoH dataset
hoh_survey = read_csv("./datasets/mll_excell_extract2020.csv")[['code', 'limbloss', 'knowsmll', 'gendamll']]
print("\n--- HOH SURVEY ---")

# count of households with MLL
print("MLL in family:", len(hoh_survey[hoh_survey.limbloss == 'yes'].index))

# count with code
print("\t with code:", len(hoh_survey[hoh_survey.limbloss == 'yes'].dropna(subset=['code']).index))

# list of unique codes
hoh_codes_list = hoh_survey[hoh_survey.limbloss == 'yes']['code'].dropna().astype({'code': 'int64'}).drop_duplicates()

# list of unique codes with counts
hoh_codes = hoh_survey[hoh_survey.limbloss == 'yes'].dropna(subset=['code']).astype({'code': 'int64'}).groupby('code')['code'].value_counts()
print("\t unique codes:", len(hoh_codes.index))

# count of HoH values in the geo dataset
print("\t in geo dataset:", len(hoh_codes.loc[[x in list(samples.id) for x, y in hoh_codes.index]].index))

# count of households who know someone with  MLL
print("\nMLL known:", len(hoh_survey[hoh_survey.knowsmll == 'yes'].index))

# vcount with code
print("\t with code:", len(hoh_survey[hoh_survey.knowsmll == 'yes'].dropna(subset=['code']).index))

# list of unique codes with counts
hoh_codes2 = hoh_survey[hoh_survey.knowsmll == 'yes'].dropna(subset=['code']).astype({'code': 'int64'}).groupby('code')['code'].value_counts()
print("\t unique codes:", len(hoh_codes2.index))

# count of HoH values in the geo dataset
print("\t in geo dataset:", len(hoh_codes2.loc[[x in list(samples.id) for x, y in hoh_codes2.index]].index))

# load MLL dataset
# mll_survey = read_csv("./datasets/limbloss_extract2020apr2.csv")
mll_survey = read_csv("./datasets/edited MLL dataset_22April2020.csv")
print("\n--- MLL SURVEY ---")

# count of MLL
print("MLL sufferers:", len(mll_survey.index))

# count with code
print("\t with code:", len(mll_survey.dropna(subset=['code1']).index))

# get list of unique codes
mll_codes_list = mll_survey['code1'].dropna().astype({'code1': 'int64'}).drop_duplicates()

# clean codes in the dataset (remove decimals that have been included)
mll_codes = mll_survey.dropna(subset=['code1']).astype({'code1': 'int64'}).groupby('code1')['code1'].value_counts()
print("\t unique codes:", len(mll_codes.index))

# count of MLL codes that appear in the geo dataset
print("\t in geo dataset:", len(mll_codes.loc[[x in list(samples.id) for x, y in mll_codes.index]].index))

# compare the two datasets
print("\n--- COMPARISON ---")

# number of the mll codes in the hoh dataset ()
print("MLL codes in HOH codes:", mll_codes.loc[mll_codes.index.isin(hoh_codes.index)].sum())
print("\t unique codes:", len(mll_codes.loc[mll_codes.index.isin(hoh_codes.index)].index))

# compare the two datasets
print("\n--- JOINING ---")

# make new tidy dataframe for HoH
hoh_out = DataFrame(data={ 'code': [x for x, y in hoh_codes.index], 'count': hoh_codes })

# join mll to geo dataset
hoh_samples = samples.merge(hoh_out, how='inner', left_on=samples.id, right_on=hoh_out.code)
print("HOH (household) successful joins:",len(hoh_samples.index))

# make new tidy dataframe for HoH
hoh_out2 = DataFrame(data={ 'code': [x for x, y in hoh_codes2.index], 'count': hoh_codes2 })

# join mll to geo dataset
hoh_samples2 = samples.merge(hoh_out2, how='inner', left_on=samples.id, right_on=hoh_out2.code)
print("HOH (household) successful joins:",len(hoh_samples2.index))

# make new tidy dataframe for MLL
mll_out = DataFrame(data={ 'code': [x for x, y in mll_codes.index], 'count': mll_codes })

# join mll to geo dataset
mll_samples = samples.merge(mll_out, how='inner', left_on=samples.id, right_on=mll_out.code)
print("MLL successful joins:", len(mll_samples.index))


print(mll_samples.head())

exit()

# join the mll data to the points
# samples.join(mll_codes, how='inner', on=samples.id)
# mll_samples = samples.loc[samples.id.isin(mll_codes_list)]
print(f"{len(mll_samples.index)} unique locations after the join")

# report mean and SD
print(f"mean: {mll_samples.dist_to_cl.mean()/1000:.2f}km; SD: {mll_samples.dist_to_cl.std()/1000:.2f}km")

exit()




# sort age data into 10 year bins
mll_distances = value_counts(cut(mll_dist.dist_to_cl, bins), sort=False, ascending=True)

# print(mll_distances)

# extract observed age values
print(cut(mll_dist.dist_to_cl, bins))
print(mll_dist.dist_to_cl.min(), mll_dist.dist_to_cl.max())
print(mll_distances)

ob_total = mll_distances.sum()
observed = mll_distances.to_numpy()
print(ob_total)

# scale expected
expected = array([ int(int(x) / ex_total * ob_total) + 0.5 for x in distances])
