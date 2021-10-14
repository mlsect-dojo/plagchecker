from api.utils.scoring.base_check import BaseCheck
from models.jaccard import Jaccard


class JaccardScore(BaseCheck):

    def __init__(self) -> None:
        self.jaccard = Jaccard()
        super().__init__(self.jaccard.comparison)

    def name(self) -> str:
        return self.__class__.__name__.lower()[:-5]
