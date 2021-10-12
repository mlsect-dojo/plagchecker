def comparison(first_phrase: str, second_phrase: str) -> float:
    if not (isinstance(first_phrase, str)) or (type(first_phrase) != type(second_phrase)):
        raise TypeError("You can only compare objects of the str type")
    first_phrase = set(first_phrase.split())
    second_phrase = set(second_phrase.split())
    number_intersections = len(first_phrase.intersection(second_phrase))
    if len(first_phrase) + len(second_phrase) == 0:
        return 1.0
    return 2 * number_intersections / (len(first_phrase) + len(second_phrase))
