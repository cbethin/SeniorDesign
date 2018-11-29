def checkDatasetForUniqueness(dataset):
    totalRepeatCount = 0 # Number of posts present more than once in dataset 

    # Loop through dataset and find repeats of posts
    for post in dataset:
        identicalPosts = list(filter(lambda x: x['id'] == post['id'], dataset))
        if len(identicalPosts) > 1:
            totalRepeatCount += 1
    
    if totalRepeatCount != 0:
        print("Found " + str(totalRepeatCount) + " duplicates in dataset")
    else:
        print("No duplicates found.")
