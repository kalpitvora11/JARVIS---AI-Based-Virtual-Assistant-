import datetime
import webbrowser
import os
import screen_brightness_control as sbc
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import sys
import pygetwindow as gw
from .Gmail import Gmail
from .Whatsapp import sendWhatsapp

# Function to get the volume object for the active audio endpoint
def get_volume_object():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume

#Function to send Emails to Client
def sendGmail(args):
    senderMail = None
    message = None
    cc = None
    bcc = None
    try:
        senderMail = args['receiver']
    except:
        pass
    try:
        message = args['message']
    except:
        pass
    try:
        cc = args['cc']
    except:
        pass
    try:
        bcc = args['bcc']
    except:
        pass
    try:
        subject = args['subject']
    except:
        pass
    gmail = Gmail()
    try:
        gmail.run(subject=subject, message=message, cc=cc, bcc=bcc, to=senderMail)
        print("Mail has been sent successfully")
    except Exception as e:
        print(e)
        print("There was some error while sending the mail!")

#Function to control the volume
def controlVolume(args):
    action = args['action']

    if action == "increaseVolume":
        step = int(args['step'])
        volume = get_volume_object()
        current_volume = volume.GetMasterVolumeLevelScalar()
        new_volume = min(1.0, current_volume + (step / 5))
        volume.SetMasterVolumeLevelScalar(new_volume, None)

    if action == "decreaseVolume":
        step = int(args['step'])
        volume = get_volume_object()
        current_volume = volume.GetMasterVolumeLevelScalar()
        new_volume = max(0.0, current_volume - (step / 5))
        volume.SetMasterVolumeLevelScalar(new_volume, None)

    if action == "muteUnmute":
        volume = get_volume_object()
        muted = volume.GetMute()
        volume.SetMute(not muted, None)


#Deletes a file from System
def deleteFile(args):
    file_path = args['path']
    try:
        # Check if the file exists before attempting to delete it
        if os.path.exists(file_path):
            os.remove(file_path)
            return True  # File successfully deleted
        else:
            return False  # File doesn't exist
    except Exception as e:
        return str(e)  # Return the error message if there was an issue

#Edits a file in System
def editFile(args):
    file_path = args['path']
    new_content = args['content']
    try:
        # Open the file in write mode to overwrite the existing content
        with open(file_path, "w") as file:
            file.write(new_content)
        return True  # Editing successful
    except Exception as e:
        return str(e)  # Return the error message if an error occurs

#Save a file in System
def saveFile(args):
    # Ensure the destination directory exists
    content = args['content']
    destination = args['path']

    # Create the file path
    file_path = destination

    # Write the content to the file
    with open(file_path, "w") as file:
        file.write(content)

    return str(file_path)

#function name:- getTime
#function description:- It will give current systems time
#parameter:- none
def getTime(args):
    time = datetime.datetime.now().strftime("%H:%M")
    return str(time)
    
#function name:- getDate
#function description:- It will give current systems date
#parameter:- none
def getDate(args):
    date = datetime.date.today()
    return str(date)

#function name:- getDay
#function description:- It will give current systems set day
#parameter:- none
def getDay(args):
    day = datetime.datetime.now().strftime("%A")
    return str(day)

def searchWikipedia(args):
    query = args['query']
    noLines = args['noLines']
    import wikipedia
    result = wikipedia.summary(query, sentences = noLines)
    return str(result)

#Doesn't return Anything
def searchGoogle(args):
    query = args['query']
    import pywhatkit
    pywhatkit.search(query)
    return "Task Done"

#Doesn't return Anything
def searchYoutube(args):
    query = args['query']
    search_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(search_url)
    return "Task Done"

#Deletes Temp Files from the System
def deleteTempFiles(args):
    temp_directory = "C:\\Users\\Admin\\AppData\\Local\\Temp"
    # Calculate yesterday's date
    today = datetime.datetime.now()
    
    # Convert the date to a string in the format "YYYYMMDD"
    today_str = today.strftime("%Y%m%d")
    
    # List files in the temp directory
    files = os.listdir(temp_directory)
    
    # Iterate through the files and delete those created yesterday
    deleted_files = []
    for file in files:
        file_path = os.path.join(temp_directory, file)
        file_stat = os.stat(file_path)
        file_creation_date = datetime.datetime.fromtimestamp(file_stat.st_ctime)
        
        if file_creation_date.strftime("%Y%m%d") != today_str:
            try:
                os.remove(file_path)
                deleted_files.append(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {str(e)}")
    
    return str(len(deleted_files)) + " Temporary files have been deleted"

def controlBrightness(args):
    controlBright = int(args['intensity'])
    controlled_brightness = sbc.set_brightness(controlBright ,no_return=False)
    return str(controlled_brightness)


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
    if "play" in action:
        song_name = args['song']
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

    elif "add" in action:
        song_name = args['song']
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

    elif "pause" in action:
        try:
            sp.pause_playback()
        except Exception as e:
            print(e)

    elif "resume" in action:
        try:
            sp.start_playback()
        except Exception as e:
            print(e)

    elif "next" in action:
        try:
            sp.next_track()
        except Exception as e:
            print(e)

    elif "previous" in action:
        try:
            sp.previous_track()
        except Exception as e:
            print(e)
            
def sendWhatsappMessage(args):
    phone_number = args['phoneNumber']
    message = args['message']
    sendWhatsapp(phn=phone_number, msg=message)



