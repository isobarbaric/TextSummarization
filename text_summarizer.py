
from utility import Matrix
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from ordered_set import OrderedSet

import string

class TextSummarizer:

    class Node:
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

    def __init__(self):
        pass

    def summarize(self, content, n=3):
        self.content = content

        # method calls
        self.__extract_words()
        self.__build_graph()
        self.__build_vector()
        self.__iterate()
        self.__score_sentences()

        summary = ''
        for i in range(min(n, len(self.scored_sentences)-1)):
            summary += self.scored_sentences[i][1] + ' '
        return summary[:-1]

    # lowercase, remove stop words, extract unique words
    def __extract_words(self):
        self.sentences = sent_tokenize(self.content)
        self.words = []

        for sentence in self.sentences:
            self.words.append([])
            for word in word_tokenize(sentence):
                revised = word.lower()
                if revised in stopwords.words('english') or revised in string.punctuation or revised in TextSummarizer.unwanted_snippets:
                    continue
                self.words[-1].append(revised)

        self.unique_words = OrderedSet()
        for sentence in self.words:
            for word in sentence:
                self.unique_words.add(word)
        self.unique_words = list(self.unique_words)
        self.N = len(self.unique_words)

    def __build_graph(self, window_size=4):
        self.graph = dict()

        # initialize all words
        for word in self.unique_words:
            self.graph[word] = TextSummarizer.Node(word)

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
            current_node.outgoing = list(current_node.outgoing)
            current_node.incoming = list(current_node.incoming)        

    def __build_vector(self):
        self.vector = [['N/A']]

        for word in self.graph:
            self.vector[0].append(word)

        for word in self.graph:
            current_row = [word]
            for _ in range(len(self.graph)):
                current_row.append(0)
            self.vector.append(current_row)

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

        self.matrix = []
        for row in self.vector:
            # skip the first row
            if type(row[1]) == str:
                continue
            self.matrix.append(row[1:])
        self.matrix = Matrix(self.matrix)

    def __iterate(self, num_iter=100, d=0.85):
        mul = []
        for i in range(len(self.unique_words)):
            mul.append([1])

        other = Matrix(mul) 
        for _ in range(num_iter):
            other = (1-d)/self.N + d * (self.matrix * other)

        self.weights = dict()
        for i in range(len(other.grid)):
            self.weights[self.unique_words[i]] = other.grid[i][0]
    
        self.weights = dict(sorted(self.weights.items(), key=lambda item: item[1]))
        # print(self.weights)

    def __score_sentences(self):
        self.scored_sentences = []        
        cnt = 0
        for parsed_sent in self.words:
            current_score = 0
            for word in parsed_sent:
                current_score += self.weights[word]
            self.scored_sentences.append([current_score, self.sentences[cnt]])
            cnt += 1
        self.scored_sentences.sort(reverse=True)
        print(self.scored_sentences)
