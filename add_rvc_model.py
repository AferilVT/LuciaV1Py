#!/usr/bin/env python3
"""
RVC Model Installation Helper Script
This script helps you add custom RVC models to Lucia's voice system.
"""

import os
import shutil
import sys
from pathlib import Path

def main():
    print("🎭 RVC Model Installation Helper")
    print("=" * 40)
    
    # Get the project root directory
    project_root = Path(__file__).parent
    rvc_path = project_root / "Retrieval-based-Voice-Conversion-WebUI"
    
    if not rvc_path.exists():
        print("❌ RVC WebUI directory not found!")
        print(f"Expected path: {rvc_path}")
        print("Please ensure the RVC WebUI is installed in the project directory.")
        return
    
    # Check if assets directory exists
    assets_path = rvc_path / "assets"
    if not assets_path.exists():
        print("❌ RVC assets directory not found!")
        print(f"Expected path: {assets_path}")
        return
    
    # Create weights and indices directories if they don't exist
    weights_path = assets_path / "weights"
    indices_path = assets_path / "indices"
    
    weights_path.mkdir(exist_ok=True)
    indices_path.mkdir(exist_ok=True)
    
    print(f"✅ RVC path: {rvc_path}")
    print(f"✅ Weights directory: {weights_path}")
    print(f"✅ Indices directory: {indices_path}")
    print()
    
    # Get model files from user
    print("📁 Model File Setup")
    print("-" * 20)
    
    pth_file = input("Enter the path to your .pth model file: ").strip().strip('"')
    if not pth_file:
        print("❌ No .pth file specified!")
        return
    
    pth_path = Path(pth_file)
    if not pth_path.exists():
        print(f"❌ .pth file not found: {pth_path}")
        return
    
    # Ask for index file (optional)
    index_file = input("Enter the path to your .index file (optional, press Enter to skip): ").strip().strip('"')
    index_path = None
    if index_file:
        index_path = Path(index_file)
        if not index_path.exists():
            print(f"❌ .index file not found: {index_path}")
            return
    
    # Get model name
    model_name = input("Enter a name for your model (without extension): ").strip()
    if not model_name:
        # Use filename without extension as default
        model_name = pth_path.stem
    
    print()
    print("📋 Installation Summary")
    print("-" * 20)
    print(f"Model Name: {model_name}")
    print(f".pth File: {pth_path}")
    if index_path:
        print(f".index File: {index_path}")
    print(f"Destination: {weights_path}")
    print()
    
    # Confirm installation
    confirm = input("Proceed with installation? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Installation cancelled.")
        return
    
    try:
        # Copy .pth file
        dest_pth = weights_path / f"{model_name}.pth"
        shutil.copy2(pth_path, dest_pth)
        print(f"✅ Copied {pth_path.name} to {dest_pth}")
        
        # Copy .index file if provided
        if index_path:
            dest_index = indices_path / f"{model_name}.index"
            shutil.copy2(index_path, dest_index)
            print(f"✅ Copied {index_path.name} to {dest_index}")
        
        print()
        print("🎉 Model installation complete!")
        print()
        print("📝 Next Steps:")
        print("1. Restart your Discord bot")
        print("2. Use /rvc_models to verify the model is detected")
        print("3. Use /set_rvc_model " + model_name + " to set it as active")
        print("4. Use /test_rvc_voice to test the model")
        print()
        print("🔧 Optional: Add to your .env file:")
        print(f"DEFAULT_RVC_MODEL={model_name}")
        print("USE_RVC=true")
        print("RVC_API_ENABLED=true")
        
    except Exception as e:
        print(f"❌ Error during installation: {e}")
        return

if __name__ == "__main__":
    main()
