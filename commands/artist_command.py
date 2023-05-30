from datetime import datetime
import requests
from sqlalchemy import Date
from models import SessionLocal, Artists
from last_fm.last_fm_sdk import LastFmSdk


def createBaseTopArtists(genre, url: str, api_key: str):
    print("starting")
    db = SessionLocal()
    last_fm_sdk = LastFmSdk(url, api_key)

    top_artists = last_fm_sdk.getTopArtistsForGenre(genre=genre, limit=1000)

    for artist in top_artists['topartists']['artist']:

        artist_name = artist['name']
        if "mbid" in artist:
            # Access the value associated with the 'mbid' key
            mbid = artist["mbid"]
        else:
            continue

        artist_new = db.query(Artists).filter(Artists.music_brainz_identifier == mbid).first()

        if artist_new is not None:
            continue


        artist_new = Artists()
        artist_new.name = artist['name']
        artist_new.music_brainz_identifier = mbid
        artist_new.description = ""

        db.add(artist_new)
        db.commit()
        print(f"Added new artist with name {artist_new.name} and id {artist_new.id}")
