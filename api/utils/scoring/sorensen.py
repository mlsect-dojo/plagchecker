from api.utils.scoring.base_check import BaseCheck
from models.sorensen import sorensens_dice

class Sorensen(BaseCheck):

    async def algorithm(self, code: str, lab: str) -> float:
        return sorensens_dice.comparison(code, lab)

    def name(self) -> str:
        return self.__class__.__name__.lower()