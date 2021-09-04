def JaccardIndex(str1 : set, str2 : set):
    """
        selects shared tokens only and union adds both sets together
    """
    str1 = set(str1)
    str2 = set(str2)
    shared = str1.intersection(str2)
    return len(shared) / len(str1.union(str2))

if __name__ == "__main__":
    str1 = input()
    str2 = input()
    print(JaccardIndex(str1, str2))
