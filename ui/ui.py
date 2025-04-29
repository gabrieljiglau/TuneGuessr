import pandas as pd
import tkinter as tk
from ttkthemes import ThemedTk
from backend.song_identifier import SongProcessor

class MusicRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Recommender")
        self.root.geometry('800x500')
        self.root.configure(bg="#f0f0f0")

        self.button_color = "#4CAF50"
        self.button_text_color = "white"
        self.label_color = "#333333"
        self.text_size = 16

        # Load questions for functionality 1
        self.questions = pd.read_csv('data/questions.csv')
        self.current_question_index = 0
        self.answers = []

        # Start main screen
        self.show_main_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_main_screen(self):
        self.clear_screen()

        main_label = tk.Label(self.root, text="Ecranul principal", font=("Helvetica", 20))
        main_label.pack(pady=20)

        func1_button = tk.Button(self.root, text="Funcționalitatea 1", command=self.show_func1_screen, bg=self.button_color, fg=self.button_text_color, font=("Helvetica", self.text_size, "bold"), width=25)
        func1_button.pack(pady=(45, 0), padx=30)

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

        question_text = self.questions.iloc[self.current_question_index]['question_name']
        question_label = tk.Label(self.root, text=question_text, font=("Helvetica", 16))
        question_label.pack(pady=20)

        self.answer_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.answer_entry.pack(pady=10)

        submit_button = tk.Button(self.root, text="Submit", command=self.save_answer, bg=self.button_color, fg=self.button_text_color, font=("Helvetica", self.text_size, "bold"))
        submit_button.pack(pady=20)

    def save_answer(self):
        answer = self.answer_entry.get()
        self.answers.append(answer)
        self.current_question_index += 1
        self.ask_question()

    def finish_questionnaire(self):
        processor = SongProcessor(self.answers)
        result = processor.predict_song()

        self.clear_screen()
        result_label = tk.Label(self.root, text=f"Melodia identificată:\n{result}", font=("Helvetica", 18))
        result_label.pack(pady=20)

        back_button = tk.Button(self.root, text="Back to Main", command=self.show_main_screen, bg=self.button_color, fg=self.button_text_color, font=("Helvetica", self.text_size, "bold"))
        back_button.pack(pady=20)

if __name__ == '__main__':
    root = ThemedTk(theme="clam")
    app = MusicRecommenderApp(root)
    root.mainloop()