import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json

# bar chart showing the most popular genres in spain
def spain_favorite_genres():

    movie_data = pd.read_json('../spain_highest_grossing.json').transpose()
    print(movie_data.head())
    # genres column will be a list of dicts {'id': genre_id, 'name': genre_name}

    # create a list of all the genres
    genres = []
    for index, row in movie_data.iterrows():
        try:
            for genre in row['genres']:
                genres.append(genre['name'])
        except:
            pass

    # create a dictionary of the genres and their counts
    genre_counts = {}
    for genre in genres:
        if genre in genre_counts:
            genre_counts[genre] += 1
        else:
            genre_counts[genre] = 1

    # sort the genres by their counts
    genre_counts = {k: v for k, v in sorted(genre_counts.items(), key=lambda item: item[1], reverse=True)}

    # plot the top 10 genres and their counts
    pal = sns.color_palette("crest", len(genre_counts))
    plt.figure(figsize=(12, 8))
    plt.rcParams['figure.facecolor'] = '#f0f6f6'
    sns.set_style("darkgrid", {'axes.facecolor': '#f0f6f6'})
    sns.barplot(x=list(genre_counts.keys())[:10], y=list(genre_counts.values())[:10], palette=pal)

    # remove all the spines
    sns.despine()

    plt.savefig('spain_favorite_genres.png', dpi=600)


# bar chart showing the most popular genres in spain compared to the world
def spain_vs_world_genres():
# read in the data
    spain_data = pd.read_json('../spain_highest_grossing.json').transpose()
    world_data = pd.read_json('../world_highest_grossing.json').transpose()

    # create a list of all the genres for spain
    genres = []
    for index, row in spain_data.iterrows():
        try:
            for genre in row['genres']:
                genres.append(genre['name'])
        except:
            pass

    # do the same for world
    world_genres = []
    for index, row in world_data.iterrows():
        try:
            for genre in row['genres']:
                world_genres.append(genre['name'])
        except:
            pass

    # create a dictionary of the genres and their counts
    genre_counts = {}
    for genre in genres:
        if genre in genre_counts:
            genre_counts[genre] += 1
        else:
            genre_counts[genre] = 1

    # do the same for world
    world_genre_counts = {}
    for genre in world_genres:
        if genre in world_genre_counts:
            world_genre_counts[genre] += 1
        else:
            world_genre_counts[genre] = 1


    genre_counts.pop('Western')

    # sort the spain genres by the greatest difference in counts between spain and world
    genre_counts = {k: v for k, v in sorted(genre_counts.items(), key=lambda item: item[1] - world_genre_counts[item[0]], reverse=True)}
    # sort the world genres to be in the same order as the spain genres
    world_genre_counts = {k: world_genre_counts[k] for k in genre_counts.keys()}


    # keep only the top 10 genres in spain
    genre_counts = {k: v for k, v in genre_counts.items() if k in list(genre_counts.keys())[:10]}
    # keep the same genres in the world data
    world_genre_counts = {k: v for k, v in world_genre_counts.items() if k in list(genre_counts.keys())[:10]}

    # combine the two dictionaries into one dataframe
    # add the spain data with a column that has all values as 'spain'
    counts = pd.DataFrame.from_dict(genre_counts, orient='index', columns=['genres'])
    counts['country'] = 'Spain'
    # concatenate the world data with a column that has all values as 'world'
    world_temp = pd.DataFrame.from_dict(world_genre_counts, orient='index', columns=['genres'])
    world_temp['country'] = 'World'
    counts = pd.concat([counts, world_temp])

    sns.set_theme(style="ticks")
    pal = sns.color_palette("crest", len(genre_counts))
    plt.figure(figsize=(12, 8), facecolor='#f0f6f6')
    plt.rcParams['figure.facecolor'] = '#f0f6f6'
    sns.set_style("darkgrid", {'axes.facecolor': '#f0f6f6'})

    # plot the top 10 genres and their counts against the same genres for the world
    # plot should have two bars for each genre, one for spain and one for the world
    sns.barplot(data=counts, x=counts.index, y='genres', hue='country', palette=pal)
    # remove all the spines
    sns.despine()

    plt.xlabel('Genre')
    plt.ylabel('Relative Popularity')
    plt.title('Spain vs World Favorite Genres')

    plt.savefig('spain_v_world_favorite_genres.png', dpi=600)

if __name__ == '__main__':
    spain_vs_world_genres()