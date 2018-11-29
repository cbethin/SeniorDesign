import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from functions import data_collection, data_validation, diagnosis_analysis, nlp_analysis, graphs, stats

def main():
    depression_dataset = data_collection.loadDatasetFromFile("datasets/extended-15k/depression_text_samples_extended.json")
    print(depression_dataset[0]['selftext'])
    post = nlp_analysis.clean_text(depression_dataset[0]['selftext'])

    # Seperate into words
    words = nltk.word_tokenize(post)
    print("------\nWords\n", words)

    # Remove stop words
    words_cleaned = [word for word in words if word not in stopwords.words('english')]
    print("------\nNo Stop Words\n", words_cleaned)

    # Lemmatize words in post
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
    print("-------\nLemmatized\n", lemmatized_words)

    # Dependency Parse Sentence
    

if __name__ == "__main__":
    main()