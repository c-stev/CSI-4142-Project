from matplotlib import pyplot as plt
import pandas as pd
import staging.stage_country as country
import staging.stage_financial_data as financial
import staging.stage_company as company
import staging.stage_date as date
import staging.stage_fact as fact

df_country = country.get_staged_df()
df_fact = fact.get_staged_df()
df_company = company.get_staged_df()
df_date = date.get_staged_df()
df_financial = financial.get_staged_df()


# Pie chart with count of returns
def pie_chart():
    pos = df_fact.loc[df_fact['returns'] > 0].count()[0]
    neg = df_fact.loc[df_fact['returns'] < 0].count()[0]
    plt.figure()
    labels = ['Positive returns', 'Negative returns']
    colors = ['#00FF00', '#FF0000']
    plt.pie([pos, neg], labels=labels, colors=colors, autopct='%.2f %%')
    plt.title('Summarization of returns')
    plt.savefig('return_count.png')


# Histogram of average yearly volatility
def histogram():
    df = pd.merge(df_financial, df_fact, on='financial_data_id')
    # Adding a year column
    df['year'] = pd.to_datetime(df['date']).dt.year
    # Calculating average volatility
    average_volatility_by_year = df.groupby('year')['volatility'].mean()
    # Creating the histogram
    plt.bar(average_volatility_by_year.index, average_volatility_by_year, color='skyblue')
    plt.title('Average Volatility by Year')
    plt.xlabel('Year')
    plt.ylabel('Average Volatility')
    plt.grid(True)
    plt.savefig('yearly_volatility.png')


# Boxplot of distribution of returns
def box_plot():
    plt.figure()
    red_outlier = dict(markerfacecolor='red', marker='o')
    mean = dict(markerfacecolor='green', marker='D', markeredgecolor='green')
    plt.boxplot(x=df_fact['returns'], flierprops=red_outlier,
                showmeans=True, meanprops=mean, notch=True)
    ax = plt.gca()
    # Set the limits of the y-axis
    ax.set_ylim([-100, 100])
    plt.title('Distribution of return by company')
    plt.ylabel('Values')
    plt.savefig('returns_distribution.png')


# Scatter plot of Volume and Returns
def scatter_plot():
    # Getting the two axis values (and filtering them)
    volume = df_financial['volume'][df_financial['volume'] < 6e9]
    returns = (df_financial['open'] - df_financial['close'])[volume.index]
    # Creating the scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(volume, returns)
    plt.title('Volume vs. Returns')
    plt.xlabel('Volume')
    plt.ylabel('Returns')
    plt.grid(True)
    plt.savefig('volume_vs_returns.png')


pie_chart()
histogram()
box_plot()
scatter_plot()