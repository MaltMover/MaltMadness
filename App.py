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

    def set_window(self, new_window):
        for window in self.windows.values():
            window.place_forget()

        print(new_window)
        self.current_window = new_window
        self.current_window.place(x=0, y=0, width=1248, height=702)

    def set_window_by_name(self, name: str):
        self.set_window(self.windows[name])

    def setup_windows(self):
        self.windows["failed"] = FailedWindow(self)
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
            command = lambda: self.parent.set_window_by_name("failed")
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


def closing_popup():
    # Failed popup window
    failed_window = Tk()
    failed_window.geometry("300x300")
    failed_window.title("Vil du skride?")
    failed_window.configure(bg="#123456")
    Label(failed_window, text="Vil du lukke programmet?", font=('Mistral 18 bold')).place(x=50, y=80)
    Label(failed_window, text="Nå, jamen det må du ikke", font=('Arial 12')).place(x=70, y=120)
    Label(failed_window, text="Fordi her. Elsker. Vi. At Hygge. :)", font=('Oswald 12 bold')).place(x=0, y=180)
    Label(failed_window, text="Du skal spille vidre, slayyyyyyy", font=('Arial 12')).place(x=30, y=220)
    Button(failed_window, text="Tak skatter <3", command=failed_window.destroy).place(x=50, y=260)


class FailedWindow(Window):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#000000")

        self.failed_label = Label(self, text="Du er så dum, men det er okay <3", bg="#000000", fg="#ffffff",
                                  font=("Oswald", 36))
        self.retry_button = OptionButton(self, "Prøv igjen", None)
        self.quit_button = OptionButton(self, "Avslutt", closing_popup)
        self.drink_button = OptionButton(self, "Drikk", None)

        self.setup()

    def setup(self):
        self.failed_label.configure(
            anchor="center",
            justify="center",
        )
        self.drink_button.configure(
            bg="#FFFF00",
            fg="#ffffff",
            font=("Arial", 12)
        )
        self.failed_label.place(x=0, y=0, width=1248, height=100)
        self.drink_button.place(x=100, y=150, width=1000, height=200)
        self.quit_button.place(x=100, y=500, width=893, height=50)
        self.retry_button.place(x=100, y=400, width=900, height=50)


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
