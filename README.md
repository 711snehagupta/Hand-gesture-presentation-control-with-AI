🖐️ Gesture Control Presentation System (Windows)

Control PowerPoint/Google Slides with Hand Gestures!

Use your hand gestures to navigate presentations seamlessly using AI-powered hand detection via MediaPipe.


✨ Features


🎯 Real-time hand gesture detection
🎬 Control presentations with hand movements
📱 Works with PowerPoint, Google Slides, and other presentation software
⚡ Low-latency gesture recognition
🖼️ Live hand skeleton visualization
📊 FPS counter and performance monitoring



🎮 Gesture Controls

GestureFingersAction✋ Open Palm4 Fingers UpNext Slide (→)✌️ Peace Sign3 Fingers UpPrevious Slide (←)☝️ Point2 Fingers UpStart Presentation (F5)✊ Fist0 FingersExit Presentation (ESC)


📋 System Requirements


OS: Windows 10/11 (64-bit)
Python: 3.8 or higher
Webcam: Any USB webcam or built-in camera
RAM: 4GB minimum, 8GB recommended
Storage: ~500MB free space



🚀 Installation Guide (Step-by-Step)

Step 1: Install Python


Download Python from: https://www.python.org/downloads/
IMPORTANT: Check "Add Python to PATH" during installation
Verify installation by opening Command Prompt and typing:


cmd   python --version

Step 2: Create a Project Folder

cmd# Create a new folder for the project
mkdir gesture_control
cd gesture_control

Step 3: Download Project Files


Copy these 3 files to your gesture_control folder:

gesture_presentation_control.py
setup_models_windows.py
requirements.txt





Step 4: Install Dependencies

Open Command Prompt in your project folder and run:

cmd# Upgrade pip first
python -m pip install --upgrade pip

# Install required packages
pip install -r requirements.txt

If you get permission errors, use:

cmdpip install --user -r requirements.txt

Step 5: Download AI Models

cmd# Download MediaPipe hand detection model
python setup_models_windows.py

This will:


✅ Create a models/ folder
✅ Download hand_landmarker.task (~4.5 MB)
✅ Verify the download is valid


Expected output:

============================================================
  MediaPipe Model Setup for Gesture Control
============================================================
✅ Models directory: C:\...\gesture_control\models
📦 Processing model: hand_landmarker
   Destination: C:\...\gesture_control\models\hand_landmarker.task
   🔄 Attempt 1/2
   📥 Downloading from: https://storage.googleapis.com/mediapipe-assets/hand_landmarker.task
   ✅ Successfully downloaded (4,589,300 bytes)

============================================================
  ✅ Setup Complete!

  You can now run:
  → python gesture_presentation_control.py
============================================================


🎯 Running the Application

First Time Run:

cmdpython gesture_presentation_control.py

Expected Output:

============================================================
  GESTURE CONTROL PRESENTATION SYSTEM (Windows)
============================================================
✅ Model found: C:\...\gesture_control\models\hand_landmarker.task
✅ Hand detector initialized
✅ Webcam opened

📋 GESTURE CONTROLS:
  ✋ 4 Fingers  → Next Slide
  ✌️ 3 Fingers  → Previous Slide
  ☝️ 2 Fingers  → Start Presentation (F5)
  ✊ Fist       → Exit Presentation (ESC)

🎮 Press 'Q' to quit the program

============================================================

Window Displays:


Live webcam feed with hand skeleton overlay
Current gesture detection
FPS counter (top-right)
Gesture status (top-left)



💡 Usage Tips

For PowerPoint:


Open your PowerPoint presentation
Run gesture_presentation_control.py
Show 2 fingers to start slideshow (F5)
Use hand gestures to navigate


For Google Slides:


Open Google Slides in browser (fullscreen)
Run gesture_presentation_control.py
Two fingers to start
Use gestures for navigation


Best Practices:


✅ Ensure good lighting (natural light is best)
✅ Position camera at chest/face height
✅ Keep hand 30-60cm from camera
✅ Wear contrasting colors
✅ Use clean, deliberate gestures
✅ Test gestures before presenting



🐛 Troubleshooting

"Model file not found" Error

❌ Error: Model file not found at C:\...\models\hand_landmarker.task
📦 Please run first: python setup_models.py

Solution:

cmdpython setup_models_windows.py

