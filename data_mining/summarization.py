import preprocessing
from staging import stage_fact
from matplotlib import pyplot as plt
import numpy as np

df_country, df_company, df_date, df_financial = preprocessing.get_processed_data()
df_fact = stage_fact.get_staged_df()
#scatter plot of volume by year
plt.scatter(df_financial['year'], df_financial['volume'] )
plt.title("Volume by year")
plt.xlabel("year")
plt.ylabel("volume")
plt.show()

#pie chart with count of returns
pos = df_fact.loc[df_fact['returns'] > 0].count()[0]
neg = df_fact.loc[df_fact['returns'] < 0].count()[0]
plt.figure()
labels = ['Positive returns', 'Negative returns']
colors = ['#abcdef', '#aabbcc']
plt.pie([pos, neg], labels = labels, colors=colors, autopct='%.2f %%')
plt.title('Summarization of returns')
plt.show()

#histogram of ranges of volatility
plt.hist(df_fact['volatility'], bins=np.arange(0, 0.21, 0.02), edgecolor='black')
plt.xlabel('Volatility')
plt.ylabel('Frequency')
plt.title('Histogram of Volatility')
plt.show()

#boxplot of distribution of returns
plt.figure()
red_outlier = dict(markerfacecolor='red', marker='o')
mean = dict(markerfacecolor='green', marker='D', markeredgecolor='green')
plt.boxplot(x=df_fact['returns'], flierprops=red_outlier, 
             showmeans=True, meanprops=mean, notch=True);
ax = plt.gca()
# Set the limits of the y-axis
ax.set_ylim([-100, 100])
plt.title('Distribution of return by company')
plt.ylabel('Values')
plt.show()