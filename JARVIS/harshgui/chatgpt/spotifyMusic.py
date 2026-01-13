import spotipy
from spotipy.oauth2 import SpotifyOAuth

def MusicControl(args):
    action = args['action']
    client_id = 'be4fa27df4d74eb289d5f272bc380607'
    client_secret = '4fad988181894473af65ad88b970de69'
    redirect_uri = 'https://localhost:3000/'
    # Create a Spotify client using OAuth 2.0 flow
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, 
                                                redirect_uri=redirect_uri, scope='user-modify-playback-state'))
    # Retrieve the access token
    token_info = sp.auth_manager.get_access_token()
    access_token = token_info['access_token']

    #Code for Playing a song at current time
    if action == "playSong":
        song_name = args['song_name']
        # Search for the song
        results = sp.search(q=song_name, type='track')
        # Check if there are search results
        if results['tracks']['items']:
            # Get the first result (you can choose a specific one if there are multiple)
            track = results['tracks']['items'][0]

            # Play the song
            sp.start_playback(uris=[track['uri']])
            print(f'Playing {track["name"]} by {", ".join(artist["name"] for artist in track["artists"])}')
        else:
            print(f'Song "{song_name}" not found.')

    elif action == "addQueue":
        song_name = args['song_name']
        # Search for the song
        results = sp.search(q=song_name, type='track')
        # Check if there are search results
        if results['tracks']['items']:
            # Get the first result (you can choose a specific one if there are multiple)
            track = results['tracks']['items'][0]
            #print(track)
            # Play the song
            sp.add_to_queue(uri = track['uri'])
            print(f'Added to Queue {track["name"]} by {", ".join(artist["name"] for artist in track["artists"])}')
        else:
            print(f'Song "{song_name}" not found.')

    elif action == "pauseSong":
        sp.pause_playback()

    elif action == "resumeSong":
        sp.start_playback()
