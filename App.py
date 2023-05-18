from Question import Question
from ExcelHandler import ExcelHandler
from WebScraper import WebScraper
from tkinter import *
from random import shuffle, choice, randint
from PIL import ImageTk, Image
import playsound


class App(Tk):
    def __init__(self):
        super().__init__()
        self.windows = {}
        self.feature_buttons = {}
        self.current_window: Window | None = None

        self.title("MaltMadness")
        self.geometry("1248x702")
        self.iconbitmap("img/icon.ico")

        self.excel_handler = ExcelHandler("slayysaft.xlsx")
        self.scraper = WebScraper()
        self.configure(
            bg="#000000"
        )

    def set_window(self, new_window):
        for window in self.windows.values():
            window.place_forget()

        self.current_window = new_window
        if isinstance(self.current_window, QuizWindow) or isinstance(self.current_window, DrinkMixer):
            self.current_window.place(x=300, y=0, width=800, height=400)
        else:
            self.current_window.place(x=0, y=0, width=1248, height=702)

    def set_window_by_name(self, name: str):
        self.set_window(self.windows[name])

    def setup(self):
        self.windows["quiz"] = QuizWindow(self, questions=self.excel_handler.read_questions())
        self.windows["drinks"] = DrinkMixer(self)
        self.windows["failed"] = FailedWindow(self)
        self.windows["won"] = WonWindow(self)
        self.set_window_by_name("quiz")

        self.setup_random_features()

    def setup_random_features(self):
        self.scraper.get_github_issues()
        self.byggemand = Image.open("img/byggemand.png")
        self.byggemand = self.byggemand.resize((200, 200), Image.ANTIALIAS)
        self.byggemand = ImageTk.PhotoImage(self.byggemand)

        self.feature_buttons["github"] = Button(
            self,
            image=self.byggemand,
            command=lambda: self.show_toplevel(choice(self.scraper.github_issues), img="img/byggemand.png"),
            bg="#000000",
            borderwidth=0,
        )
        self.feature_buttons["github"].place(x=25, y=100, width=200, height=200)

        self.drink_image = Image.open("img/drinks.png")
        self.drink_image = self.drink_image.resize((200, 200), Image.ANTIALIAS)
        self.drink_image = ImageTk.PhotoImage(self.drink_image)

        self.feature_buttons["drinks"] = Button(
            self,
            image=self.drink_image,
            command=lambda: self.set_window_by_name("drinks"),
            bg="#000000",
            borderwidth=0,
        )
        self.feature_buttons["drinks"].place(x=200, y=500, width=200, height=200)

    def show_toplevel(self, text, img=None):
        top = Toplevel(self)
        top.title("MaltMadness")
        top.geometry("300x300")
        top.configure(bg="#000000")
        Label(top, text=text, bg="#000000", fg="#ffffff", font=("Arial", 18), wraplength=280).pack()
        if img:
            self.img = Image.open(img)
            self.img = self.img.resize((200, 200), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.img)
            Label(top, image=self.img, bg="#000000").pack()

    def show_fuckdethele(self, id):
        self.select_top.destroy()
        self.set_window_by_name("quiz")
        top = Toplevel(self)
        top.title("MaltMadness")
        top.geometry("300x600")
        top.configure(bg="#000000")

        self.img = Image.open("img/wordart.png")
        self.img = self.img.resize((300, 50), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        Label(top, image=self.img, bg="#000000").pack()

        self.img2 = Image.open("img/sodLilFatter.png")
        self.img2 = self.img2.resize((300, 200), Image.ANTIALIAS)
        self.img2 = ImageTk.PhotoImage(self.img2)
        Label(top, image=self.img2, bg="#000000").pack()

        text = choice(self.excel_handler.read_player_disses(id))

        Label(top, text=text, bg="#000000", fg="#ffffff", font=("Arial", 18), wraplength=280, ).pack()

    def select_user(self):
        self.select_top = Toplevel(self)
        self.select_top.title("Hvem er svag?")
        self.select_top.geometry("500x500")
        self.select_top.configure(bg="#000000")
        Label(self.select_top, text="Hvem er svag?", bg="#000000", fg="#ffffff", font=("Arial", 18), wraplength=280).pack()

        players = self.excel_handler.read_players()
        for player in players:
            Button(self.select_top, text=player.name, command=lambda player=player: self.show_fuckdethele(player.id), bg="#a85832", borderwidth=3,
                   height=4, width=50, padx=2, pady=2).pack()


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

        self.prompt = Label(self, text="", bg="#000000", fg="#ffffff", font=("Arial", 20))
        self.setup()

    def setup(self):
        self.prompt.configure(
            anchor="center",
            justify="center",
        )
        self.prompt.place(x=0, y=0, width=800, height=100)
        for i in range(4):
            self.option_buttons.append(OptionButton(self, text="", command=self.next_question))
            x = (400 * (i % 2))
            y = 100 + (170 * (i // 2))
            self.option_buttons[i].place(
                x=x,
                y=y,
                width=300,
                height=100
            )
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
            self.parent.set_window_by_name("won")
            return

        self.current_question = self.questions[self.current_question_index]
        self.display_question()


class DrinkMixer(Window):
    def __init__(self, parent):
        super().__init__(parent)
        self.soft_drinks = self.parent.excel_handler.read_soft_drinks()
        self.alcoholic_drinks = self.parent.excel_handler.read_tough_drinks()
        self.ingredient_labels = []
        self.done_button = None

        self.configure(bg="#000000")
        self.setup()

    def setup(self):
        Label(self, text="DRIKKETID", bg="#000000", fg="#FFFFFF", font=("Arial", 22)).place(x=0, y=0, width=800, height=100)
        Button(
            self,
            text="LAV DRINK",
            command=self.show_drink,
            bg="#990280",
            fg="#FFFFFF",
            font=("Arial", 20),
            borderwidth=0,
        ).place(x=0, y=100, width=800, height=100)
        self.done_button = Button(
            self,
            text="moaar jeg færdig",
            command=self.close,
            bg="#990280",
            fg="#FFFFFF",
            font=("Arial", 20),
            borderwidth=0,
        )

    def show_drink(self):
        for l in self.ingredient_labels:
            l.destroy()
        self.done_button.place(x=0, y=100, width=800, height=100)
        self.ingredient_labels = []
        soft_drink_count = randint(1, 2)
        alcoholic_drink_count = randint(1, 2)
        ingredients = [choice(self.soft_drinks) for _ in range(soft_drink_count)] + \
                      [choice(self.alcoholic_drinks) for _ in range(alcoholic_drink_count)]

        max_amount = 300
        amounts = []
        for _ in range(len(ingredients)):
            amount = randint(0, max_amount)
            amounts.append(amount)
            max_amount -= amount

        for ingredient, amount in zip(ingredients, amounts):
            self.ingredient_labels.append(
                Label(self, text=f"{ingredient} {amount} ml", bg="#000000", fg="#FFFFFF", font=("Arial", 18))
            )

        for i, l in enumerate(self.ingredient_labels):
            l.place(x=0, y=200 + (i * 50), width=800, height=50)

    def close(self):
        for l in self.ingredient_labels:
            l.destroy()
        self.done_button.place_forget()
        self.parent.set_window_by_name("quiz")


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
        self.parent = parent
        self.configure(bg="#341265")
        self.drink_image = Image.open("img/DrikForSatan.png")
        self.drink_image = self.drink_image.resize((1000, 200), Image.ANTIALIAS)
        self.drink_image = ImageTk.PhotoImage(self.drink_image)

        self.failed_label = Label(self, text="Du er så dum, men det er okay <3", bg="#000000", fg="#ffffff",
                                  font=("Comic Sans MS", 36))
        self.retry_button = OptionButton(self, "Prøv igjen", self.hehe_you_thought_lmao)
        self.quit_button = OptionButton(self, "Avslutt", closing_popup)
        self.drink_button = Button(self, text="Drikk", image=self.drink_image, command=lambda: self.parent.set_window_by_name("drinks"))
        self.crybaby_button = OptionButton(self, "Jeg er en lille bitch", command=lambda: self.parent.select_user())

        self.setup()

    def setup(self):
        self.failed_label.configure(
            anchor="center",
            justify="center",
        )
        self.failed_label.place(x=0, y=0, width=1248, height=100)
        self.drink_button.place(x=100, y=150, width=1000, height=200)
        self.quit_button.place(x=100, y=500, width=893, height=50)
        self.retry_button.place(x=100, y=400, width=900, height=50)
        self.crybaby_button.place(x=110, y=600, width=900, height=50)

    def hehe_you_thought_lmao(self):
        self.retry_button.configure(text="Du troede du kunne slippe uden at drikke? Vi er danskere der elsker "
                                         "gruppepres :) DRIK!")


def godnat_for_satan():
    playsound.playsound('img/zzz.mp3')


def godnat_popup():
    # Failed popup window
    failed_window = Tk()
    failed_window.geometry("300x300")
    failed_window.title("Vil du skride?")
    failed_window.configure(bg="#992277")
    Label(failed_window, text="Godnat Daniel", font=('Arial 18 bold')).place(x=50, y=80)
    Label(failed_window, text="Du skal i skole i morgen", font=("Comic Sans MS", 18)).place(x=1, y=120)
    Label(failed_window, text="Godnat", font=('Oswald 12 bold')).place(x=0, y=180)
    Label(failed_window, text="YOU HAVE SCHOOL TOMORROW", font=('Oswald 12')).place(x=70, y=220)
    Button(failed_window, text="zzzzzzzzzzzzz", command=godnat_for_satan).place(x=50, y=260)


class WonWindow(Window):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(bg="#d4af37")
        self.drink_image = Image.open("img/DuVandt.png")
        self.drink_image = self.drink_image.resize((1000, 500), Image.ANTIALIAS)
        self.drink_image = ImageTk.PhotoImage(self.drink_image)

        self.won_label = Label(self, text="Grattis! Du vann! Du är fortfarande ful", bg="#000000", fg="#ffffff",
                               font=("Comic Sans MS", 18))
        self.congrats_button = Button(self, image=self.drink_image)
        self.godnat_daniel = Button(self, text="Godnat Daniel", command=godnat_popup)
        self.setup()

    def setup(self):
        self.won_label.configure(
            anchor="center",
            justify="center",
        )
        self.won_label.place(x=0, y=0, width=1248, height=100)
        self.congrats_button.place(x=100, y=150, width=1000, height=500)
        self.godnat_daniel.place(x=1110, y=130, width=100, height=25)


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
