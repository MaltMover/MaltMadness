class Question:
    def __init__(self, prompt: str, options: list[str], correct_index: int):
        self.prompt = prompt
        self.options = options
        self.correct_index = correct_index
        self.correct_answer = options[correct_index]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["prompt"], data["options"], data["correct_index"])

    @classmethod
    def from_2d_list(cls, data: list[dict]) -> list:
        questions = []
        for question in data:
            questions.append(cls.from_dict(question))
        return questions

    def to_dict(self):
        return {
            "prompt": self.prompt,
            "options": self.options,
            "correct_index": self.correct_index,
            "correct_answer": self.correct_answer
        }
