#!/usr/bin/env python3
"""
Helper script to install speech recognition dependencies for Lucia
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {package}")
        return False

def main():
    print("Installing speech recognition and voice dependencies for Lucia...")
    print("=" * 60)
    
    # List of packages to install
    packages = [
        "SpeechRecognition>=3.10.0",
        "pyaudio>=0.2.11", 
        "openai-whisper>=20231117",
        "PyNaCl>=1.5.0",
        "ffmpeg-python>=0.2.0"
    ]
    
    success_count = 0
    total_count = len(packages)
    
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print("=" * 60)
    print(f"Installation complete: {success_count}/{total_count} packages installed successfully")
    
    if success_count == total_count:
        print("✓ All speech recognition and voice dependencies installed successfully!")
        print("\nYou can now use the following commands with Lucia:")
        print("- /transcribe - Transcribe an audio file or recording")
        print("- /transcribe_live - Start real-time transcription in voice channel")
        print("- /transcribe_stop - Stop real-time transcription")
        print("- /transcribe_voice_message - Transcribe a voice message")
        print("- /join - Join a voice channel")
        print("- /record_start - Start recording voice channel")
        print("- /record_stop - Stop recording voice channel")
    else:
        print("⚠ Some packages failed to install. You may need to install them manually.")
        print("For Windows users, you might need to install Visual C++ Build Tools for pyaudio.")
        print("For voice functionality, ensure you have FFmpeg installed on your system.")

if __name__ == "__main__":
    main() 