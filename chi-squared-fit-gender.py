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
    [111, 56]
    [81, 86]
    21.57622739018088 3.400405696486798e-06
    ----------
    Reject H0: The distributions do not match (p=0.000003)
"""

from numpy import array
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from pandas import read_csv, DataFrame

''' OBSERVED VALUES '''

# read in MLL dataset and extract gender bins
# mll_survey = read_csv("./datasets/limbloss_extract2020apr2.csv")
mll_survey = read_csv("./datasets/edited MLL dataset_22April2020.csv")
mll_gender = mll_survey.gender.value_counts()
# print(mll_gender)
# print(mll_survey.tribe.value_counts())


# extract observed gender values
ob_total  = mll_gender.male + mll_gender.female
observed = array([mll_gender.male, mll_gender.female])
print(ob_total)

''' EXPECTED VALUES '''

# read in census dataset and filter to Acholi Sub -Region
census = read_csv("./datasets/census/gender.csv")
acholi_census = census[census['Sub-county'].isin(['Agago Total', 'Amuru Total', 'Arua Total', 'Gulu Total', 'Kitgum Total', 'Lamwo Total', 'Nwoya Total', 'Pader Total'])]

# extract expected gender values
ex_males = acholi_census.Male.astype(int).sum()
ex_females = acholi_census.Female.astype(int).sum()
ex_total = ex_males + ex_females

# scale to reflect the sample population
expected = array([int(((ex_males / ex_total) * ob_total) + 0.5),
    int(((ex_females / ex_total) * ob_total) + 0.5)])

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
# fig.suptitle('Distribution of Genders for MLL sufferers', fontsize=16)

# create bin labels
labels = array(['Male', 'Female'])

# observed plot
plt.subplot(131)
plt.bar(labels, observed, color="#5bc0de")
plt.xlabel('Gender')
plt.ylabel('Frequency')
plt.ylim([0, 120])
plt.title('Observed Values')

# expected plot
plt.subplot(132)
plt.bar(labels, expected, color="#f0ad4e")
plt.xlabel('Gender')
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
plt.xlabel('Gender')
plt.ylabel('Frequency')
plt.ylim([-60, 60])
plt.axhline(y=0, linewidth=0.5, color='k')
plt.title('Difference')

plt.savefig('./out/gender.png', dpi=300, bbox_inches='tight')
