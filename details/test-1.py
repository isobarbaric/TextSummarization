
import nltk
from nltk.corpus import stopwords

words = []
{}
# convert paragraphs to sentences and also tokenize them 
def convert_para_to_sentences(text: str):
    return text.lower().replace('.', '').split(' ')

# remove all stop words from a tokenized list of words in a a paragraph
def remove_stop_words(tokenized_text: list):
    # removes all stop words
    words_to_remove = stopwords.words('english')
    for word in words_to_remove:
        while word in tokenized_text:
            tokenized_text.remove(word)
    # todo: have to remove all numbers as well and other worthless alphanumberic characters as well
    return tokenized_text 

def calculate_weighted_frequency(tokenized_test: list):
    freq = nltk.FreqDist(tokenized_test)
    # todo: want to use a dictionary to store the frequency of each word and do it by myself rather than a library
    print(freq.most_common(50))
    return freq

# testing
# calculate_weighted_frequency(remove_stop_words(convert_para_to_sentences("Peter and Elizabeth took a taxi to attend the night party in the city. While in the party, Elizabeth collapsed and was rushed to the hospital. Since she was diagnosed with a brain injury, the doctor told Peter to stay besides her until she gets well. Therefore, Peter stayed with her at the hospital for 3 days without leaving")))