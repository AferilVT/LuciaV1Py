# RVC Voice Conversion Setup Guide

## 🎯 Overview
This guide will help you set up the RVC (Retrieval-based Voice Conversion) system for your Discord bot to enable custom AI voices.

## 📋 Prerequisites

### 1. **RVC Installation**
Clone and install the RVC project:
```bash
git clone https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI.git
cd Retrieval-based-Voice-Conversion-WebUI
pip install -r requirements.txt
```

### 2. **Required Dependencies**
Install additional Python packages:
```bash
pip install edge-tts
pip install ffmpeg-python
```

### 3. **FFmpeg Installation**
- **Windows**: Download from https://ffmpeg.org/download.html
- **MacOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

## 🔧 Configuration

### 1. **Environment Variables**
Add these to your `.env` file:
```env
# RVC Configuration
RVC_PATH=./Retrieval-based-Voice-Conversion-WebUI
DEFAULT_VOICE_MODEL=your_model_name
TTS_ENGINE=edge

# Voice AI Settings
VOICE_AI_ENABLED=true
AUTO_VOICE_RESPONSE=true
```

### 2. **Voice Models**
Place your trained RVC models in:
```
Retrieval-based-Voice-Conversion-WebUI/models/
├── your_model_name.pth
├── your_model_name.index (optional)
└── other_models.pth
```

## 🎭 Training Your Own Voice Model

### 1. **Data Preparation**
- Collect 10+ minutes of clean voice recordings
- Remove background noise
- Use consistent recording conditions
- Format: WAV, 44.1kHz, 16-bit

### 2. **Training Process**
1. Place audio files in `Retrieval-based-Voice-Conversion-WebUI/raw/`
2. Run the training script:
   ```bash
   python train.py --config configs/your_config.json
   ```
3. Monitor training progress
4. Test the model before full training

### 3. **Model Optimization**
- Adjust `protect` parameter (0.33 recommended)
- Fine-tune `f0_up_key` for pitch
- Use index files for better quality

## 🚀 Usage Commands

### **Voice AI Commands**
- `/voice_ai` - Enable voice AI interaction
- `/voice_ai_status` - Check system status
- `/test_voice_ai` - Test the system

### **RVC Voice Commands**
- `/voice_models` - List available models
- `/set_voice` - Change voice model
- `/test_voice` - Test current voice

### **Music Commands** (existing)
- `/join` - Join voice channel
- `/addsong` - Add music to playlist
- `/play` - Play music

## 🔄 Voice Interaction Flow

```
1. User speaks in VC
   ↓
2. Speech-to-Text (Whisper/Google)
   ↓
3. AI Processing (Ollama/LM Studio)
   ↓
4. Text-to-Speech (Edge TTS)
   ↓
5. RVC Voice Conversion
   ↓
6. Play in Discord VC
```

## 🐛 Troubleshooting

### **Common Issues**

1. **RVC Path Not Found**
   - Check `RVC_PATH` in `.env`
   - Ensure RVC is properly installed

2. **Voice Conversion Fails**
   - Verify model files exist
   - Check audio format compatibility
   - Ensure FFmpeg is installed

3. **TTS Issues**
   - Install edge-tts: `pip install edge-tts`
   - Check internet connection for Google STT

4. **Audio Quality Problems**
   - Adjust RVC parameters
   - Use higher quality input audio
   - Train model with better data

### **Performance Tips**
- Use SSD for faster model loading
- GPU acceleration for RVC (if available)
- Optimize audio sample rates
- Cache frequently used models

## 📁 File Structure
```
LuciaV1Py/
├── src/
│   ├── cogs/
│   │   ├── rvc_voice.py          # RVC voice conversion
│   │   ├── voice_interaction.py  # Voice AI coordination
│   │   └── music.py              # Music playback
│   └── utils/
│       └── Ollama_worker.py      # AI processing
├── Retrieval-based-Voice-Conversion-WebUI/  # RVC installation
└── .env                          # Configuration
```

## 🎉 Next Steps

1. **Test Basic Setup**: Use `/test_voice_ai`
2. **Train Custom Voice**: Follow training guide
3. **Fine-tune Parameters**: Adjust for best quality
4. **Expand Functionality**: Add more voice models

## 🔗 Resources

- [RVC GitHub Repository](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)
- [RVC Training Guide](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI#training)
- [Edge TTS Documentation](https://github.com/rany2/edge-tts)
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
