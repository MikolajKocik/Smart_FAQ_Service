class FaqDomain:
    def __init__(self, id_: int, question: str, answer: str):
        self.id = id_
        self.question = question
        self.answer = answer
        
    @property 
    def question(self) -> str:
        return self._question
    
    @property
    def answer(self) -> str:
        return self._answer
    
    @question.setter
    def question(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Question cannot be empty")
        if len(value) > 500:
            raise ValueError("Question too long")
        self._question = value

    @answer.setter
    def answer(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Answer cannot be empty")
        if len(value) < 1:
            raise ValueError("Answer too short")
        self._answer = value
    

