import os
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from utils import find_clusters, find_closest_song

class Recommender:

    def __init__(self, data='../data/music_dataset.csv'):
        self.df = pd.read_csv(data)

    def validate_input(self, input_list):

        """
        :return: whether all the song titles / ids exist
        """

        for value in input_list:
            if not value in self.df['name'].values and not value in self.df['id'].values:
                return False

        return True

    def find_similar_songs(self, input_list, num_songs, model_name='k_means_clusters.csv'):

        """
        apply KMeans with k = 5 clusters, corresponding to 'Pop', 'EDM', 'Jazz', 'Rap' and 'Rock';
        :param: num_songs: the number of closest songs we consider when looking for similarities
        :return: the most similar songs to the given input list, using the Euclidean distance
        """

        if not self.validate_input(input_list):
            return "Some songs/ids don't exist"

        scaler_path = 'scaler.pkl'
        k_means_path = 'k_means.pkl'

        scaler = StandardScaler()
        df_features = self.df.drop(columns=['id', 'name', 'artists', 'release_date'])
        if not os.path.exists(model_name):
            k_means_df = self.df
            scaled = scaler.fit_transform(df_features)

            k_means = KMeans(n_clusters=5, random_state=13)
            cluster_labels = k_means.fit_predict(scaled)

            k_means_df = self.df.copy()
            k_means_df['cluster'] = cluster_labels
            k_means_df.to_csv(model_name, index=False)

            joblib.dump(scaler, scaler_path)
            joblib.dump(k_means, k_means_path)
        else:
            scaler = joblib.load(scaler_path)
            k_means = joblib.load(k_means_path)
            k_means_df = pd.read_csv(model_name)

        features = df_features.columns

        clusters = find_clusters(self.df, df_features, input_list, k_means, scaler)
        closest_songs = []
        for song, cluster in zip(input_list, clusters):
            song_row = self.df[self.df['name'] == song].iloc[0]
            song_features = song_row[df_features.columns].values.reshape(1, -1)
            target_features = scaler.transform(song_features)
            closest_songs.append(find_closest_song(k_means_df, clusters, song_row, features,
                                                   target_features, scaler, num_songs))

        return closest_songs


    def find_similarities_and_differences(self, songs):

        # găsești o metrică de a calcula cele mai apropiate si departate 3 atribute
        # dintre melodiile recomandate si cele date ca 'input'
        pass



if __name__ =='__main__':

    recommender = Recommender()
    # print(recommender.validate_input())
    recommender.find_similar_songs(['Danny Boy'], 3)
