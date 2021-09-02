import levenshtein

str1 = input()
str2 = input()
tmp = max(len(str1), len(str2))
d = levenshtein.distance(str1, str2)
print(100 - d * 100 / tmp, end=" %")
