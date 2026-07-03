import tkinter as tk
from tkinter import messagebox
import threading
import time
import pygame
import pyttsx3
import queue

tts_queue = queue.Queue()

# Initialize pygame mixer for sound
pygame.mixer.init()
def play_sound():
    pygame.mixer.Sound("alert.mp3").play()

# Initialize TTS engine
def speak(text, delay):
    time.sleep(delay)
    def do_speak():
        engine = pyttsx3.init()
        engine.setProperty('rate', 170)
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    threading.Thread(target=do_speak, daemon=True).start()

# Globals
queue = []
missed = []
current_name = ""
mode = "auto"  # "auto" or "manual"
stage = 0      # 0 = idle, 1 = arrival, 2 = testing
timer_id = 0

# ---- Window Setup ----
root = tk.Tk()
root.title("Robotics Queue System")
root.geometry("1000x600")
root.configure(bg="black")

# ---- Display Frame (Left) ----
display = tk.Frame(root, bg="black")
display.pack(side="left", fill="both", expand=True, padx=10, pady=10)

# Current name
current_label = tk.Label(display, text="Waiting...", font=("Arial", 48, "bold"), fg="white", bg="black")
current_label.pack(pady=20)

# Timer
timer_label = tk.Label(display, text="", font=("Arial", 24), fg="yellow", bg="black")
timer_label.pack(pady=10)

# Next in queue
queue_label = tk.Label(display, text="Next:\n(Empty)", font=("Arial", 20), fg="lightgray", bg="black", justify="left")
queue_label.pack(pady=10)

# Marquee area
marquee_text = tk.StringVar(value="⚠ Important: Please be ready when your name is called. ❌ Missed Qs will not be recalled! ")
marquee = tk.Label(display, textvariable=marquee_text, font=("Arial", 16), fg="cyan", bg="black")
marquee.pack(side="bottom", pady=10)

def scroll_marquee():
    text = marquee_text.get()
    marquee_text.set(text[1:] + text[0])
    root.after(100, scroll_marquee)

scroll_marquee()

# ---- Control Panel (Right) ----
panel = tk.Frame(root, bg="gray20", width=300)
panel.pack(side="right", fill="y", padx=10, pady=10)

entry = tk.Entry(panel, font=("Arial", 14))
entry.pack(pady=10, fill="x")

def add_name():
    name = entry.get().strip()
    if name:
        queue.append(name)
        entry.delete(0, tk.END)
        update_display()
        if len(queue) == 1 and mode == "auto":
            start_stage(name)

tk.Button(panel, text="➕ Add Name", font=("Arial", 14), command=add_name).pack(pady=5, fill="x")

def skip_person():
    global stage, current_name
    stop_timer()
    
    if stage == 1:
        # Skip arrival, go directly to testing
        start_testing(current_name)
    elif stage == 2:
        # Skip testing, go directly to next person
        handle_next()
    else:
        # If idle, do nothing
        timer_label.config(text="Nothing to skip.")
    
def skip_entire_person():
    global timer_id, current_name
    if current_name:
        missed.append(current_name)
    current_name = ""
    stop_timer()
    if queue:
        queue.pop(0)
    update_display()
    if mode == "auto" and queue:
        start_stage(queue[0])
    else:
        current_label.config(text="Waiting...")
        timer_label.config(text="Manual Mode – Click to start")


tk.Button(panel, text="⏭️ Skip", font=("Arial", 14), command=skip_person).pack(pady=5, fill="x")
tk.Button(panel, text="❌ Skip Person", font=("Arial", 14), command=skip_entire_person).pack(pady=5, fill="x")


def call_manually():
    if queue:
        start_stage(queue[0])

tk.Button(panel, text="📣 Manual Call", font=("Arial", 14), command=call_manually).pack(pady=5, fill="x")

def toggle_mode():
    global mode
    mode = "manual" if mode == "auto" else "auto"
    mode_button.config(text=f"Mode: {mode.title()}")

mode_button = tk.Button(panel, text="Mode: Auto", font=("Arial", 14), command=toggle_mode)
mode_button.pack(pady=5, fill="x")

missed_label = tk.Label(panel, text="Missed Queue:\n(Empty)", font=("Arial", 12), fg="white", bg="gray20", justify="left")
missed_label.pack(pady=10)

# ---- Core Functions ----

def update_display():
    queue_text = "Next:\n" + "\n".join(queue[:5]) if queue else "Next:\n(Empty)"
    queue_label.config(text=queue_text)

    missed_text = "Missed:\n" + "\n".join(missed[-5:]) if missed else "Missed:\n(Empty)"
    missed_label.config(text=missed_text)

def stop_timer():
    global timer_id
    timer_id += 1  # invalidates old timers

def start_stage(name):
    global stage, timer_id, current_name
    current_name = name
    timer_id += 1
    this_id = timer_id
    stage = 1

    def arrival():
        time_left = 15
        while time_left > 0 and this_id == timer_id:
            timer_label.config(text=f"{name} → Go to mat: {time_left}s")
            time.sleep(1)
            time_left -= 1
        if this_id == timer_id:
            start_testing(name)

    threading.Thread(target=arrival, daemon=True).start()
    current_label.config(text=f"Now Calling:\n{name}")
    timer_label.config(text="Starting Arrival Timer...")
    play_sound()
    speak(f"{name}, please proceed to the mat.", 1)

def start_testing(name):
    global stage, timer_id
    timer_id += 1
    this_id = timer_id
    stage = 2

    def testing():
        time_left = 90
        while time_left > 0 and this_id == timer_id:
            timer_label.config(text=f"{name} is testing: {time_left}s left")
            time.sleep(1)
            time_left -= 1
        if this_id == timer_id:
            handle_next()

    threading.Thread(target=testing, daemon=True).start()
    current_label.config(text=f"Testing:\n{name}")
    play_sound()
    speak(f"{name}, your testing time starts now.", 1)

def handle_next():
    global current_name
    stop_timer()
    if queue:
        current_name = ""
        queue.pop(0)
        update_display()
        if mode == "auto":
            start_stage(queue[0])
        else:
            current_label.config(text="Waiting...")
            timer_label.config(text="Manual Mode – Click to start")

# ---- Run App ----
update_display()
root.mainloop()
