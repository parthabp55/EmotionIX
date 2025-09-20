import random

# Feedback options with at least 5 samples per emotion (expand as needed)
feedback_samples = {
    "happy": [
        "Keep smiling! 😊 Here's a fun fact for you...",
        "You’re radiating positivity! Keep it up!",
        "What a great mood! Let’s make today awesome!",
        "Glad to see you’re happy! 🌞 Keep spreading joy!",
        "Wonderful! Happiness looks great on you!",
        # Add more here to reach 50
    ],
    "sad": [
        "It’s okay to feel this way. Take a break and relax.",
        "You’re not alone—take it one step at a time.",
        "Maybe try listening to some calming music.",
        "Remember, every emotion is valid.",
        "Feeling low is normal. What helps you feel better?",
        # Add more here to reach 50
    ],
    "angry": [
        "Take a deep breath. Let’s focus on something positive.",
        "Let go of what you can’t control. You’ve got this!",
        "Maybe a walk could help calm your mind.",
        "Anger is tough—find what helps release it safely.",
        "Try to focus on something that brings you peace.",
        # Add more here to reach 50
    ],
    "surprised": [
        "Wow! That’s interesting. Want to share more?",
        "Life’s full of surprises—how exciting!",
        "Unexpected things make life interesting!",
        "Surprises can be fun or strange. How does it feel?",
        "Anything surprising can be an adventure!",
        # Add more here to reach 50
    ],
    "neutral": [
        "Hope you’re having a good day!",
        "Let’s keep this balance going. Feeling okay?",
        "Staying neutral is fine—ready for something new?",
        "Taking things as they come—sounds peaceful!",
        "Neutral is stable. Let’s keep that calm vibe going!",
        # Add more here to reach 50
    ],
    "optimism": [
        "You seem optimistic! Keep that energy alive!",
        "Optimism is contagious—spread the joy!",
        "Stay positive and hopeful. Great things await!",
        "Your optimism lights up the room!",
        "The glass is half full—keep it that way!",
    ],
    "anger": [
        "Take a deep breath. Let’s focus on something positive.",
        "Let go of what you can’t control. You’ve got this!",
        "Maybe a walk could help calm your mind.",
        "Anger is tough—find what helps release it safely.",
        "Try to focus on something that brings you peace.",
    ],
    "disgust": [
        "It's okay to feel unsettled. Take some time to process.",
        "Try to focus on something pleasant to shift your mood.",
        "Engaging in a positive activity might help you refocus.",
        "Remember, emotions pass with time. Stay grounded.",
        "Talk to someone who can help you process your feelings.",
    ],
    "fear": [
        "It's natural to feel fear sometimes. You're not alone.",
        "Try to focus on what you can control right now.",
        "Take deep breaths and remind yourself you’re safe.",
        "Facing fear takes courage—believe in yourself.",
        "Reach out to someone you trust for support.",
    ],
    "joy": [
        "Keep smiling! 😊 Here's a fun fact for you...",
        "You’re radiating positivity! Keep it up!",
        "What a great mood! Let’s make today awesome!",
        "Glad to see you’re happy! 🌞 Keep spreading joy!",
        "Wonderful! Happiness looks great on you!",
    ],
    "neutral": [
        "Hope you’re having a good day!",
        "Let’s keep this balance going. Feeling okay?",
        "Staying neutral is fine—ready for something new?",
        "Taking things as they come—sounds peaceful!",
        "Neutral is stable. Let’s keep that calm vibe going!",
    ],
    "sadness": [
        "It’s okay to feel this way. Take a break and relax.",
        "You’re not alone—take it one step at a time.",
        "Maybe try listening to some calming music.",
        "Remember, every emotion is valid.",
        "Feeling low is normal. What helps you feel better?",
    ],
    "surprise": [
        "Wow! That’s interesting. Want to share more?",
        "Life’s full of surprises—how exciting!",
        "Unexpected things make life interesting!",
        "Surprises can be fun or strange. How does it feel?",
        "Anything surprising can be an adventure!",
    ]
}

# Function to retrieve a random feedback sample based on emotion
def provide_feedback(emotion):
    responses = feedback_samples.get(emotion.lower())
    if responses:
        return random.choice(responses)
    else:
        return "Stay positive!"

# Example usage
if __name__ == "__main__":
    test_emotion = "happy"  # Replace with detected emotion
    print("Feedback:", provide_feedback(test_emotion))
