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
        alco_excel_data = pd.read_excel(self.path, sheet_name="alko")

        alcohols = []
        for index, row in alco_excel_data.iterrows():
            alcohols.append(row[0])

        return alcohols

    def read_soft_drinks(self):
        softdrink_excel_data = pd.read_excel(self.path, sheet_name="sode")

        softdrinks = []
        for index, row in softdrink_excel_data.iterrows():
            softdrinks.append(row[0])

        return softdrinks

    def read_players(self):
        player_excel_data = pd.read_excel(self.path, sheet_name="players")

        players = []

        index = 0

        for index, row in player_excel_data.iterrows():
            player = Player(
                id=index,
                name=row[0],
                age=row[1],
                sex=row[2],
                networth=row[3]
            )
            index+1

            players.append(player)
        return players

    def read_player_disses(self, playerID):
        player_excel_data = pd.read_excel(self.path, sheet_name="roasts")

        player_disses = []
        for index, row in player_excel_data.iterrows():
            if row[0] == int(playerID):
                player_disses.append(row[1])

        return player_disses





