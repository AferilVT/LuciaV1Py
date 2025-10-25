#!/usr/bin/env python3
"""
RVC API Server Starter
This script helps start the RVC WebUI API server for Lucia.
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def main():
    print("🎭 RVC API Server Starter")
    print("=" * 40)
    
    # Get the project root directory
    project_root = Path(__file__).parent
    rvc_path = project_root / "Retrieval-based-Voice-Conversion-WebUI"
    
    if not rvc_path.exists():
        print("❌ RVC WebUI directory not found!")
        print(f"Expected path: {rvc_path}")
        return
    
    print(f"✅ RVC path: {rvc_path}")
    
    # Check if API file exists
    api_file = rvc_path / "api_240604.py"
    if not api_file.exists():
        print("❌ RVC API file not found!")
        print(f"Expected: {api_file}")
        print("Please ensure RVC WebUI is properly installed.")
        return
    
    print(f"✅ API file found: {api_file}")
    
    # Check if port 7860 is already in use
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 7860))
        sock.close()
        
        if result == 0:
            print("⚠️  Port 7860 is already in use!")
            print("RVC API might already be running.")
            print("Try accessing: http://localhost:7860")
            
            choice = input("Continue anyway? (y/N): ").strip().lower()
            if choice != 'y':
                return
    except Exception as e:
        print(f"⚠️  Could not check port status: {e}")
    
    print("\n🚀 Starting RVC API Server...")
    print("This may take a moment...")
    print()
    
    try:
        # Change to RVC directory
        os.chdir(rvc_path)
        
        # Start the API server
        print("Starting: python api_240604.py")
        print("=" * 40)
        
        # Start the process
        process = subprocess.Popen(
            [sys.executable, "api_240604.py"],
            cwd=rvc_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Wait a bit for server to start
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ RVC API Server started successfully!")
            print()
            print("🌐 You can now:")
            print("1. Open http://localhost:7860 in your browser")
            print("2. Test your Discord bot's RVC voice")
            print("3. Use /test_rvc_voice in Discord")
            print()
            print("⚠️  Keep this window open to keep the server running!")
            print("Press Ctrl+C to stop the server.")
            
            # Try to open browser
            try:
                webbrowser.open("http://localhost:7860")
                print("✅ Opened RVC WebUI in browser")
            except:
                print("⚠️  Could not open browser automatically")
            
            # Wait for user to stop
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping RVC API Server...")
                process.terminate()
                process.wait()
                print("✅ Server stopped.")
        else:
            print("❌ RVC API Server failed to start!")
            print("Check the error messages above.")
            
    except Exception as e:
        print(f"❌ Error starting RVC API Server: {e}")
        print("Please check:")
        print("1. Python environment is correct")
        print("2. RVC dependencies are installed")
        print("3. You have permission to run the server")

if __name__ == "__main__":
    main()
