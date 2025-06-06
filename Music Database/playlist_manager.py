from datetime import datetime
from firebase_admin import firestore

class PlaylistManager:
    def __init__(self, db):
        self.db = db
        self.playlists_col = self.db.collection('playlists')
        self.songs_col     = self.db.collection('songs')

    def create_playlist(self, name, owner, description=""):
        playlist_data = {
            'name':        name,
            'owner':       owner,
            'description': description,
            'created_at':  datetime.now()
        }
        playlist_ref = self.playlists_col.document()
        playlist_ref.set(playlist_data)
        return playlist_ref.id

    def add_song(self, playlist_id, title, artist, duration, album=None, album_cover_url=None):
        song_data = {
            'playlist_id':     playlist_id,
            'title':           title,
            'artist':          artist,
            'duration':        duration,
            'album':           album,
            'album_cover_url': album_cover_url,
            'added_at':        datetime.now()
        }
        song_ref = self.songs_col.document()
        song_ref.set(song_data)
        return song_ref.id

    def move_song_to_playlist(self, song_id, new_playlist_id):
        """Assign an existing song document to a different playlist_id."""
        song_ref = self.songs_col.document(song_id)
        song = song_ref.get()
        if not song.exists:
            return False
        song_ref.update({'playlist_id': new_playlist_id})
        return True

    def get_playlist(self, playlist_id):
        pl = self.playlists_col.document(playlist_id).get()
        if not pl.exists:
            return None
        data = pl.to_dict()
        data['id'] = pl.id
        return data

    def get_all_playlists(self, owner):
        query = self.playlists_col.where('owner', '==', owner).stream()
        return [{**pl.to_dict(), 'id': pl.id} for pl in query]

    def get_all_playlists_public(self):
        """Return all playlists regardless of owner."""
        query = self.playlists_col.stream()
        return [{**pl.to_dict(), 'id': pl.id} for pl in query]

    def get_songs_for_playlist(self, playlist_id):
        query = self.songs_col.where('playlist_id', '==', playlist_id).stream()
        return [{**song.to_dict(), 'id': song.id} for song in query]

    def get_all_songs(self):
        """Return all song documents."""
        query = self.songs_col.stream()
        return [{**song.to_dict(), 'id': song.id} for song in query]

    def get_songs_for_user(self, owner):
        pls = self.get_all_playlists(owner)
        ids = [pl['id'] for pl in pls]
        if not ids:
            return []
        query = self.songs_col.where('playlist_id', 'in', ids).stream()
        return [{**song.to_dict(), 'id': song.id} for song in query]

    def unlink_song_from_playlist(self, playlist_id, song_id):
        """Clear the playlist_id of a song (keep the document)."""
        song_ref = self.songs_col.document(song_id)
        song = song_ref.get()
        if not song.exists or song.to_dict().get('playlist_id') != playlist_id:
            return False
        song_ref.update({'playlist_id': None})
        return True

    def delete_playlist(self, playlist_id):
        # delete all songs in that playlist
        for song in self.songs_col.where('playlist_id', '==', playlist_id).stream():
            self.songs_col.document(song.id).delete()
        self.playlists_col.document(playlist_id).delete()

    def delete_song(self, song_id):
        self.songs_col.document(song_id).delete()

    def export_playlist(self, playlist_id):
        """Return dict { playlist: {...}, songs: [...] }."""
        pl = self.get_playlist(playlist_id)
        if not pl:
            return None
        songs = self.get_songs_for_playlist(playlist_id)
        return {'playlist': pl, 'songs': songs}

    def import_playlist(self, owner, playlist_export):
        """
        Given exported data, recreate the playlist and its songs for `owner`.
        Expects {'playlist': {...}, 'songs': [...] }.
        """
        pl_data = playlist_export.get('playlist', {})
        songs   = playlist_export.get('songs', [])

        new_id = self.create_playlist(
            pl_data.get('name'),
            owner,
            pl_data.get('description', '')
        )

        for s in songs:
            self.add_song(
                new_id,
                s.get('title'),
                s.get('artist'),
                s.get('duration'),
                s.get('album'),
                s.get('album_cover_url')
            )

        return new_id
