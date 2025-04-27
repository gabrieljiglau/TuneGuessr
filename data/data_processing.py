import pandas as pd


def change_time_metric(ms_duration: float):
    return ms_duration / 1000


def drop_repeated_instances(df):
    repeated_instances = df[df.duplicated()]
    print(f"repeated_instances: \n{repeated_instances}")

    df = df.drop_duplicates()
    df.to_csv('music_dataset.csv')
    print("Duplicates dropped successfully")

    return df


def transform_duration(df):
    """
    :return: the duration in seconds, instead of milliseconds
    """

    df['duration_ms'] = df['duration_ms'].apply(change_time_metric)
    df.to_csv('music_dataset.csv')
    print("Duration modified successfully")

    return df


if __name__ == '__main__':

    data = pd.read_csv('music_dataset.csv')
    # drop_repeated_instances(data)  ## the dataset doesn't have repeated instances
    transform_duration(data)
