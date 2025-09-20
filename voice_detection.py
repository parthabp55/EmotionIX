import os
import numpy as np
import joblib
import sounddevice as sd
import librosa
from sklearn.svm import SVC
from scipy.io.wavfile import write

MODEL_PATH = r"emotion_model.pkl"
SAMPLE_RATE = 22050  
DURATION = 15      

try:
    model = joblib.load(MODEL_PATH)
    print("Voice emotion model loaded successfully.")
except FileNotFoundError:
    print(f"Model not found at {MODEL_PATH}. Please train the model first.")
    raise

def extract_features(audio_data, sr=SAMPLE_RATE, n_mfcc=13):
    """
    Extracts MFCC features from audio data.
    :param audio_data: The audio signal from which to extract features.
    :param sr: Sampling rate of the audio signal.
    :param n_mfcc: Number of MFCC features to extract.
    :return: Mean MFCC features as a 1D numpy array.
    """
    mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=n_mfcc)
    mfccs_mean = np.mean(mfccs.T, axis=0)  # Shape should be (13,)
    return mfccs_mean

def record_audio(duration=DURATION, sr=SAMPLE_RATE):
    """
    Records audio for a given duration and sample rate.
    :param duration: Duration of the recording in seconds.
    :param sr: Sampling rate.
    :return: Recorded audio data as a numpy array.
    """
    print(f"Recording for {duration} seconds...")
    audio_data = sd.rec(int(duration * sr), samplerate=sr, channels=1)
    sd.wait()  # Wait until recording is finished
    audio_data = audio_data.flatten()  # Flatten to 1D array
    print("Recording finished.")
    return audio_data

def detect_voice_emotion():
    """
    Detects emotion from a live audio recording.
    :return: Detected emotion label.
    """
    recorded_audio = record_audio()
    features = extract_features(recorded_audio)
    features_reshaped = features.reshape(1, -1)  
    try:
        predicted_emotion = model.predict(features_reshaped)[0]
        print(f"Detected Voice Emotion: {predicted_emotion}")
        return predicted_emotion
    except Exception as e:
        print(f"Error during emotion prediction: {e}")
        return None

if __name__ == "__main__":
    detect_voice_emotion()
