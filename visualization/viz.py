import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

netflix_data = pd.read_csv('../netflix_titles.csv')

# create numeric 'year_added' column
netflix_data['date_added'] = pd.to_datetime(netflix_data['date_added'])
netflix_data['year_added'] = netflix_data['date_added'].dt.year
def hexbin():
    global netflix_data
    # convert date_added to days since 1/1/2000
    netflix_data['date_added'] = pd.to_datetime(netflix_data['date_added'])
    netflix_data['date_added'] = (netflix_data['date_added'] - pd.to_datetime('2000-01-01')).dt.days

    # only consider elements with duration in minutes
    netflix_data = netflix_data[netflix_data['duration'].str.contains('min') == True]
    netflix_data['duration'] = netflix_data['duration'].str.replace(' min', '').astype(int)

    # crop the data to only include movies with a duration less than 200 minutes and added since 2013
    netflix_data = netflix_data[netflix_data['duration'] < 200]
    netflix_data = netflix_data[netflix_data['date_added'] > 5000]


    # Plotting the joint hexbin plot with marginal distributions
    sns.set_theme(style="ticks")
    # set the background color to $f0f6f6
    #sns.set_style("darkgrid", {'axes.facecolor': '#f0f6f6'})

    # change the figure background color to $f0f6f6
    plt.rcParams['figure.facecolor'] = '#f0f6f6'

    # remove all the spines
    sns.despine()

    plt.figure(figsize=(10, 10))
    sns.jointplot(x="date_added", y="duration", data=netflix_data, kind="hex", color="#4CB391")

    x_ticks = []
    x_tick_labels = []
    for i in range(5000, 8000, 365):
        x_ticks.append(i)
        x_tick_labels.append(str(i//365 + 2000))

    # remap the x axis to be in terms of years
    plt.xticks(x_ticks, x_tick_labels)
    plt.xlabel('Year Added')
    plt.ylabel("Duration (minutes)")


    # write the plot to a file
    plt.savefig('netflix_hexbin.png', dpi=600)



def movie_rating_stack():
    rating_counts = netflix_data.groupby(['year_added', 'rating']).size().unstack(fill_value=0)

    # only consider ratings G, PG, PG-13, R, NC-17
    rating_counts = rating_counts[reversed(['G', 'PG', 'PG-13', 'R', 'NC-17'])]

    # color space matches seaborn "crest" palette

    # Calculate the total counts of movies added at each time point
    total_counts = rating_counts.sum(axis=1)

    # Calculate the ratio of each rating relative to the total counts at each time point
    rating_ratios = rating_counts.div(total_counts, axis=0)

    # Plotting the ratios of ratings over time as a stackplot with viridis color palette
    plt.figure(figsize=(12, 8), facecolor='#f0f6f6')
    # change the figure background color to $f0f6f6
    plt.rcParams['figure.facecolor'] = '#f0f6f6'
    sns.set_style("darkgrid", {'axes.facecolor': '#f0f6f6'})

    # remove all the spines
    sns.despine()
    col = sns.color_palette("Paired", len(rating_ratios.columns))
    plt.stackplot(rating_ratios.index, rating_ratios.T, labels=rating_ratios.columns, colors=col)
    plt.xlabel('Year Added')
    plt.ylabel('Rating Prevalence')
    plt.title('Netflix Movie Rating Prevalence Over Time')
    # add a legend with labels reversed to match the stackplot
    plt.legend(title='Rating', loc='upper left', reverse=True)


    plt.savefig('movie_rating_stackplot.png', dpi=600)

def tv_rating_stack():
    rating_counts = netflix_data.groupby(['year_added', 'rating']).size().unstack(fill_value=0)

    # only consider ratings TV-MA, TV-14, TV-PG, TV-G, TV-Y, TV-Y7, TV-Y7-FV
    rating_counts = rating_counts[['TV-MA', 'TV-14', 'TV-PG', 'TV-G', 'TV-Y', 'TV-Y7', 'TV-Y7-FV']]

    # only show ratings that have been added since 2012
    rating_counts = rating_counts[rating_counts.index > 2012]

    # Calculate the total counts of movies added at each time point
    total_counts = rating_counts.sum(axis=1)

    # Calculate the ratio of each rating relative to the total counts at each time point
    rating_ratios = rating_counts.div(total_counts, axis=0)

    # Plotting the ratios of ratings over time as a stackplot with viridis color palette
    plt.figure(figsize=(12, 8),facecolor='#f0f6f6')
    # change the figure background color to $f0f6f6
    plt.rcParams['figure.facecolor'] = '#f0f6f6'
    sns.set_style("darkgrid", {'axes.facecolor': '#f0f6f6'})

    # remove all the spines
    sns.despine()
    col = sns.color_palette("Paired", len(rating_ratios.columns))
    plt.stackplot(rating_ratios.index, rating_ratios.T, labels=rating_ratios.columns, colors=col)
    plt.xlabel('Year Added')
    plt.ylabel('Rating Prevalence')
    plt.title('Netflix TV Rating Prevalence Over Time')
    plt.legend(title='Rating', loc='upper left', reverse=True)
    #plt.show()


    plt.savefig('tv_rating_stackplot.png', dpi=600)

if __name__ == '__main__':
    movie_rating_stack()