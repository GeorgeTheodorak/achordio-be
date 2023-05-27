import requests


class LastFmSdk:
    url = ""
    api_key = ""

    def __init__(self, url: str, api_key: str):
        self.url = url
        self.api_key = api_key

    def getTopArtistsForGenre(self, genre, limit=100) -> dict:
        params = {
            'method': 'tag.gettopartists',
            'api_key': self.api_key,
            'format': 'json',
            'limit': limit,
            'tag': genre
        }

        response = requests.get(self.url, params=params)
        data = response.json()
        return data

    def getArtist(self, artistName, artistISBN):
        pass
