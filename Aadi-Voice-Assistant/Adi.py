import customtkinter as ctk
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import threading
import datetime
import psutil
import numpy as np
from dotenv import load_dotenv
from groq import Groq



load_dotenv()
is_listening=False
pulse_value=0
voice_level=0
#API_masking
client=Groq(api_key=os.getenv("GROQ_API_KEY"))
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("600x650")
app.title("Adi Assistant")

title = ctk.CTkLabel(app, text="Adi", font=("Arial", 30))
title.pack(pady=20)

status_label = ctk.CTkLabel(app, text="Click Start Assistant", font=("Arial", 16))
status_label.pack(pady=10)
#animation

canvas = ctk.CTkCanvas(app, width=300, height=300, bg="black", highlightthickness=0)
canvas.pack(pady=20)

glow_circle=canvas.create_oval(90, 90, 210, 210, outline="#00ffff", width=2)
circle = canvas.create_oval(100, 100, 200, 200, outline="#00ffff", width=4)
angle=0
rotating_arc=canvas.create_arc(
    70, 70, 230, 230,
    start=0,
    extent=60,
    outline="#00ffff",
    style="arc",
    width=3
)
# pulse_value = 0
# pulse_direction = 1
# is_listening = False

def animate():
    global pulse_value, voice_level, is_listening, angle

    if is_listening:
     pulse_value = voice_level

     canvas.coords(circle,
                  100 - pulse_value,
                  100 - pulse_value,
                  200 + pulse_value,
                  200 + pulse_value)

     canvas.coords(glow_circle,
                  90 - pulse_value,
                  90 - pulse_value,
                  210 + pulse_value,
                  210 + pulse_value)

     canvas.itemconfig(circle, outline="#00ffff")
     canvas.itemconfig(glow_circle, outline="#00ffff")

    else:
      canvas.itemconfig(circle, outline="#444444")
      canvas.itemconfig(glow_circle, outline="#222222")
    angle+=5
    canvas.itemconfig(rotating_arc, start=angle)
    app.after(30, animate)
animate()

output_box = ctk.CTkTextbox(app, width=500, height=150)
output_box.pack(pady=20)
def boot_sequence():
    output_box.insert("end", "Initializing Adi System....\n")
    app.update()
    app.after(500)

    output_box.insert("end", "Loading voice Engine....\n")
    app.update()
    app.after(500)

    output_box.insert("end", "Connecting....\n")
    app.update()
    app.after(500)

    output_box.insert("end", "System Ready....\n")
    app.update()

    #start

def start_assistant():
    boot_sequence()
    threading.Thread(target=assistant, daemon=True).start()

start_button = ctk.CTkButton(app, text="Start Assistant", command=start_assistant)
start_button.pack(pady=20)



def speak(text):
    try:
        output_box.insert("end", "Adi: " + text + "\n")
        output_box.see("end")
        engine = pyttsx3.init("sapi5")
        engine.setProperty("rate", 170)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("Voice error:", e)


#listening
def take_command():
    global is_listening, voice_level
    r = sr.Recognizer()
    r.energy_threshold=300
    r.dynamic_energy_threshold=True
    r.pause_threshold = 0.8
    #volume
    with sr.Microphone() as source:
        is_listening=True
        status_label.configure(text="Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source)
            audio_data=np.frombuffer(audio.frame_data,dtype=np.int16)
            voice_level=int(np.abs(audio_data).mean()/500)
            voice_level=min(voice_level,25)
        except:
            is_listening=False
            return None
    is_listening = False
    status_label.configure(text="processing")
    try:
        command = r.recognize_google(audio, language="en-IN")
        output_box.insert("end", "You: " + command + "\n")
        output_box.see("end")
        return command.lower()
    except sr.UnknownValueError:
        #speak("I didn't catch that")
        return None
    except sr.RequestError:
        speak("Internet connection Issue")
        return None
#working with ai
def ask_ai(prompt):
    try:
        responce=client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                  "role": "system",
                   "content": "you are a smart assistant named aadi. reply briefly in 2-3 sentences"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return responce.choices[0].message.content
    except Exception as e:
        print("AI error",e)
        return "there was a problem connecting to ai"
    

def assistant():
    speak("System Ready")

    while True:
        command = take_command()

        if command is None:
            continue
        
        if "open" in command:
            app_name = command.replace("open", "").strip()

            apps = {
                "chrome": "chrome",
                "notepad": "notepad",
                "calculator": "calc",
                "paint": "mspaint",
                "vs code": "code",
                "vscode": "code",
                "explorer": "explorer",
                "file explorer": "explorer"
            }

            if app_name in apps:
                speak(f"Opening {app_name}")
                os.system(f"start {apps[app_name]}")
            else:
                speak("Application not found")

        
        elif "search" in command:
            query = command.replace("search", "").strip()
            speak("Searching " + query)
            webbrowser.open(f"https://google.com/search?q={query}")
            #battery

        elif "battery" in command:
            battery=psutil.sensors_battery()
            persent=battery.percent
            speak(f"Battery is at {persent} persent")

        #shutdown

        elif "shutdown" in command:
            speak("shuting down the system")
            os.system("shutdown /s /t 1")
            
            #restart

        elif "restart" in command:
            speak("restarting the system")
            os.system("shutdown /r /t 1")

        elif "lock" in command:
            speak("locking down the system")
            os.system("rundll32.exe user32.dll,LockWorkStation")
        #greeting
        elif "aadi"  in command:
         speak("Yes?,I'm here for your assistance")

        elif "time" in command:
            now = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {now}")

        elif "date" in command:
            Today = datetime.datetime.now().date()
            day=datetime.datetime.now().strftime("%A")
            speak(f"Today is {day} and the date is {Today}")
        
        elif "exit" in command:
            speak("Goodbye")
            os._exit(0)
        
        else:
            response=ask_ai(command)
            speak(response)


app.mainloop()
