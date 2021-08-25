from nltk.corpus import twitter_samples, stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk import NaiveBayesClassifier
from nltk import classify
import random
import pickle


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


def transform_features(token):
    feature_set = {}
    for feature in token:
        if feature not in feature_set:
            feature_set[feature] = 0
        feature_set[feature] += 1
    return feature_set


def main():
    positive_tweets = twitter_samples.tokenized("positive_tweets.json")
    negative_tweets = twitter_samples.tokenized("negative_tweets.json")
    stops = stopwords.words("english")
    positive_tweets = [remove_stopwords(lemmatize(clean_data(to_lower(item))), stops) for item in positive_tweets]
    negative_tweets = [remove_stopwords(lemmatize(clean_data(to_lower(item))), stops) for item in negative_tweets]
    positive_tweets = [(transform_features(token), "Positive") for token in positive_tweets]
    negative_tweets = [(transform_features(token), "Negative") for token in negative_tweets]
    dataset = positive_tweets + negative_tweets
    random.shuffle(dataset)
    training_data = dataset[:7001]
    test_data = dataset[7001:]
    model = NaiveBayesClassifier.train(training_data)
    print("Accuracy is: ", classify.accuracy(model, test_data))
    print(model.show_most_informative_features(10))

    with open("model.pickle", "wb") as f:
        pickle.dump(model, f)


if __name__ == "__main__":
    main()
