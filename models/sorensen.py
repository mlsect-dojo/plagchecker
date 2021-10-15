from models.base_algorithm import BaseAlgorithm


class Sorensen(BaseAlgorithm):

    def comparison(self, str1: str, str2: str) -> float:
        if not (isinstance(str1, str)) or (type(str1) != type(str2)):
            raise TypeError("You can only compare objects of the str type")

        str1_set = set(str1.split())
        str2_set = set(str2.split())
        number_intersections = len(str1_set.intersection(str2_set))

        if len(str1_set) + len(str2_set) == 0:
            return 1.0

        return 2 * number_intersections / (len(str1_set) + len(str2_set))

    def name(self) -> str:
        return self.__class__.__name__.lower()
