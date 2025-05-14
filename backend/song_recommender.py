import os
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from .utils import *


class Recommender:

    def __init__(self, input_songs, data='../data/music_dataset.csv'):

        self.input_songs = input_songs
        self.df = pd.read_csv(data)
        self.df_features = self.df.drop(columns=['Unnamed: 0.1', 'Unnamed: 0' ,'id', 'name',
                                                 'artists', 'release_date', 'year'])
        self.scaler_path = '../models/scaler.pkl'
        self.k_means_path = '../models/k_means.pkl'

    def validate_input(self, input_list):

        """
        :return: whether all the song titles / ids exist
        """

        for value in input_list:
            if not value in self.df['name'].values and not value in self.df['id'].values:
                return False

        return True

    def find_similar_songs(self, num_songs=6, model_name='../data/k_means_clusters.csv'):

        """
        applies KMeans with k = 5 clusters, corresponding to 'Pop', 'EDM', 'Jazz', 'Rap' and 'Rock';
        :param: num_songs: the number of closest songs we consider when looking for similarities
        :return: the most similar songs AS A DATAFRAME !! to the given input list in case of success,
                -1 if the song is alone in a cluster
        """

        if not self.validate_input(self.input_songs):
            return -1

        input_list = transform_input(self.df, self.input_songs)

        scaler = StandardScaler()

        if not os.path.exists(model_name):

            scaled = scaler.fit_transform(self.df_features)
            k_means = KMeans(n_clusters=5, random_state=13)
            cluster_labels = k_means.fit_predict(scaled)

            k_means_df = self.df.copy()
            k_means_df['cluster'] = cluster_labels
            k_means_df.to_csv(model_name, index=False)

            joblib.dump(scaler, self.scaler_path)
            joblib.dump(k_means, self.k_means_path)
        else:
            scaler = joblib.load(self.scaler_path)
            k_means = joblib.load(self.k_means_path)
            k_means_df = pd.read_csv(model_name)

        features = self.df_features.columns

        clusters = find_clusters(self.df, self.df_features, input_list, k_means, scaler)
        closest_songs = []
        for song, cluster in zip(input_list, clusters):
            song_row = self.df[self.df['name'] == song].iloc[0]
            song_features = song_row[self.df_features.columns].values.reshape(1, -1)
            target_features = scaler.transform(song_features)
            closest_songs.append(find_closest_song(k_means_df, cluster, song_row, features,
                                                   target_features, scaler, num_songs))

        return closest_songs


    def find_similarities_and_differences(self, closest_songs):

        """
        :param closest_songs: the closest songs identified after clustering, using Euclidean distance as the metric
        :return: the similar and different attributes as a list of lists,

        for example:
                [ [ [] ], [ [] ] ], the outer list contains m inner lists, where m - is the given number of input songs
                ,and then the inner list has n small lists, where n - is the number of close songs passed as an argument
                to the Recommender class

        actual example of differences, when there 2 songs passed, with num_songs set to 2:
        differences = [[['valence', 'key'], ['valence', 'energy', 'instrumentalness', 'key', 'popularity']],
                        [['energy', 'instrumentalness', 'mode'], ['instrumentalness', 'popularity']]]

        """

        attributes = self.df_features.columns
        similarities = []
        differences = []

        # eliminating the attributes that weren't used during clustering
        cleaned_songs = []
        for neighbour_song in closest_songs:
            cleaned_songs.append(eliminate_attributes(neighbour_song, attributes))
        closest_songs = cleaned_songs

        for song in self.input_songs:
            row_song = self.df[self.df['name'] == song]  # without iloc, it returns a dataframe
            row_song = eliminate_attributes(row_song, attributes)

            similarity = []
            difference = []
            for inner_list in closest_songs:
                per_song_similarity = []
                per_song_difference = []
                for col in attributes:
                    value1 = inner_list[col].iloc[0]
                    value2 = row_song[col].iloc[0]

                    abs_diff = abs(value1 - value2)

                    if value2 != 0:
                        percentage = abs_diff / value2
                    else:
                        percentage = 0.3  # dummy value so it doesn't get appended to similarities, nor differences

                    if percentage < 0.3:
                        per_song_similarity.append(col)

                    if percentage > 0.7:
                        per_song_difference.append(col)

                similarity.append(per_song_similarity)
                difference.append(per_song_difference)

            similarities.append(similarity)
            differences.append(difference)

        print(f"similarities = {similarities}")
        print(f"differences = {differences}")
        return similarities, differences



if __name__ =='__main__':

    songs = ['Morceaux de fantaisie, Op. 3: No. 2, Prélude in C-Sharp Minor. Lento', 'Danny Boy']  # Danny Boy
    recommender = Recommender(songs)

    found_songs = recommender.find_similar_songs(2)
    print(f"closest_songs = {found_songs}") # a dataframe
    recommender.find_similarities_and_differences(found_songs)
