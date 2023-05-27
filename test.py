import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import requests

# Set up client credentials
api_key = 'b71aef134e1632763a3f6e5e0e8e2211'
shared_secret = 'c23dbb413fa3b52829539498519c590a'

# Artist name or MBID (MusicBrainz ID)
artist = 'Adele'  # Replace with the artist name or MBID you want to search for

# Set the API endpoint URL
endpoint = "http://ws.audioscrobbler.com/2.0/"

method = "tag.gettopartists"
tag = "rock"
limit = 50

# Make the API request
params = {
    "method": method,
    "tag": tag,
    "limit": limit,
    "api_key": api_key,
    "format": "json"
}

print(endpoint)
exit()
response = requests.get(endpoint, params=params)
data = response.json()

# # Extract artist information from the response
# if "topartists" in data and "artist" in data["topartists"]:
#     artists = data["topartists"]["artist"]
#     for artist in artists:
#         artist_name = artist["name"]
#         print(artist_name)
# else:
#     print("Error occurred while fetching data.")
