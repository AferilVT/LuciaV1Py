# Bot Permissions Guide

## Issue: Bot works in other servers but not in its own server

This is a common Discord bot permission issue. Here's how to fix it:

## 🔧 Quick Fix Steps:

### 1. **Check Bot Role Permissions**
1. Go to your server settings
2. Navigate to **Roles**
3. Find your bot's role (usually named after your bot)
4. Ensure it has these permissions:
   - ✅ **Connect** - Join voice channels
   - ✅ **Speak** - Transmit audio
   - ✅ **Use Voice Activity** - Detect when users speak
   - ✅ **Attach Files** - Send audio files
   - ✅ **Send Messages** - Send text messages
   - ✅ **Use Slash Commands** - Use slash commands

### 2. **Check Voice Channel Permissions**
1. Right-click on the voice channel you're trying to join
2. Select **Edit Channel**
3. Go to **Permissions** tab
4. Check if the bot's role has:
   - ✅ **Connect** permission
   - ✅ **Speak** permission
5. If not, add the bot's role and grant these permissions

### 3. **Check Server-Wide Bot Permissions**
1. Go to **Server Settings** → **Integrations** → **Bots and Apps**
2. Find your bot in the list
3. Click on it to see permissions
4. Ensure it has the necessary permissions enabled

### 4. **Check Bot Token Permissions**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your bot application
3. Go to **Bot** section
4. Under **Privileged Gateway Intents**, enable:
   - ✅ **Message Content Intent**
   - ✅ **Server Members Intent**
   - ✅ **Presence Intent**

### 5. **Reinvite the Bot**
If permissions are still wrong, reinvite the bot with proper permissions:

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your bot
3. Go to **OAuth2** → **URL Generator**
4. Select these scopes:
   - ✅ **bot**
   - ✅ **applications.commands**
5. Select these permissions:
   - ✅ **Connect**
   - ✅ **Speak**
   - ✅ **Use Voice Activity**
   - ✅ **Attach Files**
   - ✅ **Send Messages**
   - ✅ **Use Slash Commands**
6. Copy the generated URL and open it in a browser
7. Select your server and authorize

## 🚨 Common Issues:

### **Bot Role is Below Other Roles**
- Make sure your bot's role is **above** the roles it needs to manage
- Drag the bot's role higher in the role list

### **Channel-Specific Permissions**
- Check if the voice channel has specific permission overrides
- Make sure the bot's role isn't being denied permissions

### **Server Owner Permissions**
- If you're the server owner, make sure you're not accidentally denying permissions

## 🔍 Debugging Steps:

### 1. **Test Bot Permissions**
Run this command in your server to check bot permissions:
```
/join
```
If you get a permission error, the bot will tell you exactly what permission is missing.

### 2. **Check Bot Status**
- Make sure the bot is online
- Check if it appears in the member list
- Verify it can see the voice channels

### 3. **Server-Specific Issues**
- Try creating a new voice channel
- Test in a different voice channel
- Check if the server has any special restrictions

## ✅ Quick Checklist:

- [ ] Bot role has voice permissions
- [ ] Voice channel allows bot to connect
- [ ] Bot token has proper intents enabled
- [ ] Bot is properly invited to the server
- [ ] Bot role is positioned correctly in role hierarchy

## 🆘 Still Not Working?

If the bot still doesn't work in your server:

1. **Create a new test server** and invite the bot there
2. **Compare permissions** between working and non-working servers
3. **Check server boost level** - some features require server boosts
4. **Contact Discord support** if it's a server-specific issue

The most common fix is **reinviting the bot with proper permissions** using the OAuth2 URL generator! 🎤 