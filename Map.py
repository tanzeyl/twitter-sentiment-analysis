import csv
import folium
import geopandas
import pandas as pd
from folium.plugins import FastMarkerCluster


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
            mood_location[item["location"]] = {"Positive": 0, "Negative": 0}
        mood_location[item["location"]][item["mood"]] += 1
    my_map = folium.Map()
    world = geopandas.read_file(geopandas.datasets.get_path("naturalearth_lowres"))
    country_names = []
    moods = []
    for country in mood_location:
        mood = mood_location[country]['Positive'] / (
                mood_location[country]['Positive'] + mood_location[country]['Negative'])
        moods.append(mood)
        country_names.append(country)

    data_to_plot = pd.DataFrame({'Country': country_names, 'Mood': moods})

    folium.Choropleth(
        geo_data=world,
        name='choropleth',
        data=data_to_plot,
        columns=['Country', 'Mood'],
        key_on='feature.properties.name',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Mood'
    ).add_to(my_map)
    cluster_data = []
    for row in mood_content:
        if row["latitude"] != "":
            cluster_data.append([float(row["latitude"]), float(row["longitude"])])
    FastMarkerCluster(cluster_data).add_to(my_map)

    folium.LayerControl().add_to(my_map)
    my_map.save(output_html)


if __name__ == "__main__":
    create_map("tweet_mood_java.csv", "mood_java.html")
    create_map("tweet_mood_python.csv", "mood_python.html")
