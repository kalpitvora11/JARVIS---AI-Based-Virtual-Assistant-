import pythoncom
pythoncom.CoInitialize()


import sys                                                      #pip install sys
import pyttsx3                                                  #pip  install pyttsx3        
import speech_recognition as sr                                 #pip install speechrecognition
import datetime

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
import random
import json
import torch
from Brain import NeuralNet
from NueralNetwork import bag_of_words,tokenize
from Listen import Listen
from Speak import Say
from Task import InputExecution
from Task import NonInputExecution
from chatgpt.gpt import askGPT

from mainjarvis import Ui_Dialog

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
with open("intents.json",'r') as json_data:
    intents = json.load(json_data)

FILE = "TrainData.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size,hidden_size,output_size).to(device)
model.load_state_dict(model_state)
model.eval()

#---------------------------------
Name = "Jarvis"



def wishings():
    
    hour=int(datetime.datetime.now().hour)    
    if hour>0 and hour<12:
        ui.terminalPrint("Jarvis: Good Morning BOSS")
        Say("Good Morning BOSS")
        ui.label_4text("Jarvis: Good Morning BOSS")
    elif hour>=12 and hour<17:
        print("Jarvis: Good Afternoon BOSS")
        Say("Good Afternoon BOSS") 
        ui.label_4text("Jarvis: Good Afternoon BOSS")
    elif hour>=17 and hour<20:
        print("Jarvis: Good Evening BOSS")
        Say("Good Evening BOSS")   
        ui.label_4text("Jarvis: Good Evening BOSS")
    else:
        print("Jarvis: Good Night BOSS")
        Say("Good Night BOSS") 
        ui.label_4text("Jarvis: Good Night BOSS")  
        
        
        
class jarvismainFile(QThread):

    def __init__(self):
        super(jarvismainFile, self).__init__()
         
    def run(self):   
        self.runJarvis()
                 
    def commands(self):
        
        r=sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            ui.updateMovieDynamically("listening")
            r.pause_threshold=1
            audio=r.listen(source)  
            
        try:
            
            print("Wait for few Moments..")
            ui.label_4text("Wait for few Moments..")  
            cmd=r.recognize_google(audio,language='en-in')   
            print(f"You just said: {cmd}\n")
            ui.label_4text("You Just said:"+ cmd) 
            
            
        except Exception as e:
            print(e)
            Say("Please tell me again")
            cmd="none"
        return cmd

            
    def runJarvis(self):
        
        wishings()
        while True:
            if ui.state != False :
                
                #State is Listening
                if ui.listenState == True:
                    ui.label_4text("Listening...")
                    Greet,sentence = Listen(ui.listenState)
                    ui.label_4text(Greet)
                    ui.label_4text("You Said : " + sentence)
                    ui.label_4text("\n")
                    result = str(sentence.lower())
                    
                    if sentence == "bye":
                        exit()
                        
                    sentence = tokenize(sentence)
                    X = bag_of_words(sentence,all_words)
                    X = X.reshape(1,X.shape[0])
                    X = torch.from_numpy(X).to(device)

                    output = model(X)

                    _ , predicted = torch.max(output,dim=1)

                    tag = tags[predicted.item()]

                    probs = torch.softmax(output,dim=1)
                    prob = probs[0][predicted.item()]

                    if prob.item() > 0.75:
                        for intent in intents['intents']:
                            if tag == intent["tag"]:
                                reply=random.choice(intent["responses"])

                                if "time" in reply:
                                    resp=NonInputExecution(reply)
                                    ui.label_4text("Time is : " + resp)
                                elif "date" in reply:
                                    resp=NonInputExecution(reply)
                                    ui.label_4text("Date is : " + resp)
                                    
                                elif "day" in reply:
                                    resp=NonInputExecution(reply)
                                    ui.label_4text("Day is : " + resp)
                                elif "wikipedia" in reply:
                                    resp=InputExecution(reply,result)
                                    ui.label_4text("Wikipedia Says : " + resp)
                                    Say(resp)
                                elif "google" in reply:
                                    InputExecution(reply,result)
                                    ui.label_4text("Searching Google!")
                                elif "youtube" in reply:
                                    InputExecution(reply,result)
                                    ui.label_4text("Searching Youtube!")
                                else:
                                    Say(reply)
                                    
                #Setting text to read input from textbox
                else:
                    pass
                    
            else:
                print("Program has not started!")                      

startExecution = jarvismainFile()
                
class Ui_Jarvis(QMainWindow):
    
    def __init__(self):
        super(Ui_Jarvis, self).__init__()   
        self.state = False  
        self.listenState = False
        self.firstUI = Ui_Dialog()
        self.firstUI.setupUi(self)
        self.firstUI.plainTextEdit.hide()
        self.firstUI.label_4.hide()
        self.firstUI.label_2.hide()
        self.firstUI.lineEdit.hide()
        self.firstUI.pushButton_Strat_2.hide()
        self.firstUI.pushButton_Exit.clicked.connect(self.changeListenState)
        self.firstUI.pushButton_Strat.clicked.connect(self.manualCodeFromTerminal)
        self.firstUI.pushButton_Strat_2.clicked.connect(self.manualCodeFromTerminal)
        self.runAllMovies()  # Call this method\
            
    def changeListenState(self):
        if self.listenState == False:
            self.listenState = True
            self.firstUI.pushButton_Exit.setText("Mute")
        elif self.listenState == True:
            self.listenState = False
            self.firstUI.pushButton_Exit.setText("Unmute")
            
    def label_4text(self, text):
        self.firstUI.label_4.appendPlainText(text)
        #self.firstUI.label_4.setForegroundRole(QtGui.QColor("yellow"))
                 
    def plsgettext(self):
        query =  str(self.firstUI.lineEdit.text())
        self.firstUI.lineEdit.setText(" ")
        if len(query) > 5:
            print(f"Im Called ******")
            try:
                askGPT(query)
                self.firstUI.label_4.appendPlainText("\nTask Successfull....") 
            except Exception as e:
                print(e)
                self.firstUI.label_4.appendPlainText("\nSomething went wrong, please try again!")
                
                 
    def manualCodeFromTerminal(self):
        self.firstUI.plainTextEdit.show()
        self.firstUI.label_4.show()
        self.firstUI.label_2.show()
        self.firstUI.lineEdit.show()
        self.firstUI.pushButton_Strat_2.show()
        self.firstUI.pushButton_Strat_2.clicked.connect(self.plsgettext)
        self.state = True
                    
    def terminalPrint(self, text):  
        self.firstUI.plainTextEdit.appendPlainText(text)    
          
    def updateMovieDynamically(self, state):
        if state == "speaking":       
          pass
        elif state == "listening":      
            self.firstUI.label_4.appendPlainText("\nListening...")    
        elif state == "loading":        
           pass
             
        
    def runAllMovies(self):
        self.firstUI.codingMovie = QtGui.QMovie("../GUI MATERIAL/ExtraGui/Jarvis_Gui (2).gif")
        self.firstUI.label.setMovie(self.firstUI.codingMovie)
        self.firstUI.codingMovie.start()
        
        startExecution.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_Jarvis()  # Create an instance of Ui_Jarvis
    ui.show()
    sys.exit(app.exec_())

