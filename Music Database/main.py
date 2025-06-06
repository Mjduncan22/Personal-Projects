from firestore_client import initialize_firestore
from playlist_manager import PlaylistManager

# Initialize Firestore DB
db = initialize_firestore('C:\School\Spring_2025\CSE 310\Personal-Projects\Music Database\serviceAccount.json')

pm = PlaylistManager(db)

# Create a playlist
playlist_id = pm.create_playlist("Chill Vibes", "user123", "Relaxing tunes")

# Add a song to the playlist
song_id = pm.add_song(playlist_id, "Flames Remember", "Kelly Fan Club Official", "2:10", "Flames Remember", "https://example.com/image.jpg")

# Retrieve playlist info
playlist = pm.get_playlist(playlist_id)
print("Playlist:", playlist)

# Retrieve all songs for the playlist
songs = pm.get_songs_for_playlist(playlist_id)
for song in songs:
    print(song)

# Update playlist description
pm.update_playlist(playlist_id, {"description": "Updated description"})

# Delete a song
pm.delete_song(song_id)

# Delete the playlist (and all its songs)
pm.delete_playlist(playlist_id)
