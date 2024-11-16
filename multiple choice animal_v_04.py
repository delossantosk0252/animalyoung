import csv
import tkinter as tk
import tkinter.font as tkfont
import random


class QuizData:
    """Handles loading and storing quiz questions from a CSV file."""

    def __init__(self, csv_file):
        """
        Initializes the QuizData object and attempts to load questions
        from the specified CSV file.
        """
        try:
            # Load questions from the CSV file
            self.questions = self.load_questions_from_csv(csv_file)
        except FileNotFoundError:
            # Handle missing file error
            print(f"Error: '{csv_file}' file not found. Please ensure the file is in the correct directory.")
            self.questions = []
        except csv.Error:
            # Handle invalid CSV format error
            print("Error: Could not read the CSV file. Please check its format.")
            self.questions = []

    def load_questions_from_csv(self, csv_file):
        """
        Reads the CSV file and creates quiz questions.
        Each question includes the correct answer and three random incorrect options.
        """
        questions = []
        with open(csv_file, 'r') as file:
            # Read the CSV content into a list
            animals_young_only = list(csv.reader(file, delimiter=","))
            animals_young_only.pop(0)  # Remove header row

            # Gather all possible answers for incorrect options
            all_young_names = [row[1] for row in animals_young_only]

            for row in animals_young_only:
                # Create a question and shuffle the answer options
                question = f"What is a baby {row[0]} called?"
                correct_answer = row[1]
                incorrect_options = list(set(all_young_names) - {correct_answer})
                options = [correct_answer] + random.sample(incorrect_options, 3)
                random.shuffle(options)
                questions.append({
                    "question": question,
                    "options": options,
                    "correct_index": options.index(correct_answer)
                })
        return questions


class Menu:
    """Manages the initial menu for choosing the number of quiz rounds."""

    def __init__(self, root, start_game_callback):
        """
        Initializes the Menu class.
        :param root: The main tkinter root window.
        :param start_game_callback: Callback function to start the quiz game.
        """
        self.root = root
        self.start_game_callback = start_game_callback
        self.setup_menu()

    def setup_menu(self):
        """Sets up the menu interface for choosing the number of rounds."""
        main_frame = tk.Frame(self.root, bg="#F0F4C3")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Display welcome text and instructions
        tk.Label(main_frame, text="Welcome to the Young Animal Quiz!",
                 font=("Helvetica", 14, "bold"), bg="#F0F4C3").grid(row=0, column=0, columnspan=2, pady=10, padx=20)
        tk.Label(main_frame, text="How many rounds would you like to play? (1-10)",
                 bg="#F0F4C3").grid(row=1, column=0, columnspan=2, pady=10, padx=20)

        # Entry box for the number of rounds
        self.rounds_entry = tk.Entry(main_frame)
        self.rounds_entry.grid(row=2, column=0, columnspan=2, pady=10, padx=20)

        # Error label for displaying invalid input messages
        self.error_label = tk.Label(main_frame, text="", fg="red", bg="#F0F4C3", font=("Helvetica", 10))
        self.error_label.grid(row=3, column=0, columnspan=2, pady=(5, 10))

        # Submit button
        tk.Button(main_frame, text="SUBMIT", command=self.submit_rounds, bg="#AED581").grid(row=4, column=0,
                                                                                            columnspan=2, pady=10,
                                                                                            padx=20)

    def submit_rounds(self):
        """Validates the user's input and starts the game if valid."""
        try:
            rounds = int(self.rounds_entry.get())
            if 1 <= rounds <= 10:
                # Clear any existing error message
                self.error_label.config(text="")
                # Start the game with the specified number of rounds
                self.start_game_callback(rounds)
            else:
                # Show an error if the number is out of bounds
                self.error_label.config(text="Please enter a number between 1 and 10.")
        except ValueError:
            # Show an error if the input is not a number
            self.error_label.config(text="Please enter a valid number.")


