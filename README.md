# 🎵 Discord Music Selfbot
A simple **Discord selfbot music player** written in Python using `discord.py-self`, `yt-dlp`, and FFmpeg.  
Supports **YouTube playback**, **song queuing**, and basic music controls.

> ⚠ **WARNING**
> This project uses a **Discord selfbot**, which **violates Discord’s Terms of Service**.
> Use at your own risk..

---

## 📦 Requirements

- Python **3.9+**
- FFmpeg
- Discord token (**NOT** a bot token)

---

## 🔧 Installation

### 1️⃣ Install discord.py-self
```bash
pip install -U --no-cache-dir git+https://github.com/dolfies/discord.py-self@master
```

### 2️⃣ Install dependencies
```bash
pip install yt-dlp
```

### 3️⃣ Download FFmpeg
Download FFmpeg from:
https://ffmpeg.org/download.html

Place `ffmpeg.exe` inside a `bin` folder:

```
project/
├── bin/
│   └── ffmpeg.exe
├── main.py
```

---

## 🎶 Commands

| Command | Description |
|-------|------------|
| `!play <url>` | Plays a YouTube song or adds it to the queue |
| `!skip` | Skips the currently playing song |
| `!stop` | Stops playback and clears the queue |
| `!queue` | Displays the current queue |
| `!leave` | Leaves the voice channel |
| `!help` | Shows the help message |

---

## 📚 Disclaimer
I am **not** responsible for bans, account restrictions, or misuse.
