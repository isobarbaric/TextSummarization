
class TextRank:

    def __init__(self, words: set, d=0.85):
        self.words = words
        self.scores = {}

    def tabulate(self):
        pass
    
# use proper implementation later (numpy?)
def getCol(arr):
    cols = []
    for i in range(len(arr[0])):
        cols.append([])
        for j in range(len(arr)):
            cols[-1].append(arr[j][i])
    return cols

# q = [[9, 24], [7, 18], [25, 63]]
# print(getCol(q))

def matrix_multiplication(a, b):
    # len(col of first) = len(row of second) 
    assert(len(a[0]) == len(b))

    results = []    
    for row in a:
        results.append([])
        for col in getCol(b):
            current_sum = 0
            for i in range(len(row)):
                current_sum += row[i]*col[i]
            results[-1].append(current_sum)

    return results

x = [
    [4, -1],
    [0, 2],
    [-8, 3]
]

y = [
    [6, -2, 1],
    [5, 0, 7]
]

a = matrix_multiplication(x, y)
print(a)