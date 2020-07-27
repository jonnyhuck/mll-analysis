"""
* This is Chi Squared Goodness of Fit test - the distance those with MLL to GROW
*  from the whole sample.
*
* THIS ANALYSIS USES THE DISTANCES GENERATED FROM GEOCODED PARISH LOCATIONS FROM
*   THE MLL DATASET (171 - ONLY 13 COULDN'T BE LOCATED)
*
* https://stats.stackexchange.com/questions/110718/chi-squared-test-with-scipy-whats-the-difference-between-chi2-contingency-and/375063
*
* https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html
* https://colorswall.com/images/palettes/bootstrap-4-colors-3-colorswall.png
*
* Result:
    mean: 68.73km; SD: 40.34km
    mean: 64.51km; SD: 40.16km

    [33 33 29 23 43 16 13  7  1]
    [20.5 36.5 34.5 29.5 31.5 16.5 23.5  5.5  0.5]
    20.080727126259017 0.010034910304116709
    ----------
    Reject H0: The distributions do not match (p=0.010035)
"""

from geopandas import read_file
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from numpy import zeros, array, mean, std
from pandas import read_csv, DataFrame, IntervalIndex, cut, value_counts


def create_bins(lower_bound, width, quantity):
    """
    * returns an ascending list of tuples, representing the intervals.
    """
    bins = []
    for low in range(lower_bound, lower_bound + quantity * width + 1, width):
        bins.append((low, low+width))
    return bins


''' EXPECTED VALUES '''

# read in MLL dataset
samples = read_csv("./datasets/distance/distance_distribution_8000.csv")

# report mean and SD
print(f"mean: {samples.dist_to_cl.mean()/1000:.2f}km; SD: {samples.dist_to_cl.std()/1000:.2f}km")

# sort age data into 10 km bins
bin_width = 20000
bins = IntervalIndex.from_tuples(create_bins(0, bin_width, int(max(samples.dist_to_cl) / bin_width)))
distances = value_counts(cut(samples.dist_to_cl, bins), sort=False, ascending=True)

# extract observed age values
ex_total = distances.sum()

# set samples index for use in join later
samples = samples.set_index(samples.id)


''' OBSERVED VALUES '''

# read in MLL dataset
mll_survey = read_file("../distance-analysis/parishes_mll.shp")

# filter for those parishes with MLL sufferers
mll_survey = mll_survey.loc[mll_survey.mll > 0]

# construct list of distances (allowing for multiple per parish)
mll_distances = []
for i, d in mll_survey.iterrows():
    for j in range(int(d.mll)):
        mll_distances.append(d['distance'])
print(f"{len(mll_distances)} MLL sufferers, ({mll_survey.mll.sum()})")
mll_distances = array(mll_distances)

# # report mean and SD
print(f"mean: {mll_distances.mean()/1000:.2f}km; SD: {mll_distances.std()/1000:.2f}km")

# sort age data into 10 year bins
mll_distances_binned = value_counts(cut(mll_distances, bins), sort=False, ascending=True)

# extract observed age values
ob_total = mll_distances_binned.sum()
observed = mll_distances_binned.to_numpy()

# scale expected
expected = array([ int(int(x) / ex_total * ob_total) + 0.5 for x in distances])

# get chi2 and p values
chi2, p = chisquare(observed, f_exp=expected)

# output to console
print("")
print(observed)
print(expected)
print(chi2, p)
print("----------")
if (p < 0.05):
    print(f"Reject H0: The distributions do not match (p={p:.6f})")
else:
    print(f"Cannot Reject H0, difference not significant (p={p:.6f})")
print("")

''' PLOT '''

# init plot
fig, axes = plt.subplots(figsize=(15, 8), nrows=1, ncols=3)
# fig.suptitle('Distribution of Distance to GROW for sample locations', fontsize=16)

# create bin labels
# labels = array([f"{int(x/1000)} - {int((x+10000)/1000)}" for x in range(0, 170000, 10000)])
labels = array([f"{int(x/1000)}" for x in range(0, 170000, bin_width)])

# observed plot
plt.subplot(131)
plt.bar(labels, observed, color="#5bc0de") #width=9, align='edge',
plt.xlabel('Distance (km)')
plt.ylabel('Frequency')
# plt.xlim([0, 90])
plt.ylim([0, 50])
plt.xticks(rotation=90)
plt.title('MLL Distance from GROW')

# expected plot
plt.subplot(132)
plt.bar(labels, expected, color="#f0ad4e") #width=9, align='edge',
plt.xlabel('Distance (km)')
plt.ylabel('Frequency')
# plt.xlim([0, 90])
plt.xticks(rotation=90)
plt.ylim([0, 50])
plt.title('Sample Distance from GROW')

# calculate difference (balance) for third plot
difference = observed - expected

# difference plot
plt.subplot(133)
for x, y in zip(labels, difference):
    if y < 0:
        plt.bar(x, y, color="#d9534f")
    else:
        plt.bar(x, y, color="#0275d8")
plt.xlabel('Distance (km)')
plt.ylabel('Frequency')
# plt.xlim([0, 90])
plt.ylim([-25, 25])
plt.xticks(rotation=90)
plt.axhline(y=0, linewidth=0.5, color='k')
plt.title('Difference')

# output image
plt.savefig('./out/distance_mll_parish.png', dpi=300)
