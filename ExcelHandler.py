import pandas as pd
from Question import Question


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

    def read_drinks(self):
        alchohols = []

        alko_excel_data = pd.read_excel(self.path, sheet_name="alko")

        for index, row in alko_excel_data.iterrows():
            alchohols.append(row[0])

        return alchohols
