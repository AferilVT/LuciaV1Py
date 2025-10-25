# 🎭 RVC Voice Conversion Setup Guide

## 🎯 Overview
This guide will help you set up **custom RVC voices** for your Discord bot! RVC (Retrieval-based Voice Conversion) allows you to clone any voice and make your bot speak with it.

## 🚀 **Two Ways to Use RVC**

### **Option 1: RVC WebUI (Recommended - Easier)**
Use the RVC WebUI with API access for voice conversion.

### **Option 2: Local RVC (Advanced)**
Install RVC locally for full control (requires Python 3.10).

---

## 🔧 **Option 1: RVC WebUI Setup (Recommended)**

### **Step 1: Install RVC WebUI**
```bash
# Clone RVC WebUI
git clone https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI.git
cd Retrieval-based-Voice-Conversion-WebUI

# Install dependencies (use Python 3.10)
pip install -r requirements.txt
```

### **Step 2: Download Voice Models**
Download pre-trained RVC models from:
- [RVC Models Hub](https://huggingface.co/lj1995/VoiceConversionWebUI)
- [Civitai RVC Models](https://civitai.com/models?tag=rvc)

Place `.pth` and `.index` files in the `models` folder.

### **Step 3: Start RVC WebUI**
```bash
# Start the WebUI
python app.py

# Or with specific settings
python app.py --listen --port 7860 --api
```

### **Step 4: Configure Bot for RVC API**
Add these environment variables to your `.env` file:
```env
USE_RVC=true
RVC_API_ENABLED=true
RVC_API_URL=http://localhost:7860
RVC_PATH=./rvc
```

---

## 🐍 **Option 2: Local RVC Setup (Advanced)**

### **Step 1: Install Python 3.10**
RVC requires Python 3.10 (not 3.11+):
```bash
# Download Python 3.10 from python.org
# Or use conda: conda create -n rvc python=3.10
```

### **Step 2: Install RVC Dependencies**
```bash
pip install torch==2.0.1 torchaudio==2.0.2
pip install fairseq
pip install ffmpeg-python
```

### **Step 3: Install RVC**
```bash
git clone https://github.com/RVC-Project/Retrieval-based-Voice-Conversion.git
cd Retrieval-based-Voice-Conversion
pip install -r requirements.txt
```

---

## 🎤 **Using RVC Voices in Your Bot**

### **New Commands Available:**
- `/rvc_models` - List available RVC voice models
- `/set_rvc_model <name>` - Set specific RVC model
- `/toggle_rvc` - Enable/disable RVC voice conversion
- `/test_rvc_voice` - Test current RVC voice

### **Voice Models Supported:**
- **.pth files** - Main voice model files
- **.index files** - Voice feature index files
- **Custom trained models** - Your own voice clones

---

## 🔄 **How It Works**

1. **Text Input** → Bot receives text to speak
2. **Edge TTS** → Generates base audio (any voice)
3. **RVC Conversion** → Converts to your custom voice
4. **Audio Playback** → Plays in Discord voice channel

---

## 🎯 **Quick Start (RVC WebUI)**

1. **Install RVC WebUI** (follow Option 1 steps)
2. **Download voice models** and place in `models/` folder
3. **Start WebUI**: `python app.py --listen --port 7860 --api`
4. **Set environment variables** in your `.env` file
5. **Restart your bot**
6. **Test with**: `/rvc_models` → `/set_rvc_model <name>` → `/test_rvc_voice`

---

## 🚨 **Troubleshooting**

### **Common Issues:**
- **Port 7860 in use**: Change port in RVC WebUI startup
- **Models not found**: Check file paths and permissions
- **API errors**: Ensure `--api` flag is used when starting WebUI
- **Voice quality**: Adjust RVC parameters in the WebUI

### **Fallback System:**
If RVC fails, the bot automatically falls back to Edge TTS voices, so your bot will always work!

---

## 🎉 **What You Get**

✅ **Custom Voices** - Clone any voice you want  
✅ **High Quality** - Professional voice conversion  
✅ **Easy Setup** - WebUI interface for management  
✅ **Fallback Safety** - Always works even if RVC fails  
✅ **Real-time** - Instant voice conversion  

Your Discord bot will now have **custom AI voices** that sound exactly like whoever you want! 🎭✨
