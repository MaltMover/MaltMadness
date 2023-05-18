import pandas as pd
from Question import Question
from Player import Player


class ExcelHandler:

    def __init__(self, path):
        self.path = path

    def read_questions(self):
        questions = []

        excel_data = pd.read_excel(self.path, sheet_name="hva")

        for index, row in excel_data.iterrows():
            question = Question(
                prompt=row[0],
                options=[
                    row[1],
                    row[2],
                    row[3],
                    row[4]
                ],
                correct_index=int(row[5]) - 1
            )
            questions.append(question)

        return questions

    def read_tough_drinks(self):
        alchohols = []

        alko_excel_data = pd.read_excel(self.path, sheet_name="alko")

        for index, row in alko_excel_data.iterrows():
            alchohols.append(row[0])

        return alchohols

    def read_soft_drinks(self):
        alchohols = []

        softdrinks_excel_data = pd.read_excel(self.path, sheet_name="alko")

        for index, row in softdrinks_excel_data.iterrows():
            alchohols.append(row[0])

        return alchohols

    def read_players(self):
        players = []

        player_excel_data = pd.read_excel(self.path, sheet_name="players")

        for index, row in player_excel_data.iterrows():
            player = Player(
                id=row.index(),
                name=row[0],
                age=row[1],
                networth=[2]
            )

            players.append(player)

        return players

    def read_player_disses(self, playerID):
        player_disses = []

        player_excel_data = pd.read_excel(self.path, sheet_name="roasts")

        for index, row in player_excel_data.iterrows():
            if row[0] == playerID:
                player_disses.append(row[1])

        return player_disses