class Play:
    """Controls the main gameplay, displaying questions and options."""

    def __init__(self, root, quiz_data, rounds, show_menu_callback, display_help_callback, show_final_score_callback):
        """
        Initializes the Play class.
        :param root: The main tkinter root window.
        :param quiz_data: The QuizData object containing quiz questions.
        :param rounds: Total number of rounds to play.
        :param show_menu_callback: Callback to return to the menu.
        :param display_help_callback: Callback to display help information.
        :param show_final_score_callback: Callback to display the final score.
        """
        self.root = root
        self.quiz_data = quiz_data
        self.num_rounds = rounds
        self.round_count = 0
        self.score = 0
        self.current_question_index = 0
        self.show_menu_callback = show_menu_callback
        self.display_help_callback = display_help_callback
        self.show_final_score_callback = show_final_score_callback

        # Shuffle the questions at the start of each game
        random.shuffle(self.quiz_data.questions)

        self.display_question()

    def display_question(self):
        """Displays the current question and answer options."""
        self.clear_window()
        main_frame = tk.Frame(self.root, bg="#F0F4C3")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        if self.round_count < self.num_rounds:
            # Get the current question data
            question_data = self.quiz_data.questions[self.current_question_index]

            # Display question number, score, and the question
            tk.Label(main_frame, text=f"Question {self.round_count + 1} of {self.num_rounds}",
                     font=("Helvetica", 16, "bold"), bg="#F0F4C3").grid(row=0, column=0, columnspan=2, pady=10)
            tk.Label(main_frame, text=f"Score: {self.score}",
                     font=("Helvetica", 14), bg="#F0F4C3").grid(row=1, column=0, columnspan=2, pady=5)
            tk.Label(main_frame, text=question_data["question"], font=("Helvetica", 12), bg="#F0F4C3").grid(
                row=2, column=0, columnspan=2, pady=10, padx=20)

            # Display answer options
            option_frame = tk.Frame(main_frame, bg="#F0F4C3")
            option_frame.grid(row=3, column=0, columnspan=2, pady=10)
            for i, option in enumerate(question_data["options"]):
                tk.Button(option_frame, text=option,
                          command=lambda opt=option: self.check_answer(opt),
                          bg="#FFCC80", font=("Helvetica", 12), relief="flat").grid(row=i // 2, column=i % 2, padx=10,
                                                                                    pady=5)

            # Display HELP and CANCEL buttons
            button_frame = tk.Frame(main_frame, bg="#F0F4C3")
            button_frame.grid(row=4, column=0, columnspan=2, pady=20)
            tk.Button(button_frame, text="HELP", command=self.display_help_callback,
                      bg="#90CAF9", font=("Helvetica", 12), relief="flat").grid(row=0, column=0, padx=10)
            tk.Button(button_frame, text="CANCEL", command=self.show_menu_callback,
                      bg="#F48FB1", font=("Helvetica", 12), relief="flat").grid(row=0, column=1, padx=10)
        else:
            # End the game and show the final score
            self.show_final_score_callback(self.score)

    def check_answer(self, selected_option):
        """Checks if the selected answer is correct and updates the score."""
        question_data = self.quiz_data.questions[self.current_question_index]
        correct_option = question_data["options"][question_data["correct_index"]]

        if selected_option == correct_option:
            self.score += 1
            feedback_text = "Correct!"
            feedback_color = "#cde777"  # Light green for correct answer
        else:
            feedback_text = f"Incorrect! The correct answer is {correct_option}."
            feedback_color = "#E76C6C"  # Light red for incorrect answer

        self.display_feedback(feedback_text, feedback_color)

    def display_feedback(self, feedback_text, feedback_color):
        """Displays feedback for the user's answer before moving to the next question."""
        self.clear_window()

        feedback_frame = tk.Frame(self.root, bg=feedback_color)
        feedback_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(feedback_frame, text=feedback_text, font=("Helvetica", 14), bg=feedback_color).grid(
            row=0, column=0, columnspan=2, pady=20, padx=20)

        # Button to move to the next question
        next_button = tk.Button(feedback_frame, text="Next Question", command=self.next_question,
                                font=("Helvetica", 12), bg="#C2C2C2", relief="flat")
        next_button.grid(row=1, column=0, columnspan=2, pady=10)

    def next_question(self):
        """Moves to the next question."""
        self.round_count += 1
        self.current_question_index += 1
        self.display_question()

    def clear_window(self):
        """Clears the tkinter window of all widgets."""
        for widget in self.root.winfo_children():
            widget.destroy()


class Help:
    """Displays help instructions for the quiz."""

    def __init__(self, root, dismiss_help_callback):
        """
        Initializes the Help class.
        :param root: The main tkinter root window.
        :param dismiss_help_callback: Callback to dismiss the help screen.
        """
        self.root = root
        self.dismiss_help_callback = dismiss_help_callback
        self.show_help()

    def show_help(self):
        """Displays help text explaining the quiz rules."""
        self.clear_window()
        main_frame = tk.Frame(self.root, bg="#DAE8FC")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(main_frame, text="This is a quiz about young animals. Select your answer from the options.",
                 wraplength=300, justify="center", bg="#DAE8FC", font=("Helvetica", 12)).grid(row=0, column=0, padx=20,
                                                                                              pady=10)
        tk.Button(main_frame, text="Dismiss", command=self.dismiss_help_callback,
                  bg="#AED581", font=("Helvetica", 12), relief="flat").grid(row=1, column=0, pady=20, padx=20)

    def clear_window(self):
        """Clears the tkinter window of all widgets."""
        for widget in self.root.winfo_children():
            widget.destroy()


class YoungAnimalQuiz:
    """Main app that orchestrates the menu, gameplay, and help functionality."""

    def __init__(self, root):
        """
        Initializes the YoungAnimalQuiz app.
        :param root: The main tkinter root window.
        """
        self.root = root
        self.root.title("Young Animal Quiz")
        self.root.geometry("450x450")  # Set a fixed window size for better display
        self.root.configure(bg="#F0F4C3")
        self.quiz_data = QuizData('animals_young_only.csv')  # Load quiz questions from the CSV file
        self.show_menu()

    def show_menu(self):
        """Displays the main menu screen."""
        self.clear_window()
        self.menu = Menu(self.root, self.start_game)

    def start_game(self, rounds):
        """Starts the game with the specified number of rounds."""
        self.clear_window()
        self.play = Play(self.root, self.quiz_data, rounds, self.show_menu, self.show_help, self.show_final_score)

    def show_help(self):
        """Displays the help screen."""
        self.clear_window()
        self.help = Help(self.root, self.play.display_question)

    def show_final_score(self, score):
        """Displays the final score at the end of the game."""
        self.clear_window()
        main_frame = tk.Frame(self.root, bg="#F0F4C3")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(main_frame, text=f"End of {self.play.num_rounds} rounds. Your final score is {score}", bg="#F0F4C3",
                 font=("Helvetica", 14)).grid(row=0, column=0, pady=10, padx=20)
        tk.Button(main_frame, text="Play Again", command=self.show_menu, bg="#AED581", font=("Helvetica", 12),
                  relief="flat").grid(row=1, column=0, pady=20, padx=20)

    def clear_window(self):
        """Clears the tkinter window of all widgets."""
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = YoungAnimalQuiz(root)
    root.mainloop()
