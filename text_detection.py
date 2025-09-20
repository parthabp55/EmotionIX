from transformers import pipeline
classifier = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-emotion")
def detect_text_emotion(text):
    try:
        result = classifier(text)
        return result[0]["label"]  # Returns the detected emotion label
    except Exception as e:
        print("Error in text emotion detection:", e)
        return None
