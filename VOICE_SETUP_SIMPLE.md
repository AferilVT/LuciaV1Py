# 🎤 Simple Voice AI Setup Guide

## 🎯 Overview
This guide will help you set up the **immediate voice functionality** for your Discord bot using Edge TTS. This gives you voice AI interaction without needing to install RVC.

## ✅ **What You Get Right Now**

### **Voice Commands**
- `/voices` - List available voices
- `/set_voice` - Change voice (e.g., "en-US-AriaNeural")
- `/test_voice` - Test current voice
- `/speak` - Make bot speak text

### **Voice AI Commands**
- `/voice_ai` - Enable voice AI interaction
- `/voice_ai_status` - Check system status
- `/test_voice_ai` - Test the complete system

### **Available Voices**
- **en-US-AriaNeural** - Female, clear (default)
- **en-US-DavisNeural** - Male, clear
- **en-US-JennyNeural** - Female, friendly
- **en-US-GuyNeural** - Male, friendly
- **en-GB-SoniaNeural** - British female
- **en-GB-RyanNeural** - British male
- **en-AU-NatashaNeural** - Australian female
- **en-AU-WilliamNeural** - Australian male

## 🚀 **Quick Start**

### 1. **Install Dependencies**
```bash
pip install edge-tts
```

### 2. **Start Your Bot**
```bash
cd src
python main.py
```

### 3. **Test Voice Commands**
1. Join a voice channel
2. Use `/join` to make bot join
3. Use `/test_voice` to test voice
4. Use `/test_voice_ai` to test AI interaction

## 🔄 **Voice AI Flow**

```
Your Voice → Speech-to-Text → AI Processing → Text Response + Voice Response
    ↓              ↓              ↓              ↓
  Discord VC   Whisper/STT    Ollama/LM      Chat + Edge TTS
```

## 🎭 **Future: RVC Integration**

When you're ready for custom voices, you can:

1. **Install Python 3.10** (RVC requirement)
2. **Clone RVC repository** and install
3. **Replace** `simple_voice.py` with `rvc_voice.py`
4. **Train custom voice models**

## 🐛 **Troubleshooting**

### **Common Issues**

1. **"SimpleVoiceCog not found"**
   - Check that `simple_voice.py` is in `src/cogs/`
   - Verify cogs.py loads `simple_voice`

2. **TTS Fails**
   - Ensure `edge-tts` is installed
   - Check internet connection
   - Verify FFmpeg is installed

3. **Voice Quality Issues**
   - Try different voice models
   - Check audio settings
   - Ensure good internet connection

### **Performance Tips**
- Use SSD for faster file operations
- Good internet for Edge TTS
- Optimize Discord voice settings

## 📁 **Current File Structure**
```
LuciaV1Py/
├── src/
│   ├── cogs/
│   │   ├── simple_voice.py        # Edge TTS voice system
│   │   ├── voice_interaction.py   # Voice AI coordination
│   │   └── music.py               # Music playback
│   └── utils/
│       └── Ollama_worker.py       # AI processing
└── .env                           # Configuration
```

## 🎉 **You're Ready!**

Your bot now has:
- ✅ **Text-to-Speech** with multiple voices
- ✅ **Voice AI interaction** (Speech → AI → Voice)
- ✅ **Music playback** functionality
- ✅ **Easy voice switching**

Start with `/test_voice_ai` to see the magic happen! 🎤🤖✨

## 🔗 **Next Steps**

1. **Test the system** with `/test_voice_ai`
2. **Customize voices** with `/set_voice`
3. **Enable voice AI** with `/voice_ai`
4. **Train custom RVC models** when ready
