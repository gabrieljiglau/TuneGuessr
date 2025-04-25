import os
import pandas as pd


def find_song_titles(songs):
    song = []
    for _, row in songs.iterrows():
        song = (row['name'])
    return song


def load_data(file_path='../data/music_dataset.csv'):

    """
    :param file_path: the path where the csv resides
    :return:  i) return None if the DataFrame doesn't exist or there is a problem parsing the csv
             ii) return -1 if there is a problem when loading the data for training
            iii) if successful, return the input attributes and target_y (the song id)
    """

    df, x_in = None, None
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
        except pd.errors.ParserError as e:
            print(f"Parse error on the following csv, {file_path}: {e}")
    else:
        print("Input file doesn't exist")
        return df

    columns = ['artists', 'name', 'id', 'year', 'release_date']
    x_in  = df.drop(columns=[col for col in columns])
    return x_in, df['id']  # df['id'] = y_target


def split_data(x_in, y_target):

    train_size = int(0.8 * len(x_in))
    x_train, x_eval = x_in[:train_size], x_in[train_size:]
    y_train, y_eval = y_target[:train_size], y_target[train_size:]

    return x_train, y_train, x_eval, y_eval


if __name__ == '__main__':

    x, y = load_data()
    print(y[:20])