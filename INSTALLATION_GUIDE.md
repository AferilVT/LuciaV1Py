# Lucia Discord Bot - Complete Installation Guide

This guide will help you restore and set up the Lucia Discord Bot project after a PC reset.

## 📋 Prerequisites

### System Requirements
- **Windows 10/11** (64-bit)
- **Python 3.10+** (for RVC) and **Python 3.11** (for Lucia Bot)
- **Git** (for cloning repositories)
- **Discord Bot Token** (from Discord Developer Portal)
- **8GB+ RAM** (recommended for RVC voice conversion)
- **NVIDIA GPU** (optional, for faster RVC processing)

### Required Software
1. **Miniconda** or **Anaconda** (Python environment manager)
2. **Visual Studio Build Tools** (for PyAudio compilation)
3. **FFmpeg** (for audio processing)

## 🚀 Step-by-Step Installation

### Step 1: Install Python Environment Manager

1. Download and install **Miniconda** from: https://docs.conda.io/en/latest/miniconda.html
2. During installation, check "Add conda to PATH"
3. Restart your command prompt/PowerShell

### Step 2: Create Python Environments

Open **Command Prompt** or **PowerShell** as Administrator and run:

```bash
# Create RVC environment (Python 3.10)
conda create -n rvc python=3.10 -y

# Create Lucia Bot environment (Python 3.11)
conda create -n lucia python=3.11 -y

# Activate environments to verify
conda activate rvc
python --version  # Should show Python 3.10.x
conda deactivate

conda activate lucia
python --version  # Should show Python 3.11.x
conda deactivate
```

### Step 3: Install Visual Studio Build Tools

1. Download **Visual Studio Build Tools** from: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022
2. Install with "C++ build tools" workload
3. This is required for PyAudio compilation

### Step 4: Install FFmpeg

1. Download FFmpeg from: https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system PATH
4. Verify installation: `ffmpeg -version`

### Step 5: Restore Project Files

1. Extract the `LuciaV1Py_Backup.zip` to your desired location (e.g., `C:\Users\YourName\Desktop\`)
2. Navigate to the project directory: `cd C:\Users\YourName\Desktop\LuciaV1Py`

### Step 6: Set Up RVC (Retrieval-based Voice Conversion)

1. **Activate RVC environment:**
   ```bash
   conda activate rvc
   ```

2. **Navigate to RVC directory:**
   ```bash
   cd Retrieval-based-Voice-Conversion-WebUI
   ```

3. **Install RVC dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install PyTorch with CUDA support (if you have NVIDIA GPU):**
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

5. **Or install CPU-only PyTorch:**
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
   ```

6. **Test RVC installation:**
   ```bash
   python api_240604.py --help
   ```

### Step 7: Set Up Lucia Discord Bot

1. **Activate Lucia environment:**
   ```bash
   conda activate lucia
   ```

2. **Navigate to project root:**
   ```bash
   cd ..  # Go back to LuciaV1Py root
   ```

3. **Install Lucia dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install speech recognition dependencies:**
   ```bash
   python install_speech_deps.py
   ```

### Step 8: Configure Environment Variables

1. **Create `.env` file** in the project root (`LuciaV1Py` folder):
   ```env
   TOKEN=your_discord_bot_token_here
   ```

2. **Get Discord Bot Token:**
   - Go to https://discord.com/developers/applications
   - Create a new application or select existing one
   - Go to "Bot" section
   - Copy the token and paste it in the `.env` file

### Step 9: Update Batch Files

Edit the batch files to match your new conda installation path:

1. **Edit `activate_bot.bat`:**
   ```batch
   @echo off
   echo Activating Lucia Bot Environment (Python 3.11)...
   call C:\Users\YourName\miniconda3\Scripts\activate.bat lucia
   echo.
   echo Environment activated! Now you can run your bot.
   echo.
   echo Commands:
   echo   cd src
   echo   python main.py
   echo.
   cmd /k
   ```

2. **Edit `activate_rvc.bat`:**
   ```batch
   @echo off
   echo Activating RVC Environment (Python 3.10)...
   call C:\Users\YourName\miniconda3\Scripts\activate.bat rvc
   echo.
   echo Environment activated! Now you can install and run RVC.
   echo.
   echo Commands:
   echo   pip install -r requirements.txt
   echo   python app.py --listen --port 7860 --api
   echo.
   cmd /k
   ```

Replace `YourName` with your actual Windows username.

## 🎮 Running the Bot

### Method 1: Using Batch Files (Recommended)

1. **Start RVC API Server:**
   - Double-click `activate_rvc.bat`
   - In the opened terminal, run: `python start_rvc_api.py`
   - Keep this window open

2. **Start Lucia Bot:**
   - Double-click `activate_bot.bat`
   - In the opened terminal, run:
     ```bash
     cd src
     python main.py
     ```

### Method 2: Manual Terminal Commands

1. **Terminal 1 - RVC Server:**
   ```bash
   conda activate rvc
   cd Retrieval-based-Voice-Conversion-WebUI
   python api_240604.py --listen --port 7860 --api
   ```

2. **Terminal 2 - Lucia Bot:**
   ```bash
   conda activate lucia
   cd src
   python main.py
   ```

## 🔧 Troubleshooting

### Common Issues

1. **"TOKEN not found" error:**
   - Ensure `.env` file exists in project root
   - Check that TOKEN is properly set in `.env`
   - Verify no extra spaces or quotes around the token

2. **PyAudio installation fails:**
   - Install Visual Studio Build Tools
   - Try: `pip install pipwin` then `pipwin install pyaudio`

3. **RVC API not starting:**
   - Check if port 7860 is already in use
   - Ensure all RVC dependencies are installed
   - Try running `python api_240604.py --help` first

4. **Voice features not working:**
   - Ensure FFmpeg is installed and in PATH
   - Check microphone permissions
   - Verify RVC API is running on port 7860

5. **Discord bot not responding:**
   - Check bot token is correct
   - Verify bot has proper permissions in Discord server
   - Check logs in `logs/lucia.log`

### Log Files

- **Lucia Bot logs:** `logs/lucia.log`
- **RVC logs:** `Retrieval-based-Voice-Conversion-WebUI/logs/`

## 📁 Project Structure

```
LuciaV1Py/
├── src/                          # Main bot source code
│   ├── cogs/                     # Discord bot cogs (modules)
│   ├── utils/                    # Utility functions
│   ├── lucia.py                  # Main bot class
│   └── main.py                   # Bot entry point
├── Retrieval-based-Voice-Conversion-WebUI/  # RVC voice conversion
├── logs/                         # Bot log files
├── requirements.txt              # Python dependencies
├── .env                         # Environment variables (create this)
├── activate_bot.bat             # Bot environment activator
├── activate_rvc.bat             # RVC environment activator
└── start_rvc_api.py             # RVC API starter script
```

## 🎯 Features

- **Music Playback:** Play songs from YouTube, Spotify, etc.
- **AI Chat:** Powered by Ollama for intelligent responses
- **Voice Conversion:** Real-time voice conversion using RVC
- **Speech-to-Text:** Transcribe voice messages and live audio
- **VTube Studio Integration:** Control your VTuber avatar
- **Slash Commands:** Modern Discord command interface

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review log files for error messages
3. Ensure all dependencies are properly installed
4. Verify environment variables are set correctly

## 🔄 Updates

To update the bot:
1. Pull latest changes: `git pull origin master`
2. Update dependencies: `pip install -r requirements.txt --upgrade`
3. Restart both RVC API and Lucia Bot

---

**Happy botting!** 🤖✨
