import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import os
import tkinter as tk
import random
from threading import Thread
import pyautogui
import smtplib


engine = pyttsx3.init()
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
root = tk.Tk()
root.title("AI Voice Assistant")
root.geometry("700x500")
root.configure(bg="#0f172a")

title = tk.Label(root, text="AI Voice Assistant",
                 font=("Arial", 24, "bold"),
                 fg="cyan", bg="#0f172a")
title.pack(pady=10)

status_label = tk.Label(root, text="Ready",
                        font=("Arial", 14),
                        fg="white", bg="#0f172a")
status_label.pack()

output_box = tk.Text(root, height=10, width=70,
                     bg="#1e293b", fg="white")
output_box.pack(pady=10)

canvas = tk.Canvas(root, width=500, height=120,
                   bg="#0f172a", highlightthickness=0)
canvas.pack()

bars = []

for i in range(25):
    x = 20 + i * 18
    bar = canvas.create_rectangle(x, 60, x + 10, 60,
                                  fill="cyan", outline="")
    bars.append(bar)

wave_running = False

def animate_wave():
    if wave_running:
        for bar in bars:
            h = random.randint(10, 90)
            x1, y1, x2, y2 = canvas.coords(bar)
            canvas.coords(bar, x1, 60 - h/2, x2, 60 + h/2)
    else:
        for bar in bars:
            x1, y1, x2, y2 = canvas.coords(bar)
            canvas.coords(bar, x1, 55, x2, 65)

    root.after(100, animate_wave)

animate_wave()

def speak(text):
    output_box.insert(tk.END, "Assistant: " + text + "\n")
    output_box.see(tk.END)
    engine.say(text)
    engine.runAndWait()
def welcome_user():
     speak("Welcome Muhammad Israr, your assistant is ready")

def take_command():

    global wave_running

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        wave_running = True
        audio = recognizer.listen(source)

    try:
        status_label.config(text="Ready")

        command = recognizer.recognize_google(audio, language='en-US')

        wave_running = False

        output_box.insert(tk.END, "You: " + command + "\n")
        output_box.see(tk.END)

        return command.lower()

    except:
        wave_running = False
        speak("Sorry I did not understand")
        return "none"
    
def run_assistant():

    while True:

        query = take_command()

        # =============================
        # YOUTUBE
        # =============================
        if 'youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        # =============================
        # GOOGLE
        # =============================
        elif 'google' in query:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        # =============================
        # CHATGPT
        # =============================
        elif 'chatgpt' in query:
            speak("Opening ChatGPT")
            webbrowser.open("https://chat.openai.com")

        # =============================
        # GITHUB
        # =============================
        elif 'github' in query:
            speak("Opening GitHub")
            webbrowser.open("https://github.com")

        # =============================
        # LINKEDIN
        # =============================
        elif 'linkedin' in query:
            speak("Opening LinkedIn")
            webbrowser.open("https://linkedin.com")

        # =============================
        # TIME
        # =============================
        elif 'time' in query:
            time = datetime.datetime.now().strftime('%I:%M %p')
            speak(f"The time is {time}")

        # =============================
        # DATE
        # =============================
        elif 'date' in query:
            date = datetime.datetime.now().strftime('%d %B %Y')
            speak(f"Today's date is {date}")

        # =============================
        # WIKIPEDIA
        # =============================
        elif 'wikipedia' in query:
            speak("Searching Wikipedia")

            query = query.replace("wikipedia", "")

            result = wikipedia.summary(query, sentences=2)

            speak("According to Wikipedia")
            speak(result)

        # =============================
        # SEARCH GOOGLE
        # =============================
        elif 'search' in query:
            search_query = query.replace("search", "")
            speak(f"Searching {search_query}")
            webbrowser.open(f"https://www.google.com/search?q={search_query}")

        # =============================
        # PLAY MUSIC
        # =============================
        elif 'play music' in query:
            music_dir = "C:\\Users\\Public\\Music"
            songs = os.listdir(music_dir)

            if songs:
                os.startfile(os.path.join(music_dir, songs[0]))
                speak("Playing music")
            else:
                speak("No music found")

        # =============================
        # JOKE
        # =============================
        elif 'joke' in query:
            speak("Why do programmers prefer dark mode? Because light attracts bugs")

        # =============================
        # HOW ARE YOU
        # =============================
        elif 'how are you' in query:
            speak("I am fine and ready to help you Muhamamd Israr")

        # =============================
        # YOUR NAME
        # =============================
        elif 'your name' in query:
            speak("I am your AI Voice Assistant")

        # =============================
        # SCREENSHOT
        # =============================
        elif 'screenshot' in query:
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")
            speak("Screenshot saved successfully")

        # =============================
        # SHUTDOWN
        # =============================
        elif 'shutdown' in query:
            speak("Shutting down computer")
            os.system("shutdown /s /t 5")

        # =============================
        # RESTART
        # =============================
        elif 'restart' in query:
            speak("Restarting computer")
            os.system("shutdown /r /t 5")

        # =============================
        # SEND EMAIL
        # =============================
        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = take_command()

                sender_email = "your_email@gmail.com"
                sender_password = "your_password"
                receiver_email = "receiver@gmail.com"

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, content)
                server.quit()

                speak("Email sent successfully")

            except Exception as e:
                speak("Sorry, I could not send email")
                print(e)

        # =============================
        # EXIT
        # =============================
        elif 'exit' in query or 'stop' in query:
            speak("Goodbye")
            root.destroy()
            break

        # =============================
        # DEFAULT
        # =============================
        else:
            speak("I did not understand that command")

welcome_user()

def start():
    Thread(target=run_assistant).start()

start()
root.mainloop()
