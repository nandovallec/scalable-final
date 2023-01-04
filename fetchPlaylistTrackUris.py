import requests
import base64
import json
import sys

def get_playlist_track_uris(playlist_id):
    client_id = '3b8cc27251bf4dfda64a3f3426f1bc2e'
    client_secret = '166aeccbd32c4b87baa8c96412b21e75'

    # client_credentials_bytes = (client_id + ':' + client_secret).encode('ascii')
    access_token = get_access_token(client_id, client_secret)

    playlist_data = get_playlist_data(access_token, playlist_id)

    # Output the playlist data to a file
    # with open('playlist-tracks.json', 'w') as outfile:
        # json.dump(json.loads(playlist_response.text), outfile)

    track_uris = [item['track']['uri'] for item in playlist_data['tracks']['items']]
    print(track_uris)

    # Output the track uris into a file
    # with open('track-uris-new.txt', 'w') as output_file:
    #     output_file.write('\n'.join(track_uris))

    return track_uris
    


def get_access_token(client_id, client_secret) -> str: 
    base64_string = base64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')

    auth_headers = {
            'Authorization': 'Basic ' + base64_string,
            'Content-type': 'application/x-www-form-urlencoded'
    }
    auth_data = {'grant_type': 'client_credentials'}

    auth_response = requests.post('https://accounts.spotify.com/api/token', headers=auth_headers, json=True, data=auth_data)
    access_token = json.loads(auth_response.text)['access_token']

    return access_token

def get_playlist_data(access_token, playlist_id):
    get_playlist_headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json',
    }

    playlist_response = requests.get('https://api.spotify.com/v1/playlists/' + playlist_id, headers=get_playlist_headers)
    playlist_data = json.loads(playlist_response.text)

    return playlist_data

if __name__ == "__main__":
    playlist_id = sys.argv[1]

    get_playlist_track_uris(playlist_id)