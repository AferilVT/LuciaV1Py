@echo off
echo ========================================
echo Lucia Discord Bot - Quick Setup
echo ========================================
echo.
echo This script will help you set up Lucia after PC reset.
echo.
echo Prerequisites:
echo 1. Install Miniconda/Anaconda
echo 2. Install Visual Studio Build Tools
echo 3. Install FFmpeg
echo 4. Extract LuciaV1Py_Backup.zip
echo.
echo Press any key to continue or Ctrl+C to exit...
pause >nul
echo.
echo Step 1: Creating Python environments...
echo.
call conda create -n rvc python=3.10 -y
call conda create -n lucia python=3.11 -y
echo.
echo Step 2: Environments created successfully!
echo.
echo Next steps:
echo 1. Run activate_rvc.bat to set up RVC
echo 2. Run activate_bot.bat to set up Lucia Bot
echo 3. Create .env file with your Discord bot token
echo 4. Follow INSTALLATION_GUIDE.md for detailed instructions
echo.
echo Press any key to exit...
pause >nul
