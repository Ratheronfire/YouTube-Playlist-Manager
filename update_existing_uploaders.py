__author__ = "David"

import json
from find_account_playlists import find_account_playlists
from youtube_playlist import load_config

config = load_config()


def update_existing_uploaders():
    with open(config["video_prefs_path"], "r") as prefs:
        prefs_json = json.load(prefs)

    for uploader in prefs_json["uploaders"]:
        print("Now updating playlists from", prefs_json["uploaders"][uploader]["name"])

        find_account_playlists(uploader, False)
        print("\n------------------\n")


if __name__ == "__main__":
    update_existing_uploaders()