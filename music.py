from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Create a SQLite database and a 'songs' table
conn = sqlite3.connect('songs.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY,
        artist TEXT,
        genre TEXT,
        title TEXT
    )
''')

# Insert 10 songs into the 'songs' table
songs_data = [
    ("Queen", "Rock", "Bohemian Rhapsody"),
    ("Michael Jackson", "Pop", "Thriller"),
    ("Bob Marley", "Reggae", "No Woman, No Cry"),
    ("The Beatles", "Rock", "Hey Jude"),
    ("Beyoncé", "R&B", "Single Ladies"),
    ("Elvis Presley", "Rock and Roll", "Jailhouse Rock"),
    ("David Bowie", "Rock", "Space Oddity"),
    ("Prince", "Funk", "Purple Rain"),
    ("Johnny Cash", "Country", "Ring of Fire"),
    ("Miles Davis", "Jazz", "So What"),
]

cursor.executemany('''
    INSERT INTO songs (artist, genre, title)
    VALUES (?, ?, ?)
''', songs_data)

conn.commit()
conn.close()

@app.route('/', methods=['GET'])
def index():
    conn = sqlite3.connect('songs.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM songs')
    songs_data = cursor.fetchall()
    songs_list = [{
        'id': song[0],
        'artist': song[1],
        'genre': song[2],
        'title': song[3],
    } for song in songs_data]

    conn.close()
    return render_template('index2.html', songs=songs_list)

@app.route('/songs', methods=['GET', 'POST'])
def get_or_add_songs():
    conn = sqlite3.connect('songs.db')
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM songs')
        songs_data = cursor.fetchall()
        songs_list = []
        for song in songs_data:
            songs_list.append({
                'id': song[0],
                'artist': song[1],
                'genre': song[2],
                'title': song[3],
            })
        conn.close()
        return jsonify(songs_list)

    elif request.method == 'POST':
        new_artist = request.form['artist']
        new_genre = request.form['genre']
        new_title = request.form['title']

        cursor.execute('''
            INSERT INTO songs (artist, genre, title)
            VALUES (?, ?, ?)
        ''', (new_artist, new_genre, new_title))

        conn.commit()
        conn.close()

        return 'Song added successfully', 201

@app.route('/songs/<int:song_id>', methods=['GET', 'PUT', 'DELETE'])
def get_update_delete_song(song_id):
    conn = sqlite3.connect('songs.db')
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM songs WHERE id = ?', (song_id,))
        song = cursor.fetchone()
        if song:
            song_data = {
                'id': song[0],
                'artist': song[1],
                'genre': song[2],
                'title': song[3],
            }
            conn.close()
            return jsonify(song_data)
        else:
            conn.close()
            return 'Song not found', 404

    elif request.method == 'PUT':
        cursor.execute('SELECT * FROM songs WHERE id = ?', (song_id,))
        existing_song = cursor.fetchone()

        if existing_song:
            updated_artist = request.form.get('artist', existing_song[1])
            updated_genre = request.form.get('genre', existing_song[2])
            updated_title = request.form.get('title', existing_song[3])

            cursor.execute('''
                UPDATE songs
                SET artist=?, genre=?, title=?
                WHERE id=?
            ''', (updated_artist, updated_genre, updated_title, song_id))

            conn.commit()
            conn.close()
            return 'Song updated successfully'
        else:
            conn.close()
            return 'Song not found', 404

    elif request.method == 'DELETE':
        cursor.execute('SELECT * FROM songs WHERE id = ?', (song_id,))
        song = cursor.fetchone()

        if song:
            cursor.execute('DELETE FROM songs WHERE id = ?', (song_id,))
            conn.commit()
            conn.close()
            return 'Song deleted successfully'
        else:
            conn.close()
            return 'Song not found', 404
        

        

if __name__ == '__main__':
    app.run(debug=True)