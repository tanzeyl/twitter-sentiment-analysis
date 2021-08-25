import json
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tag import pos_tag
from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim


class MoodClassifier:
    def __init__(self, classifier_file='model.pickle'):
        f = open(classifier_file, 'rb')
        self.classifier = pickle.load(f)
        f.close()
        self.stop_words = stopwords.words('english')

    def clean_data(self, token):
        return [item for item in token if not item.startswith('@') and not item.startswith('http')]

    def to_lower(self, token):
        return [item.lower() for item in token]

    def lemmatize(self, token):
        lemmatizer = WordNetLemmatizer()

        result = []
        for item, tag in pos_tag(token):
            if tag[0].lower() in "nva":
                result.append(lemmatizer.lemmatize(item, tag[0].lower()))
            else:
                result.append((lemmatizer.lemmatize(item)))

        return result

    def remove_stop_words(self, token):
        return [item for item in token if item not in self.stop_words]

    def transform_features(self, token):
        feature_set = {}
        for feature in token:
            if feature not in feature_set:
                feature_set[feature] = 0
            feature_set[feature] += 1
        return feature_set

    def get_mood(self, token):
        custom_tokens = self.remove_stop_words(self.lemmatize(self.clean_data(self.to_lower(word_tokenize(token)))))
        category = self.classifier.classify(self.transform_features(custom_tokens))
        return category


class Locator:
    def __init__(self):
        self.geo_locator = Nominatim(user_agent="LearnPython")
        self.location_store = {}
        self.lookups = 0

    def get_location(self, location_name):
        if location_name in self.location_store:
            return self.location_store[location_name]
        try:
            self.lookups += 1
            location = self.geo_locator.geocode(location_name, language = "en")
            self.location_store[location_name] = location
        except GeocoderTimedOut:
            location = None
        return location


def process(input_file, output_file):
    tweets = None
    with open(input_file) as f:
        tweets = json.load(f)

    print("Number of tweets", len(tweets))

    classifier = MoodClassifier()
    locator = Locator()
    cnt = 0
    csv_data = []
    for tweet in tweets:
        csv_data_item = {"mood" : None, "location" : None, "latitude" : None, "longitude" : None}
        if "retweeted_status" in tweet:
            tweet = tweet["retweeted_status"]
        csv_data_item["mood"] = classifier.get_mood(tweet["full_text"])
        if "location" in tweet["user"]:
            location = locator.get_location(tweet["user"]["location"])
            if location:
                csv_data_item["location"] = str(location.address).split(", ")[-1]
                csv_data_item["latitude"] = location.latitude
                csv_data_item["longitude"] = location.longitude
        csv_data.append(csv_data_item)
        cnt += 1
        if cnt > 10:
            break
    print(csv_data)
    # The percentage of positive mood is 0.5525186647215309. (Python)


if __name__ == "__main__":
    input_file = "tweets_with_java.json"
    process(input_file, None)
