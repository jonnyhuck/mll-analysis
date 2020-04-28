"""
* This is Chi Squared Goodness of Fit test - comparing one distribution with another
* https://stats.stackexchange.com/questions/110718/chi-squared-test-with-scipy-whats-the-difference-between-chi2-contingency-and/375063
*
* https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html
* https://colorswall.com/images/palettes/bootstrap-4-colors-3-colorswall.png
*
* Census Data:
* https://www.ubos.org/explore-statistics/statistical-datasets/6133/
*
* Result:
    [2, 14, 21, 37, 37, 32, 11, 8, 5]
    [54, 43, 29, 18, 11, 7, 3, 2, 1]
    297.9682587898306 1.1144422117951244e-59
    ----------
    Reject H0: The distributions do not match (p=0.000000)
"""
from numpy import zeros, array, mean, std
import matplotlib.pyplot as plt
from scipy.stats import chisquare, shapiro
from pandas import read_csv, DataFrame, IntervalIndex, cut, value_counts


def create_bins(lower_bound, width, quantity):
    """
    * returns an ascending list of tuples, representing the intervals.
    """
    bins = []
    for low in range(lower_bound, lower_bound + quantity * width + 1, width):
        bins.append((low, low+width))
    return bins

''' OBSERVED VALUES '''

# read in MLL dataset
# mll_survey = read_csv("./datasets/limbloss_extract2020apr2.csv")
mll_survey = read_csv("./datasets/edited MLL dataset_22April2020.csv")

# report mean and SD
print(f"observed mean: {mll_survey.age.mean()}; SD: {mll_survey.age.std()}")

# sort age data into 10 year bins
bin_width = 10
bins = IntervalIndex.from_tuples(create_bins(0, bin_width, int(max(mll_survey.age)/bin_width)))
mll_ages = value_counts(cut(mll_survey.age, bins), sort=False, ascending=True)

# extract observed age values
ob_total = mll_ages.sum()
observed = mll_ages.to_numpy()
print(ob_total)

''' EXPECTED VALUES '''

# read in census dataset
census = read_csv("./datasets/census/age.csv")

# extract year of interest, transpose and convert to floats (removing thousand separators)
census2018 = census['2018'].T.iloc[:81].apply(lambda x: int(x.replace(",", "")))

# assign counts to bins
expected = list(zeros(9))
ages = []
for i, x in census2018.iteritems():
    expected[int(i/bin_width)] += x
    # ages += [i for j in range(x)]

# report mean and SD
# print(f"expected mean: {mean(ages)}; SD: {std(ages)}")
# ages = None

# scale to get expected values
ex_total = sum(expected)
expected = array([ int((x / ex_total * ob_total) + 0.5) for x in expected])

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
fig.suptitle('Distribution of Ages for MLL sufferers', fontsize=16)

# create bin labels
labels = array(list(range(0, 90, 10)))

# observed plot
plt.subplot(131)
plt.bar(labels, observed, width=9, align='edge', color="#5bc0de")
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.xlim([0, 90])
plt.ylim([0, 60])
plt.title('Observed Values')

# expected plot
plt.subplot(132)
plt.bar(labels, expected, width=9, align='edge', color="#f0ad4e")
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.xlim([0, 90])
plt.ylim([0, 60])
plt.title('Expected Values')

# calculate difference (balance) for third plot
difference = observed - expected

# difference plot
plt.subplot(133)
mask1 = difference < 0
mask2 = difference >= 1
plt.bar(labels[mask1], difference[mask1], width=9, align='edge', color="#d9534f")
plt.bar(labels[mask2], difference[mask2], width=9, align='edge', color="#0275d8")
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.xlim([0, 90])
plt.ylim([-60, 60])
plt.axhline(y=0, linewidth=0.5, color='k')
plt.title('Difference')

# output image
plt.savefig('./out/age.png')
