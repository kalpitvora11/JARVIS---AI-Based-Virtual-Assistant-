
from ctypes.wintypes import PHANDLE
import pywhatkit
import pyautogui
import time


def send_whatsapp_message(contact_name, message):
    try:
        # Send the WhatsApp message
        pywhatkit.sendwhatmsg_instantly(contact_name, message, 15, 0)
        # Delay to give you time to focus on the input field
        print(f"WhatsApp message sent to {contact_name}: {message}")
        time.sleep(20)
        # Simulate pressing the Enter key
        pyautogui.press('enter')
        print("KeyPressed")
    except Exception as e:
        print(f"An error occurred while sending the WhatsApp message: {str(e)}")

def sendWhatsapp(phn, msg):
    # Initialize the speech recognizer
    contact_name = phn
    message = msg
    try:
        print(f"{contact_name}")
        print(f"{message}")
        send_whatsapp_message(contact_name, message)

    except:
        print("Sorry, I couldn't understand the audio.")

