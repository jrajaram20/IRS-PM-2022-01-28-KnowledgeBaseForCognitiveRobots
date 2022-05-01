import pyttsx3
from intentpredict import chat1
import time
import speech_recognition as sr

def chat():
    #engine = pyttsx3.init() 
    #i = 0
    #while(i<20):
    with sr.Microphone() as source:
        print('Speak now')
        r1=sr.Recognizer()
        audio =r1.listen(source)
        try:
            text=r1.recognize_google(audio)
            print(text)
            c1 = chat1()
            getr = c1.chatbot_response(text)
            print(getr[1])
            return getr[1]
            # initialisation 
            #engine.say(getr)
            #engine.runAndWait()
            
        except:
            return "Sorry unable to understand"
            print(text)

if __name__ == "__main__":
    chat()