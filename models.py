from pydantic import BaseModel
from typing import List


class Sentence(BaseModel):
    wrong_sentence: str
    corrected_sentence: str
    type_of_error: str


class GrammarChecker(BaseModel):
    modifications: List[Sentence]
    full_corrected_text: str


class ModelRefusalError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
