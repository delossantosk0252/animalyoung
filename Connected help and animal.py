import tkinter as tk
import tkinter.font as tkfont
import random


class YoungAnimalQuiz:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Young Animal Quiz")

        # Define a larger font size
        self.default_font = tkfont.nametofont("TkDefaultFont")
        self.default_font.configure(size=14, family="Lucida Console")

        self.num_rounds = 0
        self.round_count = 0
        self.score = 0
        self.current_question_index = 0

        # Questions data (unchanged)
        self.questions = [
            # Your questions data here
        ]

        self.choose_rounds()

    def choose_rounds(self):
        rounds_frame = tk.Frame(self.root)
        rounds_frame.pack()

        rounds_label = tk.Label(rounds_frame, text="How many rounds would you like to play? (1-10)",
                                font=self.default_font)
        rounds_label.grid(row=0, column=0)

        self.rounds_entry = tk.Entry(rounds_frame, font=self.default_font)
        self.rounds_entry.grid(row=1, column=0)

        submit_button = tk.Button(rounds_frame, text="Submit", command=self.start_game, bg="#FFF2CC",
                                  font=self.default_font)
        submit_button.grid(row=2, column=0, pady=10)

    def start_game(self):
        input_value = self.rounds_entry.get().strip()

        if input_value.isdigit():
            self.num_rounds = int(input_value)
            if 1 <= self.num_rounds <= 10:
                self.round_count = 0
                self.score = 0
                random.shuffle(self.questions)  # Shuffle questions for random order
                self.display_question()
            else:
                self.display_error_message("Please enter a number between 1 and 10.")
        else:
            self.display_error_message("Please enter a valid number.")

    def display_error_message(self, message):
        error_label = tk.Label(self.root, text=message, font=self.default_font)
        error_label.pack(pady=10)

    def display_question(self):
        self.clear_window()

        if self.round_count < self.num_rounds:
            question_data = self.questions[self.current_question_index % len(self.questions)]
            question_label = tk.Label(self.root, text=question_data["question"], font=self.default_font)
            question_label.pack(pady=10)

            # Shuffle options
            shuffled_options = list(question_data["options"])
            random.shuffle(shuffled_options)

            option_frame = tk.Frame(self.root)
            option_frame.pack(pady=10)

            for option in shuffled_options:
                option_button = tk.Button(option_frame, text=option, command=lambda opt=option: self.check_answer(opt),
                                          font=self.default_font)
                option_button.pack(side=tk.LEFT, padx=10)

            button_frame = tk.Frame(self.root)
            button_frame.pack(pady=20)

            help_button = tk.Button(button_frame, text="Help", command=self.display_help, bg="#CCE5FF",
                                    font=self.default_font)
            help_button.pack(side=tk.LEFT, padx=10)

            cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel_game, bg="#E1D5E7",
                                      font=self.default_font)
            cancel_button.pack(side=tk.LEFT, padx=10)

        else:
            self.display_final_score()

    def check_answer(self, selected_option):
        selected_index = self.questions[self.current_question_index % len(self.questions)]["options"].index(
            selected_option)
        correct_index = self.questions[self.current_question_index % len(self.questions)]["correct_index"]

        if selected_index == correct_index:
            self.score += 1

        self.current_question_index += 1
        self.round_count += 1

        self.clear_window()

        if self.round_count < self.num_rounds:
            correct_answer = self.questions[(self.current_question_index - 1) % len(self.questions)]["options"][
                correct_index]
            feedback = f"{'Correct!' if selected_index == correct_index else f'Incorrect. The correct answer is {correct_answer}.'}"
            feedback_label = tk.Label(self.root, text=feedback, font=self.default_font)
            feedback_label.pack()

            next_round_button = tk.Button(self.root, text="Next Round", command=self.display_question,
                                          font=self.default_font)
            next_round_button.pack(pady=10)
        else:
            self.display_final_score()

    def cancel_game(self):
        self.clear_window()
        self.choose_rounds()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def display_help(self):
        self.clear_window()
        help_text = "This is a quiz about young animals. You will be asked a series of questions about what baby " \
                    "animals are called. Select your answer from the options and you will proceed to the next " \
                    "question. Good luck!"
        help_label = tk.Label(self.root, text=help_text, wraplength=400, justify="center", bg="#DAE8FC",
                              font=self.default_font)
        help_label.pack(pady=20)

        dismiss_button = tk.Button(self.root, text="Dismiss", command=self.display_question, bg="#E1D5E7",
                                   font=self.default_font)
        dismiss_button.pack(pady=10)

    def display_final_score(self):
        self.clear_window()
        final_score_label = tk.Label(self.root,
                                     text=f"End of {self.num_rounds} rounds. Your final score is {self.score}",
                                     font=self.default_font)
        final_score_label.pack(pady=20)

        play_again_button = tk.Button(self.root, text="Play Again", command=self.play_again, font=self.default_font)
        play_again_button.pack(pady=10)

    def play_again(self):
        self.clear_window()
        self.choose_rounds()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = YoungAnimalQuiz()
    game.run()
