import tkinter as tk
from tkinter import messagebox, ttk
import PIL
from PIL import Image, ImageTk, ImageOps
import random
from quiz_data import quiz_data
from ttkbootstrap import Style

class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Guessing Flag Game")
        self.root.geometry("600x500")
        self.style = Style(theme="flatly")

        self.current_question = 0
        self.used_questions = set()
        self.question_timer = None
        self.score = 0

        self.create_widgets()

    def create_widgets(self):
        # Initial screen frame
        self.initial_frame = ttk.Frame(self.root)
        self.initial_frame.pack(pady=50)

        # Create "PLAY" button to start the game
        self.play_button = ttk.Button(self.initial_frame, text="PLAY", command=self.play_game, padding=(40, 30))
        self.play_button.pack(pady=50)

        # Create "How to Play" button
        self.how_to_play_button = ttk.Button(self.initial_frame, text="How to Play", command=self.how_to_play, padding=(40, 30))
        self.how_to_play_button.pack(pady=50)

        # Quiz game frame
        self.game_frame = ttk.Frame(self.root)

        # Create the question label
        self.qs_label = ttk.Label(self.game_frame, anchor="center", wraplength=500, padding=10)
        self.qs_label.pack(pady=10)

        # Create the choice buttons
        self.choice_btns = []
        for i in range(3):
            button = ttk.Button(self.game_frame, command=lambda i=i: self.check_answer(i))
            button.pack(pady=5)
            self.choice_btns.append(button)

        # Create the feedback label
        self.feedback_label = ttk.Label(self.game_frame, anchor="center", padding=1)
        self.feedback_label.pack(pady=10)

        # Initialize the score
        self.score_label = ttk.Label(self.game_frame, text="Score: 0/{}".format(len(quiz_data)), anchor="center", padding=1)
        self.score_label.pack(pady=10)

        # Create the next button
        self.next_btn = ttk.Button(self.game_frame, text="Next", command=self.next_question, state="disabled")
        self.next_btn.pack(pady=10)

        # Create the "Go Back" button
        self.go_back_btn = ttk.Button(self.game_frame, text="Go Back", command=self.go_back)
        self.go_back_btn.pack(pady=10)

    def play_game(self):
        self.play_button.pack_forget()
        self.initial_frame.pack_forget()
        self.game_frame.pack()
        self.show_question()

    def how_to_play(self):
        messagebox.showinfo("How to Play", "Guess the flag based on the given image. "
                                           "Select the correct answer within 10 seconds to earn points. "
                                           "Try to answer as many questions as you can!")

    def show_question(self):
        global current_question
        global used_questions
        global question_timer

        # Check if all questions have been used
        if len(used_questions) == len(quiz_data):
            messagebox.showinfo("Quiz Completed",
                                "Quiz Completed! Final score: {}/{}".format(score, len(quiz_data)))
            root.destroy()
            return

        # Choose a random question that hasn't been used yet
        while True:
            current_question = random.randint(0, len(quiz_data) - 1)
            if current_question not in used_questions:
                used_questions.add(current_question)
                break

        question = quiz_data[current_question]

        # Load the image
        image = Image.open(question["question"])

        # Calculate the border size based on the loaded image size
        max_border_size = 10  # Maximum border size
        border_size = min(max_border_size, image.width // 20, image.height // 20)

        # Add a black border around the image
        image = ImageOps.expand(image, border=border_size, fill=(0, 0, 0))

        # Resize the image as needed
        image = image.resize((200, 150), PIL.Image.Resampling.LANCZOS)  # Adjust the size as needed

        imgtk = ImageTk.PhotoImage(image)

        # Set the image to the label
        qs_label.config(image=imgtk)
        qs_label.image = imgtk

        # Shuffle the choices for the current question
        choices = question["choices"]
        random.shuffle(choices)

        # Display the shuffled choices on the buttons
        for i in range(len(choices)):
            choice_btns[i].config(text=choices[i], state="normal")

        # Clear the feedback label and disable the next button
        feedback_label.config(text="")
        next_btn.config(state="disabled")

        # Start the question timer
        question_timer = root.after(10000, time_up)
    def check_answer(self, choice):
        root.after_cancel(question_timer)

        # Get the current question from the quiz_data list
        question = quiz_data[current_question]
        selected_choice = choice_btns[choice].cget("text")

        # Check if the selected choice matches the correct answer
        if selected_choice == question["answer"]:
            # Update the score and display it
            global score
            score += 1
            score_label.config(text="Score: {}/{}".format(score, len(quiz_data)))
            feedback_label.config(text="Correct!", foreground="green")
        else:
            feedback_label.config(text="Incorrect!", foreground="red")

        # Disable all choice buttons and enable the next button
        for button in choice_btns:
            button.config(state="disabled")
        next_btn.config(state="normal")

    def time_up(self):
        feedback_label.config(text="Time's up!", foreground="red")
        next_question()

    def next_question(self):
        if len(used_questions) == len(quiz_data):
            messagebox.showinfo("Quiz Completed",
                                "Quiz Completed! Final score: {}/{}".format(score, len(quiz_data)))
            root.destroy()
        else:
            show_question()

    def go_back(self):
        self.game_frame.pack_forget()
        self.play_button.pack()
        self.initial_frame.pack()

if __name__ == "__main__":
    root = tk.Tk()
    game = QuizGame(root)
    root.mainloop()
