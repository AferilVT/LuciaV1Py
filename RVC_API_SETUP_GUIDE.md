# 🎭 RVC API Setup Guide

This guide explains how to set up the RVC WebUI API server that Lucia needs for voice conversion.

## 🚨 **Current Issue**

Your bot is configured to use RVC but the RVC WebUI API server is not running. The bot is trying to connect to `http://localhost:7860` but getting no response.

## 🔧 **Solution: Start RVC WebUI API Server**

### **Option 1: Start RVC WebUI with API (Recommended)**

1. **Navigate to RVC directory:**
   ```bash
   cd Retrieval-based-Voice-Conversion-WebUI
   ```

2. **Start RVC WebUI with API enabled:**
   ```bash
   python api_240604.py
   ```

3. **Or use the batch file:**
   ```bash
   go-web.bat
   ```

### **Option 2: Use the provided batch file**

You already have `activate_rvc.bat` in your project root. Run it:
```bash
activate_rvc.bat
```

## 📋 **Verification Steps**

### **1. Check if RVC API is running**
Open your browser and go to: `http://localhost:7860`

You should see the RVC WebUI interface.

### **2. Test the API endpoint**
Try accessing: `http://localhost:7860/docs`

This should show the API documentation.

### **3. Check bot logs**
Look for these messages in your bot logs:
- ✅ "RVC API connected successfully"
- ❌ "RVC API connection failed"

## 🔄 **Alternative: Disable RVC API (Use Edge TTS)**

If you don't want to run the RVC API server, you can disable it:

1. **Update your `.env` file:**
   ```env
   RVC_API_ENABLED=false
   USE_RVC=false
   ```

2. **Restart your bot**

This will make Lucia use Edge TTS instead of RVC.

## 🎯 **Discord Commands After Setup**

Once the RVC API is running:

```
/rvc_models                    # Should show your models
/set_rvc_model KasaneTetotalkV1_240e_7680s
/test_rvc_voice               # Should work now
```

## 🔍 **Troubleshooting**

### **RVC API Server Won't Start**

1. **Check Python environment:**
   ```bash
   cd Retrieval-based-Voice-Conversion-WebUI
   python --version
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Check for errors:**
   Look for error messages when starting the API server.

### **Port 7860 Already in Use**

1. **Find what's using the port:**
   ```bash
   netstat -ano | findstr :7860
   ```

2. **Kill the process or use a different port:**
   Update your `.env` file:
   ```env
   RVC_API_URL=http://localhost:7861
   ```

### **Model Not Found in RVC API**

1. **Check RVC WebUI interface:**
   - Go to `http://localhost:7860`
   - Check if your model appears in the model list

2. **Verify model files:**
   - Ensure `.pth` and `.index` files are in the correct directories
   - Check file permissions

## 📝 **Complete Setup Checklist**

- [ ] RVC WebUI installed and working
- [ ] Model files in correct directories
- [ ] RVC API server running on port 7860
- [ ] Bot `.env` file configured correctly
- [ ] Bot restarted after configuration
- [ ] `/rvc_models` command shows your models
- [ ] `/test_rvc_voice` command works

## 🎨 **Advanced Configuration**

### **Custom RVC API Settings**

You can modify the RVC API parameters in the bot code:

```python
rvc_payload = {
    "audio": tts_audio,
    "model": self.current_voice_model,
    "pitch": 0,              # Pitch adjustment
    "index_rate": 0.5,       # Index rate (0.0-1.0)
    "filter_radius": 3,      # Filter radius
    "resample_sr": 0,        # Resample sample rate
    "rms_mix_rate": 0.25     # RMS mix rate
}
```

### **Multiple RVC Models**

You can switch between different models:
```
/set_rvc_model model_name_1
/set_rvc_model model_name_2
```

## 🆘 **Still Having Issues?**

1. **Check the bot logs** for specific error messages
2. **Verify RVC WebUI is working** by testing it manually
3. **Try disabling RVC** and using Edge TTS as fallback
4. **Check file permissions** and paths

## 📞 **Support**

If you continue to have issues:
1. Check the RVC WebUI logs for errors
2. Verify all file paths are correct
3. Ensure Python dependencies are installed
4. Try running RVC WebUI manually first
