#!/usr/bin/env python3
"""
RVC Diagnostic Script
This script helps diagnose and fix RVC path configuration issues.
"""

import os
import sys
from pathlib import Path

def main():
    print("🔍 RVC Diagnostic Tool")
    print("=" * 40)
    
    # Get the project root directory
    project_root = Path(__file__).parent
    print(f"Project root: {project_root}")
    
    # Check for .env file
    env_file = project_root / ".env"
    if env_file.exists():
        print(f"✅ .env file found: {env_file}")
        with open(env_file, 'r') as f:
            env_content = f.read()
            if "RVC_PATH" in env_content:
                print("✅ RVC_PATH found in .env file")
            else:
                print("❌ RVC_PATH not found in .env file")
    else:
        print(f"❌ .env file not found: {env_file}")
    
    # Check RVC installation
    rvc_paths = [
        project_root / "Retrieval-based-Voice-Conversion-WebUI",
        project_root / "rvc",
        Path("./Retrieval-based-Voice-Conversion-WebUI"),
        Path("./rvc")
    ]
    
    print("\n📁 Checking RVC installations:")
    for rvc_path in rvc_paths:
        if rvc_path.exists():
            print(f"✅ Found: {rvc_path}")
            
            # Check for assets directory
            assets_path = rvc_path / "assets"
            if assets_path.exists():
                print(f"  ✅ Assets directory: {assets_path}")
                
                # Check for weights and indices
                weights_path = assets_path / "weights"
                indices_path = assets_path / "indices"
                
                if weights_path.exists():
                    print(f"  ✅ Weights directory: {weights_path}")
                    # List .pth files
                    pth_files = list(weights_path.glob("*.pth"))
                    if pth_files:
                        print(f"    📄 Found {len(pth_files)} .pth files:")
                        for pth_file in pth_files:
                            print(f"      - {pth_file.name}")
                    else:
                        print("    ❌ No .pth files found")
                else:
                    print(f"  ❌ Weights directory not found: {weights_path}")
                
                if indices_path.exists():
                    print(f"  ✅ Indices directory: {indices_path}")
                    # List .index files
                    index_files = list(indices_path.glob("*.index"))
                    if index_files:
                        print(f"    📄 Found {len(index_files)} .index files:")
                        for index_file in index_files:
                            print(f"      - {index_file.name}")
                    else:
                        print("    ❌ No .index files found")
                else:
                    print(f"  ❌ Indices directory not found: {indices_path}")
            else:
                print(f"  ❌ Assets directory not found: {assets_path}")
        else:
            print(f"❌ Not found: {rvc_path}")
    
    # Check environment variables
    print("\n🔧 Environment Variables:")
    rvc_path_env = os.getenv("RVC_PATH")
    if rvc_path_env:
        print(f"✅ RVC_PATH: {rvc_path_env}")
        if os.path.exists(rvc_path_env):
            print(f"  ✅ Path exists")
        else:
            print(f"  ❌ Path does not exist")
    else:
        print("❌ RVC_PATH not set (will use default: './rvc')")
    
    # Recommendations
    print("\n💡 Recommendations:")
    
    # Find the best RVC path
    best_rvc_path = None
    for rvc_path in rvc_paths:
        if rvc_path.exists() and (rvc_path / "assets").exists():
            best_rvc_path = rvc_path
            break
    
    if best_rvc_path:
        print(f"1. Set RVC_PATH to: {best_rvc_path}")
        
        # Check if .env file needs to be created or updated
        if not env_file.exists():
            print("2. Create .env file with:")
            print(f"   RVC_PATH={best_rvc_path}")
            print("   USE_RVC=true")
            print("   RVC_API_ENABLED=true")
        else:
            print("2. Update .env file to include:")
            print(f"   RVC_PATH={best_rvc_path}")
            print("   USE_RVC=true")
            print("   RVC_API_ENABLED=true")
        
        # Check if models exist
        weights_path = best_rvc_path / "assets" / "weights"
        if weights_path.exists():
            pth_files = list(weights_path.glob("*.pth"))
            if pth_files:
                print(f"3. Found {len(pth_files)} model(s): {[f.name[:-4] for f in pth_files]}")
                print("   Set DEFAULT_RVC_MODEL to one of these names")
            else:
                print("3. No .pth model files found in weights directory")
                print("   Add your .pth files to the weights directory")
    else:
        print("❌ No valid RVC installation found!")
        print("   Please ensure RVC WebUI is properly installed")
    
    print("\n🔧 Quick Fix:")
    if best_rvc_path:
        print("Create or update your .env file with:")
        print("-" * 40)
        print(f"RVC_PATH={best_rvc_path}")
        print("USE_RVC=true")
        print("RVC_API_ENABLED=true")
        if weights_path.exists():
            pth_files = list(weights_path.glob("*.pth"))
            if pth_files:
                print(f"DEFAULT_RVC_MODEL={pth_files[0].stem}")
        print("-" * 40)

if __name__ == "__main__":
    main()
