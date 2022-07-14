
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import string

from ordered_set import OrderedSet

from matrix import Matrix

class Text:

    class Node:    
        # initialize all words first, then add reference wherever necessary
        def __init__(self, word):
            self.word = word
            self.incoming = OrderedSet()
            self.outgoing = OrderedSet()

        def __repr__(self):
            info = 'incoming:{'
            for current_node in self.incoming:
                info += current_node.word + ', '
            info = info[:-2]
            info += '} outgoing:{' 
            for current_node in self.outgoing:
                info += current_node.word + ', ' 
            info = info[:-2]
            info += '}\n'
            return info

    unwanted_snippets = ["'s"]

    def __init__(self, content):
        self.content = content
        
        # method calls
        self.extract_words()
        self.build_graph()
        self.build_vector()
        self.iterate()

        # self.build_vector()
        # self.score_sentences()

    # lowercase, remove stop words, extract unique words
    def extract_words(self):
        self.sentences = sent_tokenize(self.content)
        self.words = []

        for sentence in self.sentences:
            self.words.append([])
            for word in word_tokenize(sentence):
                revised = word.lower()
                if revised in stopwords.words('english') or revised in string.punctuation or revised in Text.unwanted_snippets:
                    continue
                self.words[-1].append(revised)

        self.unique_words = OrderedSet()
        for sentence in self.words:
            for word in sentence:
                self.unique_words.add(word)
        self.unique_words = list(self.unique_words)
        self.N = len(self.unique_words)

    def build_graph(self, window_size=4):
        self.graph = dict()

        # initialize all words
        for word in self.unique_words:
            self.graph[word] = Text.Node(word)

        # set ingoing and outgoing words
        self.windows = []

        for i in range(len(self.unique_words)-window_size+1):
            self.windows.append(self.unique_words[i:i+window_size])
        
        # print(self.windows)

        for window in self.windows:
            for i in range(len(window)):
                for j in range(len(window)):
                    if i == j:
                        continue
                    # edge from first_word to second_word
                    first_word, second_word = window[i], window[j]
                    self.graph[first_word].outgoing.add(self.graph[second_word])
                    self.graph[second_word].incoming.add(self.graph[first_word])
        
        # ensuring only unique words are in self.graph
        assert len(self.graph) == len(set(self.graph))

        for word, current_node in self.graph.items():
            # print(word, current_node)
            current_node.outgoing = list(current_node.outgoing)
            current_node.incoming = list(current_node.incoming)        
        # print(self.graph)

    def build_vector(self):
        self.vector = [['N/A']]

        for word in self.graph:
            self.vector[0].append(word)

        for word in self.graph:
            current_row = [word]
            for _ in range(len(self.graph)):
                current_row.append(0)
            self.vector.append(current_row)

        # column of word in graph is = self.unique_words.find(word) + 1

        for i in range(len(self.unique_words)):
            vector_col = i+1
            adjacency_list = self.graph[self.unique_words[i]].outgoing
            for connected_node in adjacency_list:
                assert connected_node.word != self.unique_words[i]

                vector_row = -1
                # locating index (speed up using dictionary?)
                for j in range(len(self.unique_words)):
                    if self.unique_words[j] == connected_node.word:
                        vector_row = j+1
                        break

                self.vector[vector_row][vector_col] = 1/len(adjacency_list)    

        # reduction to matrix
        self.matrix = []
        for row in self.vector:
            # skip the first row
            if type(row[1]) == str:
                continue
            self.matrix.append(row[1:])
        self.matrix = Matrix(self.matrix)
        # print(self.matrix)

    def iterate(self, num_iter=100, d=0.85):
        self.d = d

        def eval(w):
            return (1-self.d)/self.N + w*self.d

        mul = []
        for i in range(len(self.unique_words)):
            mul.append([1])

        other = Matrix(mul) 

        for _ in range(10):
            other = (1-self.d)/self.N + self.d * (self.matrix * other)
            print(_)
            print(other)
            print()
        
        # print(other)

    #  def score_sentences(self):
    #     ranker = TextRank(self.unique_words)
    #     ranker.tabulate()
    #     self.weights = ranker.scores
    #     self.scored_sentences = []        
    #     for sentence in self.sentences:
    #         current_score = 0
    #         for word in sentence:
    #             if word in self.weights:
    #                 current_score += self.weights[word]
    #         self.score_sentences.append([current_score, sentence])
    #     self.scored_sentences.sort(reverse=True)

    def summarize(self, n=3):
        summary = ''
        for i in range(min(n, len(self.score_sentences)-1)):
            summary += self.scored_sentences[i][1]
        return summary

a = Text("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")

# print(a.vector)
# summary = a.summarize()