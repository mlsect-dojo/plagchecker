from api.utils.scoring.base_check import BaseCheck
from models.Jaccard import jaccard

class Jaccard(BaseCheck):

    async def algorithm(self, code: str, lab: str) -> float:
        return jaccard.JaccardIndex(code, lab)

    def name(self) -> str:
        return self.__class__.__name__.lower()
