import openai
import time
import json
from .tasks import getTime,getDay,getDate,searchGoogle,searchWikipedia,searchYoutube,editFile,deleteFile,saveFile,deleteTempFiles,controlBrightness,MusicControl,sendGmail,sendWhatsappMessage
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

#Memory Variable
mem_var = 3



SAVE_FILE_DESCRIPTION = """
    SAVES a fie into the local system with specified **path**,**content**
    The '<<path>>' parameter will specify the file path where the data is located, and the '<<content>>' parameter will contain the actual text data.
    
    ALWAYS GIVE ME THE SPECIFIED PARAMETER NAMES
    ex,
    
    IWrite numbers 0-100 in file named Soham.txt in Jarvis Folder in D drive of my computert's crucial to ensure that you correctly identify and understand the parameters. I am providing you with two parameters: 'path' and 'content.' The 'path' parameter represents the file location, and the 'content' parameter contains the text data itself. Please provide me with a response that specifically addresses these parameters and avoids any confusion regarding their names. Accurate and contextually relevant responses are essential.
    
    Write numbers 0-10 in file named Soham.txt in Jarvis Folder in D drive of my computer
    here, args will be as follows
    ****
    {
        "path" : "D://Jarvis/",
        "content" : "1,2,3,4,5,6,7,8,9,10"
    }
    ****
    ONLY USE THE PARAMETERS PROVIDED AND GIVEN IN REQUIRED TO YOU AND NOT ANY NEW PARAMETER NAMES ON YOUR OWN CREATE ON YOUR OWN
    """



# Initializing the memory
user_history = []
response_history = []

SYSTEM_PROMPT = """
You are a helpful assistant with functions to help user in local system. Always use the provided functions given to you to answer most of the questions.
Only use functions that you are provided with.

ONLY PROVIDE FUNCTION CALLS AND NOT CONTENT FROM YOURSELF. 
STRICTLY FOLLOW ARGUMENT NAMES PROVIDED ALONG WITH THE FUNCTIONS AND THOSE SPECIFIED IN REQUIRED

Do not provide code to do a function, instead use of the below functions given to you to perform the task

You have the following functions to you to work with it
{"name":"saveFile" ,
"description" : "Creates and saves the file in the destination location with specified content", 
"arguments" : {
    "path": file path,
    "content": content to be written in the file,
    }
}

{"name":"editFile",
"description": "Edits the file in the specified location with new content",
"arguments":{
    "path" : file path,
    "content" : Content to be overwritten in the file,
    }
}

{
    "name":"deleteFile",
    "description": "Deletes the specified file from the system",
    "arguments" : {
        "path" : file path
    }
}

{
    "name":"deleteTempFiles",
    "description": "Deletes the TEMPORARY files from the system",
    "arguments" : {
        
    }
}

{
    "name":"controlBrightness",
    "description": "Controls the BRIGHTNESS level of screen",
    "arguments" : {
        "intensity": Choose a number from 0-100. Select a number according to the user requirement
    }
}

{
    "name":"MusicControl",
    "description": "Controls the music system on the PC",
    "arguments" : {
        "action": "play","add","pause","resume","next","previous". Select any option as per user query,
        "song" : Name of the song that will get played or add into the queue,
    }
}

{
    "name":"sendGmail",
    "description": "Used to send Mails/Gmails to people",
    "arguments" : {
        "receiver": The mail id of the person whom the mail should be sent,
        "subject" : The main topic of the sent Mail in 1-2 words,
        "cc" : The mail id of the person who should be included in cc of the mail,
        "bcc" : The mail id of the person who should be included in bcc of the mail,
        "message" : The content of the mail to be sent,
    }
}

**sendWhatsappMessage** : Sends a WHATSAPP message to the specified person with Phone Number

"""

