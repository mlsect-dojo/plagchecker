from api.utils.scoring.base_check import BaseCheck
from models.levenshtein import Levenshtein


class LevenshteinScore(BaseCheck):

    def __init__(self) -> None:
        self.levenshtein = Levenshtein()
        super().__init__(self.levenshtein.comparison)
        
    def name(self) -> str:
        return self.__class__.__name__.lower()[:-5]
