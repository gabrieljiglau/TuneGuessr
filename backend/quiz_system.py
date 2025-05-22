import pandas as pd
import numpy as np
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import os
import joblib
from dotenv import load_dotenv

load_dotenv()
decision_tree = os.getenv('DECISION_TREE')
dataset = os.getenv('DATASET')
quiz_path = os.getenv('QUIZ')

class MusicQuizSystem:
    def __init__(self, data_path, questions_path, model_path=decision_tree):
        self.data = pd.read_csv(data_path)
        print(f"questions_path = {questions_path}")
        self.questions = pd.read_csv(questions_path)
        self.model = None
        self.model_path = model_path
        self.feature_mapping = self.create_feature_mapping()
        self._prepare_data()

    def create_feature_mapping(self):
        # Mapăm întrebările la atributele relevante
        return {
            0: 'duration_ms',   # durata
            1: 'valence',       # cât de bine te simți
            2: 'instrumentalness', # muzică electronică
            3: 'danceability',  # dansabil
            4: 'energy',        # energie
            5: 'speechiness',   # multe versuri
            6: 'liveness',      # live sau studio
            7: 'loudness',      # zgomot
            8: 'mode',          # ton emoțional (major/minor)
            9: 'speechiness',   # multe cuvinte (din nou speechiness)
            10: 'tempo',        # tempo
        }

    def _prepare_data(self):
        self.data.fillna(0, inplace=True)

        if self.data['mode'].dtype == object:
            le = LabelEncoder()
            self.data['mode'] = le.fit_transform(self.data['mode'])

        features = list(self.feature_mapping.values())
        X = self.data[features]
        y = self.data['name']

        # Verificăm dacă există modelul salvat
        if os.path.exists(self.model_path):
            print(f" Modelul găsit la {self.model_path}, îl încarc...")
            self.model = joblib.load(self.model_path)
        else:
            print(" Modelul NU există, antrenez unul nou...")
            self.model = DecisionTreeClassifier(max_depth=5)
            self.model.fit(X, y)
            joblib.dump(self.model, self.model_path)
            print(f" Modelul a fost antrenat și salvat în {self.model_path}")

    def select_song(self, song_id=None, song_name=None):
        if song_id:
            song = self.data[self.data['id'] == song_id]
        elif song_name:
            song = self.data[self.data['name'] == song_name]
        else:
            song = self.data.sample(1)  # random song
        return song.iloc[0]

    def ask_questions(self, song):
        '''
        Pentru melodia selectată: Iterează prin toate întrebările.Pune întrebarea utilizatorului.Citește răspunsul (input()).Stochează atât răspunsul utilizatorului cât și valoarea corectă.Returnează listele de răspunsuri
        '''
        correct_answers = []
        user_answers = []
        features = list(self.feature_mapping.values())

        print(f"\nAm selectat melodia: {song['name']}")

        for qid, feature in self.feature_mapping.items():
            question = self.questions.loc[self.questions['id'] == qid, 'question_name'].values[0]
            correct_value = song[feature]

            # Pregătim afișarea întrebării
            print(f"\nÎntrebare: {question}")

            user_input = input("Răspunsul tău: ")

            # Salvăm răspunsurile
            user_answers.append(user_input)
            correct_answers.append(correct_value)

        return user_answers, correct_answers

    def evaluate(self, user_answers, correct_answers):
        '''
        Compară fiecare răspuns al utilizatorului cu cel corect
        '''
        score = 0
        total = len(user_answers)
        print("\nRezultate:")

        for idx, (ua, ca) in enumerate(zip(user_answers, correct_answers)):
            try:
                ua_float = float(ua)
                ca_float = float(ca)
                similarity = 1 - abs(ua_float - ca_float) / (abs(ca_float) + 1e-5)
                similarity = max(0, similarity)
            except:
                similarity = 1 if str(ua).lower() == str(ca).lower() else 0

            if similarity > 0.6:
                score += 1
                result = "Corect"
            else:
                result = "Gresit"

            print(f"Întrebarea {idx+1}: {result} (Răspuns corect: {ca})")

        print(f"\nScor final: {score} / {total}")

    def run(self, song_id=None, song_name=None):
        song = self.select_song(song_id, song_name)
        user_answers, correct_answers = self.ask_questions(song)
        self.evaluate(user_answers, correct_answers)


if __name__ == '__main__':

    quiz = MusicQuizSystem(data_path=dataset, questions_path=quiz_path)
    quiz.run()  # fara args alege random sau quiz.run(song_id="0QU5xT6Mik4vpyt1ItsRXK") pentru un anumit ID
