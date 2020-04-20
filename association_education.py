"""
* This is Chi Squared test for Association - looking for a relationship
* between healthcare / access to a prostheric & education / work
*
* https://stats.stackexchange.com/questions/110718/chi-squared-test-with-scipy-whats-the-difference-between-chi2-contingency-and/375063
*
* https://docs.scipy.org/doc/scipy-0.13.0/reference/generated/scipy.stats.chisquare.html
* https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html
* https://machinelearningmastery.com/chi-squared-test-for-machine-learning/
* https://machinelearningmastery.com/critical-values-for-statistical-hypothesis-testing/
"""

from pandas import read_csv, crosstab
from scipy.stats import chi2, chi2_contingency
from matplotlib.pyplot import subplots, setp, savefig

# read in dataset
survey = read_csv("./datasets/limbloss_extract2020apr2.csv")[['educ', 'complete', 'hlthcare', 'contrib', 'rehabacs']]

# drop any na's
survey = survey.dropna()

# process data into clean classes
education = []
healthcare = []
device = []
rehab = []
to_drop = []
for i, x in survey.iterrows():

    # no education / didn't complete primary school
    if (x.educ == 'none') or (x.educ == 'primary' and x.complete == 'no'):
        education.append('none')

    # primary education / didn't complete secondary school
    elif (x.educ == 'primary' and x.complete == 'yes') or (x.educ == 'secondary' and x.complete == 'no'):
        education.append('primary')

    # secondary school or better
    elif (x.educ == 'secondary' and x.complete == 'yes') or (x.educ == 'tertiary'):
        education.append('secondary')

    else:
        to_drop.append(i)

    # healthcare
    if x.hlthcare == 'No':
        healthcare.append(False)
    else:
        healthcare.append(True)

    # device (e.g. prosthetic)
    if x.contrib == 'Never':
        device.append(False)
    else:
        device.append(True)

    # rehabilitation services
    if x.rehabacs == 'Never':
        rehab.append(False)
    else:
        rehab.append(True)

# drop non-contributing rows
survey.drop(to_drop, inplace=True)

# add new classified column
survey['education2'] = education
survey['healthcare2'] = healthcare
survey['device2'] = device
survey['rehab2'] = rehab


''' ASSOCIATION TESTING '''

# extract the columns that we are interested in
# independents = ['hlthcare', 'contrib', 'rehabacs']   # healthcare, assitive device and rehabilitation
independents = ['healthcare2', 'device2', 'rehab2']

# loop through the categorical columns
for independent in independents:

    # make contingency table
    contingency = crosstab(survey.education2, survey[independent])
    print(contingency)

    # chi squared analysis
    # chi2, p, degrees of freedom, expected frequencies
    stat, p, dof, expected = chi2_contingency(contingency)

    # get critical value (0.95 is 0.05 p)
    critical = chi2.ppf(0.95, dof)
    '''
    If stat > critical then we can reject the null, but we don't need to do this as
     we can just use the p value...
    '''

    # print only true relationships
    if p < 0.05:
        print(independent, expected, stat, critical, p, "Dependent (reject H0)")
    else:
        print(independent, expected, stat, critical, p, 'Independent (fail to reject H0)')
    print("")
