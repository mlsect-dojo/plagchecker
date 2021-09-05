def Sorensen_Dice_Coeff(str1: set, str2: set):
    str1 = set(str1)
    str2 = set(str2)

    shared = str1.intersection(str2)

    return (2 * len(shared) / (len(str1) + len(str2)))