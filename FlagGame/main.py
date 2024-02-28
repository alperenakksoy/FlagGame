import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
from PIL import Image, ImageOps, ImageTk
import random
from quiz_data import quiz_data

class Exercise:
    def __init__(self, root):
        self.root = root
        self.frame = ttk.Frame(self.root)
        self.setup_ui()

    def setup_ui(self):
        self.frame.pack(pady=50)

        # Create the question label
        self.qs_label = ttk.Label(
            self.frame,
            anchor="center",
            wraplength=400,
            padding=10
        )
        self.qs_label.pack(pady=10)

        # Create the answer label with a larger font size
        self.answer_label = ttk.Label(
            self.frame,
            anchor="center",
            padding=1,
            font=("Helvetica", 31)  # Adjust the font size as needed
        )
        self.answer_label.pack(pady=10)

        # Create the next button
        self.next_btn = ttk.Button(
            self.frame,
            text="Next",
            command=self.show_question,
            state="normal"
        )
        self.next_btn.pack(pady=10)

        # Initialize the current question index
        self.current_question = 0

        # Track used questions
        self.used_questions = set()

        # Show the first question
        self.show_question()

        back_button = ttk.Button(self.frame, text="Go Back", command=self.go_back)
        back_button.pack(pady=1)

    def show_question(self):
        # Check if all questions have been used
        if len(self.used_questions) == len(quiz_data):
            messagebox.showinfo("Exercise Completed", "Exercise Completed!")
            self.root.destroy()
            return

        # Choose a random question that hasn't been used yet
        while True:
            self.current_question = random.randint(0, len(quiz_data) - 1)
            if self.current_question not in self.used_questions:
                self.used_questions.add(self.current_question)
                break

        # Load the image
        image = Image.open(quiz_data[self.current_question]["question"])

        # Calculate the border size based on the loaded image size
        max_border_size = 10  # Maximum border size
        border_size = min(max_border_size, image.width // 10, image.height // 10)

        # Add a black border around the image
        image = ImageOps.expand(image, border=border_size, fill=(0, 0, 0))

        # Resize the image as needed
        image = image.resize((200, 150), Image.LANCZOS)  # Adjust the size as needed

        imgtk = ImageTk.PhotoImage(image)

        # Set the image to the label
        self.qs_label.config(image=imgtk)
        self.qs_label.image = imgtk

        # Set the answer to the label
        answer_text = " {}".format(quiz_data[self.current_question]["answer"])
        self.answer_label.config(text=answer_text)

        # Enable the next button
        self.next_btn.config(state="normal")

    def go_back(self):
        self.frame.pack_forget()
        play_button.pack()
        exercise_button.pack()
        how_to_play_button.pack()
        initial_frame.pack()

def show_question():
    global current_question
    global used_questions

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
    image = image.resize((200, 150), Image.LANCZOS)  # Adjust the size as needed

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



def check_answer(choice):

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

def time_up():
    # If time is up, move to the next question
    feedback_label.config(text="Time's up!", foreground="red")
    next_question()

def next_question():
    # If all questions have been used, show the final score and end the quiz
    if len(used_questions) == len(quiz_data):
        messagebox.showinfo("Quiz Completed",
                            "Quiz Completed! Final score: {}/{}".format(score, len(quiz_data)))
        root.destroy()
    else:
        show_question()

def play_game():
    play_button.pack_forget()
    exercise_button.pack_forget()
    how_to_play_button.pack_forget()
    initial_frame.pack_forget()
    game_frame.pack()
    show_question()

def go_back():
    game_frame.pack_forget()
    play_button.pack()
    exercise_button.pack()
    how_to_play_button.pack()
    initial_frame.pack()

def open_exercise_game():
    exercise_game = Exercise(root)
    exercise_game.frame.pack_forget()
    play_button.pack_forget()
    exercise_button.pack_forget()
    how_to_play_button.pack_forget()
    exercise_game.frame.pack()

def how_to_play():
    messagebox.showinfo("How to Play", "Guess the flag based on the given image."
                                       "Try to answer as many questions as you can!")

root = tk.Tk()
root.title("Guessing Flag Game")
root.geometry("900x700")
style = Style(theme="flatly")

initial_frame = ttk.Frame(root)
initial_frame.pack(pady=50)

button_width = 15

play_button = ttk.Button(initial_frame, text="PLAY", command=play_game, padding=(40, 30), width=button_width)
play_button.pack(side=tk.LEFT, padx=(0, 10))

exercise_button = ttk.Button(initial_frame, text="Exercise", command=open_exercise_game, padding=(40, 30), width=button_width)
exercise_button.pack(side=tk.LEFT)

how_to_play_button = ttk.Button(initial_frame, text="How to Play", command=how_to_play, padding=(40, 30), width=button_width)
how_to_play_button.pack(side=tk.RIGHT, padx=(10, 0))

game_frame = ttk.Frame(root)

qs_label = ttk.Label(
    game_frame,
    anchor="center",
    wraplength=500,
    padding=10
)
qs_label.pack(pady=10)

# Create the choice buttons
choice_btns = []
for i in range(3):
    button = ttk.Button(
        game_frame,
        command=lambda i=i: check_answer(i)
    )
    button.pack(pady=5)
    choice_btns.append(button)

# Create the feedback label
feedback_label = ttk.Label(
    game_frame,
    anchor="center",
    padding=1
)
feedback_label.pack(pady=10)

# Initialize the score
score = 0

# Create the score label
score_label = ttk.Label(
    game_frame,
    text="Score: 0/{}".format(len(quiz_data)),
    anchor="center",
    padding=1
)
score_label.pack(pady=10)

# Create the next button
next_btn = ttk.Button(
    game_frame,
    text="Next",
    command=next_question,
    state="disabled"
)
next_btn.pack(pady=10)

# Create the "Go Back" button
go_back_btn = ttk.Button(
    game_frame,
    text="Go Back",
    command=go_back
)
go_back_btn.pack(pady=10)

# Initialize the current question index
current_question = 0

# Track used questions
used_questions = set()


root.mainloop()
