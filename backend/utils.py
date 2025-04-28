import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings('ignore')


def find_song_titles(songs):
    song = []
    for _, row in songs.iterrows():
        song = (row['name'])
    return song


def transform_input(df, input_list):

    new_list = []
    for song_identifier in input_list:
        if not df[df['id'] == song_identifier].empty:
            song_name = df[df['id'] == song_identifier].iloc[0]['name']
            new_list.append(song_name)
        else:
            new_list.append(song_identifier)

    return new_list


def find_clusters(df, df_features, input_songs, k_means, scaler):

    """
    :param df: the dataframe that holds the data
    :param df_features: the dataframe that contains only the attributes that will be used during clusterization
    :param input_songs: the songs selected by the user
    :param k_means: the already trained clusterization algorithm
    :param scaler: scale the features to have mean = 0 and std = 1
    :return: the clusters for each song
    """

    songs = []
    for song_name in input_songs:
        match = df[df['name'] == song_name]
        if not match.empty:
            songs.append(match.iloc[0])
        else:
            print(f"Warning: song '{song_name}' not found in dataset!")

    if not songs:
        raise ValueError("No valid input songs found in dataset.")

    song_features = np.vstack([song[df_features.columns].values for song in songs])
    features_df = pd.DataFrame(song_features, columns=df_features.columns)
    target_features = scaler.transform(features_df)
    target_clusters = k_means.predict(target_features)

    return target_clusters

def compute_distance(scaler, row, features, target_features):
    row_features = scaler.transform([row[features].values])
    return np.linalg.norm(row_features - target_features)


def find_closest_song(df, target_cluster, input_song, features, target_features, scaler, num_songs):

    same_cluster = df[(df['cluster'] == target_cluster) & (df['name'] != input_song['name'])]

    if same_cluster.empty:
        return f"No similar songs for {input_song}"

    same_cluster = same_cluster.copy()
    same_cluster['distance'] = same_cluster.apply(
        lambda row: compute_distance(scaler, row, features, target_features),
        axis=1
    )

    closest_songs = same_cluster.sort_values('distance').iloc[0:num_songs]
    for _, song in closest_songs.iterrows():
        print(f"closest_songs: {song['name']} by {song['artists']}")

    return closest_songs
