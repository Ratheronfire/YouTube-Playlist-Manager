__author__ = "David"

# from play_videos import play_videos
# from add_playlist import add_playlist
# from find_account_playlists import find_account_playlists
# from generate_playlist import generate_playlist
# from update_existing_uploaders import update_existing_uploaders

# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.client import OAuth2WebServerFlow
import requests
import json
import os

default_config = {'players': [], 'video_prefs_path': os.getcwd() + "/video_prefs.json",
                  'playlist_prefs_path': os.getcwd() + "\\playlist_prefs.json",
                  'playlist_file_path': os.getcwd() + "\\videos.pls", 'api_key': ""}

def prompt_for_api_key():
    print("No valid API key was found.  You must generate one through https://console.developers.google.com/"
          ", and put the API key in configs.json.")
    # TODO: implement better method for generating API key

    exit(1)

def initialize_config():
    with open("config.json", "w", encoding="utf8") as config_file:
        json.dump(default_config, config_file, indent=2)

def send_get_request(url):
    response_json = dict()

    try:
        response_json = requests.get(url).json()
    except Exception as e:
        print("Error trying to send GET request for {0}\n Error {1} - {2}".format(url, type(e), e.args))

    if "error" in response_json:
        if response_json["error"]["errors"][0]["reason"] == "keyInvalid":
            prompt_for_api_key()

    return response_json

def load_config():
    if os.access("config.json", os.F_OK):
        with open("config.json", "r", encoding="utf8") as config_file:
            config = json.load(config_file)
    else:
        print("No config file found, creating default file.")
        initialize_config()
        return default_config

    return config

# def main():
#     option = input("[1] Play Videos\n[2] Add Playlist\n[3] Find Playlists for an Account\n[4] Generate Playlist\n[5] Update Existing Uploaders\nEnter an option: ")
#
#     if option == "1":
#         play_videos()
#     elif option == "2":
#         add_playlist()
#     elif option == "3":
#         find_account_playlists()
#     elif option == "4":
#         generate_playlist()
#     elif option == "5":
#         update_existing_uploaders()
#
#
# if __name__ == "__main__":
#     main()
