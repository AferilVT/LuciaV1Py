#!/usr/bin/env python3
"""
Lucia Discord Bot - Project Backup Script
This script creates a complete backup of your Lucia project for PC reset.
"""

import os
import shutil
import zipfile
import json
from datetime import datetime
from pathlib import Path
import sys

def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.absolute()

def create_backup_info():
    """Create backup information file."""
    backup_info = {
        "backup_date": datetime.now().isoformat(),
        "project_name": "Lucia Discord Bot",
        "version": "1.0",
        "python_versions": {
            "lucia_bot": "3.11",
            "rvc": "3.10"
        },
        "conda_environments": {
            "lucia": "Python 3.11 environment for Lucia bot",
            "rvc": "Python 3.10 environment for RVC voice conversion"
        },
        "important_paths": {
            "project_root": str(get_project_root()),
            "src_directory": str(get_project_root() / "src"),
            "rvc_directory": str(get_project_root() / "Retrieval-based-Voice-Conversion-WebUI"),
            "logs_directory": str(get_project_root() / "logs"),
            "assets_directory": str(get_project_root() / "src" / "assets")
        },
        "required_files": [
            "requirements.txt",
            "src/",
            "Retrieval-based-Voice-Conversion-WebUI/",
            "activate_bot.bat",
            "activate_rvc.bat",
            "start_rvc_api.py",
            "INSTALLATION_GUIDE.md",
            "README.md",
            "*.md"  # All markdown files
        ],
        "excluded_files": [
            "__pycache__/",
            "*.pyc",
            "*.pyo",
            "*.log",
            "logs/",
            ".git/",
            "node_modules/",
            "venv/",
            ".env"  # Exclude .env for security
        ],
        "notes": [
            "Remember to create .env file with your Discord bot token after restoration",
            "Update conda paths in batch files to match your new installation",
            "Install Visual Studio Build Tools for PyAudio compilation",
            "Install FFmpeg and add to PATH",
            "Create conda environments: 'lucia' (Python 3.11) and 'rvc' (Python 3.10)"
        ]
    }
    
    return backup_info

def should_exclude_file(file_path, excluded_patterns):
    """Check if file should be excluded from backup."""
    file_path_str = str(file_path)
    
    for pattern in excluded_patterns:
        if pattern.endswith('/'):
            # Directory pattern
            if pattern.rstrip('/') in file_path_str.split(os.sep):
                return True
        elif pattern.startswith('*'):
            # Wildcard pattern
            if file_path.name.endswith(pattern[1:]):
                return True
        else:
            # Exact match
            if file_path.name == pattern:
                return True
    
    return False

def create_backup():
    """Create the complete project backup."""
    project_root = get_project_root()
    backup_info = create_backup_info()
    
    # Create backup directory
    backup_dir = project_root / "backup"
    backup_dir.mkdir(exist_ok=True)
    
    # Create zip file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"LuciaV1Py_Backup_{timestamp}.zip"
    zip_path = backup_dir / zip_filename
    
    print(f"Creating backup: {zip_filename}")
    print(f"Project root: {project_root}")
    print(f"Backup location: {zip_path}")
    print()
    
    excluded_patterns = backup_info["excluded_files"]
    files_backed_up = 0
    total_size = 0
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add backup info
        zipf.writestr("backup_info.json", json.dumps(backup_info, indent=2))
        
        # Add installation guide
        if (project_root / "INSTALLATION_GUIDE.md").exists():
            zipf.write(project_root / "INSTALLATION_GUIDE.md", "INSTALLATION_GUIDE.md")
        
        # Walk through project directory
        for root, dirs, files in os.walk(project_root):
            # Skip backup directory itself
            if "backup" in root:
                continue
                
            # Skip excluded directories
            dirs[:] = [d for d in dirs if not should_exclude_file(Path(d), excluded_patterns)]
            
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(project_root)
                
                # Skip excluded files
                if should_exclude_file(file_path, excluded_patterns):
                    continue
                
                try:
                    # Add file to zip
                    zipf.write(file_path, relative_path)
                    files_backed_up += 1
                    total_size += file_path.stat().st_size
                    
                    if files_backed_up % 100 == 0:
                        print(f"Backed up {files_backed_up} files...")
                        
                except Exception as e:
                    print(f"Warning: Could not backup {file_path}: {e}")
    
    # Convert size to human readable
    size_mb = total_size / (1024 * 1024)
    
    print()
    print("Backup completed successfully!")
    print(f"Statistics:")
    print(f"   Files backed up: {files_backed_up}")
    print(f"   Total size: {size_mb:.2f} MB")
    print(f"   Backup file: {zip_path}")
    print()
    print("Next steps:")
    print("1. Save the backup file to a safe location (cloud storage, external drive)")
    print("2. After PC reset, extract the backup to your desired location")
    print("3. Follow the INSTALLATION_GUIDE.md for setup instructions")
    print("4. Don't forget to create your .env file with the Discord bot token!")
    
    return zip_path

def main():
    """Main function."""
    print("Lucia Discord Bot - Project Backup Script")
    print("=" * 50)
    print()
    
    try:
        zip_path = create_backup()
        print(f"\nBackup created successfully: {zip_path}")
        
    except Exception as e:
        print(f"Error creating backup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
