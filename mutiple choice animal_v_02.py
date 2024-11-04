import csv
import tkinter as tk
import tkinter.font as tkfont
import random


class YoungAnimalQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Young Animal Quiz")
        self.root.geometry("450x450")  # Set the window size to 450x450
        self.root.configure(bg="#F0F4C3")  

        # Set up the default font for all widgets
        self.default_font = tkfont.nametofont("TkDefaultFont")
        self.default_font.configure(size=12, family="Helvetica")
        self.root.option_add("*Font", ("Helvetica", 12))

        # Initialize game variables
        self.num_rounds = 0  # Total number of rounds to play
        self.round_count = 0  # Counter for the current round
        self.score = 0  # Player's score
        self.current_question_index = 0  # Index of the current question

        # Load quiz questions from the CSV file
        self.questions = self.load_questions_from_csv('animals_young_only.csv')

        # Initialize the error label for displaying input errors
        self.error_label = tk.Label(self.root, text="", font=self.default_font, fg="red", bg="#F0F4C3")

        # Start the quiz by asking the user how many rounds they'd like to play
        self.choose_rounds()

    def load_questions_from_csv(self, csv_file):
        questions = []
        with open(csv_file, 'r') as file:
            animals_young_only = list(csv.reader(file, delimiter=","))
            animals_young_only.pop(0)  # Remove header row

            all_young_names = [row[1] for row in animals_young_only]

            for row in animals_young_only:
                question = f"What is a baby {row[0]} called?"
                correct_answer = row[1]

                # Select random incorrect options and ensure no duplicates
                incorrect_options = random.sample([name for name in all_young_names if name != correct_answer], 3)
                options = [correct_answer] + incorrect_options
                random.shuffle(options)

                # Ensure the correct answer is included and the options are unique
                questions.append(
                    {"question": question, "options": options, "correct_index": options.index(correct_answer)})
        return questions

    def choose_rounds(self):
        self.clear_window()

        main_frame = tk.Frame(self.root, bg="#F0F4C3")
        main_frame.pack(pady=20)

        welcome_label = tk.Label(main_frame, text="Welcome to the Young Animal Quiz!", font=("Helvetica", 14, "bold"),
                                 bg="#F0F4C3")
        welcome_label.pack(pady=10)

        explanation_label = tk.Label(main_frame, text=("In this quiz, you'll be asked a series of questions about "
                                                       "what baby animals are called. Try to guess correctly and "
                                                       "see how well you know your young animals!"),
                                     wraplength=350, justify="center", bg="#F0F4C3", font=self.default_font)
        explanation_label.pack(pady=10)

        rounds_label = tk.Label(main_frame, text="How many rounds would you like to play? (1-10)",
                                font=self.default_font, bg="#F0F4C3")
        rounds_label.pack(pady=10)

        self.rounds_entry = tk.Entry(main_frame, font=self.default_font, relief="solid", bd=2, highlightthickness=1,
                                     highlightcolor="#AED581")
        self.rounds_entry.pack(pady=10)

        self.rounds_entry.bind("<Return>", lambda event: self.start_game())

        submit_button = tk.Button(main_frame, text="SUBMIT", command=self.start_game, bg="#AED581",
                                  activebackground="#8BC34A",
                                  font=self.default_font, relief="flat", bd=2, padx=10, pady=5)
        submit_button.pack(pady=20)

        self.error_label.pack(pady=10)
        self.error_label.pack_forget()

    def start_game(self):
        input_value = self.rounds_entry.get().strip()

        if input_value.isdigit():
            self.num_rounds = int(input_value)
            if 1 <= self.num_rounds <= 10:
                self.round_count = 0
                self.score = 0
                random.shuffle(self.questions)
                self.display_question()
                self.error_label.pack_forget()
            else:
                self.display_error_message("Please enter a number between 1 and 10.")
        else:
            self.display_error_message("Please enter a valid number.")

    def display_error_message(self, message):
        self.error_label.config(text=message)
        self.error_label.pack()

    def display_question(self):
        self.clear_window()

        # Add question heading
        question_heading = tk.Label(self.root, text=f"Question {self.round_count + 1} of {self.num_rounds}",
                                    font=("Helvetica", 16, "bold"), bg="#F0F4C3")
        question_heading.pack(pady=10)

        # Add score label
        score_label = tk.Label(self.root, text=f"Score: {self.score}",
                               font=("Helvetica", 14), bg="#F0F4C3")
        score_label.pack(pady=10)

        if self.round_count < self.num_rounds:
            question_data = self.questions[self.current_question_index % len(self.questions)]
            question_label = tk.Label(self.root, text=question_data["question"], font=self.default_font, bg="#F0F4C3")
            question_label.pack(pady=20)

            shuffled_options = list(question_data["options"])
            random.shuffle(shuffled_options)

            option_frame = tk.Frame(self.root, bg="#F0F4C3")
            option_frame.pack(pady=10)

            for option in shuffled_options:
                option_button = tk.Button(option_frame, text=option, command=lambda opt=option: self.check_answer(opt),
                                          font=self.default_font, bg="#FFCC80", activebackground="#FFA726",
                                          relief="flat", bd=2, padx=5, pady=5)
                option_button.pack(side=tk.LEFT, padx=10)

            button_frame = tk.Frame(self.root, bg="#F0F4C3")
            button_frame.pack(pady=20)

            help_button = tk.Button(button_frame, text="HELP", command=self.display_help, bg="#90CAF9",
                                    font=self.default_font, relief="flat", bd=2, padx=10, pady=5)
            help_button.pack(side=tk.LEFT, padx=10)

            cancel_button = tk.Button(button_frame, text="CANCEL", command=self.cancel_game, bg="#F48FB1",
                                      font=self.default_font, relief="flat", bd=2, padx=10, pady=5)
            cancel_button.pack(side=tk.LEFT, padx=10)

        else:
            self.display_final_score()

    def check_answer(self, selected_option):
        selected_index = self.questions[self.current_question_index % len(self.questions)]["options"].index(
            selected_option)
        correct_index = self.questions[self.current_question_index % len(self.questions)]["correct_index"]

        feedback_frame = tk.Frame(self.root)
        feedback_frame.pack(fill="both", expand=True)

        if selected_index == correct_index:
            self.score += 1
            feedback_frame.configure(bg="#cde777")  # Set feedback frame background to green for correct answer
            feedback = "Correct!"
        else:
            feedback_frame.configure(bg="#E76C6C")  # Set feedback frame background to red for incorrect answer
            correct_answer = self.questions[self.current_question_index % len(self.questions)]["options"][correct_index]
            feedback = f"Incorrect. The correct answer is {correct_answer}."

        self.current_question_index += 1
        self.round_count += 1

        feedback_label = tk.Label(feedback_frame, text=feedback, font=self.default_font, bg=feedback_frame["bg"])        
        feedback_label.pack(pady=20)

        next_round_button = tk.Button(feedback_frame, text="Next Round", command=self.display_question,
                                      font=self.default_font, bg="#C2C2C2", activebackground="#8BC34A",
                                      relief="flat", bd=2, padx=10, pady=5)
        next_round_button.pack(pady=20)

        if self.round_count >= self.num_rounds:
            self.display_final_score()

    def cancel_game(self):
        self.clear_window()
        self.choose_rounds()

    def clear_window(self):
        for widget in self.root.winfo_children():
            if widget != self.error_label:
                widget.destroy()

    def display_help(self):
        self.clear_window()

        self.root.configure(bg="#DAE8FC")

        help_text = ("This is a quiz about young animals. You will be asked a series of questions "
                     "about what baby animals are called. Select your answer from the options and you "
                     "will proceed to the next question. You got this!")
        help_label = tk.Label(self.root, text=help_text, wraplength=300, justify="center", bg="#DAE8FC",
                              font=self.default_font)
        help_label.pack(pady=20)

        dismiss_button = tk.Button(self.root, text="Dismiss", command=self.dismiss_help, bg="#AED581",
                                   activebackground="#8BC34A",
                                   font=self.default_font, relief="flat", bd=2, padx=10, pady=5)
        dismiss_button.pack(pady=20)

    def dismiss_help(self):
        self.clear_window()
        self.root.configure(bg="#F0F4C3")
        self.display_question()

    def display_final_score(self):
        self.clear_window()
        final_score_label = tk.Label(self.root,
                                     text=f"End of {self.num_rounds} rounds. Your final score is {self.score}",
                                     font=self.default_font, bg="#F0F4C3")
        final_score_label.pack(pady=20)

        play_again_button = tk.Button(self.root, text="Play Again", command=self.play_again, font=self.default_font,
                                      bg="#AED581", activebackground="#8BC34A", relief="flat", bd=2, padx=10, pady=5)
        play_again_button.pack(pady=20)

    def play_again(self):
        self.clear_window()
        self.choose_rounds()


if __name__ == "__main__":
    root = tk.Tk()
    app = YoungAnimalQuiz(root)
    root.mainloop()
