# robo-queue

A queue management system built for Robotics competition preparation.

Built with **Tkinter** for the GUI, **Pygame** for audio playback, and **pyttsx3** (Windows) / `say` (macOS) for text-to-speech announcements.

No more screaming names across the hall until your voice disappears.

---

## Features

- Automatic voice announcements
- Alert sound before every call
- 15-second arrival timer
- 90-second testing timer
- Add competitors to the queue
- Skip the current stage
- Skip an entire competitor (moves them to Missed Queue)
- Missed Queue tracking
- Automatic and Manual calling modes
- Large display suitable for TVs or projectors

---

## Installing

As a wise ShitHub user once said:

> "WHY IS THERE CODE??? MAKE A .EXE FILE!"

Unfortunately...

...this is Python.

Clone the repository:

```bash
git clone https://github.com/Xia-Qi2450/robo-queue
cd robo-queue
pip install -r requirements.txt
python robo-queue_youros.py
```

Enjoy!

---

## How to use

1. Enter a competitor's name into the text box.
2. Press **Add Name**.
3. The queue will begin automatically if Auto Mode is enabled.

Buttons:

- ➕ **Add Name** — Add a competitor.
- ⏭️ **Skip** — Skip the current stage only.
- ❌ **Skip Person** — Skip the competitor entirely and move them to the Missed Queue.
- 📣 **Manual Call** — Start the next competitor manually.
- 🔄 **Mode** — Switch between Auto and Manual modes.

---

## Audio

Place an `alert.mp3` file in the project root.

This sound is played before each competitor is announced.

---

## Intended Use

Originally made for personal use during preparations for Robotics competitions, but honestly it'll work anywhere you need to repeatedly shout people's names without actually shouting people's names. Just edit the text and the say functions.

---
## Screenshots
The Tkinter GUI
<img width="1112" height="744" alt="image" src="https://github.com/user-attachments/assets/a2e54e0a-f146-4871-a295-bfa81a06958e" />

<small>REMEMBER YOUR `alert.mp3` OR THIS WILL HAPPEN</small>
<img width="1722" height="1080" alt="image" src="https://github.com/user-attachments/assets/d0ce657b-7752-4e37-b927-8d4b3f4639e4" />


