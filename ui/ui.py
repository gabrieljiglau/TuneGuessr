import pandas as pd
import tkinter as tk
from ttkthemes import ThemedTk

def main_screen():
    # Clear the old screen
    for widget in root.winfo_children():
        widget.destroy()

    # Recreate the main menu
    main_screen_label = tk.Label(root, text="Ecranul principal", font=("Helvetica", 20))
    main_screen_label.pack(pady=20)

    func_1_button = tk.Button(root, text="Funcționalitatea 1", command=func_1_screen, bg=button_color, fg=button_text_color, font=("Helvetica", text_size, "bold"), width=25)
    func_1_button.pack(pady =(45,0), padx=30)

    func_2_button = tk.Button(root, text="Funcționalitatea 2", command=func_2_screen, bg=button_color, fg=button_text_color, font=("Helvetica", text_size, "bold"), width=25)
    func_2_button.pack(pady=(45,0), padx=30)

    func_3_button = tk.Button(root, text="Funcționalitatea 3", command=func_2_screen, bg=button_color, fg=button_text_color, font=("Helvetica", text_size, "bold"), width=25)
    func_3_button.pack(pady=(45,0), padx=30)


def func_1_screen():
    # Clear the old screen
    for widget in root.winfo_children():
        widget.destroy()

    # Load questions
    df = pd.read_csv('questions.csv')
    questions = df['question_name'].tolist()

    answers = []
    current_question = [0]

    def func_1_show_question():
        if current_question[0] < len(questions):
            question_label.config(text=questions[current_question[0]])
            answer_entry.delete(0, tk.END)
            answer_entry.focus_set()
        else:
            # No more questions, call func_1_identify function
            result = func_1_identify(answers)
            func_1_display_result(result)

    def func_1_next_question():
        answer = answer_entry.get()
        if answer.strip() != "":
            answers.append(answer)
            current_question[0] += 1
            func_1_show_question()

    def func_1_display_result(result_text):
        # Clear screen
        for widget in root.winfo_children():
            widget.destroy()

        result_label = tk.Label(root, text="Rezultat: " + result_text, font=("Helvetica", 20), wraplength=700, justify="center")
        result_label.pack(pady=30)

        back_button = tk.Button(root, text="Înapoi la meniul principal", command=main_screen, bg=button_color, fg=button_text_color, font=("Helvetica", text_size, "bold"))
        back_button.pack(pady=20)

    # GUI elements
    question_label = tk.Label(root, text="", font=("Helvetica", 18), wraplength=700, justify="center")
    question_label.pack(pady=30)

    answer_entry = tk.Entry(root, font=("Helvetica", 16), width=50)
    answer_entry.pack(pady=10)

    next_button = tk.Button(root, text="Următoarea întrebare", command=func_1_next_question, bg=button_color, fg=button_text_color, font=("Helvetica", text_size, "bold"))
    next_button.pack(pady=15)

    back_button = tk.Button(root, text="Înapoi", command=main_screen, bg=button_color, fg=button_text_color, font=("Helvetica", text_size, "bold"))
    back_button.pack(pady=10)

    func_1_show_question()

# This is the function you will implement yourself
def func_1_identify(answers):
    # Dummy example
    print(answers)
    return f"Te gandesti la 'Buddy Holly' de Weezer"

def func_2_screen():
    pass

def func_3_screen():
    pass


if __name__ == '__main__':
    root = ThemedTk(theme="clam")
    root.title("Music Recommender")
    root.geometry('800x500')

    bg_color = "#f0f0f0"  # light gray
    button_color = "#4CAF50"  # green
    button_text_color = "white"
    label_color = "#333333"  # gray
    combobox_color = "#ffffff"  # white
    text_size = 16

    root.configure(bg=bg_color)

    main_screen()

    root.mainloop()