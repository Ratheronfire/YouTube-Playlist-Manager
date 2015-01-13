# YouTube-Playlist-Manager
A little Python program that can manage a collection of YouTube playlists and view them in certain media players.

At the moment this program isn't quite ready for anyone to use it.  In the future I want to be able to configure it so users can use the Google OAuth service to gain access to the YouTube API, but for now I just hard-coded my public key to a config file.

Essentially, what this program does is manage a collection of YouTube videos, which it gathers from YouTube playlists.

## Brief Overview

### Scripts
find_account_playlists.py is used to fetch a list of all available playlists for a given user.
add_playlist.py is used to collect videos from a given playlist, which is saved in video_prefs.json.
update_existing_uploaders.py checks all of the uploaders the user has playlists from, and updates any playlists that have changed.

### JSON Files

video_prefs.json contains a list of uploaders, each containing a list of playlist which contains a list of videos:
* "uploaders" : List of uploader IDs
  * Uploader ID
    * "name" : The uploader's username
    * "playlists" : List of playlist IDs associated with this uploader
        * Playlist ID
            * "videos" : List of videos associated with this playlist
                * "id"
                * "title"
            * "count" : The number of videos in the playlist
            * "name" : The playlist's name

playlist_prefs.json contains a set of playlist IDs, with a boolean value indicating whether or not to add that playlist.  This is used when a player uses find_account_playlists.py to find all the playlists for an account.  For each playlist, the script will first check playlist_prefs to determine whether or not to add it.  If no entry is found, the user will be asked whether or not to add it, and their choice will then be saved to playlist_prefs.
