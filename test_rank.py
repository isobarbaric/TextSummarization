

# class TextRank:

#     def __init__(self, words: list[Node], d=0.85):
#         self.words = words
#         self.scores = {}

#         # for word in self.words:
#         #     self.cost[word] = 1/self.N
        
#         self.d = d
#         self.cost = dict()

 
    # def tabulate(self):
        
    #     for i in range(10):

def build_vector(self):
    self.edges = dict()
    
    # keys are all strings 
    for first_word in self.graph:
        self.edges[first_word] = dict() 
        for second_word in self.graph:
            if first_word == second_word:
                continue
            self.edges[first_word][second_word] = 0

    # handle sinks
    for word in self.graph:
        if len(self.graph[word].outgoing) == 0:
            for connect_word in self.unique_words:
                self.graph[word].outgoing.append(self.graph[connect_word])

    # test numbers later with a specific example, for now just assuming that this works 
    for first_word in self.edges:
        for existing_word in self.graph[first_word].outgoing:
            print(type(existing_word))
            self.edges[first_word][existing_word] = 1/len(self.graph[first_word].outgoing)

    # for word in self.edges:
    #     print(word)

# temporary storage below

def build_vector(self):
    self.edges = dict()
    
    # keys are all strings 
    for first_word in self.graph:
        self.edges[first_word] = dict() 
        for second_word in self.graph:
            if first_word == second_word:
                continue
            self.edges[first_word][second_word] = 0

    # handle sinks
    for word in self.graph:
        if len(self.graph[word].outgoing) == 0:
            for connect_word in self.unique_words:
                self.graph[word].outgoing.append(self.graph[connect_word])

    # test numbers later with a specific example, for now just assuming that this works 
    for first_word in self.edges:
        for existing_word in self.graph[first_word].outgoing:
            print(type(existing_word))
            self.edges[first_word][existing_word] = 1/len(self.graph[first_word].outgoing)

    # for word in self.edges:
    #     print(word)

# def build_graph(self, window_size=4):
#     self.graph = dict()

#     # initialize all words
#     for word in self.unique_words:
#         self.graph[word] = Text.Node(word)

#     # set ingoing and outgoing words
#     self.windows = []

#     for i in range(len(self.unique_words)-window_size+1):
#         self.windows.append(self.unique_words[i:i+window_size])
    
#     # print(self.windows)

#     for window in self.windows:
#         for i in range(len(window)):
#             for j in range(len(window)):
#                 if i == j:
#                     continue
#                 # edge from first_word to second_word
#                 first_word, second_word = window[i], window[j]
#                 self.graph[first_word].outgoing.append(self.graph[second_word])
#                 self.graph[second_word].incoming.append(self.graph[first_word])
    
#     # ensuring only unique words are in self.graph
#     assert len(self.graph) == len(set(self.graph))

#     for word, current_node in self.graph.items():
#         # print(word, current_node)
#         current_node.outgoing = list(current_node.outgoing)
#         current_node.incoming = list(current_node.incoming)        
#     # print(self.graph)

def matrix_multiplication(a, b):            
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

x = [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [1, 0.5, 0, 0],
     [0, 0.5, 0, 0]]

y = [[1], [1], [1], [1]]

a = matrix_multiplication(x, y)
print(a)


def iterate(self, num_iter=100, d=0.85):
    self.d = d

    def eval(w):
        return (1-self.d)/self.N + w*self.d

    self.prev_cost, self.current_cost = dict(), dict()

    # assuming equal probability
    for word in self.graph:
        self.prev_cost[word] = 1/len(self.unique_words)
        self.current_cost[word] = 0

    for _ in range(num_iter):
        for word in self.graph:
            rank_sum = 0
            for connected_word in self.graph[word].incoming:
                rank_sum += eval(self.prev_cost[connected_word.word]/len(self.graph[connected_word.word].outgoing))
            self.current_cost[word] = rank_sum

        self.ranks = self.current_cost.copy()

        # update prev_cost and current_cost
        for word in self.graph:
            self.prev_cost[word] = self.current_cost[word] 
            self.current_cost[word] = 0

    # print(self.ranks)
    self.ranked_words = []
    values = set()
    for key in self.ranks:
        self.ranked_words.append([self.ranks[key], key])
        values.add(self.ranks[key])
        # print(key, self.ranks[key])
    self.ranked_words.sort(reverse=True)

    print(self.ranked_words)
    print(values)