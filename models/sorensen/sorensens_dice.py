from typing import List


def intersection_counter(first_list: List[str], second_list: List[str]) -> int:
    count = 0
    for item in first_list:
        if item in second_list:
            count += 1
            second_list.remove(item)
    return count


def comparison(first_phrase: str, second_phrase: str) -> float:
    if type(first_phrase) != type(second_phrase):
        raise TypeError("You can only compare objects of the str type")
    first_phrase = list(first_phrase)
    second_phrase = list(second_phrase)
    number_intersections = intersection_counter(first_phrase.copy(), second_phrase.copy())
    if len(first_phrase) + len(second_phrase) == 0:
        return 1.0
    return 2 * number_intersections / (len(first_phrase) + len(second_phrase))
