from typing import List


def comparison(first_phrase: List[str], second_phrase: List[str]) -> float:
    first_phrase = set(first_phrase)
    second_phrase = set(second_phrase)
    if not(isinstance(first_phrase, list)) or (type(first_phrase) != type(second_phrase)):
        raise TypeError("You can only compare objects of the list type")
    number_intersections = len(first_phrase.intersection(second_phrase))
    if len(first_phrase) + len(second_phrase) == 0:
        return 1.0
    return 2 * number_intersections / (len(first_phrase) + len(second_phrase))
