"""
* This is Chi Squared Goodness of Fit test - comparing one distribution with another
* https://stats.stackexchange.com/questions/110718/chi-squared-test-with-scipy-whats-the-difference-between-chi2-contingency-and/375063
*
* https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html
*
* Census Data:
* http://catalog.data.ug/dataset/2014-census-data
*
* Result:
    [117  34  15]
    [30 89 48]
    308.97626404494383 8.065972613330855e-68
    ----------
    Reject H0: The distributions do not match (p=0.000000)
"""

from numpy import array
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from pandas import read_csv, DataFrame

''' OBSERVED VALUES '''

# read in MLL dataset and extract education bins
# mll_survey = read_csv("./datasets/limbloss_extract2020apr2.csv")
mll_survey = read_csv("./datasets/edited MLL dataset_22April2020.csv")
# mll_ed = mll_survey.educ.value_counts()

# loop through each row
counts = [0, 0, 0]
for i, x in mll_survey.iterrows():

    # no education / didn't complete primary school
    if (x.educ == 'none') or (x.educ == 'primary' and x.complete == 'no'):
        counts[0] += 1

    # primary education / didn't complete secondary school
    elif (x.educ == 'primary' and x.complete == 'yes') or (x.educ == 'secondary' and x.complete == 'no'):
        counts[1] += 1

    # secondary school or better
    elif (x.educ == 'secondary' and x.complete == 'yes') or (x.educ == 'tertiary'):
        counts[2] += 1

# extract observed education values
# ob_total = mll_ed.sum()
# observed = array([mll_ed.none, mll_ed.primary, mll_ed.secondary + mll_ed.tertiary])
ob_total = sum(counts)
observed = array(counts)
print(ob_total)

''' EXPECTED VALUES '''

# read in census dataset and filter to Acholi Sub -Region
census = read_csv("./datasets/census/education.csv")
acholi_census = census[census['Sub-county'].isin(['Agago Total', 'Amuru Total', 'Arua Total', 'Gulu Total', 'Kitgum Total', 'Lamwo Total', 'Nwoya Total', 'Pader Total'])]

# extract expected education values
ex_none = acholi_census['Never  been to School'].astype(int).sum()
ex_primary = acholi_census.Primary.astype(int).sum()
ex_secondary = acholi_census['Secondary and above'].astype(int).sum()
ex_total = ex_none + ex_primary + ex_secondary

# scale to reflect the sample population
expected = array([
    int(((ex_none / ex_total) * ob_total) + 0.5),
    int(((ex_primary / ex_total) * ob_total) + 0.5),
    int(((ex_secondary / ex_total) * ob_total) + 0.5)
    ])

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
fig, axes = plt.subplots(figsize=(17, 8), nrows=1, ncols=3)
# fig.suptitle('Distribution of Education Level for MLL sufferers', fontsize=16)

# create bin labels
labels = array(['None', 'Primary', 'Secondary+'])

# observed plot
plt.subplot(131)
plt.bar(labels, observed, color="#5bc0de")
plt.xlabel('Education')
plt.ylabel('Frequency')
plt.ylim([0, 120])
plt.title('Observed Values')

# expected plot
plt.subplot(132)
plt.bar(labels, expected, color="#f0ad4e")
plt.xlabel('Education')
plt.ylabel('Frequency')
plt.ylim([0, 120])
plt.title('Expected Values')

# difference plot
plt.subplot(133)

# calculate difference (balance) for third plot
difference = observed - expected

# use masks to flip the colours at y=0
mask1 = difference < 0
mask2 = difference >= 1
plt.bar(labels[mask2], difference[mask2], color="#0275d8")
plt.bar(labels[mask1], difference[mask1], color="#d9534f")
plt.xlabel('Education')
plt.ylabel('Frequency')
plt.ylim([-120, 120])
plt.axhline(y=0, linewidth=0.5, color='k')
plt.title('Difference')

plt.savefig('./out/education.png', dpi=300)
