import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('guessing_all_wordles.csv')

fig = plt.figure()
sns.histplot(data, y='num_guesses', binwidth=1, binrange=(0.5, 6.5))
plt.title("GUESS DISTRIBUTION")
plt.ylabel("# Guesses")
fig.savefig('guess_distribution.svg')
