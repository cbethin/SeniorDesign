import os, nltk, spacy 
from spacy import displacy
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from functions import data_collection, data_validation, diagnosis_analysis, nlp_analysis, graphs, stats
from external import symspell
import time


def main():
    # depression_dataset = data_collection.loadDatasetFromFile("datasets/extended-15k/depression_text_samples_extended.json")
    # print(depression_dataset[2]['selftext'], "\n---------")
    # post = nlp_analysis.clean_text(depression_dataset[2]['selftext'])
    nlp = spacy.load('en_core_web_lg')

    # Load dataset

    # # Seperate into words
    # words = nltk.word_tokenize(post)
    # print("------\nWords\n", words)

    # # Remove stop words
    # words_cleaned = [word for word in words if word not in stopwords.words('english')]
    # print("------\nNo Stop Words\n", words_cleaned)

    # # Lemmatize words in post
    # lemmatizer = WordNetLemmatizer()
    # lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    # print("-------\nLemmatized\n", lemmatized_words)


    # # Noun Chunking
    # # Tokenize and pos tag the sentence sentence 
    # sentence = "The quick brown fox jumped over the lazy dog."
    # sentence_processed = nltk.pos_tag(nltk.word_tokenize(sentence))
    # grammar = "NP: {<DT>?<JJ>*<NN><NN>+}"
    # cp = nltk.RegexpParser(grammar)
    # noun_chunked = cp.parse(sentence_processed)
    # print("-------\nNoun Chunking\n", noun_chunked)

    # spacy 
    post = "I like apples"
    doc = nlp(post)
    print(doc[0], doc[0].is_punct)

if __name__ == "__main__":
    main()