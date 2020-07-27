import matplotlib.pyplot as plt
from numpy import array

# init plot
fig, axes = plt.subplots(figsize=(12, 8), nrows=1, ncols=1)

# create bin labels
labels = array(['War', 'Road Traffic\nAccidents', 'Chronic\nDisease', 'Other\nAccident', 'Burns', 'Birth\nDefect', 'Domestic\nViolence', 'Other'])
data = array([48.9, 11.8, 10.5, 8.9, 8.4, 4.6, 3.4, 3.4])

# populate plot
plt.subplot(111)
plt.bar(labels, data, color="#5bc0de")
plt.xlabel('Cause of MLL', fontsize=12)
plt.ylabel('Frequency (%)', fontsize=12)
plt.ylim([0, 50])

# add bar labels
for i, v in enumerate(data):
    plt.text(i, v - 2, str(v) + "%", color='#333333', horizontalalignment='center', fontsize=12)

# output
plt.savefig('./out/causes.png', dpi=300)
