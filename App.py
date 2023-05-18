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
        self.windows["quiz"] = QuizWindow(self)
        self.set_window_by_name("quiz")


class Window(Frame):
    def __init__(self, parent, bg="#000000"):
        super().__init__(parent, bg=bg)
        self.parent = parent


class QuizWindow(Window):
    def __init__(self, parent):
        super().__init__(parent)
        self.option_buttons = []

        self.configure(bg="#000000")
        self.setup()

    def setup(self):
        for i in range(4):
            self.option_buttons.append(OptionButton(self, f"Option {i+1}", None))
            self.option_buttons[i].place(x=100, y=100 + i * 100, width=200, height=50)


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
