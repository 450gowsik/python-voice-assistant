import datetime
import pyttsx3
import speech_recognition as sr
import wikipedia
from wikipedia import search
import webbrowser
import os
import time
import warnings

# Suppress wikipedia parser warnings
warnings.filterwarnings("ignore", category=UserWarning)

# ================= TEXT TO SPEECH =================
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)   # Female voice
engine.setProperty('rate', 170)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.4)

# ================= GREETING =================
def wishMe():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning")
    elif hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("Hello, I am Jarvis. How can I help you")

# ================= VOICE INPUT =================
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.6)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("You:", query)
        return query.lower().strip()
    except:
        return ""

# ================= WEBSITE MAP =================
sites = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "amazon": "https://www.amazon.in",
    "flipkart": "https://www.flipkart.com",
    "gmail": "https://mail.google.com",
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
    "linkedin": "https://www.linkedin.com",
    "zomato": "https://www.zomato.com",
    "swiggy": "https://www.swiggy.com",
    "sbi login": "https://retail.onlinesbi.sbi/retail/login.htm"
}

# ================= MAIN =================
if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand()
        if query == "":
            continue

        # ----- HUMAN CONVERSATION -----
        if any(x in query for x in ["how are you", "how r you", "how are you doing"]):
            speak("I am doing well. Thank you for asking")

        elif any(x in query for x in ["who are you", "your name"]):
            speak("I am Jarvis, your personal voice assistant")

        elif any(x in query for x in ["what can you do", "your features"]):
            speak("I can talk with you, open websites, search Wikipedia, and help you offline")

        elif "thank you" in query:
            speak("You are welcome")

        # ----- TIME -----
        elif "time" in query:
            time_now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {time_now}")

        # ----- WIKIPEDIA / WIKI / TELL ME ABOUT -----
        elif query.startswith("wikipedia") or query.startswith("wiki") or "tell me about" in query:
            speak("Searching Wikipedia")

            topic = query.replace("wikipedia", "") \
                         .replace("wiki", "") \
                         .replace("tell me about", "") \
                         .strip()

            if topic == "":
                speak("Please say the topic name")
                continue

            try:
                results = search(topic)
                if not results:
                    speak("Sorry, I could not find information on that topic")
                    continue

                page = wikipedia.page(results[0])
                summary = wikipedia.summary(page.title, sentences=2)

                speak(f"According to Wikipedia. {summary}")
                webbrowser.open(page.url)

            except Exception as e:
                speak("Sorry, I could not fetch that information")
                print("DEBUG:", e)

        # ----- OPEN WEBSITE -----
        elif query.startswith("open"):
            site_name = query.replace("open", "").strip()
            if site_name in sites:
                speak(f"Opening {site_name}")
                webbrowser.open(sites[site_name])
            else:
                speak(f"Searching {site_name} on Google")
                webbrowser.open("https://www.google.com/search?q=" + site_name)

        # ----- EXIT -----
        elif any(x in query for x in ["exit", "stop", "bye"]):
            speak("Goodbye. Have a nice day")
            break

        # ----- DEFAULT -----
        else:
            speak("I am still learning. Please try another command")
