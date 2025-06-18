from flask import Flask, jsonify
import requests
import csv

app = Flask(__name__)

RICK_AND_MORTY_API = "https://rickandmortyapi.com/api/character"
CSV_FILE = "output.csv"
cached_data = []

def fetch_characters():
    global cached_data
    characters = []
    next_url = RICK_AND_MORTY_API

    while next_url:
        response = requests.get(next_url)
        response.raise_for_status()
        data = response.json()

        for char in data['results']:
            if (
                char['species'].lower() == 'human'
                and char['status'].lower() == 'alive'
                and char['origin']['name'].lower() == 'earth'
            ):
                characters.append({
                    "name": char['name'],
                    "location": char['location']['name'],
                    "image": char['image']
                })

        next_url = data['info']['next']

    cached_data = characters
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Name", "Location", "Image"])
        writer.writeheader()
        for item in characters:
            writer.writerow({
                "Name": item['name'],
                "Location": item['location'],
                "Image": item['image']
            })

@app.route("/healthcheck")
def healthcheck():
    return jsonify({"status": "ok"}), 200

@app.route("/characters")
def characters():
    if not cached_data:
        fetch_characters()
    return jsonify(cached_data)

@app.route("/")
def index():
    return jsonify({"message": "Hello from Rick and Morty API!"})

if __name__ == '__main__':
    fetch_characters()
    app.run(host='0.0.0.0', port=5000)
