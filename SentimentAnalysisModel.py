from nltk.corpus import twitter_samples, stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag


def clean_data(token):
    return [item for item in token if not item.startswith("@") and not item.startswith("https")]


def to_lower(token):
    return [item.lower() for item in token]


def lemmatize(token):
    lemmatizer = WordNetLemmatizer()
    result = []
    for item, tag in pos_tag(token):
        if tag[0].lower() in "nva":
            result.append(lemmatizer.lemmatize(item, tag[0].lower()))
        else:
            result.append(lemmatizer.lemmatize(item))
    return result


def remove_stopwords(token, stops):
    return [item for item in token if item not in stops]


def main():
    positive_tweets = twitter_samples.tokenized("positive_tweets.json")
    negative_tweets = twitter_samples.tokenized("negative_tweets.json")
    print(positive_tweets[0])
    print(negative_tweets[0])

    stops = stopwords.words("english")
    positive_tweets = [remove_stopwords(lemmatize(clean_data(to_lower(item))), stops) for item in positive_tweets]
    negative_tweets = [remove_stopwords(lemmatize(clean_data(to_lower(item))), stops) for item in negative_tweets]
    print(positive_tweets[0])
    print(negative_tweets[0])


if __name__ == "__main__":
    main()
