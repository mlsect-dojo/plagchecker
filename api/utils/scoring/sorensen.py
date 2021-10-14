from api.utils.scoring.base_check import BaseCheck
from models.sorensen import Sorensen


class SorensenScore(BaseCheck):

    def __init__(self) -> None:
        self.sorensen = Sorensen()
        super().__init__(self.sorensen.comparison)

    def name(self) -> str:
        return self.__class__.__name__.lower()[:-5]
