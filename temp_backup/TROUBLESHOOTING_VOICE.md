# Voice Connection Troubleshooting

## Error: "WebSocket closed with 4006"

This error typically indicates one of these issues:

### 1. **Missing Voice Intents** ✅ FIXED
The bot was missing required voice intents. This has been fixed in `src/lucia.py`.

### 2. **Discord Rate Limiting**
Discord may be rate limiting voice connections. Solutions:
- Wait 1-2 minutes before trying again
- Try connecting to a different voice channel
- Restart the bot

### 3. **Bot Permissions**
Ensure your bot has these permissions:
- **Connect** - Join voice channels
- **Speak** - Transmit audio
- **Use Voice Activity** - Detect when users speak
- **Attach Files** - Send audio files

### 4. **Network Issues**
- Check your internet connection
- Try using a different network
- Restart your router if needed

### 5. **Discord API Issues**
Sometimes Discord's voice servers have issues:
- Check Discord status: https://status.discord.com/
- Try again later

## Quick Fixes to Try:

### 1. **Restart the Bot**
```bash
# Stop the current bot (Ctrl+C)
# Then restart
cd src
python main.py
```

### 2. **Test with Simple Bot**
Run the test script to isolate the issue:
```bash
python test_voice.py
```

### 3. **Check Bot Permissions**
In Discord:
1. Go to Server Settings → Integrations → Bots and Apps
2. Find your bot
3. Ensure it has voice permissions

### 4. **Try Different Voice Channel**
- Try joining a different voice channel
- Make sure the channel isn't full
- Check if the channel has any restrictions

## Common Solutions:

### **If the error persists:**
1. **Wait 5 minutes** - Discord rate limiting
2. **Try a different server** - Test in another Discord server
3. **Check bot token** - Ensure the bot token is correct
4. **Update dependencies** - Run `pip install -r requirements.txt`

### **For Windows users:**
- Ensure Windows Defender isn't blocking the connection
- Try running as administrator
- Check firewall settings

## Still Having Issues?

The error code 4006 is often temporary. Try these steps in order:

1. **Wait 2-3 minutes** and try again
2. **Restart the bot**
3. **Try a different voice channel**
4. **Test in a different Discord server**
5. **Check Discord status page**

Most voice connection issues are resolved by waiting a few minutes and trying again! 🎤 