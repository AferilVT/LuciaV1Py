# 🎭 RVC Model Setup Guide

This guide explains how to add your custom RVC (Retrieval-based Voice Conversion) models to Lucia's voice system.

## 📁 Model File Structure

RVC models consist of two main file types:
- **`.pth`** - The main model weights file
- **`.index`** - The feature index file (optional but recommended)

## 🗂️ Where to Place Your Models

### Option 1: RVC WebUI Assets Directory (Recommended)
Place your models in the RVC WebUI assets directory:

```
Retrieval-based-Voice-Conversion-WebUI/
├── assets/
│   ├── weights/           ← Place your .pth files here
│   ├── indices/           ← Place your .index files here
│   ├── pretrained/        ← Pre-trained models
│   └── pretrained_v2/     ← Pre-trained v2 models
```

### Option 2: Custom RVC Path
If you have a separate RVC installation, set the `RVC_PATH` environment variable in your `.env` file:

```env
RVC_PATH=C:/path/to/your/rvc/installation
```

## 📋 Step-by-Step Setup

### 1. Prepare Your Model Files

Ensure you have:
- Your custom `.pth` model file
- Your custom `.index` file (if available)
- Note the exact filenames (without extensions)

### 2. Copy Files to RVC Directory

```bash
# Copy your .pth file to weights directory
cp "your_model.pth" "Retrieval-based-Voice-Conversion-WebUI/assets/weights/"

# Copy your .index file to indices directory (if you have one)
cp "your_model.index" "Retrieval-based-Voice-Conversion-WebUI/assets/indices/"
```

### 3. Restart the Bot

The bot automatically scans for new models on startup.

### 4. Verify Model Detection

Use the Discord command to list available models:
```
/rvc_models
```

You should see your custom model in the list.

### 5. Set Your Model as Active

```
/set_rvc_model your_model_name
```

### 6. Test Your Model

```
/test_rvc_voice
```

## 🔧 Configuration Options

### Environment Variables

Add these to your `.env` file:

```env
# RVC Settings
RVC_PATH=./Retrieval-based-Voice-Conversion-WebUI
RVC_API_ENABLED=true
DEFAULT_RVC_MODEL=your_model_name

# Voice Settings
USE_RVC=true
```

### Model Naming Convention

- Use descriptive names without spaces
- Avoid special characters except underscores and hyphens
- Examples: `lucia_voice`, `anime_girl`, `deep_voice`

## 🎯 Discord Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `/rvc_models` | List all available RVC models | `/rvc_models` |
| `/set_rvc_model` | Set active RVC model | `/set_rvc_model lucia_voice` |
| `/toggle_rvc` | Enable/disable RVC voice | `/toggle_rvc` |
| `/test_rvc_voice` | Test current RVC model | `/test_rvc_voice` |

## 🔍 Troubleshooting

### Model Not Detected

1. **Check File Location**: Ensure files are in the correct directory
2. **Check File Extensions**: Only `.pth` and `.index` files are detected
3. **Check Permissions**: Ensure the bot can read the files
4. **Restart Bot**: Models are scanned on startup only

### Common Issues

#### "Model not found" Error
- Verify the exact model name (case-sensitive)
- Use `/rvc_models` to see the exact names
- Check for typos in the model name

#### "RVC path not found" Error
- Verify `RVC_PATH` environment variable is correct
- Ensure the path exists and is accessible
- Check for typos in the path

#### Voice Quality Issues
- Ensure you have both `.pth` and `.index` files
- Try different models to compare quality
- Check if the model was trained properly

### File Structure Examples

#### Correct Structure:
```
Retrieval-based-Voice-Conversion-WebUI/
├── assets/
│   ├── weights/
│   │   ├── lucia_voice.pth
│   │   └── anime_girl.pth
│   └── indices/
│       ├── lucia_voice.index
│       └── anime_girl.index
```

#### Model Detection:
The bot will detect:
- `lucia_voice` (from lucia_voice.pth)
- `anime_girl` (from anime_girl.pth)

## 📝 Example Setup

### 1. Download Custom Model
You have a model called `my_custom_voice.pth` and `my_custom_voice.index`

### 2. Copy Files
```bash
# Copy to RVC directory
cp my_custom_voice.pth "Retrieval-based-Voice-Conversion-WebUI/assets/weights/"
cp my_custom_voice.index "Retrieval-based-Voice-Conversion-WebUI/assets/indices/"
```

### 3. Update .env File
```env
DEFAULT_RVC_MODEL=my_custom_voice
USE_RVC=true
RVC_API_ENABLED=true
```

### 4. Restart Bot and Test
```
/rvc_models          # Should show "my_custom_voice"
/set_rvc_model my_custom_voice
/test_rvc_voice      # Test in voice channel
```

## 🎨 Advanced Configuration

### Multiple Models
You can have multiple models and switch between them:

```
/set_rvc_model lucia_voice    # Switch to Lucia voice
/set_rvc_model anime_girl     # Switch to anime voice
/set_rvc_model deep_voice     # Switch to deep voice
```

### Model Parameters
Some models may work better with different settings. The bot uses default parameters, but you can modify the RVC API settings if needed.

## 🔗 Useful Links

- [RVC WebUI GitHub](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)
- [RVC Model Training Guide](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/docs/training.md)
- [Pre-trained Models](https://huggingface.co/lj1995/VoiceConversionWebUI)

## 📞 Support

If you encounter issues:
1. Check the bot logs for error messages
2. Verify file paths and permissions
3. Ensure model files are not corrupted
4. Try with a known working model first
