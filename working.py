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

    #symspell checker
    ss = symspell.SymSpell(max_edit_distance=2)
    print("Loading SymSpell dataset...")
    words_dict = ss.load_datasets(["external/bad-words.csv", "external/english_words_479k.txt"])
    print("Dataset loaded")
    nlp = spacy.load('en_core_web_lg')

    # Load dataset
    filenames = ['datasets/extended-15k/'+x for x in os.listdir('datasets/extended-15k/pretty')] 
    print("Looking at files:", filenames)
    for file in filenames:
        print("Fixing file: ", file)
        dataset = data_collection.loadDatasetFromFile(file)
        fields = ['selftext', 'title']
        for i, post in enumerate(dataset):
            if i % 50 == 0:
                print(i)
            for field in fields:
                if field in post:
                    post_data = nlp_analysis.clean_text(post[field])
                    doc = nlp(post_data)
                    post_text_tokenized = [token.text for token in doc]
                    post[field] = "".join(ss.spell_corrector(post_text_tokenized, words_dict))
        data_collection.writeDatasetToFile(dataset, file.split("/")[2], 'datasets/extended-15k/spellcorrected')

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



if __name__ == "__main__":
    main()