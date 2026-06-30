"""
Gesture Control for Presentation Slides (Windows Compatible)
Slide presentations with hand gestures using MediaPipe and AI detection
Features:
  - 4 fingers up = Next Slide
  - 3 fingers up = Previous Slide  
  - 2 fingers up = Start Presentation
  - Fist (0 fingers) = Exit Presentation
"""

import cv2
import mediapipe as mp
import pyautogui
import time
from mediapipe.tasks.python import vision
import os
import sys
import platform

# ============================================================================
# CONFIGURATION
# ============================================================================

MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "hand_landmarker.task")

# Gesture cooldown to prevent repeated actions
COOLDOWN_SECONDS = 1.5

# Confidence thresholds for hand detection
MIN_HAND_DETECTION_CONFIDENCE = 0.7
MIN_HAND_PRESENCE_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.7

# ============================================================================
# VALIDATION & SETUP
# ============================================================================

def check_os_compatibility():
    """Check if running on Windows"""
    if platform.system() != "Windows":
        print(f"⚠️  This code is optimized for Windows but detected {platform.system()}")
        print("   Some features may not work as expected")
        return False
    return True

def validate_model():
    """Validate that the hand landmarker model exists"""
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Error: Model file not found at {MODEL_PATH}")
        print("📦 Please run first: python setup_models.py")
        sys.exit(1)
    else:
        print(f"✅ Model found: {MODEL_PATH}")

# ============================================================================
# MEDIAPIPE INITIALIZATION
# ============================================================================

def initialize_hand_detector():
    """Initialize MediaPipe hand landmarker"""
    try:
        base_options = mp.tasks.BaseOptions(model_asset_path=MODEL_PATH)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=MIN_HAND_DETECTION_CONFIDENCE,
            min_hand_presence_confidence=MIN_HAND_PRESENCE_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        )
        hand_landmarker = vision.HandLandmarker.create_from_options(options)
        print("✅ Hand detector initialized")
        return hand_landmarker
    except Exception as e:
        print(f"❌ Failed to initialize hand detector: {e}")
        sys.exit(1)

# ============================================================================
# GESTURE RECOGNITION
# ============================================================================

def fingers_up(hand_landmarks):
    """
    Detect which fingers are up based on landmark positions
    
    Finger structure:
    - Thumb: landmarks 0-4
    - Index: landmarks 5-8 (tip index: 8)
    - Middle: landmarks 9-12 (tip index: 12)
    - Ring: landmarks 13-16 (tip index: 16)
    - Pinky: landmarks 17-20 (tip index: 20)
    
    Returns: List of 4 values [index_up, middle_up, ring_up, pinky_up]
    """
    tips = [8, 12, 16, 20]   # Fingertip indices
    pips = [6, 10, 14, 18]   # PIP joint indices (knuckles)

    fingers = []

    for tip, pip in zip(tips, pips):
        # If fingertip is above PIP joint, finger is up
        if hand_landmarks[tip].y < hand_landmarks[pip].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

def draw_hand_landmarks(frame, hand_landmarks, frame_width, frame_height):
    """Draw hand skeleton on frame"""
    # Draw landmark points
    for landmark in hand_landmarks:
        x = int(landmark.x * frame_width)
        y = int(landmark.y * frame_height)
        cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

    # Draw connections between landmarks
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 4),                # Thumb
        (5, 6), (6, 7), (7, 8),                        # Index
        (9, 10), (10, 11), (11, 12),                   # Middle
        (13, 14), (14, 15), (15, 16),                  # Ring
        (17, 18), (18, 19), (19, 20),                  # Pinky
        (0, 5), (5, 9), (9, 13), (13, 17), (0, 17)     # Palm
    ]

    for connection in connections:
        start_idx, end_idx = connection
        start = hand_landmarks[start_idx]
        end = hand_landmarks[end_idx]
        x1, y1 = int(start.x * frame_width), int(start.y * frame_height)
        x2, y2 = int(end.x * frame_width), int(end.y * frame_height)
        cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

# ============================================================================
# PRESENTATION CONTROL (WINDOWS)
# ============================================================================

