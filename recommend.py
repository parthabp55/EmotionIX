import google.generativeai as genai
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Configure the Google Generative AI API key
genai.configure(api_key="")

# Spotify API credentials
SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""
REDIRECT_URI = "http://localhost:8888/callback"

# Set up Spotify API authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="playlist-read-private"
    )
)

#Define the function to generate recommendations
def generate_recommendations(emotion):
    """
    Generates recommendations using the Gemini model based on the detected emotion.
    """
    prompt = (
        f"You are a helpful assistant for an emotional support application. Based on the detected emotion '{emotion}', "
        "please suggest some practical tips and YouTube video ideas that might help the user feel better."
    )

    # Create the generative model instance
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Generate content based on the prompt
    response = model.generate_content(prompt)

    # Return the generated content
    return response.text if response.text else "No recommendations available at the moment."
#

def fetch_spotify_recommendations(emotion):
    """
    Fetches Spotify playlists or songs based on the detected emotion.
    """
    # Define emotion-to-music mapping
    emotion_to_music = {
        "Sad": "happy music",
        "Happy": "joyful party music",
        "Angry": "calming music",
        "Relaxed": "chill vibes",
        "Excited": "energetic music",
        "Lonely": "uplifting acoustic songs"
    }

    # Get the mood from the mapping or default to 'mood music'
    mood = emotion_to_music.get(emotion, "mood music")

    try:
        # Use the Spotify instance to search playlists
        results = sp.search(q=mood, type="playlist", limit=3)

        recommendations = []
        for playlist in results["playlists"]["items"]:
            recommendations.append(
                f"{playlist['name']} - {playlist['external_urls']['spotify']}"
            )

        return recommendations if recommendations else ["No music recommendations available at the moment."]
    except Exception as e:
        return [f"Error fetching music recommendations: {str(e)}"]

def main():
    print("Welcome to Emotionix Support System!")

    # Get the detected emotion from the user
    detected_emotion = input("Enter the detected emotion: ").strip().capitalize()

    # Fetch AI-generated recommendations
    print("\nFetching recommendations for you...")
    ai_recommendations = generate_recommendations(detected_emotion)
    print("\nHere are the AI-generated recommendations:")
    print(ai_recommendations)

    # Fetch Spotify music recommendations
    print("\nFetching Spotify music recommendations...")
    music_recommendations = fetch_spotify_recommendations(detected_emotion)
    print("\nHere are some music recommendations for you:")
    for recommendation in music_recommendations:
        print(f"- {recommendation}")

    print("\nThank you for using Emotionix! Take care and stay positive.")

if __name__ == "__main__":
    main()
