import operator
from functions import data_collection, nlp_analysis

def get_word_counts_for_file(filename):
    dataset = data_collection.loadDatasetFromFile(filename)
    
    counts_for_word = {}
    for i, post in enumerate(dataset):
        print(i) if i % 500 == 0 else None
        post_wordcounts = nlp_analysis.get_word_counts_for_post(post)
        for word in post_wordcounts:
            if word in counts_for_word:
                counts_for_word[word] += post_wordcounts[word]
            else:
                counts_for_word[word] = post_wordcounts[word]
    
    return dict(reversed(sorted(counts_for_word.items(), key=operator.itemgetter(1))))