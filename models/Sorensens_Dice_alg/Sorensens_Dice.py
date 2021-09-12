def sorensen_dice(first_phrase: str, second_phrase: str) -> float:
    first_phrase = set(first_phrase)
    second_phrase = set(second_phrase)
    shared = first_phrase.intersection(second_phrase)
    return 2 * len(shared) / (len(first_phrase) + len(second_phrase))
