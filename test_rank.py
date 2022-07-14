
from text import Node

class TextRank:

    def __init__(self, words: list[Node], d=0.85):
        self.words = words
        self.scores = {}

        # for word in self.words:
        #     self.cost[word] = 1/self.N
        
        self.d = d
        self.cost = dict()

    def matrix_multiplication(self, a, b):            
        # use proper implementation later (numpy?)
        def getCol(arr):
            cols = []
            for i in range(len(arr[0])):
                cols.append([])
                for j in range(len(arr)):
                    cols[-1].append(arr[j][i])
            return cols

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

    # def tabulate(self):
        
    #     for i in range(10):
            
