


import seaborn as sns
import matplotlib.pyplot as plt



def plot_variable_pairs(df):

    '''Plot pairwise relationships with regression lines for each pair of variables in the dataframe'''

    sns.set(style="ticks")
    sns.pairplot(df, kind="reg", height=3)
    plt.show()


def plot_categorical_and_continuous(df, x, y):
    '''takes in a df and provides visualizations''' 
    # Boxplot
    sns.boxplot(x=x, y=y, data=df)
    plt.title('Boxplot')
    plt.show()

    # Stripplot
    sns.stripplot(x=x, y=y, data=df)
    plt.title('Stripplot')
    plt.show()

    # Barplot
    sns.barplot(x=x, y=y, data=df)
    plt.title('Barplot')
    plt.show()
    