#Definig Functions to be used with Chatgpt
gpt_functions = [
        {

            "name": "deleteFile",
            "description": "Deletes the specified file from the system. Always use this function when user wants to delete files from the system ",
            "parameters":{
                "type": "object",
                "properties":{
                    "path": {
                        "type": "string",
                        "description" : "The file path to be deleted from the system ex, 'D:\\hii\\abc.txt'. Note that file path should be divided by '//'",
                    }
                },
                "required": ["file_path"],
            },
            "name": "saveFile",
            "description": SAVE_FILE_DESCRIPTION,
            "parameters":{
                "type": "object",
                "properties":{
                    "**content**": {
                        "type": "string",
                        "description" : "The Content to be written in the file ex, Hello from Vedant",
                    },
                    "**path**": {
                        "type": "string",
                        "description" : "The path onto which the system should save the file ex, 'D:\\hii\\abc.txt'. Note that file path should be divided by '//'",
                    }
                },
                "required": ["path","path"],
            },

            "name": "editFile",
            "description": "Edits or Overwrites a file into the system. Use this function when user wants to edit an existing file",
            "parameters":{
                "type": "object",
                "properties":{
                    "path": {
                        "type": "string",
                        "description" : "The file path to be edited or to overwrite in the system ex, 'D:\\hii\\abc.txt'. Note that file path should be divided by '//'",
                    },
                    "content": {
                        "type": "string",
                        "description" : "Content to be written in the file ex, Hello from Vedant",
                    }
                },
                "required": ["path","content"],
            },

            "name": "deleteTempFiles",
            "description": "Deletes specifically temp or temporary files from the system",
            "parameters":{
                "type": "object",
                "properties":{},
                "required": [],
            },

            "name": "controlBrightness",
            "description": "Control the brightness of the System",
            "parameters":{
                "type": "object",
                "properties":{
                    "intensity": {
                        "type": "integer",
                        "description" : "Choose a number from 0-100. Select a number according to the user requirement",
                    },
                },
                "required": ["intensity"],
            },
            
            "name": "MusicControl",
            "description": "Always use the function when user wants to play songs and playlists for the user from Spotify Music app. It takes 2 parametes <<action>> and <<song_name>>",
            "parameters":{
                "type": "object",
                "properties":{
                    "action": {
                        "type": "string",
                        "enum" : ["play","add","pause","resume","next","previous"],
                        "description" : "Use the parameters given according to user query only",
                    },
                    "song":{
                        "type": "string",
                        "description" : "Name of the song that will get played or add into the queue",
                    }
                },
                "required": ["action","song_name"],
            },

            "name": "sendGmail",
            "description": "Used to send Mails/Gmails to people",
            "parameters":{
                "type": "object",
                "properties":{
                    "reciever": {
                        "type": "string",
                        "description" : "The mail id of the person whom the mail should be sent",
                    },
                    "subject": {
                        "type": "string",
                        "description" : "The main topic of the sent Mail in 1-2 words",
                    },
                    "cc":{
                        "type": "string",
                        "description" : "The mail id of the person who should be included in cc of the mail",
                    },
                    "bcc":{
                        "type": "string",
                        "description" : "The mail id of the person who should be included in bcc of the mail",
                    },
                    "message":{
                        "type": "string",
                        "description" : "The content of the mail to be sent",
                    },
                },
                "required": ["reciever","message","subject"],
            },
            
            "name": "sendWhatsappMessage",
            "description": "Used to send a Whatsapp Message to a phonenumber",
            "parameters":{
                "type": "object",
                "properties":{
                    "phoneNumber": {
                        "type": "string",
                        "description" : "The Phone Number of the Person whom the text should be sent",
                    },
                    "message": {
                        "type": "string",
                        "description" : "The message to be sent to the receiver",
                    }
                },
                "required": ["phoneNumber","message"],
            },
        }
    ]

def askGPT(msg):
    send_msg = [{"role": "system", "content": SYSTEM_PROMPT}]
    user_input = msg

    #Creating the message to be passed to the gpt
    for i,j in zip(user_history, response_history):
        send_msg.append({"role": "user", "content": i})
        send_msg.append({"role": "assistant", "content": j})

    send_msg.append({"role": "user", "content": user_input})
    
    print(f"Send MSG {send_msg}\n\n")
    #print(f"Send User {user_history}")
    #print(f"Send Response {response_history}")

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = send_msg,
        functions = gpt_functions,
        function_call = "auto",
    )
    
    print(f"Response f{response}\n\n")
    gpt_response = response["choices"][0]["message"]["content"]
    response = response["choices"][0]["message"]
    
    if response.get("function_call"):
        available_functions = {
            "getTime" : getTime,
            "getDay" : getDay,
            "getDate" : getDate,
            "searchWikipedia" : searchWikipedia,
            "searchGoogle" : searchGoogle,
            "searchYoutube" : searchYoutube,
            "saveFile" : saveFile,
            "editFile" : editFile,
            "deleteFile" : deleteFile,
            "deleteTempFiles" : deleteTempFiles,
            "controlBrightness" : controlBrightness,
            "MusicControl" : MusicControl,
            "sendGmail" : sendGmail,
            "sendWhatsappMessage" : sendWhatsappMessage,
        }
        function_name = response["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response["function_call"]["arguments"])
        print(f"Function Arguments f{function_args}\n\n")
        function_response = function_to_call(function_args)
        print(f"Function Response f{function_response}\n\n")
        response_history.append(f"{function_name} Function was used to answer the query")
        
    else:
        print(f"GPT RESPONSE: f{gpt_response}\n\n")
        response_history.append(gpt_response)
        
        
    user_history.append(user_input)

    #Limiting The Values to MemVar variable
    if len(user_history) == mem_var:
        user_history.pop(0)
    if len(response_history) == mem_var:
        response_history.pop(0)
  
#askGPT("Play Maharani Song")
"""
You are a helpful assistant with functions to help user in local system. Always use the provided functions given to you to answer most of the questions.
Only use functions that you are provided with.

ONLY PROVIDE FUNCTION CALLS AND NOT CONTENT FROM YOURSELF. 
STRICTLY FOLLOW ARGUMENT NAMES PROVIDED ALONG WITH THE FUNCTIONS AND THOSE SPECIFIED IN REQUIRED

Do not provide code to do a function, instead use of the below functions given to you to perform the task

You have the following functions to you to work with it
**saveFile** : Creates and saves the file in the destination location with specified content
**editFile** : Edits the file in the specified location with new content
**deleteFile** : Deletes the file from the specified location from the computer
**deleteTempFiles** : Deleted all the TEMPORARY FILES from the System
**controlBrightness** : Controls the BRIGHTNESS level of screen
**MusicControl** : Controls the MEDIA PLAYER and MUSIC on the pc
**sendGmail** : Sends a GMAIL to the specified person with Specified content
**sendWhatsappMessage** : Sends a WHATSAPP message to the specified person with Phone Number

"""