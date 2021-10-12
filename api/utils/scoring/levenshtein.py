from api.utils.scoring.base_check import BaseCheck
from models.levenshtein import levenshtein

class Levenshtein(BaseCheck):

    async def algorithm(self, code: str, lab: str) -> float:
        return levenshtein.distance(code, lab)

    def name(self) -> str:
        return self.__class__.__name__.lower()