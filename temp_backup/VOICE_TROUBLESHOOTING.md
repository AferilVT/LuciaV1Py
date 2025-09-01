# Voice Troubleshooting Guide

## 🎤 Common Voice Issues & Solutions

### **Issue 1: "Failed to join voice channel"**

**Causes:**
- Missing voice dependencies
- Bot permissions
- Discord rate limiting
- Network issues

**Solutions:**
1. **Install dependencies:**
   ```bash
   pip install PyNaCl ffmpeg-python
   ```

2. **Check bot permissions:**
   - Use `/voice_status` to check permissions
   - Ensure bot has "Connect" and "Speak" permissions

3. **Wait and retry:**
   - Discord rate limiting (wait 2-3 minutes)
   - Try different voice channels

### **Issue 2: "Recording failed"**

**Causes:**
- Missing "Attach Files" permission
- Already recording
- Voice client issues

**Solutions:**
1. **Check permissions:**
   - Bot needs "Attach Files" permission
   - Use `/voice_status` to verify

2. **Stop existing recording:**
   - Use `/record_stop` if already recording
   - Wait a few seconds between recordings

### **Issue 3: "WebSocket closed with 4006"**

**Causes:**
- Missing voice intents
- Discord API issues
- Network problems

**Solutions:**
1. **Restart the bot** (fixed intents in code)
2. **Wait 5 minutes** (Discord rate limiting)
3. **Check internet connection**

## 🔧 Diagnostic Commands

### **`/voice_status`**
Check current voice connection and permissions:
- Connection status
- Recording status
- Bot permissions
- Playlist status

### **`/join [channel]`**
Join a specific voice channel with detailed error messages

### **`/record_start`**
Start recording with permission checks

### **`/record_stop`**
Stop recording safely

## 🚨 Quick Fixes

### **1. Restart the Bot**
```bash
# Stop the bot (Ctrl+C)
cd src
python main.py
```

### **2. Check Dependencies**
```bash
pip install PyNaCl ffmpeg-python
ffmpeg -version  # Should show version info
```

### **3. Reinvite Bot**
If permissions are wrong, reinvite with proper permissions:
- Go to Discord Developer Portal
- OAuth2 → URL Generator
- Select: bot, applications.commands
- Permissions: Connect, Speak, Use Voice Activity, Attach Files

### **4. Test with Diagnostic Bot**
```bash
python voice_diagnostic.py
```
Then use `/test_voice` command

## 📋 Permission Checklist

**Required Bot Permissions:**
- ✅ **Connect** - Join voice channels
- ✅ **Speak** - Transmit audio
- ✅ **Use Voice Activity** - Detect when users speak
- ✅ **Attach Files** - Send audio files (for recordings)
- ✅ **Send Messages** - Send text messages
- ✅ **Use Slash Commands** - Use slash commands

## 🎯 Step-by-Step Troubleshooting

### **Step 1: Check Status**
```
/voice_status
```

### **Step 2: Test Connection**
```
/join [voice_channel]
```

### **Step 3: Test Recording**
```
/record_start
```
Then speak for a few seconds and:
```
/record_stop
```

### **Step 4: Check Logs**
Look for errors in `logs/lucia.log`

## 🆘 Still Having Issues?

### **Common Solutions:**
1. **Wait 5 minutes** - Discord rate limiting
2. **Try different server** - Test in another Discord server
3. **Check FFmpeg** - Ensure FFmpeg is installed and in PATH
4. **Restart router** - Network connectivity issues

### **Windows-Specific:**
- Install Visual C++ Build Tools for PyNaCl
- Use `pipwin install pyaudio` if pyaudio fails
- Check Windows Defender/firewall settings

### **Get Help:**
1. Run `/voice_status` and share the output
2. Check `logs/lucia.log` for error messages
3. Try the diagnostic bot: `python voice_diagnostic.py`

Most voice issues are resolved by checking permissions and restarting the bot! 🎤 