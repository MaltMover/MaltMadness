import pandas as pd

from Question import Question


def read_questions(path):
    questions = []

    excel_data = pd.read_excel(path, sheet_name="hva")

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
