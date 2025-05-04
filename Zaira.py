import os
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import pyautogui
import pywhatkit
import psutil
import pyjokes
import threading
import tkinter as tk
from tkinter import messagebox

# root = tk.Tk()

# Initialize voice engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

stop_listening = False  # Flag for stopping assistant

def speak(text):
    print("Zaira:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print("You:", command)
        return command
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Sorry, the service is down.")
        return ""

def detect_wake_word():
    print("Listening for 'hey zaira'...")
    command = listen()
    if "hey zaira" in command:
        speak("Yes, I'm listening.")
        return True
    return False

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Zaira, your AI assistant. How can I help you?")

def open_file_or_folder(name):
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    for root, dirs, files in os.walk(desktop):
        for item in dirs + files:
            if name.lower() in item.lower():
                path = os.path.join(root, item)
                os.startfile(path)
                return
    speak("I couldn't find that on the desktop.")

def notepad_write(text):
    os.system('start notepad')
    pyautogui.sleep(2)
    pyautogui.write(text)

def system_control(command):
    if "shutdown" in command:
        os.system("shutdown /s /f /t 1")
    elif "restart" in command:
        os.system("shutdown /r /f /t 1")
    elif "logout" in command:
        os.system("shutdown /l")
    elif "sleep" in command:
        os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")

def run_zaira():
    global stop_listening
    wish()
    while not stop_listening:
        if detect_wake_word():
            command = listen()

            if "wikipedia" in command:
                speak("Searching Wikipedia...")
                query = command.replace("wikipedia", "").strip()
                if not query:
                    speak("What should I search on Wikipedia?")
                    query = listen()

                try:
                    result = wikipedia.summary(query, sentences=2)
                    speak(result)
                except wikipedia.exceptions.DisambiguationError:
                    speak("Your search term is ambiguous. Please be more specific.")
                except wikipedia.exceptions.PageError:
                    speak("Sorry, I couldn't find any page with that title.")
                except Exception:
                    speak("Sorry, an error occurred while searching Wikipedia.")

            elif "open" in command and "folder" in command:
                folder_name = command.replace("open folder", "").strip()
                open_file_or_folder(folder_name)

            elif "open" in command:
                file_name = command.replace("open", "").strip()
                open_file_or_folder(file_name)

            elif "search" in command:
                # query = command.replace("search", "").strip()
                # webbrowser.open(f"https://www.google.com/search?q={query}")
                speak("What should I search for?")
                query = listen()
                if query:
                    speak(f"Searching for {query} on Google...")
                    pywhatkit.search(query)
                else:
                    speak("I didn't catch that. Please try again.")

            elif "play music" in command:
                speak("What song do you want to hear?")
                song = listen()
                pywhatkit.playonyt(song)

            elif "play" in command and "youtube" in command:
                song = command.replace("play", "").replace("from youtube", "").strip()
                pywhatkit.playonyt(song)

            elif "notepad" in command:
                speak("What should I write?")
                text = listen()
                notepad_write(text)

            elif "shutdown" in command or "restart" in command or "logout" in command or "sleep" in command:
                system_control(command)

            elif "battery" in command:
                battery = psutil.sensors_battery()
                speak(f"Battery is at {battery.percent} percent.")

            elif "time" in command:
                time_now = datetime.datetime.now().strftime('%I:%M %p')
                speak(f"The time is {time_now}")

            elif "joke" in command:
                joke = pyjokes.get_joke()
                speak(joke)

            elif "exit" in command or "quit" in command:
                speak("Do you really want to close the application?")
                confirm = listen()
                if "yes" in confirm or "close" in confirm:
                    speak("Closing now. Goodbye!")
                    engine.stop() # <-- Safely stop pyttsx3
                    app.quit()  # <-- this closes the GUI window
                    break
                else:
                    speak("Okay, staying active.")


            elif command != "":
                speak("Sorry, I can't do that yet.")

# GUI with Tkinter
def start_zaira():
    global stop_listening
    stop_listening = False
    threading.Thread(target=run_zaira).start()
    status_var.set("Zaira is active...")

def stop_zaira():
    global stop_listening
    stop_listening = True
    status_var.set("Zaira has stopped.")

app = tk.Tk()
app.title("Zaira - Voice Assistant")
app.geometry("400x300")
app.configure(bg="#282c34")

status_var = tk.StringVar()
status_var.set("Zaira is idle...")

tk.Label(app, text="Zaira - AI Voice Assistant", font=("Arial", 16), bg="#282c34", fg="white").pack(pady=20)
tk.Button(app, text="Start Zaira", command=start_zaira, width=20, bg="#61afef", fg="black", font=("Arial", 12)).pack(pady=10)
tk.Button(app, text="Stop Zaira", command=stop_zaira, width=20, bg="#e06c75", fg="black", font=("Arial", 12)).pack(pady=10)
tk.Label(app, textvariable=status_var, bg="#282c34", fg="white", font=("Arial", 10)).pack(pady=20)

app.mainloop()
