
import os
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import joblib
import librosa.effects as effects

# Define the path to your audio dataset
DATASET_PATH = r"RAVDESS"

# Specify the path for saving the model
model_path = r"emotion_model.pkl"

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(model_path), exist_ok=True)

# Emotion labels mapping
emotion_map = {
    "01": "neutral",
    "02": "calm",
    "03": "happy",
    "04": "sad",
    "05": "angry",
    "06": "fearful",
    "07": "disgust",
    "08": "surprised"
}
def extract_features(audio_data, sample_rate):
    """Extract various audio features from an audio file."""
    # MFCCs
    mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=13)
    mfccs_mean = np.mean(mfccs.T, axis=0)

    # Chroma
    chroma = librosa.feature.chroma_stft(y=audio_data, sr=sample_rate)
    chroma_mean = np.mean(chroma.T, axis=0)

    # Mel-spectrogram
    mel = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate)
    mel_mean = np.mean(mel.T, axis=0)

    # Spectral contrast
    contrast = librosa.feature.spectral_contrast(y=audio_data, sr=sample_rate)
    contrast_mean = np.mean(contrast.T, axis=0)

    # Concatenate all features
    features = np.concatenate((mfccs_mean, chroma_mean, mel_mean, contrast_mean))
    return features

def augment_audio(audio_data, sample_rate):
    # Original audio
    yield audio_data
    
    # Apply pitch shift
    pitch_shifted = librosa.effects.pitch_shift(audio_data, sr=sample_rate, n_steps=2)
    yield pitch_shifted

    # Apply speed change
    speed_changed = librosa.effects.time_stretch(audio_data, rate=1.1)
    yield speed_changed


def extract_features_from_dataset(dataset_path):
    features = []
    labels = []
    print(f"Dataset path: {dataset_path}")  # Confirm the dataset path

    # Loop through each actor's directory
    for actor_dir in os.listdir(dataset_path):
        actor_path = os.path.join(dataset_path, actor_dir)

        # Check if it's a directory
        if os.path.isdir(actor_path):
            print(f"Processing actor directory: {actor_dir}")  # Print each actor directory being processed

            # Loop through each audio file in the actor's directory
            for filename in os.listdir(actor_path):
                full_path = os.path.join(actor_path, filename)

                # Process only .wav files
                if filename.endswith(".wav") and os.path.isfile(full_path):
                    print(f"Processing file: {filename}")  # Print each file being processed

                    # Extract the emotion ID from the filename (adjust as necessary)
                    emotion_id = filename.split("-")[2]  # Adjust this based on actual filename format
                    emotion_label = emotion_map.get(emotion_id)

                    if emotion_label:
                        audio_data, sample_rate = librosa.load(full_path, sr=None)
                        mfccs = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=13)
                        mfccs_mean = np.mean(mfccs.T, axis=0)

                        features.append(mfccs_mean)
                        labels.append(emotion_label)
                    else:
                        print(f"Invalid emotion label for file: {filename}")

    print(f"Extracted {len(features)} features and {len(labels)} labels.")  # Final count
    return np.array(features), np.array(labels)

print("Files in dataset directory:")
print(os.listdir(DATASET_PATH))


# Extract features and labels
X, y = extract_features_from_dataset(DATASET_PATH)

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the SVM model
model = SVC(kernel='linear')
model.fit(X_train, y_train)

# Save the trained model
joblib.dump(model, model_path)

print("Model trained and saved successfully!")
