import json
import requests

subreddit_utc_times = {}

def getPosts(subreddit="depression", limit=1000, utcTime=None):
    url = "https://api.pushshift.io/reddit/submission/search?subreddit="+str(subreddit)+"&limit="+str(limit)
    if subreddit in subreddit_utc_times:
        utcTime = subreddit_utc_times[subreddit]
    
    if utcTime != None:
        url += "&before="+str(utcTime)

    # Request URL
    response = requests.get(url)
    
    #update last received utc time for this dataset
    posts = response.json()
    if 'data' in posts and len(posts['data']) > 0 and 'created_utc' in posts['data'][len(posts['data'])-1]:
            subreddit_utc_times[subreddit] = posts['data'][len(posts['data'])-1]['created_utc']

    return posts['data']

def getPostsForUser(user="cbethin", limit=1000):
    url = "https://api.pushshift.io/reddit/submission/search?author="+str(user)+"&limit="+str(limit)
    response = requests.get(url).json()
    return response['data']

def getDatasetForSubreddit(subreddit="depression", n_batches=1):
    lastTimeRecieved = None # UTC time of last received post
    dataset_complete = [] # Whole dataset

    # Get n_batches of data. Make sure the posts are only those received before t
    # the time of the last received post as to assure all posts are unique
    print("Getting data for subreddit " + subreddit)
    for i in range(n_batches):
        print(i)
        data = getPosts(subreddit, 1000, lastTimeRecieved)

        # Add posts in this batch to dataset
        for post in data:
            dataset_complete.append(post)
            lastTimeRecieved = post["created_utc"]
            subreddit_utc_times[subreddit] = lastTimeRecieved
        
    return dataset_complete

def getDatasetForUser(user="cbethin", n_batches=1):
    lastTimeRecieved = None # UTC time of last received post
    dataset_complete = [] # Whole dataset

    # Get n_batches of data. Make sure the posts are only those received before t
    # the time of the last received post as to assure all posts are unique
    print("Getting data for user: " + user)
    for _ in range(n_batches):
        data = getPostsForUser(user=user)

        # Add posts in this batch to dataset
        for post in data:
            dataset_complete.append(post)
            lastTimeRecieved = post["created_utc"]
            subreddit_utc_times[user] = lastTimeRecieved
        
    return dataset_complete

def writeDatasetToFile(dataset, filename='', folder="'datasets"):
    with open(folder+'/'+filename, 'w') as outfile:
        dataset_out = {}
        dataset_out['data'] = dataset
        json.dump(dataset_out, outfile)

def loadDatasetFromFile(filename):
    with open(filename) as f:
        return json.load(f)['data']

def main():

    ## GETTING DATA FOR SUBREDDITS
    # subreddits = ['depression', 'Anxiety', 'foreveralone', 'socialanxiety', 'SuicideWatch', 
    #                 'berkeley', 'PowerLedger', 'TalesFromYourServer', 'tifu']
    # subreddits = ['socialanxiety']

    # for subreddit in subreddits:
    #     dataset_complete = getDatasetForSubreddit(subreddit=subreddit, n_batches=100)
    #     writeDatasetToFile(dataset_complete, filename=subreddit+'_text_samples_extended.json', folder='datasets/extended-100k')

    ## GETTING DATA FOR DEPRESSED USERS
    with open('datasets/extended-15k/id-depression.json') as f:
        data = json.load(f)
        posts = data['data']

        totalCount = 0

        for post in posts:
            if 'author' in post:
                postsForUser = getDatasetForUser(user=post['author'])
                totalCount += len(postsForUser)
                print(totalCount)
                writeDatasetToFile(postsForUser, filename=post['author']+'_depressed_samples.json', folder='datasets/extended-15k/depressed-users')

                if totalCount >= 15000:
                    return

if __name__ == "__main__":
    main()