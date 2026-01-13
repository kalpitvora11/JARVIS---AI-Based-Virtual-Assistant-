#Function
#Task.py File
import datetime
import webbrowser
from Speak import Say
# 2 types 
#1- Non Input
#eg: Time, Date, Speedtest
def YouTubeSearch(query):
    # Open a web browser and perform a YouTube search
    search_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(search_url)



def Time():
    time = datetime.datetime.now().strftime("%H:%M")
    Say(time)
    return str(time)

def Date():
    date = datetime.date.today()
    Say(date)
    return str(date)

def Day():
    day = datetime.datetime.now().strftime("%A")
    Say(day)
    return str(day)

def NonInputExecution(query):
    query = str(query)
    if "time" in query:
        return (Time())
    elif "date" in query:
       return (Date())
    elif "day" in query:
        return (Day())
    
#2- Input
#eg - google search, wikipidea


def InputExecution(tag,query):
    if "wikipedia" in tag:
        name = str(query).replace("who is","").replace("about","").replace("what is","").replace("wikipedia","")
        import wikipedia
        result = wikipedia.summary(title=name,sentences=2)
        return result

    elif "google" in tag:
       query =  str(query).replace("google","")
       query = query.replace("search","")
       import pywhatkit
       pywhatkit.search(query)

    elif "youtube" in tag:
        query = query.replace("youtube", "").replace("search", "")
        YouTubeSearch(query)


# def TaskExe():

#     def Music():
#         Say("Tell Me The NamE oF The Song!")
#         musicName = takecommand()
#         pywhatkit.playonyt(musicName)

#         Say("Your Song Has Been Started! , Enjoy Sir!")

#     def OpenApps():
#         Say("Ok Sir , Wait A Second!")
        
#         if 'code' in query:
#             os.startfile("E:\\Applications\\Microsoft VS Code\\Microsoft VS Code\\Code.exe")

#         elif 'telegram' in query:
#             os.startfile("E:\\Applications\\Telegram Desktop\\Telegram Desktop\\Telegram.exe")

#         elif 'chrome' in query:
#             os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        
#         elif 'facebook' in query:
#             webbrowser.open('https://www.facebook.com/')

#         elif 'instagram' in query:
#             webbrowser.open('https://www.instagram.com/')

#         elif 'maps' in query:
#             webbrowser.open('https://www.google.com/maps/@28.7091225,77.2749958,15z')

#         elif 'youtube' in query:
#             webbrowser.open('https://www.youtube.com')

#         Say("Your Command Has Been Completed Sir!")
