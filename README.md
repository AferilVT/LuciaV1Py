# Lucia Discord Bot

A modern, robust Discord bot with music, AI, speech-to-text, and more. Designed for easy deployment as both a Python script and a Windows EXE.

## Features
- Music playback and playlist management
- AI chat (Ollama integration)
- **Speech-to-text transcription** (Whisper & Google Speech Recognition)
- Real-time voice channel transcription
- Voice message transcription
- Slash commands and modern Discord features
- Robust logging and error handling

## Setup

### 1. Clone the Repository
```
git clone https://github.com/AferilVT/LuciaV1Py.git
cd LuciaV1Py
```

### 2. Python Environment
- Python 3.10+
- Install dependencies:
```
pip install -r requirements.txt
```

### 3. Speech Recognition Setup (Optional)
For speech-to-text functionality, install additional dependencies:
```
python install_speech_deps.py
```

**Note for Windows users:** You may need to install Visual C++ Build Tools for `pyaudio`:
- Download from Microsoft Visual Studio Build Tools
- Or use: `pip install pipwin` then `pipwin install pyaudio`

### 4. .env File
Create a `.env` file in the **project root** (next to README.md):
```
TOKEN=your_discord_bot_token_here
```

### 5. Run the Bot (Python)
```
cd src
python main.py
```

### 6. Build and Run as EXE (Optional)
- Use PyInstaller or your preferred tool to build an EXE from `src/main.py`.
- Place the EXE in any folder. The bot will always look for `.env` and write logs in the project root.

### 7. Logs
- Logs are written to `logs/lucia.log` in the project root.

## Speech-to-Text Commands

### `/transcribe`
Transcribe an audio file or the most recent recording.
- **Usage:** `/transcribe [file]`
- **File:** Optional audio file attachment
- If no file provided, uses the most recent recording from `/record_start`

### `/transcribe_live`
Start real-time transcription in a voice channel.
- **Usage:** `/transcribe_live`
- **Requirements:** You must be in a voice channel
- Transcribes speech in real-time and posts to the text channel

### `/transcribe_stop`
Stop real-time transcription.
- **Usage:** `/transcribe_stop`
- **Requirements:** You must be in the voice channel being transcribed

### `/transcribe_voice_message`
Transcribe the most recent voice message in the channel.
- **Usage:** `/transcribe_voice_message`
- Automatically finds and transcribes voice messages from recent messages

### `/auto_transcribe`
Enable automatic transcription for all voice channels.
- **Usage:** `/auto_transcribe`
- **Effect:** Bot automatically starts transcribing when someone joins any voice channel
- **Output:** Sends transcriptions to the general text channel

### `/disable_auto_transcribe`
Disable automatic transcription.
- **Usage:** `/disable_auto_transcribe`
- **Effect:** Stops automatic transcription for the server

### `/transcribe_status`
Check current transcription status.
- **Usage:** `/transcribe_status`
- **Shows:** Auto-transcription status and active transcription channels

## 🎤 Voice-to-Text Features

### **Real-time Transcription**
- **Manual:** Use `/transcribe_live` to start transcription in a specific voice channel
- **Automatic:** Use `/auto_transcribe` to enable automatic transcription for all voice channels
- **Output:** All speech is transcribed and sent to text channels in real-time

### **Smart Channel Detection**
- Automatically finds the best text channel to send transcriptions to
- Prioritizes channels named "general", "chat", or "main"
- Falls back to the first available text channel

### **User Identification**
- Shows the speaker's name with each transcription
- Format: **Username:** "What they said"

### **Dual Engine Support**
- **Whisper** (offline): High-quality transcription using OpenAI's Whisper model
- **Google Speech Recognition** (online): Fallback for when Whisper isn't available

### **Easy Control**
- Start/stop transcription with simple commands
- Check status anytime with `/transcribe_status`
- Enable/disable automatic transcription per server

## Troubleshooting
- **Bot won't start?** Check for errors in the console and `logs/lucia.log`.
- **.env not found?** Ensure `.env` is in the project root, not in `src` or the EXE folder.
- **No DM on startup?** Check Discord permissions and your privacy settings.
- **Speech recognition not working?** 
  - Ensure you've run `python install_speech_deps.py`
  - For Windows, install Visual C++ Build Tools
  - Check that microphone permissions are enabled
- **Still stuck?** Add more logging or contact the maintainer.

---

Happy hacking! 
