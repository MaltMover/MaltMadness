from Question import Question
from tkinter import *
from random import shuffle

QUESTIONS = [
    {
        "prompt": "What is 1 + 1?",
        "options": ["1", "2", "3", "4"],
        "correct_index": 1
    },
    {
        "prompt": "What is 2 + 2?",
        "options": ["1", "2", "3", "4"],
        "correct_index": 3
    },
]

class App(Tk):
    def __init__(self):
        super().__init__()
        self.windows = {}
        self.current_window: Window | None = None

        self.title("MaltMadness")
        self.geometry("1248x702")

        self.configure(
            bg="#000000"
        )

    def set_window(self, window):
        for window in self.windows.values():
            window.place_forget()

        self.current_window = window
        self.current_window.place(x=0, y=0, width=1248, height=702)

    def set_window_by_name(self, name: str):
        self.current_window = self.windows.get(name, None)
        if self.current_window is None:
            raise ValueError(f"Window with name {name} does not exist")
        self.set_window(self.current_window)

    def setup_windows(self):
        self.windows["quiz"] = QuizWindow(self, questions=Question.from_2d_list(QUESTIONS))
        self.set_window_by_name("quiz")


class Window(Frame):
    def __init__(self, parent, bg="#000000"):
        super().__init__(parent, bg=bg)
        self.parent = parent


class QuizWindow(Window):
    def __init__(self, parent, questions: list[Question]):
        super().__init__(parent)
        self.questions = questions
        shuffle(self.questions)

        self.current_question_index = 0
        self.current_question = self.questions[self.current_question_index]

        self.option_buttons = []
        self.configure(bg="#000000")

        self.prompt = Label(self, text="", bg="#000000", fg="#ffffff", font=("Arial", 16))
        self.setup()

    def setup(self):
        self.prompt.configure(
            anchor="center",
            justify="center",
        )
        self.prompt.place(x=0, y=0, width=1248, height=100)
        for i in range(4):
            self.option_buttons.append(OptionButton(self, text="2", command=self.next_question))
            self.option_buttons[i].place(x=100, y=100 + i * 150, width=300, height=100)
        self.display_question()

    def display_question(self):
        self.prompt.configure(text=self.current_question.prompt)
        for i in range(4):
            command = None  # TODO: Make this show wrong
            if i == self.current_question.correct_index:
                command = self.next_question
            self.option_buttons[i].configure(text=self.current_question.options[i], command=command)

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index >= len(self.questions):
            self.parent.set_window_by_name("end")
            return

        self.current_question = self.questions[self.current_question_index]
        self.display_question()


class OptionButton(Button):
    def __init__(self, parent, text, command, bg="#FF0000", fg="#ffffff", font=("Arial", 12)):
        Button.__init__(self, parent, text=text, command=command, bg=bg, fg=fg, font=font)
        self.configure(
            activebackground="#000000",
            activeforeground="#ffffff",
            bd=0,
            highlightthickness=0,
            relief="flat"
        )
