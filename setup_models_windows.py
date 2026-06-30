"""
Setup Script - Download Required MediaPipe Models for Windows
Run this once before using the gesture control system
"""

import os
import urllib.request
import ssl
import sys
import hashlib

# ============================================================================
# CONFIGURATION
# ============================================================================

MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

# Model information with multiple download sources
MODELS = {
    "hand_landmarker": {
        "filename": "hand_landmarker.task",
        "urls": [
            "https://storage.googleapis.com/mediapipe-assets/hand_landmarker.task",
            "https://github.com/google-ai-edge/mediapipe/releases/download/v0.10.0/hand_landmarker.task",
        ],
        "min_size": 4000000,  # Minimum file size (4MB)
    }
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_model_directory():
    """Create models directory if it doesn't exist"""
    os.makedirs(MODEL_DIR, exist_ok=True)
    print(f"✅ Models directory: {MODEL_DIR}")

def check_file_validity(file_path, min_size=1000):
    """
    Check if downloaded file is valid
    """
    try:
        if not os.path.exists(file_path):
            return False, "File does not exist"

        file_size = os.path.getsize(file_path)
        
        if file_size < min_size:
            return False, f"File too small ({file_size} bytes, minimum {min_size} bytes)"

        # Check if file is binary (not text/XML error)
        with open(file_path, 'rb') as f:
            header = f.read(100)
            
            if b'<?xml' in header or b'<Error>' in header or b'<html>' in header:
                return False, "File is HTML/XML error response"
            
            if b'<!DOCTYPE' in header:
                return False, "File is HTML document"

        return True, "Valid"
    except Exception as e:
        return False, str(e)

def download_file(url, destination, timeout=30):
    """
    Download file with timeout and error handling for Windows
    """
    try:
        # Disable SSL verification (safe for model downloads from official sources)
        ssl._create_default_https_context = ssl._create_unverified_context
        
        print(f"  📥 Downloading from: {url}")
        
        # Set a reasonable timeout
        urllib.request.urlopen(url, timeout=timeout)
        urllib.request.urlretrieve(url, destination, timeout=timeout)
        
        return True, None
    except urllib.error.HTTPError as e:
        return False, f"HTTP Error {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return False, f"URL Error: {e.reason}"
    except Exception as e:
        return False, str(e)

def download_model(model_name, model_info):
    """
    Download a single model with fallback URLs
    """
    model_path = os.path.join(MODEL_DIR, model_info["filename"])
    min_size = model_info.get("min_size", 1000)
    
    print(f"\n📦 Processing model: {model_name}")
    print(f"   Destination: {model_path}")
    
    # Check if model already exists and is valid
    if os.path.exists(model_path):
        is_valid, status = check_file_validity(model_path, min_size)
        if is_valid:
            print(f"   ✅ Model already exists and is valid")
            return True
        else:
            print(f"   ⚠️  Existing file is invalid ({status}), re-downloading...")
            try:
                os.remove(model_path)
            except Exception as e:
                print(f"   ❌ Could not delete invalid file: {e}")
                return False
    
    # Try each URL
    for idx, url in enumerate(model_info["urls"], 1):
        print(f"   🔄 Attempt {idx}/{len(model_info['urls'])}")
        
        success, error = download_file(url, model_path)
        
        if success:
            # Verify downloaded file
            is_valid, status = check_file_validity(model_path, min_size)
            if is_valid:
                file_size = os.path.getsize(model_path)
                print(f"   ✅ Successfully downloaded ({file_size:,} bytes)")
                return True
            else:
                print(f"   ⚠️  Downloaded file is invalid: {status}")
                try:
                    os.remove(model_path)
                except:
                    pass
        else:
            print(f"   ❌ Download failed: {error}")
    
    print(f"   ❌ Could not download {model_name} from any source")
    return False

# ============================================================================
# MAIN SETUP
# ============================================================================

def main():
    """Main setup function"""
    
    print("\n" + "=" * 60)
    print("  MediaPipe Model Setup for Gesture Control")
    print("=" * 60)
    
    # Step 1: Create model directory
    create_model_directory()
    
    # Step 2: Download all models
    all_success = True
    for model_name, model_info in MODELS.items():
        success = download_model(model_name, model_info)
        if not success:
            all_success = False
    
    # Step 3: Summary
    print("\n" + "=" * 60)
    if all_success:
        print("  ✅ Setup Complete!")
        print("\n  You can now run:")
        print("  → python gesture_presentation_control.py")
    else:
        print("  ⚠️  Setup completed with errors")
        print("\n  Please check your internet connection and try again:")
        print("  → python setup_models.py")
    
    print("=" * 60 + "\n")
    
    return 0 if all_success else 1

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    sys.exit(main())
