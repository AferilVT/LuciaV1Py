# Voice Setup Guide for Lucia

This guide will help you set up voice functionality for Lucia Discord bot.

## Prerequisites

### 1. FFmpeg Installation

**Windows:**
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract to a folder (e.g., `C:\ffmpeg`)
3. Add `C:\ffmpeg\bin` to your system PATH
4. Restart your terminal/command prompt

**Alternative for Windows:**
```bash
# Using Chocolatey
choco install ffmpeg

# Using Scoop
scoop install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 2. Python Dependencies

Install the required Python packages:

```bash
# Install all dependencies
pip install -r requirements.txt

# Or use the helper script
python install_speech_deps.py
```

### 3. Voice-Specific Dependencies

The following packages are required for voice functionality:

- **PyNaCl**: Voice encoding/decoding
- **ffmpeg-python**: Audio processing
- **SpeechRecognition**: Speech-to-text (optional)
- **pyaudio**: Audio input/output (optional)
- **openai-whisper**: Advanced speech recognition (optional)

## Troubleshooting Voice Issues

### Common Error: "ConnectionClosed: Shard ID None WebSocket closed with 4006"

**Causes:**
1. Missing FFmpeg installation
2. Missing PyNaCl package
3. Network connectivity issues
4. Discord API rate limiting

**Solutions:**
1. **Install FFmpeg** (see above)
2. **Install PyNaCl:**
   ```bash
   pip install PyNaCl
   ```
3. **Check your internet connection**
4. **Wait a few minutes** and try again (rate limiting)

### Common Error: "No module named 'nacl'"

**Solution:**
```bash
pip install PyNaCl
```

### Common Error: "FFmpeg not found"

**Solution:**
1. Install FFmpeg (see above)
2. Ensure FFmpeg is in your system PATH
3. Restart your terminal/command prompt

### Windows-Specific Issues

**If you get errors installing pyaudio:**
```bash
# Try using pipwin
pip install pipwin
pipwin install pyaudio
```

**If you get Visual C++ errors:**
1. Install Visual Studio Build Tools
2. Or download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

## Testing Voice Functionality

1. **Start the bot:**
   ```bash
   cd src
   python main.py
   ```

2. **Test voice commands:**
   - `/join` - Join a voice channel
   - `/leave` - Leave voice channel
   - `/record_start` - Start recording
   - `/record_stop` - Stop recording
   - `/transcribe_live` - Start live transcription

3. **Check logs** for any errors in `logs/lucia.log`

## Bot Permissions

Ensure your bot has these permissions:
- **Connect** - Join voice channels
- **Speak** - Transmit audio
- **Use Voice Activity** - Detect when users speak
- **Attach Files** - Send audio files

## Still Having Issues?

1. **Check the logs** in `logs/lucia.log`
2. **Verify FFmpeg installation:**
   ```bash
   ffmpeg -version
   ```
3. **Test PyNaCl:**
   ```python
   import nacl
   print("PyNaCl installed successfully")
   ```
4. **Restart the bot** after installing dependencies

## Support

If you're still experiencing issues:
1. Check the error logs
2. Ensure all dependencies are installed
3. Verify FFmpeg is in your PATH
4. Try running the bot in a different voice channel 