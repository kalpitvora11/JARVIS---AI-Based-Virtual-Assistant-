from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import sys
import pygetwindow as gw

# Function to increase the volume by a specified amount
def increase_volume(step):
    volume = get_volume_object()
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(1.0, current_volume + (step / 5))
    volume.SetMasterVolumeLevelScalar(new_volume, None)

# Function to decrease the volume by a specified amount
def decrease_volume(step):
    volume = get_volume_object()
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = max(0.0, current_volume - (step / 5))
    volume.SetMasterVolumeLevelScalar(new_volume, None)

# Function to mute/unmute the volume
def toggle_mute():
    volume = get_volume_object()
    muted = volume.GetMute()
    volume.SetMute(not muted, None)

# Function to get the volume object for the active audio endpoint
def get_volume_object():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume

if __name__ == "__main__":
    while True:
        print("Volume Control:")
        print("1. Increase Volume")
        print("2. Decrease Volume")
        print("3. Toggle Mute")
        print("4. Quit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            step = float(input("Enter the amount to increase the volume (0-5): "))
            if 0 <= step <= 5:
                increase_volume(step)
            else:
                print("Volume adjustment must be in the range of 0 to 5.")
        elif choice == "2":
            step = float(input("Enter the amount to decrease the volume (0-5): "))
            if 0 <= step <= 5:
                decrease_volume(step)
            else:
                print("Volume adjustment must be in the range of 0 to 5.")
        elif choice == "3":
            toggle_mute()
        elif choice == "4":
            sys.exit(0)
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")
