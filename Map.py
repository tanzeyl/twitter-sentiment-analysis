import csv


def load_csv(csv_file):
    content = []
    with open(csv_file) as f:
        reader = csv.DictReader(f)
        for row in reader:
            content.append(row)
    return content


def create_map(csv_file, output_html):
    mood_content = load_csv(csv_file)
    mood_location = {}
    for item in mood_content:
        if item["location"] not in mood_location:
            mood_location[item["location"]] = {"Positive" : 0, "Negative" : 0}
        mood_location[item["location"]][item["mood"]] += 1
    for item in mood_location:
        print(item)


if __name__ == "__main__":
    create_map("2.1 tweet_mood_java.csv", None)
