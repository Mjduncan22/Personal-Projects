from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth, firestore

from playlist_manager import PlaylistManager

app = Flask(__name__)
CORS(app)  # enable CORS for all routes

# Initialize Firebase Admin
cred = credentials.Certificate(
    r'C:\School\Spring_2025\CSE 310\Personal-Projects\Music Database\serviceAccount.json'
)
firebase_admin.initialize_app(cred)
db = firestore.client()
pm = PlaylistManager(db)


# Helper: Verify Firebase ID Token
def get_user_from_token():
    data = request.get_json(silent=True) or {}
    token = data.get('idToken')
    if not token:
        return None, "Missing ID token"
    try:
        decoded = auth.verify_id_token(token)
        return decoded['uid'], None
    except Exception as e:
        return None, str(e)


# 1. Verify Token
@app.route('/api/verify-token', methods=['POST', 'OPTIONS'])
def verify_token():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json() or {}
    token = data.get('idToken')
    if not token:
        return jsonify({'error': 'Missing ID token'}), 400
    try:
        decoded = auth.verify_id_token(token)
        return jsonify({'message': 'Token valid', 'uid': decoded['uid']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401


# 2. Create a new playlist
@app.route('/api/playlists', methods=['POST', 'OPTIONS'])
def create_playlist():
    if request.method == 'OPTIONS':
        return '', 200
    uid, err = get_user_from_token()
    if err:
        return jsonify({'error': err}), 401
    data = request.get_json() or {}
    name = data.get('name')
    desc = data.get('description', '')
    if not name:
        return jsonify({'error': 'Missing playlist name'}), 400
    pid = pm.create_playlist(name, uid, desc)
    return jsonify({'playlist_id': pid}), 201

# 3. Add new song (not assigned to a playlist yet)
@app.route('/api/songs', methods=['POST', 'OPTIONS'])
def create_song():
    if request.method == 'OPTIONS':
        return '', 200
    uid, err = get_user_from_token()
    if err:
        return jsonify({'error': err}), 401

    data = request.get_json() or {}
    title = data.get('title')
    artist = data.get('artist')
    duration = data.get('duration')
    album = data.get('album', '')
    cover = data.get('album_cover_url', '')

    if not (title and artist and duration):
        return jsonify({'error': 'Missing title, artist, or duration'}), 400

    song_id = pm.add_song(None, title, artist, duration, album, cover, user_id=uid) 
    return jsonify({'song_id': song_id}), 201

# 4. Get playlist details
@app.route('/api/playlists/<playlist_id>', methods=['GET', 'OPTIONS'])
def get_playlist(playlist_id):
    if request.method == 'OPTIONS':
        return '', 200
    pl = pm.get_playlist(playlist_id)
    if not pl:
        return jsonify({'error': 'Playlist not found'}), 404
    return jsonify(pl), 200


# 5. Add new song to a playlist
@app.route('/api/playlists/<playlist_id>/songs', methods=['POST', 'OPTIONS'])
def add_song(playlist_id):
    if request.method == 'OPTIONS':
        return '', 200
    uid, err = get_user_from_token()
    if err:
        return jsonify({'error': err}), 401
    data = request.get_json() or {}
    title = data.get('title')
    artist = data.get('artist')
    duration = data.get('duration')
    album = data.get('album', '')
    cover = data.get('album_cover_url', '')
    if not (title and artist and duration):
        return jsonify({'error': 'Missing title, artist, or duration'}), 400
    sid = pm.add_song(playlist_id, title, artist, duration, album, cover, user_id=uid)
    return jsonify({'song_id': sid}), 201


# 6. List songs in a playlist
@app.route('/api/playlists/<playlist_id>/songs', methods=['GET', 'OPTIONS'])
def get_songs(playlist_id):
    if request.method == 'OPTIONS':
        return '', 200
    songs = pm.get_songs_for_playlist(playlist_id)
    return jsonify(songs), 200


# 7. List all songs for current user
@app.route('/api/songs', methods=['GET', 'OPTIONS'])
def list_songs():
    if request.method == 'OPTIONS':
        return '', 200
    authh = request.headers.get('Authorization', '')
    token = authh.split(' ')[1] if ' ' in authh else authh
    try:
        uid = auth.verify_id_token(token)['uid']
    except Exception as e:
        return jsonify({'error': str(e)}), 401
    songs = pm.get_songs_for_user(uid)
    return jsonify(songs), 200


# 8. Assign existing song to a playlist
@app.route('/api/songs/<song_id>/playlist', methods=['PUT', 'OPTIONS'])
def move_song(song_id):
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json() or {}
    new_pid = data.get('playlist_id')
    if not new_pid:
        return jsonify({'error': 'Missing playlist_id'}), 400
    ok = pm.move_song_to_playlist(song_id, new_pid)
    if not ok:
        return jsonify({'error': 'Song or playlist not found'}), 404
    return jsonify({'message': 'Song moved'}), 200


# 9. Permanently delete a song
@app.route('/api/songs/<song_id>', methods=['DELETE', 'OPTIONS'])
def delete_song(song_id):
    if request.method == 'OPTIONS':
        return '', 200
    pm.delete_song(song_id)
    return jsonify({'message': 'Song deleted'}), 200


# 10. Permanently delete a playlist (and its songs)
@app.route('/api/playlists/<playlist_id>', methods=['DELETE', 'OPTIONS'])
def delete_playlist(playlist_id):
    if request.method == 'OPTIONS':
        return '', 200
    pm.delete_playlist(playlist_id)
    return jsonify({'message': 'Playlist deleted'}), 200


# 11. Export a playlist
@app.route('/api/playlists/<playlist_id>/export', methods=['GET', 'OPTIONS'])
def export_playlist(playlist_id):
    if request.method == 'OPTIONS':
        return '', 200
    data = pm.export_playlist(playlist_id)
    if not data:
        return jsonify({'error': 'Playlist not found'}), 404
    return jsonify(data), 200


# 12. Import a playlist
@app.route('/api/playlists/import', methods=['POST', 'OPTIONS'])
def import_playlist():
    if request.method == 'OPTIONS':
        return '', 200
    uid, err = get_user_from_token()
    if err:
        return jsonify({'error': err}), 401
    data = request.get_json() or {}
    export = data.get('playlist')
    if not export:
        return jsonify({'error': 'Missing playlist export'}), 400
    new_id = pm.import_playlist(uid, export)
    return jsonify({'imported_playlist_id': new_id}), 201


# 13. Explore public playlists
@app.route('/api/explore', methods=['GET', 'OPTIONS'])
def explore_playlists():
    if request.method == 'OPTIONS':
        return '', 200
    pls = pm.get_all_playlists_public()
    return jsonify(pls), 200

# 14. List all playlists for current user
@app.route('/api/playlists', methods=['GET', 'OPTIONS'])
def list_playlists():
    if request.method == 'OPTIONS':
        return '', 200
    authh = request.headers.get('Authorization', '')
    token = authh.split(' ')[1] if ' ' in authh else authh
    try:
        uid = auth.verify_id_token(token)['uid']
    except Exception as e:
        return jsonify({'error': str(e)}), 401
    pls = pm.get_all_playlists(uid)
    return jsonify(pls), 200

if __name__ == '__main__':
    app.run(debug=True)
