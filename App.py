from tkinter import *


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
        self.windows["quiz"] = QuizWindow(self, "Hvem?", ["Jeg", "Du", "Han", "Hun"], 0)
        self.set_window_by_name("quiz")


class Window(Frame):
    def __init__(self, parent, bg="#000000"):
        super().__init__(parent, bg=bg)
        self.parent = parent


class QuizWindow(Window):
    def __init__(self, parent, question: str, options: list[str], correct_index: int):
        super().__init__(parent)
        self.question = question
        self.options = options
        self.correct_index = correct_index
        self.prompt = Label(self, text=question, bg="#000000", fg="#ffffff", font=("Arial", 12))
        self.option_buttons = []

        self.configure(bg="#000000")
        self.setup()

    def setup(self):
        self.prompt.configure(
            text=self.question,
            anchor="center",
            justify="center",
        )
        self.prompt.place(x=0, y=0, width=1248, height=100)
        for i in range(4):
            self.option_buttons.append(OptionButton(self, self.options[i], None))
            self.option_buttons[i].place(x=100, y=100 + i * 100, width=200, height=50)


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