def perform_gesture_action(total_fingers, current_time, last_time, last_action):
    """
    Map finger count to presentation actions
    Returns: (gesture_name, new_last_action, new_last_time)
    """
    
    if current_time - last_time < COOLDOWN_SECONDS:
        return last_action, last_action, last_time

    gesture = "Waiting..."
    action_performed = False

    if total_fingers == 4:
        # ✋ OPEN PALM = NEXT SLIDE
        try:
            pyautogui.press("right")
            gesture = "✋ NEXT SLIDE"
            action_performed = True
        except Exception as e:
            print(f"Error sending next slide command: {e}")

    elif total_fingers == 3:
        # ✌️ THREE FINGERS = PREVIOUS SLIDE
        try:
            pyautogui.press("left")
            gesture = "✌️ PREVIOUS SLIDE"
            action_performed = True
        except Exception as e:
            print(f"Error sending previous slide command: {e}")

    elif total_fingers == 2:
        # ☝️ TWO FINGERS = START PRESENTATION
        try:
            # Windows PowerPoint: F5 starts from beginning, Shift+F5 from current
            pyautogui.press("f5")
            gesture = "☝️ START PRESENTATION"
            action_performed = True
        except Exception as e:
            print(f"Error starting presentation: {e}")

    elif total_fingers == 0:
        # ✊ FIST = EXIT PRESENTATION
        try:
            pyautogui.press("esc")
            gesture = "✊ EXIT PRESENTATION"
            action_performed = True
        except Exception as e:
            print(f"Error exiting presentation: {e}")

    if action_performed:
        return gesture, gesture, current_time
    else:
        return last_action, last_action, last_time

# ============================================================================
# MAIN LOOP
# ============================================================================

def main():
    """Main gesture control loop"""
    
    print("=" * 60)
    print("  GESTURE CONTROL PRESENTATION SYSTEM (Windows)")
    print("=" * 60)
    
    # Check compatibility
    check_os_compatibility()
    
    # Validate model
    validate_model()
    
    # Initialize hand detector
    hand_landmarker = initialize_hand_detector()

    # Open webcam
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Error: Cannot open webcam. Check camera connection.")
            sys.exit(1)
        print("✅ Webcam opened")
    except Exception as e:
        print(f"❌ Error opening webcam: {e}")
        sys.exit(1)

    # Initialize state variables
    last_action = "Waiting..."
    last_time = time.time()

    print("\n📋 GESTURE CONTROLS:")
    print("  ✋ 4 Fingers  → Next Slide")
    print("  ✌️ 3 Fingers  → Previous Slide")
    print("  ☝️ 2 Fingers  → Start Presentation (F5)")
    print("  ✊ Fist       → Exit Presentation (ESC)")
    print("\n🎮 Press 'Q' to quit the program\n")
    print("=" * 60)

    frame_count = 0
    fps = 0
    prev_time = time.time()

    try:
        while True:
            success, frame = cap.read()

            if not success:
                print("❌ Failed to read frame from webcam")
                break

            # Mirror the frame for natural interaction
            frame = cv2.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape

            # Convert BGR to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create MediaPipe image
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            # Detect hand landmarks
            try:
                detection_result = hand_landmarker.detect(mp_image)
            except Exception as e:
                print(f"⚠️  Detection error: {e}")
                detection_result = None

            gesture = last_action

            # Process detected hands
            if detection_result and detection_result.hand_landmarks:
                for hand_landmarks in detection_result.hand_landmarks:
                    # Draw hand skeleton
                    draw_hand_landmarks(frame, hand_landmarks, frame_width, frame_height)

                    # Detect fingers
                    fingers = fingers_up(hand_landmarks)
                    total_fingers = fingers.count(1)

                    current_time = time.time()

                    # Perform gesture action
                    gesture, last_action, last_time = perform_gesture_action(
                        total_fingers, current_time, last_time, last_action
                    )

            # Calculate and display FPS
            frame_count += 1
            curr_time = time.time()
            fps = frame_count / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
            if frame_count % 30 == 0:
                prev_time = curr_time
                frame_count = 0

            # Display gesture status
            cv2.putText(
                frame,
                gesture,
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.2,
                (0, 255, 0),
                2
            )

            # Display FPS
            cv2.putText(
                frame,
                f"FPS: {int(fps)}",
                (frame_width - 150, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                1
            )

            # Display instructions
            cv2.putText(
                frame,
                "Press 'Q' to quit",
                (30, frame_height - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1
            )

            # Show frame
            cv2.imshow("Gesture Control - Presentation Slides", frame)

            # Check for quit command
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or key == ord("Q"):
                print("\n👋 Exiting application...")
                break

    except KeyboardInterrupt:
        print("\n⚠️  Application interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Cleanup complete")

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
