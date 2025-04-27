import pandas as pd
from typing import List
from utils import find_song_titles


class SongProcessor:

   def __init__(self, answers: List, input_csv='../data/music_dataset.csv'):
      self.data_frame = pd.read_csv(input_csv)
      self.answers = answers

   def predict_song(self):

      """
      filter the songs step-by-step as answers from the user are processed
      :return: the most similar song based on (some) answers
      """

      song = None
      interrupted_search = False
      has_errors = False

      df = self.data_frame
      previous_df = df.copy()

      for index, answer in enumerate(self.answers):

         previous_df = df.copy()

         if index == 0:
            if isinstance(answer, (int, float)):
               df = df[df['duration_ms'] <= answer]
            else:
               has_errors = True

         elif index == 1:
            answer = answer.lower()
            if answer == 'deprimat':
               df = df[df['valence'] < 0.3]
            elif answer == 'melancolic':
               df = df[(df['valence'] >= 0.3) & (df['valence'] < 0.6)]
            elif answer == 'bucuros':
               df = df[df['valence'] >= 0.6]

         elif index == 2:
            answer = answer.lower()
            if answer == 'da, foarte multe':
               df = df[df['acousticness'] < 0.3]
            elif answer == 'are suficiente':
               df = df[(df['acousticness'] >= 0.3) & (df['acousticness'] < 0.6)]
            elif answer == 'nu prea':
               df = df[df['acousticness'] >= 0.6]

         elif index == 3:
            answer = answer.lower()
            if answer == 'nu prea':
               df = df[df['danceability'] < 0.4]
            elif answer == 'poti sa incerci':
               df = df[(df['danceability'] >= 0.4) & (df['danceability'] < 0.7)]
            elif answer == 'rupi podeaua':
               df = df[df['danceability'] >= 0.7]

         elif index == 4:
            answer = answer.lower()
            if answer == 'este mai inceata':
               df = df[df['energy'] < 0.3]
            elif answer == 'are suficienta energie':
               df = df[(df['energy'] >= 0.3) & (df['energy'] < 0.6)]
            elif answer == 'iti da aaaripi':
               df = df[df['energy'] >= 0.6]

         elif index == 5:
            answer = answer.lower()
            if answer == 'da, foarte multe':
               df = df[df['instrumentalness'] < 0.3]
            elif answer == 'are suficiente':
               df = df[(df['instrumentalness'] >= 0.3) & (df['instrumentalness'] < 0.7)]
            elif answer == 'este aproape numai instrument':
               df = df[df['instrumentalness'] >= 0.7]

         elif index == 6:
            answer = answer.lower()
            if answer == '100% inregistrata':
               df = df[df['liveness'] < 0.3]
            elif answer == 'inregistrata, dar are si ceva audienta':
               df = df[(df['liveness'] >= 0.3) & (df['liveness'] < 0.7)]
            elif answer == 'clar demonstratie live':
               df = df[df['liveness'] >= 0.7]

         elif index == 7:
            answer = answer.lower()
            if answer == 'clar nezgomotoasa':
               df = df[(df['loudness'] > -60) & (df['loudness'] <= -30)]
            elif answer == 'nu prea zgomotoasa':
               df = df[(df['loudness'] > -30) & (df['loudness'] < -5)]
            elif answer == 'foarte zgomotoasa':
               df = df[df['loudness'] >= -5]

         elif index == 8:
            if answer == 'trist':
               df = df[df['mode'] == 0]
            elif answer == 'fericit':
               df = df[df['mode'] == 1]

         elif index == 9:
            answer = answer.lower()
            if answer == 'nu prea':
               df = df[df['speechiness'] <= 0.3]
            elif answer == 'are suficiente cuvinte':
               df = df[(df['speechiness'] > 0.3) & (df['speechiness'] < 0.7)]
            elif answer == 'are foarte multe':
               df = df[df['speechiness'] >= 0.7]

         elif index == 10:
            answer = answer.lower()
            if answer == 'incet':
               df = df[(df['tempo'] >= 40) & (df['tempo'] <= 80)]
            elif answer == 'intre incet si rapid':
               df = df[(df['tempo'] > 80) & (df['tempo'] < 120)]
            elif answer == 'foarte rapid':
               df = df[df['tempo'] >= 120]

         if df.empty:
            print(f"No results after question {index}")
            song = previous_df.sample(min(1, len(previous_df)))
            interrupted_search = True
            break

      if interrupted_search:
         return find_song_titles(song)

      if has_errors:
         return "Câteva informații au fost greșit introduse !"

      return find_song_titles(df.sample(min(1, len(df))))


if __name__ == '__main__':

   answers_list = [80, 'deprimat', 'are suficiente', 'poti sa incerci', 'iti da aaaripi', 'da, foarte multe',
                   '100% inregistrata', 'foarte zgomotoasa', 0, 'are suficiente cuvinte', 'foarte rapid']
   processor = SongProcessor(answers_list)
   print(processor.predict_song())
