from models.base_algorithm import BaseAlgorithm


class Levenshtein(BaseAlgorithm):

    def comparison(self, str1: str, str2: str) -> float:
        """The Levenshtein distance is a string metric for measuring the difference between two sequences.
        It is calculated as the minimum number of single-character edits necessary to transform one string into another"""

        n, m = len(str1), len(str2)

        if n > m:
            str1, str2 = str2, str1
            n, m = m, n
            
        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if str1[j - 1] != str2[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]
