import nltk, re

# PROCESSING 
def clean_text(text): 
    REPLACE_SPACE = re.compile("(\n)|(\*)")
    REPLACE_NO_SPACE = re.compile("(\')")

    text = REPLACE_SPACE.sub(" ", text)
    text = REPLACE_NO_SPACE.sub("", text)

    return text.encode("unicode_escape").replace(b'\\\\u', b'\\u').decode('unicode-escape')

## LANGUAGE STATISTICS
def get_total_pos_counts_for_posts(post_dataset, as_array=False):
    post_dict = {}
    
    for x in range(0, len(post_dataset)):
        if x % 500 == 0:
            print(x)
        if 'selftext' in post_dataset[x]:
            tok = nltk.word_tokenize(post_dataset[x]['selftext'])
            post_dict[post_dataset[x]['title']] = nltk.pos_tag(tok)

    # list all parts of speech, and count instances of each

    pos = post_dict.values()
    counts = dict()
    # poss = pos.split()

    for post in pos:
        for word_pos_pair in post:
            if word_pos_pair[1] in counts:
                counts[word_pos_pair[1]] += 1
            else:
                counts[word_pos_pair[1]] = 1
    
    return counts

def get_percent_pos_count_per_post(post_dataset):
    post_dict = {}

    for x in range(0, len(post_dataset)):
        pos_counts_for_this_post = {}
        total_word_count_for_this_post = 0

        if x % 500 == 0:
            print(x)
        if 'selftext' in post_dataset[x]:
            tokenized_words = nltk.word_tokenize(post_dataset[x]['selftext'])
            for word in tokenized_words:
                total_word_count_for_this_post += 1
                if word[1] in pos_counts_for_this_post:
                    pos_counts_for_this_post[word[1]] += 1
                else:
                    pos_counts_for_this_post[word[1]] = 1
            
            for pos in pos_counts_for_this_post:
                print(pos)

def get_word_counts_for_post(post):
    counts_for_word = {}

    fieldsToSearchThrough = ['selftext', 'title']

    for field in fieldsToSearchThrough:
        if field in post:
            fieldData = clean_text(post[field])
            words = nltk.word_tokenize(fieldData)
            for word in words:
                word = word.lower()
                if word in counts_for_word:
                    counts_for_word[word] += 1
                else:
                    counts_for_word[word] = 1
    
    return counts_for_word

## 

def main():
    # with open('datasets/extended-15k/Anxiety_text_samples_extended.json') as f:
    #     data = json.load(f)
    #     posts = data['data']
    #     get_percent_pos_count_per_post(posts)

    text = "Something I can\u2019t try here.\n\nIt's bad luck."
    print(clean_text(text))

if __name__ == "__main__":
    main()
            
                