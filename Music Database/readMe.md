# Overview

As a software engineer looking to gain hands-on experience with cloud-based systems, I developed a **Music Playlist Manager** that stores and manages playlists and songs in a scalable NoSQL database. This project helped me explore full-stack development, user authentication, and data persistence in a cloud environment.

The application allows users to:
- Create and manage playlists
- Add, remove, and move songs between playlists
- Export and import playlists in JSON format
- View all songs and playlists they've created

This program uses **Google Firebase Firestore** to persist data. It includes a Python backend with Flask, a simple HTML/CSS/JavaScript interface. Playlists and songs are stored in Firestore collections, enabling fast and flexible cloud data access.

To use the program:
1. Start the Flask server (`python app.py`)
2. Open the provided HTML interface in a browser
3. Create playlists, add songs, and manage your music in real time

[Software Demo Video](http://youtube.link.goes.here)

---

# Cloud Database

This project uses **Google Firebase Firestore**, a NoSQL cloud database that allows serverless, real-time data storage. It is part of the Google Cloud ecosystem and integrates easily with Firebase Authentication and other Firebase tools.

### Database Structure

The Firestore database uses two primary collections:

- **playlists**
  - Fields: name, description, uid, created_at
  - Each playlist has a unique playlist_id

- **songs**
  - Fields: title, artist, duration, album, album_cover_url, playlist_id, uid

Each song references the playlist it belongs to using the playlist_id field, creating a logical relationship between the collections.

---

# Development Environment

### Tools Used
- **Firebase Firestore** — Cloud NoSQL database
- **Firebase Admin SDK** — Used to access Firestore from Python
- **Firebase Authentication** — For secure user logins
- **Flask** — Lightweight backend framework to expose REST API
- **HTML/CSS/JavaScript** — For building the frontend UI

### Programming Language and Libraries
- `Python 3.10+`
- `firebase-admin`
- `flask`
- `flask-cors`

---

# Useful Websites

- [Firebase Firestore Documentation](https://firebase.google.com/docs/firestore)
- [Firebase Admin SDK (Python)](https://firebase.google.com/docs/admin/setup)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Authentication Setup](https://cloud.google.com/iam/docs/creating-managing-service-account-keys)
- [YouTube: Firestore Tutorial for Beginners](https://www.youtube.com/watch?v=2Vf1D-rUMwE)

---

# Future Work

- Allow songs to be in multiple playlists
- Allowing viewing of other users' public playlists
- Improving the UI for better user experience
