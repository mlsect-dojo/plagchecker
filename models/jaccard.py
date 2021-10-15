from models.base_algorithm import BaseAlgorithm


class Jaccard(BaseAlgorithm):

    def comparison(self, str1: str, str2: str) -> float:
        """Selects shared tokens only and union adds both sets together"""

        str1_set = set(str1)
        str2_set = set(str2)
        shared = str1_set.intersection(str2_set)

        return len(shared) / len(str1_set.union(str2_set))

    def name(self) -> str:
        return self.__class__.__name__.lower()
