import openai
import os
import pyttsx3
import AppOpener
import urllib.request
import speech_recognition as sr
from playsound import playsound
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAIAPI")
internet = False



def ask_question(question):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=question,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response.choices[0].text


def speak(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


def checkInternet():
    url = "http://www.google.com"
    try:
        urllib.request.urlopen(url)
        return True
    except urllib.error.URLError:
        speak("By the way, before you ask any questions, I see that you are not connected to the internet or there is a connection problem.")
        speak("I cannot answer any of your questions without internet. So please try again, after ensuring strong internet connection.")
        playsound("end.mp3")
        return False


def startAssistant():
    while internet == True:
        r = None
        r = sr.Recognizer()
        r.pause_threshold = 1
        r.energy_threshold = 300
        with sr.Microphone() as source:
            playsound("start.mp3")
            print("Listening...")
            audio = r.listen(source)

        continueQuestion = True
        try:
            print("Recognizing...")
            question = r.recognize_google(audio)
            print("\nYou: "+question.lower())
            if question == ("no" or "NO" or "No"):
                continueQuestion = False
            elif question.lower() == ("open whatsapp"):
                speak("Opening Whatsapp")
                AppOpener.open("whatsapp")
            elif question.lower() == ("open chrome" or "open google chrome"):
                speak("Opening Google Chrome")
                AppOpener.open("google chrome")
                playsound("end.mp3")
                break
        except sr.UnknownValueError:
            speak("No audio detected!")
            continueQuestion = False
        except sr.RequestError as e:
            speak("Could not request results from Google Speech Recognition service")
            continueQuestion = False

        if continueQuestion == True:
            response = ask_question(question)
            print("\nFriday: "+response)
            speak(str(response))
            r = None
        else:
            playsound("end.mp3")
            break


playsound("start.mp3")
speak("Hello, I am Friday, you can ask me any questions if you want, say no to quit the program.")
# while True:
#     r = sr.Recognizer()
#     r.pause_threshold = 1
#     r.energy_threshold = 300
#     with sr.Microphone() as source:
#         phrase = r.listen(source)
#     try:
#         text = r.recognize_google(phrase)
#         r = None
#         if text.lower() == ("ok robin" or "Ok Robin" or "ok Robin"):
#             print("Input Received Successfully!\r")
internet = checkInternet()
startAssistant()
r = None
    # except sr.UnknownValueError:
    #     print("Retrying!")
    #     continue
