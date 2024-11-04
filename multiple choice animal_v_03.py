import csv
import tkinter as tk
import tkinter.font as tkfont
import random


class YoungAnimalQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Young Animal Quiz")
        self.root.geometry("450x450")
        self.root.configure(bg="#F0F4C3")

        # Set up the default font for all widgets
        self.default_font = tkfont.nametofont("TkDefaultFont")
        self.default_font.configure(size=12, family="Helvetica")
        self.root.option_add("*Font", ("Helvetica", 12))

        # Initialize game variables
        self.num_rounds = 0
        self.round_count = 0
        self.score = 0
        self.current_question_index = 0

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

            all_young_names = [row[1] for row in animals_young_only]  # List of all possible young animal names

            for row in animals_young_only:
                question = f"What is a baby {row[0]} called?"
                correct_answer = row[1]

                # Select 3 unique incorrect options that do not include the correct answer
                incorrect_options = list(set(all_young_names) - {correct_answer})
                options = [correct_answer] + random.sample(incorrect_options,
                                                           3)  # Add 3 random unique incorrect options
                random.shuffle(options)  # Shuffle to randomize the position of the correct answer

                questions.append(
                    {"question": question, "options": options, "correct_index": options.index(correct_answer)}
                )
        return questions

    def choose_rounds(self):
        self.clear_window()

        main_frame = tk.Frame(self.root, bg="#F0F4C3")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the main frame

        welcome_label = tk.Label(main_frame, text="Welcome to the Young Animal Quiz!", font=("Helvetica", 14, "bold"),
                                 bg="#F0F4C3")
        welcome_label.grid(row=0, column=0, columnspan=2, pady=10)

        explanation_label = tk.Label(main_frame, text=("In this quiz, you'll be asked a series of questions about "
                                                       "what baby animals are called. Try to guess correctly and "
                                                       "see how well you know your young animals!"),
                                     wraplength=300, justify="center", bg="#F0F4C3", font=self.default_font)
        explanation_label.grid(row=1, column=0, columnspan=2, pady=10)

        rounds_label = tk.Label(main_frame, text="How many rounds would you like to play? (1-10)",
                                font=self.default_font, bg="#F0F4C3")
        rounds_label.grid(row=2, column=0, columnspan=2, pady=10)

        self.rounds_entry = tk.Entry(main_frame, font=self.default_font, relief="solid", bd=2, highlightthickness=1,
                                     highlightcolor="#AED581")
        self.rounds_entry.grid(row=3, column=0, columnspan=2, pady=10)

        submit_button = tk.Button(main_frame, text="SUBMIT", command=self.start_game, bg="#AED581",
                                  activebackground="#8BC34A",
                                  font=self.default_font, relief="flat", bd=2, padx=10, pady=5)
        submit_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Place the error label below the submit button but keep it hidden initially
        self.error_label = tk.Label(main_frame, text="", font=self.default_font, fg="red", bg="#F0F4C3")
        self.error_label.grid(row=5, column=0, columnspan=2, pady=10)
        self.error_label.grid_remove()  # Hide it initially

    def start_game(self):
        input_value = self.rounds_entry.get().strip()
        if input_value.isdigit():
            self.num_rounds = int(input_value)
            if 1 <= self.num_rounds <= 10:
                self.round_count = 0
                self.score = 0
                random.shuffle(self.questions)
                self.display_question()
                self.error_label.grid_remove()
            else:
                self.display_error_message("Please enter a number between 1 and 10.")
        else:
            self.display_error_message("Please enter a valid number.")

    def display_error_message(self, message):
        # Configure and display the error message below the submit button
        self.error_label.config(text=message)
        self.error_label.grid()  # Make it visible

    def display_question(self):
        self.clear_window()

        main_frame = tk.Frame(self.root, bg="#F0F4C3")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the main frame

        question_heading = tk.Label(main_frame, text=f"Question {self.round_count + 1} of {self.num_rounds}",
                                    font=("Helvetica", 16, "bold"), bg="#F0F4C3")
        question_heading.grid(row=0, column=0, columnspan=2, pady=10)

        score_label = tk.Label(main_frame, text=f"Score: {self.score}",
                               font=("Helvetica", 14), bg="#F0F4C3")
        score_label.grid(row=1, column=0, columnspan=2, pady=10)

        if self.round_count < self.num_rounds:
            question_data = self.questions[self.current_question_index % len(self.questions)]
            question_label = tk.Label(main_frame, text=question_data["question"], font=self.default_font, bg="#F0F4C3")
            question_label.grid(row=2, column=0, columnspan=2, pady=20)

            option_frame = tk.Frame(main_frame, bg="#F0F4C3")
            option_frame.grid(row=3, column=0, columnspan=2, pady=10)

            for i, option in enumerate(question_data["options"]):
                option_button = tk.Button(option_frame, text=option, command=lambda opt=option: self.check_answer(opt),
                                          font=self.default_font, bg="#FFCC80", activebackground="#FFA726",
                                          relief="flat", bd=2, padx=5, pady=5)
                option_button.grid(row=i // 2, column=i % 2, padx=10, pady=5)

            button_frame = tk.Frame(main_frame, bg="#F0F4C3")
            button_frame.grid(row=4, column=0, columnspan=2, pady=20)

            help_button = tk.Button(button_frame, text="HELP", command=self.display_help, bg="#90CAF9",
                                    font=self.default_font, relief="flat", bd=2, padx=10, pady=5)
            help_button.grid(row=0, column=0, padx=10)

            cancel_button = tk.Button(button_frame, text="CANCEL", command=self.cancel_game, bg="#F48FB1",
                                      font=self.default_font, relief="flat", bd=2, padx=10, pady=5)
            cancel_button.grid(row=0, column=1, padx=10)
        else:
            self.display_final_score()

    # The rest of your class methods remain the same

    def check_answer(self, selected_option):
        selected_index = self.questions[self.current_question_index % len(self.questions)]["options"].index(
            selected_option)
        correct_index = self.questions[self.current_question_index % len(self.questions)]["correct_index"]

        # Update the score if the answer is correct
        if selected_index == correct_index:
            self.score += 1

        # Clear the window to display feedback
        self.clear_window()

        feedback_color = "#cde777" if selected_index == correct_index else "#E76C6C"
        feedback_frame = tk.Frame(self.root, bg=feedback_color)
        feedback_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the feedback frame

        feedback = "Correct!" if selected_index == correct_index else f"Incorrect. The correct answer is {self.questions[self.current_question_index % len(self.questions)]['options'][correct_index]}."
        feedback_label = tk.Label(feedback_frame, text=feedback, font=self.default_font, bg=feedback_color)
        feedback_label.grid(row=0, column=0, columnspan=2, pady=(5, 10))

        next_round_button = tk.Button(feedback_frame, text="Next Round", command=self.display_question,
                                      font=self.default_font, bg="#C2C2C2", activebackground="#8BC34A",
                                      relief="flat", bd=2, padx=10, pady=5)
        next_round_button.grid(row=1, column=0, columnspan=2, pady=(5, 10))

        # Move to the next question and update the round count
        self.current_question_index += 1
        self.round_count += 1

    def cancel_game(self):
        self.clear_window()
        self.choose_rounds()

    def clear_window(self):
        for widget in self.root.winfo_children():
            if widget != self.error_label:
                widget.destroy()

    def display_help(self):
        self.clear_window()
        main_frame = tk.Frame(self.root, bg="#DAE8FC")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        help_text = "This is a quiz about young animals. Select your answer from the options."
        help_label = tk.Label(main_frame, text=help_text, wraplength=300, justify="center", bg="#DAE8FC",
                              font=self.default_font)
        help_label.grid(row=0, column=0, padx=10, pady=20)
        dismiss_button = tk.Button(main_frame, text="Dismiss", command=self.dismiss_help, bg="#AED581",
                                   activebackground="#8BC34A", font=self.default_font, relief="flat", bd=2, padx=10,
                                   pady=5)
        dismiss_button.grid(row=1, column=0, pady=20)

    def dismiss_help(self):
        self.clear_window()
        self.display_question()

    def display_final_score(self):
        self.clear_window()
        main_frame = tk.Frame(self.root, bg="#F0F4C3")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        final_score_label = tk.Label(main_frame,
                                     text=f"End of {self.num_rounds} rounds. Your final score is {self.score}",
                                     font=self.default_font, bg="#F0F4C3")
        final_score_label.grid(row=0, column=0, columnspan=2, pady=20)
        play_again_button = tk.Button(main_frame, text="Play Again", command=self.play_again, font=self.default_font,
                                      bg="#AED581", activebackground="#8BC34A", relief="flat", bd=2, padx=10, pady=5)
        play_again_button.grid(row=1, column=0, columnspan=2, pady=20)

    def play_again(self):
        self.clear_window()
        self.choose_rounds()


if __name__ == "__main__":
    root = tk.Tk()
    app = YoungAnimalQuiz(root)
    root.mainloop()
