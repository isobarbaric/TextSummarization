from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import string

from test_rank import TextRank

class Text:

    unwanted_snippets = ["'s"]

    def __init__(self, content):
        self.content = content
        
        # method calls
        self.extract_words()
        self.score_sentences()

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

        self.unique_words = set()
        for sentence in self.words:
            for word in sentence:
                self.unique_words.add(word)

        print(a.unique_words)

    def score_sentences(self):
        ranker = TextRank(self.unique_words)
        ranker.tabulate()
        self.weights = ranker.scores
        
        self.scored_sentences = []        
        for sentence in self.sentences:
            current_score = 0
            for word in sentence:
                if word in self.weights:
                    current_score += self.weights[word]
            self.score_sentences.append([current_score, sentence])

        self.scored_sentences.sort(reverse=True)

    def summarize(self, n=3):
        summary = ''
        for i in range(min(n, len(self.score_sentences)-1)):
            summary += self.scored_sentences[i][1]
        return summary

a = Text("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")

# summary = a.summarize()