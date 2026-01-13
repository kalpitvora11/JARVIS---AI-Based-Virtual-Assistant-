import pythoncom
pythoncom.CoInitialize()

#Speak.py File
#Converts text to speech using TTS engine
import pyttsx3



def Say(Text):
    engine = pyttsx3.init(driverName="sapi5")
     #here get property method is used to retrieve current value of property
    voices = engine.getProperty('voices')
   
    engine.setProperty('voices',voices[0].id)
    engine.setProperty('rate',170)

    print("   ")
    print(f"A.I : {Text}")
    engine.say(text=Text)
    engine.runAndWait()
    print("   ")
#Say("Bye Bye")