from sklearn.manifold import MDS
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import json, nltk, numpy, os, sys

from functions import nlp_analysis as nlp
from functions import stats

def get_pos_counts_for_file(filename):
    with open(filename) as f:
        try:
            data = json.load(f)
            print("Loading data for " + filename)
            return nlp.get_total_pos_counts_for_posts(data['data'])
        except Exception as ex:
            print("Could not load file:", filename)
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

def get_pos_counts_for_subreddit(subreddit="depression"):
    with open('datasets/'+subreddit+'_text_samples_extended.json') as f:
        data = json.load(f)

    print("Loading data for subreddit " + subreddit)
    return nlp.get_total_pos_counts_for_posts(data['data'])

def main():

    # Get pos counts for each subreddit
    subreddits = ['depression', 'Anxiety', 'foreveralone', 'socialanxiety', 'SuicideWatch', 
                    'berkeley', 'PowerLedger', 'TalesFromYourServer', 'tifu']

    ## LIST FILES TO BE SEARCHED THROUGH FOR MDS
    # depressed_user_filenames = ['depressed-users/'+x for x in os.listdir('datasets/extended-15k/depressed-users')] 
    depressed_user_filenames = []
    other_filenames = ['id-depression.json'] + [x+'_text_samples_extended.json' for x in subreddits]
    filenames = other_filenames + depressed_user_filenames

    totalCounts = []

    # GET POS COUNT FOR THE DATA IN EACH FILE
    workingFilenames = []
    for filename in filenames:
        counts = get_pos_counts_for_file('datasets/extended-15k/'+filename)
        
        # convert dictionary to array of just counts
        countsArray = []
        for pos in counts:
            countsArray.append(counts[pos])

        # normalize 
        if countsArray != [] and max(countsArray) - min(countsArray) != 0:
            countsArrayNormalized = [x for x in countsArray] # stats.normalize(countsArray)
            totalCounts.append(countsArrayNormalized)
            workingFilenames.append(filename)


    print("Total:", totalCounts)
    # Assure each subreddit is an array of the same size
    vec = []
    longest_row_len = max(len(row) for row in totalCounts)

    ## COMBINE THE NORMALIZED POS COUNTS IN ONE VECTOR
    for row in totalCounts:
        row = np.append(np.array(row), np.zeros(longest_row_len-len(row)))
        vec = np.append(vec, row)

    # Reshape array to be 2D array
    print(vec.shape)
    vec = np.reshape(vec, (len(workingFilenames), int(vec.shape[0]/len(workingFilenames))))

    # BEGIN MDS PLOTTING   
    embedding = MDS(n_components=2)
    X_transformed = embedding.fit_transform(vec)
    X_transformed.shape

    _, ax = plt.subplots()
    ax.scatter(vec[:, 0], vec[:, 1])
    for i, subreddit in enumerate(other_filenames):
        ax.annotate(subreddit.split('_')[0], (vec[i][0], vec[i][1]))

    plt.show()


if __name__ == '__main__':

        main()
