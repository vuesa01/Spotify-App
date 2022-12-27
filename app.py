from flask import Flask, request, render_template, jsonify
import requests
import sqlite3
import json
from crud import createSong_DB, createArtist_DB, createAlbum_DB

app = Flask(__name__)


def artistInfo(id):
    id = id.replace('spotify:artist:', '')
    url = "https://spotify23.p.rapidapi.com/artists/"
    querystring = {"ids":f"{id}"}
    headers = {
        "X-RapidAPI-Key": "c8d4bda2afmsh37be1110137e001p143d64jsn23dc2415e5dc",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    r = json.loads(response.text)
    name = (r['artists'][0]['name'])
    artistUrl = r['artists'][0]['external_urls']['spotify']
    followers = r['artists'][0]['followers']['total']
    genre_list = []
    for i in r['artists'][0]['genres']:
        genre_list.append(i)

    url2 = "https://spotify23.p.rapidapi.com/artist_overview/"
    querystring = {"id":f"{id}"}
    response2 = requests.request("GET", url2, headers=headers, params=querystring)
    responseStats = json.loads(response2.text)
    monthlyListeners = responseStats['data']['artist']['stats']['monthlyListeners']
    worldRank = responseStats['data']['artist']['stats']['worldRank']

    artistData = [name, artistUrl, followers, len(genre_list), monthlyListeners, worldRank]

    return artistData


def albumInfo(id):
    id = id.replace('spotify:album:', '')
    url = "https://spotify23.p.rapidapi.com/album_tracks/"
    querystring = {"id":f"{id}"}
    headers = {
        "X-RapidAPI-Key": "c8d4bda2afmsh37be1110137e001p143d64jsn23dc2415e5dc",
        "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    r = json.loads(response.text)
    all_songs = r['data']['album']['tracks']['totalCount']

    albumData = [all_songs]
    return albumData


@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        return render_template("base.html")


@app.route("/addSong", methods=['GET', 'POST'])
def addSongs():
    if request.method == "GET":
        return render_template("addSong.html")
    else:
        song = request.form.get('song')
        url = "https://spotify23.p.rapidapi.com/search/"
        querystring = {"q":f"{song}","type":"multi","offset":"0","limit":"10","numberOfTopResults":"5"}
        headers = {
            "X-RapidAPI-Key": "c8d4bda2afmsh37be1110137e001p143d64jsn23dc2415e5dc",
            "X-RapidAPI-Host": "spotify23.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        r = json.loads(response.text)
        try:
            name = r['tracks']['items'][0]['data']['name']
        except IndexError:
            error = "Could not find a song related to search"
            return render_template("addSong.html", error=error)

        artist = r['tracks']['items'][0]['data']['artists']['items'][0]['profile']['name']
        time = r['tracks']['items'][0]['data']['duration']['totalMilliseconds']
        album = r['tracks']['items'][0]['data']['albumOfTrack']['name']
        albumId = r['tracks']['items'][0]['data']['albumOfTrack']['uri']
        artistId = str(r['tracks']['items'][0]['data']['artists']['items'][0]['uri'])

        time = int(time/1000)
        minutes = int(time/60)
        seconds = time - (minutes * 60)
        duration = f"{minutes}:{seconds}"
        songData = [name, artist, album, duration]
        print(songData)
        # create song DB
        createSong_DB(songData, "song.sqlite3")

        artistInformation = artistInfo(artistId)
        print(artistInformation)
        # create artist DB
        createArtist_DB(artistInformation, "song.sqlite3")

        albumInformation = albumInfo(albumId)
        albumInformation.insert(0, artist)
        albumInformation.insert(0, album)
        print(albumInformation)
        # create album DB
        createAlbum_DB(albumInformation, "song.sqlite3")

        return render_template("addSong.html")


@app.route("/list")  # have not done yet
def showList():
    # Make three tables. Therefore return 3 things
    # Table 1 is the Song List
    # Table 2 is Artist information
    # Table 3 is Album information
    songList = []
    try:
        conn = sqlite3.connect("song.sqlite3")
        cursor = conn.cursor()
        query = "SELECT DISTINCT * FROM songs JOIN artist ON songs.artist = artist.name JOIN album ON album.artist = artist.name;"
        cursor.execute(query)
        for aSong in cursor:
            print(aSong)
            songList.append(aSong)
        return render_template("list.html", playlist=songList)
    except sqlite3.OperationalError:
        notify = 'Playlist currently empty'
        return render_template("list.html", msg=notify)
