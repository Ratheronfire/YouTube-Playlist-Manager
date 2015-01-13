__author__ = "David"

from random import shuffle
import os
import json
import subprocess
from youtube_playlist import load_config

config = load_config()


def generate_playlist():
    video_ids = list()
    video_links = list()

    with open(config["video_prefs_path"], "r", encoding="utf8") as videos:
        videos_json = json.load(videos)

    for uploader in videos_json["uploaders"]:
        for playlist in videos_json["uploaders"][uploader]["playlists"]:
            for video in videos_json["uploaders"][uploader]["playlists"][playlist]["videos"]:
                video_ids.append(video["id"])

    for video in video_ids:
        video_links.append("http://www.youtube.com/watch?v=" + video)

    return video_links


def play_videos():
    videos = generate_playlist()

    # for line in videos:
    # if re.match(".*[<>|&;$].*", line):
    #         print(u"WARNING: Possible injection detected on: {0:s}".format(line))
    #         exit(-1)
    #
    #     #thanks to http://www.regexbuddy.com/ for this URL Regex
    #     if re.match("(\b(https?|ftp|file)://)?[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]", line):
    #         line = re.sub("\n", "", line)
    #         videos.append(line)

    shuffle(videos)

    playlist_file = "[playlist]\n"

    for i in range(len(videos)):
        playlist_file += "File%i=%s\n" % (i + 1, videos[i])

    playlist_file += "NumberOfEntries=%i" % len(videos)

    playlist_out = open(config["playlist_file_path"], "w")
    playlist_out.write(playlist_file)
    playlist_out.close()

    found_player = False

    for media_player in config["players"]:
        if os.access(media_player, os.F_OK) and not found_player:
            found_player = True
            subprocess.check_call([media_player, config["playlist_file_path"]])

    if not found_player:
        print("Error: Could not find suitable media player.")
        exit(-2)

    os.remove(config["playlist_file_path"])


if __name__ == "__main__":
    play_videos()