Webcam Not Opening

Problem: ❌ Error: Cannot open webcam

Solutions:


Check camera connection
Allow Python camera access (Windows settings)
Close other applications using camera
Try different camera index (modify line in main file)


To test camera:

cmdpython -c "import cv2; cap = cv2.VideoCapture(0); print(cap.isOpened())"

"No gesture detected"

Possible causes:


⚠️ Poor lighting conditions
⚠️ Hand too small/far from camera
⚠️ Hand not fully visible
⚠️ Confidence threshold too high


Solutions:


Improve room lighting
Move hand closer to camera
Ensure entire hand is in frame
Check hand detection with visualization


"Slow Performance / Low FPS"

Solutions:


Close unnecessary programs
Reduce resolution (modify camera settings)
Lower confidence thresholds (advanced)
Use USB 3.0 webcam for better performance


PyAutoGUI Not Working

Problem: Gestures detected but presentation not advancing

Solutions:

cmd# Install accessibility tools if needed
pip install pyautogui --upgrade

# Test PyAutoGUI:
python -c "import pyautogui; pyautogui.press('right')"

Import Errors

cmd# Reinstall all dependencies
pip install --force-reinstall -r requirements.txt


⚙️ Advanced Configuration

Adjusting Gesture Sensitivity

Edit gesture_presentation_control.py, around line 30:

python# Gesture cooldown to prevent repeated actions
COOLDOWN_SECONDS = 1.5  # Increase for less sensitivity

# Confidence thresholds for hand detection
MIN_HAND_DETECTION_CONFIDENCE = 0.7  # Lower = more lenient (range 0-1)
MIN_HAND_PRESENCE_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7

Changing Gestures/Hotkeys

Edit the perform_gesture_action() function (around line 140):

pythonif total_fingers == 4:
    pyautogui.press("right")  # Change this key
    gesture = "✋ NEXT SLIDE"

Common keys:


"right", "left", "up", "down"
"enter", "space", "esc"
"f5", "f6" (PowerPoint shortcuts)


Using Different Camera

If you have multiple cameras:

pythoncap = cv2.VideoCapture(0)  # Change 0 to 1, 2, etc.


📊 Performance Optimization

Recommended Settings:

AspectRecommendationCamera Resolution1280x720 minimumLighting500+ lux (well-lit room)Hand Distance30-80cm from cameraPresentation WindowFullscreenCPU UsageShould stay <30%GPU UsageNot required


🔧 File Structure

gesture_control/
├── gesture_presentation_control.py    # Main application
├── setup_models_windows.py            # Model downloader
├── requirements.txt                   # Dependencies
├── README.md                          # This file
└── models/
    └── hand_landmarker.task          # AI model (downloaded)


📝 Keyboard Shortcuts

KeyActionQQuit applicationESCExit presentation slideshow→Next slide←Previous slideF5Start presentation (PowerPoint)


🛡️ Security & Privacy


✅ All processing happens locally on your PC
✅ No data sent to external servers (except model download)
✅ Webcam feed only displayed locally
✅ No recording or data storage
✅ Open source - inspect the code anytime



📦 Dependencies Information

PackageVersionPurposemediapipe0.10.35Hand detection & trackingopencv-python≥4.8.0Video capture & processingpyautogui≥0.9.54Keyboard controlPillow≥10.0.0Image processing


🐍 Python Version Check

cmdpython --version

Supported: Python 3.8+


🆘 Getting Help

Common Issues Checklist:


 Python installed and in PATH?
 All files in same folder?
 Dependencies installed? (pip list)
 Model downloaded? (check models/ folder)
 Webcam working? (test in other apps)
 Good lighting in room?
 Sufficient disk space?


Debug Mode:

Add this to see detailed information:

pythonimport logging
logging.basicConfig(level=logging.DEBUG)


📚 Additional Resources


MediaPipe Documentation: https://mediapipe.dev/
OpenCV Documentation: https://docs.opencv.org/
PyAutoGUI Documentation: https://pyautogui.readthedocs.io/



📄 License

This project uses open-source libraries. See their respective licenses for details.


🎉 Ready to Go!

You're all set! Now run:

cmdpython gesture_presentation_control.py

Enjoy gesture-controlled presentations! 🚀


Last Updated: June 2026
Tested On: Windows 10/11 with Python 3.8-3.11
