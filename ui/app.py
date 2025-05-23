import pandas as pd
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk
from youtubesearchpython import VideosSearch
import webbrowser
import sys
import os
from PIL import Image, ImageTk
from dotenv import load_dotenv
from backend.song_identifier import SongProcessor
from backend.song_recommender import Recommender
from backend.quiz_system import MusicQuizSystem

load_dotenv()
questions_path = os.getenv('QUESTIONS')
answers_path = os.getenv('ANSWERS')
dataset_path = os.getenv('DATASET')
quiz_path = os.getenv('QUIZ')
akinator_path = os.getenv('AKINATOR')


class MusicRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Recommender")
        self.root.geometry('800x600')
        self.root.configure(bg="#f0f0f0")

        self.button_color = "#4CAF50"
        self.button_text_color = "white"
        self.label_color = "#333333"
        self.text_size = 16

        # Load questions for functionality 1
        self.questions = pd.read_csv(questions_path)
        self.answer_variants = pd.read_csv(answers_path)
        self.current_question_index = 0
        self.answers = []

        # Load quiz system for functionality 2
        self.quiz_system = MusicQuizSystem(
        data_path=dataset_path,
        questions_path=quiz_path
        )
        self.quiz_song = None
        self.quiz_correct_answers = []
        self.quiz_user_answers = []
        self.quiz_current_index = 0

        # Start main screen
        self.show_main_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_screen(self):
        self.clear_screen()

        try:  # make akinator a background picture
            if akinator_path and os.path.exists(akinator_path):
                self.bg_image = Image.open(akinator_path)
                self.bg_image = self.bg_image.resize((800, 600))
                self.bg_photo = ImageTk.PhotoImage(self.bg_image)

                bg_label = tk.Label(self.root, image=self.bg_photo)
                bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                bg_label.lower()
            else:
                print(f"Image not found at: {akinator_path}")
                # Fallback to colored background
                self.root.configure(bg="#f0f0f0")
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.root.configure(bg="#f0f0f0")

        main_label = tk.Label(self.root, text="TuneGuessr", font=("Helvetica", 20))
        main_label.pack(pady=(60,0))

        func1_button = tk.Button(self.root, text="TuneGuessr Ghiceste Melodia", command=self.show_func1_screen, bg=self.button_color, fg=self.button_text_color, font=("Helvetica", self.text_size, "bold"), width=25)
        func1_button.pack(pady=(50, 0), padx=30)

        func2_button = tk.Button(
        self.root, text="Tu ghicești Melodia",
        command=self.start_quiz,
        bg=self.button_color, fg=self.button_text_color,
        font=("Helvetica", self.text_size, "bold"), width=25
        )   
        func2_button.pack(pady=(40,0))


        func3_button = tk.Button(
            self.root, text="TuneGuessr Recomanda Melodii", command=self.show_func3_screen,
            bg=self.button_color, fg=self.button_text_color,
            font=("Helvetica", self.text_size, "bold"), width=25
        )
        func3_button.pack(pady=(40,0))

    def show_func1_screen(self):
        self.clear_screen()
        self.answers = []
        self.current_question_index = 0
        self.ask_question()

    def ask_question(self):
        self.clear_screen()
        if self.current_question_index >= len(self.questions):
            self.finish_questionnaire()
            return

        question_id = self.current_question_index + 1  # assuming question IDs start from 1
        question_text = self.questions.iloc[self.current_question_index]['question_name']

        question_label = tk.Label(self.root, text=question_text, font=("Helvetica", 16))
        question_label.pack(pady=20)

        # Get the answer variant for this question
        row = self.answer_variants[self.answer_variants['id'] == question_id]
        if not row.empty:
            answers = row.iloc[0]['answers']
            if answers.strip() == "int":
                # Create entry box for integer input
                self.answer_entry = tk.Entry(self.root, font=("Helvetica", 14))
                self.answer_entry.pack(pady=10)
                self.answer_entry.focus_set()

                submit_button = tk.Button(self.root, text="Trimite", command=self.save_answer_from_entry,
                                          bg=self.button_color, fg=self.button_text_color,
                                          font=("Helvetica", self.text_size, "bold"))
                submit_button.pack(pady=20)
            else:
                # Create buttons for each option
                options = [opt.strip() for opt in answers.split(',')]
                for opt in options:
                    btn = tk.Button(self.root, text=opt,
                                    command=lambda o=opt: self.save_answer_from_button(o),
                                    bg=self.button_color, fg=self.button_text_color,
                                    font=("Helvetica", self.text_size))
                    btn.pack(pady=5)
        else:
            # Fallback: simple entry if something went wrong
            self.answer_entry = tk.Entry(self.root, font=("Helvetica", 14))
            self.answer_entry.pack(pady=10)

            submit_button = tk.Button(self.root, text="Trimite", command=self.save_answer_from_entry,
                                      bg=self.button_color, fg=self.button_text_color,
                                      font=("Helvetica", self.text_size, "bold"))
            submit_button.pack(pady=20)

    def save_answer(self, answer):
        self.answers.append(answer)
        self.current_question_index += 1
        self.ask_question()

    def save_answer_from_entry(self):
        answer = self.answer_entry.get()
        self.answers.append(answer)
        self.current_question_index += 1
        self.ask_question()

    def save_answer_from_button(self, answer):
        self.answers.append(answer)
        self.current_question_index += 1
        self.ask_question()

    def finish_questionnaire(self):
        processor = SongProcessor(self.answers)
        result = processor.predict_song()

        self.clear_screen()
        result_label = tk.Label(self.root, text=f"Melodia identificată:\n{result}", font=("Helvetica", 18))
        result_label.pack(pady=20)

        videos_search = VideosSearch(result, limit=1)
        video_result = videos_search.result()['result'][0]
        video_url = video_result['link']

        play_button = tk.Button(self.root, text="Ascultă pe YouTube", command=lambda: webbrowser.open(video_url),
                                bg=self.button_color, fg=self.button_text_color,
                                font=("Helvetica", self.text_size, "bold"))
        play_button.pack(pady=10)

        back_button = tk.Button(self.root, text="Înapoi la ecranul principal", command=self.show_main_screen, bg=self.button_color, fg=self.button_text_color, font=("Helvetica", self.text_size, "bold"))
        back_button.pack(pady=20)

    def show_func3_screen(self):
        self.clear_screen()
        label = tk.Label(self.root, text="Introdu titluri de melodii sau ID (separate de return):", font=("Helvetica", 16))
        label.pack(pady=20)


        self.songs_text = tk.Text(self.root, font=("Helvetica", 14), width=60, height=10)
        self.songs_text.pack(pady=10)
        self.songs_text.focus_set()

        submit_button = tk.Button(self.root, text="Găsește melodii similare", command=self.find_similar_songs_func3,
                                  bg=self.button_color, fg=self.button_text_color,
                                  font=("Helvetica", self.text_size, "bold"))
        submit_button.pack(pady=20)

        back_button = tk.Button(self.root, text="Înapoi la ecranul principal", command=self.show_main_screen,
                                bg=self.button_color, fg=self.button_text_color,
                                font=("Helvetica", self.text_size, "bold"))
        back_button.pack(pady=10)

    def find_similar_songs_func3(self):
        song_input = self.songs_text.get("1.0", tk.END)
        song_list = [s.strip() for s in song_input.split('\n') if s.strip()]

        recommender = Recommender(song_list)
        closest_songs = recommender.find_similar_songs(2)

        self.clear_screen()

        if closest_songs == -1:
            error_label = tk.Label(self.root, text="Melodii invalide, reîncearcă.", font=("Helvetica", 16),
                                   fg="red")
            error_label.pack(pady=20)
        else:
            result_label = tk.Label(self.root, text="Melodii recomandate:", font=("Helvetica", 18))
            result_label.pack(pady=20)

            for group in closest_songs:
                label = tk.Label(self.root, text=" ", font=("Helvetica", 14))
                label.pack(pady=2)
                for index, row in group.iterrows():
                    song_name = row['name']
                    artist = row['artists']
                    label = tk.Label(self.root, text=f"{song_name} de {artist}", font=("Helvetica", 14))
                    label.pack(pady=2)

        back_button = tk.Button(self.root, text="Înapoi la ecranul principal", command=self.show_main_screen,
                                bg=self.button_color, fg=self.button_text_color,
                                font=("Helvetica", self.text_size, "bold"))
        back_button.pack(pady=20)

    #functionalitatea 2 (Tu Ghicești Melodia)
    def show_quiz_question(self):
        self.clear_screen()
        if self.quiz_current_index >= len(self.quiz_system.feature_mapping):
            self.finish_quiz()
            return

        qid = self.quiz_current_index
        feature = self.quiz_system.feature_mapping[qid]
        question = self.quiz_system.questions.loc[self.quiz_system.questions['id'] == qid, 'question_name'].values[0]
        correct_value = self.quiz_song[feature]

        self.quiz_correct_answers.append(correct_value)

        label = tk.Label(self.root, text=question, font=("Helvetica", 16))
        label.pack(pady=20)
