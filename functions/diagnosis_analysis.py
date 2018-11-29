import json

def isPostDiagnosisPositive(post, positive_triggers):
    for trigger in positive_triggers:
        if 'selftext' in post and trigger in post['selftext'].lower():
            return (True, trigger)
        
        elif 'title' in post and trigger in post['title'].lower():
            return (True, trigger) 
    
    return (False, None)

def identifyDiagnosesPosts(posts):
    with open('files/diagnospatterns_positive.txt') as f:
        positive_triggers = [x[:len(x)-1] for x in f.readlines()]

        pos_diagnosis_posts = []
        for _, post in enumerate(posts['data']):   
            # print(i) if i % 10 == 0 else None
            pos_diagnos, _ = isPostDiagnosisPositive(post, positive_triggers)
            if pos_diagnos:
                pos_diagnosis_posts.append(post)

        return pos_diagnosis_posts

def main():
    depression_set = []
    while len(depression_set) < 100000:
        
        # get a new batch of posts and pull out those with positive diagnoses
        posts = data_collection.getPosts(subreddit='depression', limit=1000)
        pos_diagnos_posts = identifyDiagnosesPosts(posts)
        depression_set += pos_diagnos_posts
        print(len(depression_set))

        # update dataset file 
        with open('datasets/extended-100k/id-depression.json', 'w') as f:
            outset = {}
            outset['data'] = depression_set
            json.dump(outset, f)

    
    
    

if __name__ == '__main__':
    main()