__author__ = "David"

import json
import sys
from youtube_playlist import load_config, send_get_request

playlist_id = str()
config = load_config()


def process_pages(json_page):
    videos = list()

    finished = False

    while not finished:
        video_entries = json_page["items"]

        for video in video_entries:
            videos.append(dict(title=video["snippet"]["title"], id=video["snippet"]["resourceId"]["videoId"]))

        if "nextPageToken" in json_page:
            json_page = send_get_request(
                "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&pageToken={0}&playlistId={1}"
                "&key={2}".format(json_page["nextPageToken"], playlist_id, config["api_key"]))
        else:
            finished = True

    return videos


def add_playlist(i):
    global playlist_id
    playlist_id = i

    # we request the first page of data for the playlist separately from the rest
    # this lets us skip the rest if we already have up-to-date data for it
    initial_playlist_json = send_get_request("https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&"
                                             "playlistId={0}&key={1}".format(playlist_id, config["api_key"]))

    if len(initial_playlist_json["items"]) == 0:
        print("No videos found for", playlist_id)
        return -1

    uploader_id = initial_playlist_json["items"][0]["snippet"]["channelId"]
    uploader_name = initial_playlist_json["items"][0]["snippet"]["channelTitle"]
    playlist_name = initial_playlist_json["items"][0]["snippet"]["title"]

    with open(config["video_prefs_path"], "r", encoding="utf8") as prefs_raw:
        prefs = json.load(prefs_raw)

    new_count = int(initial_playlist_json["pageInfo"]["totalResults"])

    if uploader_name in prefs["uploaders"] and playlist_name in prefs["uploaders"][uploader_name]["playlists"]:
        old_count = prefs["uploaders"][uploader_name]["playlists"][playlist_name]["count"]
    else:
        old_count = 0

    if not new_count == old_count:
        videos = process_pages(initial_playlist_json)

        prefs["uploaders"][uploader_id]["name"] = uploader_name
        prefs["uploaders"][uploader_id]["playlists"][playlist_id] = dict()
        prefs["uploaders"][uploader_id]["playlists"][playlist_id]["name"] = playlist_name
        prefs["uploaders"][uploader_id]["playlists"][playlist_id]["videos"] = videos
        prefs["uploaders"][uploader_id]["playlists"][playlist_id]["count"] = len(videos)

        with open(config["video_prefs_path"], "w", encoding="utf8") as outfile:
            json.dump(prefs, outfile, indent=2)
    else:
        print("No change in playlist", playlist_name, "from uploader", uploader_name, "- no action taken.")

    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(sys.argv, len(sys.argv))
        print("USAGE: {0} playlist-id".format(sys.argv[0]))
        exit(-1)

    add_playlist(sys.argv[1])