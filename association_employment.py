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
survey = read_csv("./datasets/limbloss_extract2020apr2.csv")

# process education and employment
employment = []
to_drop = []
for i, x in survey.iterrows():

    # peasent
    if x.occup == 'Peasant farmer' or x.othaocup == 'FARMER':
        education.append('peasent')

    # unskilled
    elif x.occup == 'others' and x.othaocup in ['FETCHES WATER FOR PEOPLE', 'MOTOR CAR CONDUCTOR']:
        education.append('unskilled labour')

    # trader
    elif x.occup == 'others' and x.othaocup in ['SMALL  BUSINESS', 'BUSINESS IN THE MARKET', 'SMALL SCALE BUSINESS', 'MY OWN BUSINESS', 'BUSINESS WOMAN', 'BUSINESS']:
        education.append('trader')

    # skilled
    elif x.occup in ['cobbler/shoe repairer', 'radio repairer'] or (x.occup == 'others' and x.othaocup in ['COBLER', 'TAILOR', 'CARPENTER', 'REPAIRE BICYCLE', 'MAKING BASKET', 'MECHANIC', 'BUILDER', 'SOLDIER']):
        education.append('skilled labour')

    # professional
    elif x.occup == 'teacher' or (x.occup == 'others' and x.othaocup in ['DISEASE COUNCILLOR', 'POLITICIAN']):
        education.append('professional')

    # nothing
    elif x.occup == 'others' and x.othaocup in ['NONE', 'NOTHING', 'HE IS NOT DOING ANYTHING', "HE IS DISABLE CAN'T DO ANYTHIN", 'NOT WORKING', "SHE DIDN'T ATTAIN ANY EDUCATIO", 'DISABILITY', 'LOW LEVEL OF EDUCATION', 'I DONT HAVE BOTH LEGS', 'NO SKILLS', 'HE IS  TOO WEAK TO WORK', 'NO JOB', 'LACK OF SUPPOR', 'NOT DOING ANYTHING', 'NOT FORMALLY EDUCATED', 'SPORTS']:
        education.append('none')

    else:
        to_drop.append(i)

# drop non-contributing rows
survey.drop(to_drop, inplace=True)

print(len(survey.index), len(employment))
exit()

# add new classified column
survey['employment2'] = employment


''' ASSOCIATION TESTING '''

# extract the columns that we are interested in
independents = ['hlthcare', 'contrib', 'rehabacs']   # healthcare, assitive device and rehabilitation

# loop through the categorical columns
for independent in independents:

    # make contingency table
    contingency = crosstab(survey[independent], survey.employment2)

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
        print(column , stat, critical, p, "**")
    else:
        print(column , stat, critical, p)
