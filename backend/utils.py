import numpy as np


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
    for i in range(len(input_songs)):
        songs.append(df[df['name'] == input_songs[i]].iloc[0])

    target_features = scaler.transform([song[df_features.columns].values for song in songs])
    target_clusters = k_means.predict(target_features)

    return target_clusters


def compute_distance(scaler, row, features, target_features):
    row_features = scaler.transform([row[features].values])
    return np.linalg.norm(row_features - target_features)


def find_closest_song(df, target_cluster, input_song, features, target_features, scaler, num_songs):

    same_cluster = df[(df['cluster'] == target_cluster) & (df['name'] != input_song['name'])]

    if same_cluster.empty:
        return f"No similar songs for {input_song}"

    same_cluster['distance'] = same_cluster[features].apply(
        lambda row: compute_distance(scaler, row, features, target_features),
        axis=1
    )

    closest_songs = same_cluster.sort_values('distance').iloc[0:num_songs]
    for song in closest_songs:
        print(f"closest_songs: {song['name']}")

    return closest_songs


def find_song_titles(songs):
    song = []
    for _, row in songs.iterrows():
        song = (row['name'])
    return song


if __name__ == '__main__':
    pass