#custom intervals
        if "duration" in feature.lower():
            slider_from = 5
            slider_to = 5500
            resolution = 1
        elif "decibel" in feature.lower() or "db" in feature.lower() or feature.lower() == "loudness":
            slider_from = -60
            slider_to = 4
            resolution = 1
        elif "tempo" in feature.lower():
            slider_from = 0
            slider_to = 250
            resolution = 1
        else:
            slider_from = 0.0
            slider_to = 1.0
            resolution = 0.01

        self.quiz_answer_slider = tk.Scale(
            self.root, from_=slider_from, to=slider_to, resolution=resolution,
            orient=tk.HORIZONTAL, length=400, font=("Helvetica", 12), showvalue=True
        )

        #  pozitia default a slideurilui la mijloc
        self.quiz_answer_slider.set((slider_from + slider_to) / 2)
        self.quiz_answer_slider.pack(pady=10)

        submit_button = tk.Button(self.root, text="Trimite", command=self.save_quiz_answer,
                                bg=self.button_color, fg=self.button_text_color,
                                font=("Helvetica", self.text_size, "bold"))
        submit_button.pack(pady=20)



    def submit_quiz_answer_event(self, event):
        self.save_quiz_answer()

    def save_quiz_answer(self):
        answer = self.quiz_answer_slider.get()
        self.quiz_user_answers.append(answer)
        self.quiz_current_index += 1
        self.show_quiz_question()

    def finish_quiz(self):
        self.clear_screen()
        score = 0
        total = len(self.quiz_user_answers)

        result_label = tk.Label(self.root, text=f"Melodia era:\n{self.quiz_song['name']}", font=("Helvetica", 18))
        result_label.pack(pady=20)

        for idx, (ua, ca) in enumerate(zip(self.quiz_user_answers, self.quiz_correct_answers)):
            try:
                ua_float = float(ua)
                ca_float = float(ca)
                similarity = 1 - abs(ua_float - ca_float) / (abs(ca_float) + 1e-5)
                similarity = max(0, similarity)
            except:
                similarity = 1 if str(ua).lower() == str(ca).lower() else 0

            if similarity > 0.8:
                score += 1
                status = "✔ Corect"
            else:
                status = f"✘ Greșit (corect: {ca})"

            feedback = tk.Label(self.root, text=f"Întrebarea {idx+1}: {status}", font=("Helvetica", 14))
            feedback.pack()

        score_label = tk.Label(self.root, text=f"\nScor final: {score} / {total}", font=("Helvetica", 16, "bold"))
        score_label.pack(pady=20)

        back_button = tk.Button(self.root, text="Înapoi la ecranul principal", command=self.show_main_screen,
                                bg=self.button_color, fg=self.button_text_color,
                                font=("Helvetica", self.text_size, "bold"))
        back_button.pack(pady=20)

    def start_quiz(self):
        self.clear_screen()
        self.quiz_song = self.quiz_system.select_song()
        self.quiz_correct_answers = []
        self.quiz_user_answers = []
        self.quiz_current_index = 0

        song_title = self.quiz_song['name']
        label = tk.Label(self.root, text=f"Melodia selectată este:\n{song_title}", font=("Helvetica", 18))
        label.pack(pady=20)

        # YouTube search and button
        videos_search = VideosSearch(song_title, limit=1)
        video_result = videos_search.result()['result'][0]
        video_url = video_result['link']

        play_button = tk.Button(self.root, text="Ascultă pe YouTube", command=lambda: webbrowser.open(video_url),
                                bg=self.button_color, fg=self.button_text_color,
                                font=("Helvetica", self.text_size, "bold"))
        play_button.pack(pady=10)

        # Start quiz button
        start_button = tk.Button(self.root, text="Începe chestionar", command=self.show_quiz_question,
                                 bg=self.button_color, fg=self.button_text_color,
                                 font=("Helvetica", self.text_size, "bold"))
        start_button.pack(pady=20)


if __name__ == '__main__':
    root = ThemedTk(theme="clam")
    app = MusicRecommenderApp(root)
    root.mainloop()