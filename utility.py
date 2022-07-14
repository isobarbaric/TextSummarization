
from gtts import gTTS
from playsound import playsound
import os
# import atexit
  
class Reader:

    def __init__(self):
        pass
    
    def read(self, text):
        speech_audio = gTTS(text = text, lang = 'en', slow = False)
        speech_audio.save('text-spoken.mp3')
        playsound('text-spoken.mp3')
        os.remove('text-spoken.mp3')

class Matrix:
    def __init__(self, grid):
        self.grid = grid
    
    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            t = Matrix(self.grid.copy())
            for i in range(len(t.grid)):
                for j in range(len(t.grid[i])):
                    t.grid[i][j] += other
            return t
        else: 
            raise TypeError('Matrix - Matrix addition has not been implemented')

    def __radd__(self, other):
        return self.__add__(other)    

    def __sub__(self, other):
        return self.__add__(-1*other)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            t = Matrix(self.grid.copy())
            for i in range(len(t.grid)):
                for j in range(len(t.grid[i])):
                    t.grid[i][j] *= other
            return t
        elif type(other) == Matrix:
            # use proper implementation later (numpy?)
            def getCol(arr):
                cols = []
                for i in range(len(arr[0])):
                    cols.append([])
                    for j in range(len(arr)):
                        cols[-1].append(arr[j][i])
                return cols

            # len(col of first) = len(row of second) 
            assert(len(self.grid[0]) == len(other.grid))

            results = []    
            for row in self.grid:
                results.append([])
                for col in getCol(other.grid):
                    current_sum = 0
                    for i in range(len(row)):
                        current_sum += row[i]*col[i]
                    results[-1].append(current_sum)
            return Matrix(results)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __repr__(self):
        return str(self.grid)