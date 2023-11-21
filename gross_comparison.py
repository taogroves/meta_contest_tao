import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# this function compares the top grossing movies in spain and the world,
# and finds the movies that were the most successful in spain compared to the world as a whole
# in other words, the movies that spain liked the most compared to the rest of the world
def gross_comparison():
    # read in the data
    spain = pd.read_csv('top_grossing_movies_spain_2023.csv')
    world = pd.read_csv('top_grossing_movies_world_2023.csv')

    # rename "Release Group" in the world data and "Release" in the spain data to "Title"
    world.rename(columns={'Release Group': 'Title'}, inplace=True)
    spain.rename(columns={'Release': 'Title'}, inplace=True)

    # rename "Gross" in each data set to "Gross_x" and "Gross_y" respectively
    world.rename(columns={'Worldwide': 'Gross_y'}, inplace=True)
    spain.rename(columns={'Gross': 'Gross_x'}, inplace=True)

    # merge the data
    merged = pd.merge(spain, world, on='Title', how='inner')

    # reform the gross columns to be numeric
    merged['Gross_x'] = merged['Gross_x'].str.replace('$', '').str.replace(',', '').astype(int)
    merged['Gross_y'] = merged['Gross_y'].str.replace('$', '').str.replace(',', '').astype(int)

    # calculate the ratio of the gross in spain to the gross in the world
    merged['Ratio'] = merged['Gross_x'] / merged['Gross_y']

    # sort the data by the ratio
    merged.sort_values(by='Ratio', inplace=True, ascending=False)

    # print the top 10 movies
    print(merged.head(10))

    # plot the top 10 movies
    #plt.figure(figsize=(12, 6))
    #sns.barplot(x='Ratio', y='Title', data=merged.head(10), palette='Blues_d')
    #plt.title('Top 10 Movies in Spain Compared to the World')
    #plt.xlabel('Ratio of Gross in Spain to Gross in the World')
    #plt.ylabel('Movie Title')
    #plt.tight_layout()
    #plt.show()

    # save a new csv file with all movies, their gross in spain and the world, and the ratio
    # rename Gross_x to Gross_Spain and Gross_y to Gross_World
    merged.rename(columns={'Gross_x': 'Gross_Spain', 'Gross_y': 'Gross_World'}, inplace=True)
    # remove the columns [Genre, Budget, Running Time, Estimated, Theaters]
    merged.drop(columns=['Genre', 'Budget', 'Running Time', 'Estimated', 'Theaters'], inplace=True)

    # move the 'Rank_y' column (currently 7th) to the beginning of the data set
    world_rank = merged.pop('Rank_y')
    merged.insert(0, 'Rank_World', world_rank)

    # rename 'Rank_x' to 'Rank_Spain'
    merged.rename(columns={'Rank_x': 'Rank_Spain'}, inplace=True)

    merged.to_csv('top_grossing_movies_spain_world_2023.csv', index=False)

# This method finds the movies present in both the spain and world data sets
# and creates a new data set with only those movies
def find_common_movies():
    # read in the data
    spain = pd.read_csv('top_grossing_movies_spain_2023.csv')
    world = pd.read_csv('top_grossing_movies_world_2023.csv')

    # rename "Release Group" in the world data and "Release" in the spain data to "Title"
    world.rename(columns={'Release Group': 'Title'}, inplace=True)
    spain.rename(columns={'Release': 'Title'}, inplace=True)


    # merge the data
    merged = pd.merge(spain, world, on='Title', how='inner')

    # save the data
    merged.to_csv('same_movies.csv', index=False)

# plot the 10 movies with a rank in spain least similar to their rank in the world
def plot_least_similar():
    # read in the data
    merged = pd.read_csv('top_grossing_movies_spain_world_2023.csv')

    # calculate the difference between the ranks in spain and the world
    merged['Rank_Difference'] = merged['Rank_World'] - merged['Rank_Spain']

    # sort the data by the rank difference
    merged.sort_values(by='Rank_Difference', inplace=True, ascending=False)

    # set the color palette to "ticks"
    sns.color_palette("crest", as_cmap=True)

    # set the background color to $f0f6f6
    sns.set_style("darkgrid", {'axes.facecolor': '#f0f6f6'})

    # change the figure background color to $f0f6f6
    plt.rcParams['figure.facecolor'] = '#f0f6f6'

    # plot the top 10 movies
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Rank_Difference', y='Title', data=merged.head(10), palette='crest')
    plt.title('Top 10 Movies in Spain Least Similar to the World')
    plt.xlabel('Rank Difference')
    plt.ylabel('Movie Title')
    plt.tight_layout()

    plt.show()


if __name__ == '__main__':
    plot_least_similar()