import cv2
from deepface import DeepFace
import time
from collections import Counter

def detect_face_emotion(duration=5):
    """
    Detect the dominant emotion from live video feed over a specified duration.
    
    Args:
    - duration (int): Duration in seconds to analyze video feed.
    
    Returns:
    - str: The most commonly detected emotion or None if no emotion is detected.
    """
    cap = cv2.VideoCapture(0)  # Start video capture from the default camera
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return None

    emotion_results = []  # Store detected emotions
    frame_count = 0  # Keep track of analyzed frames

    # Initialize the timer
    start_time = time.time()
    while time.time() - start_time < duration:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Preprocess frame to improve detection accuracy
        resized_frame = cv2.resize(frame, (640, 480))  # Resize to a standard resolution
        rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

        try:
            # Analyze the current frame for emotions
            analysis = DeepFace.analyze(rgb_frame, actions=["emotion"], enforce_detection=False)
            dominant_emotion = analysis[0]['dominant_emotion']  # Get the dominant emotion
            emotion_results.append(dominant_emotion)  # Append to results
            frame_count += 1
        except Exception as e:
            print(f"Warning: Error analyzing frame. Skipping. Details: {e}")

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

    # Determine the most common emotion if any were detected
    if emotion_results:
        common_emotion = Counter(emotion_results).most_common(1)[0][0]
        print(f"Frames Analyzed: {frame_count}, Detected Emotion: {common_emotion}")
        return common_emotion

    print("No emotions detected.")
    return None