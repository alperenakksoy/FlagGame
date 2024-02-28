import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style
import PIL.Image
import random
from quiz_data import quiz_data
from PIL import Image, ImageTk, ImageOps
class Exercise:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        self.frame = ttk.Frame(self.root)
        self.frame.pack(pady=50)

        # Create the question label
        self.qs_label = ttk.Label(
            self.frame,
            anchor="center",
            wraplength=500,
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
        border_size = min(max_border_size, image.width // 20, image.height // 20)

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

# Create the main window
root = tk.Tk()
root.title("Exercise Game")
root.geometry("600x500")
style = Style(theme="flatly")

# Create an instance of the Exercise class
exercise_game = Exercise(root)

# Start the main event loop
root.mainloop()