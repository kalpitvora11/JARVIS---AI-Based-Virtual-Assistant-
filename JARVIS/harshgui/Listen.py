#Listen.py File
import speech_recognition as sr
def Listen(state):
    wal=""
    query=""

    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.energy_threshold=10000
        r.adjust_for_ambient_noise=(source,1.2)
        print("Listening..")
        
        r.pause_threshold = 5
        audio = r.listen(source,0,5)
        

    try:
        if state != False:
            print("Recognizing..")
            query = r.recognize_google(audio,language="en-in")
            wal="Recognizing"
            print(f"You Said : {query}")

    except:
       pass
    
    query = str(query)
    return ["Recognizing..",query]

