def JaccardIndex(str1 : str, str2 : str) -> float:
    """
        selects shared tokens only and union adds both sets together
    """
    str1 = set(str1)
    str2 = set(str2)
    shared = str1.intersection(str2)
    return len(shared) / len(str1.union(str2))
