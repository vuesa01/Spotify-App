#!/usr/bin/env python3

import sqlite3


# Will Need To Fix These
def createSong_DB(data: list, filename_dst: str) -> None:
    conn = sqlite3.connect(filename_dst)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS songs (name, artist, album, duration);")
    cursor.execute(f"INSERT INTO songs (name, artist, album, duration) VALUES ('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}')")
    conn.commit()
    conn.close()


def createArtist_DB(data: list, filename_dst: str) -> None:
    conn = sqlite3.connect(filename_dst)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS artist (name, url, followers, genres, monthlyListeners, rank);")
    cursor.execute(f"INSERT INTO artist (name, url, followers, genres, monthlyListeners, rank) VALUES ('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}', '{data[5]}')")
    conn.commit()
    conn.close()


def createAlbum_DB(data: list, filename_dst: str) -> None:
    conn = sqlite3.connect(filename_dst)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS album (album, artist, numberOfSongs);")
    cursor.execute(f"INSERT INTO album (album, artist, numberOfSongs) VALUES ('{data[0]}', '{data[1]}', '{data[2]}')")
    # cursor.executemany("INSERT INTO game VALUES(?, ?, ?, ?);", all_games)
    conn.commit()
    conn.close()
