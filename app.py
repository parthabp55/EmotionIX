from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from src.text_detection import detect_text_emotion
from src.voice_detection import detect_voice_emotion
from face_detection import detect_face_emotion
from src.chatbot import chat_with_bot
from src.recommend import generate_recommendations, fetch_spotify_recommendations

# Initialize the Dash app with a Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Custom Styles for Background Video
VIDEO_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "width": "100%",
    "height": "100%",
    "objectFit": "cover",  # Ensure the video covers the full screen
    "zIndex": -1,  # Place the video behind all content
}

# Custom Styles for the rest of the app with transparent background
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "height": "100%",
    "width": "250px",
    "backgroundColor": "rgba(52, 58, 64, 0.8)",  # Semi-transparent background
    "padding": "20px",
    "color": "white",
    "fontFamily": "Arial",
    "boxShadow": "2px 0px 5px rgba(0,0,0,0.5)",
}

CONTENT_STYLE = {
    "marginLeft": "270px",
    "padding": "20px",
    "backgroundColor": "rgba(52, 58, 64, 0.8)",  # Semi-transparent content background
    "minHeight": "100vh",
}

BUTTON_STYLE = {
    "backgroundColor": "#441752",
    "color": "white",
    "border": "none",
    "borderRadius": "5px",
    "padding": "10px 20px",
    "marginTop": "10px",
}

HEADER_STYLE = {"textAlign": "center", "padding": "10px", "backgroundColor": "#1B1833", "color": "white"}

CARD_STYLE = {
    "padding": "20px",
    "borderRadius": "10px",
    "backgroundColor": "rgba(255, 255, 255, 0.8)",  # Semi-transparent background for cards
    "boxShadow": "0 4px 8px rgba(0,0,0,0.2)",
    "border": "2px solid #441752",
    
}

# Sidebar Layout
sidebar = html.Div(
    [
        html.H2("Emotionix", style={"textAlign": "center", "marginBottom": "30px", "fontWeight": "bold","backgroundColor": "#1B1833",'color':'white'}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Text Detection", href="/text-detection", active="exact"),
                dbc.NavLink("Voice Detection", href="/voice-detection", active="exact"),
                dbc.NavLink("Video Detection", href="/video-detection", active="exact"),
                dbc.NavLink("Chatbot", href="/chatbot", active="exact"),
            ],
            vertical=True,
            pills=True,
            style={"marginTop": "20px"},
        ),
    ],
    style=SIDEBAR_STYLE,
)

# App Layout
app.layout = html.Div(
    [
        # Background Video (served from the assets folder)
        html.Video(
            src="/assets/background-video.mp4",  # Path to the video file inside the assets folder
            autoPlay=True,
            loop=True,
            muted=True,
            style=VIDEO_STYLE,
        ),
        dcc.Location(id="url"),
        sidebar,
        html.Div(id="page-content", style=CONTENT_STYLE),
    ]
)

# Pages Layout for each section: Text, Voice, Video, and Chatbot
text_detection_layout = html.Div(
    [
        html.H4("Text Detection", style=HEADER_STYLE),
        dbc.Card(
            [
                html.P("Enter text below to analyze its emotional content."),
                dbc.Input(id="text-input", placeholder="Type text here...", type="text", className="mb-2",style={"border": "1px solid #441752"}),
                dbc.Button("Analyze", id="analyze-text-btn", style=BUTTON_STYLE),
                dcc.Loading(
                    id="loading-text",
                    type="default",
                    children=html.Div(id="text-recommend-output", className="mt-4"),
                ),
            ],
            style=CARD_STYLE,
        ),
    ]
)

voice_detection_layout = html.Div(
    [
        html.H4("Voice Detection", style=HEADER_STYLE),
        dbc.Card(
            [
                html.P("Click to record and analyze your voice's emotional tone."),
                dbc.Button("Record Voice", id="record-voice-btn", style=BUTTON_STYLE),
                dcc.Loading(
                    id="loading-voice",
                    type="default",
                    children=html.Div(id="voice-recommend-output", className="mt-4"),
                ),
            ],
            style=CARD_STYLE,
        ),
    ]
)

video_detection_layout = html.Div(
    [
        html.H4("Video Detection", style=HEADER_STYLE),
        dbc.Card(
            [
                html.P("Click to analyze emotions in your facial expression."),
                dbc.Button("Detect Emotion", id="video-detect-btn", style=BUTTON_STYLE),
                dcc.Loading(
                    id="loading-video",
                    type="default",
                    children=html.Div(id="video-recommend-output", className="mt-4"),
                ),
            ],
            style=CARD_STYLE,
        ),
    ]
)

# Chatbot Layout
chatbot_layout = html.Div(
    [
        html.H4("Chatbot", style=HEADER_STYLE),
        dbc.Card(
            [
                html.Div(
                    id="chatbot-conversation",
                    style={
                        "height": "300px",
                        "overflowY": "auto",
                        "border": "1px solid #441752",
                        "padding": "10px",
                        "marginBottom": "10px",
                        "backgroundColor": "#f8f9fa",
                        "borderRadius": "5px",
                    },
                ),
                dbc.Input(
                    id="chatbot-input",
                    placeholder="Type your message...",
                    type="text",
                    className="mb-2",
                    style={"width": "calc(100% - 70px)", "display": "inline-block", "marginRight": "5px", "border": "1px solid #441752"},
                ),
                dbc.Button(
                    "Send",
                    id="send-chat-btn",
                    style={
                        "backgroundColor": "#441752",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "5px",
                        "padding": "10px 20px",
                        "display": "inline-block",
                    },
                ),
            ],
            style=CARD_STYLE,
        ),
    ]
)

# Helper: Format Recommendations
def format_recommendations(ai_recommendations, spotify_recommendations):
    """
    Formats the AI and Spotify recommendations for display in the frontend.
    """
    spotify_content = (
        html.Ul(
            [
                html.Li(
                    html.A(
                        playlist.split(" - ")[0],  # Display the playlist name
                        href=playlist.split(" - ")[-1],  # Use the URL as the hyperlink
                        target="_blank",  # Open in a new tab
                        style={"color": "#007bff", "textDecoration": "none"},  # Styled as clickable links
                    )
                )
                for playlist in spotify_recommendations
            ]
        )
        if spotify_recommendations
        else html.P("No Spotify recommendations available.", style={"color": "red"}))

    return html.Div(
        [
            html.H5("AI-Generated Recommendations:", style={"color": "#007bff"}),
            dcc.Markdown(ai_recommendations, style={"marginBottom": "20px"}),  # Using Markdown for AI text
            html.H5("Spotify Recommendations:", style={"color": "#007bff"}),
            spotify_content,
        ],
        style={"padding": "10px", "border": "1px solid #ddd", "borderRadius": "5px", "backgroundColor": "#ffffff"},
    )

# Callbacks for text, voice, and video analysis
@app.callback(
    Output("text-recommend-output", "children"),
    Input("analyze-text-btn", "n_clicks"),
    State("text-input", "value"),
    prevent_initial_call=True,
)
def analyze_text_and_recommend(n_clicks, text):
    if text:
        emotion = detect_text_emotion(text)
        recommendations = generate_recommendations(emotion)
        spotify_recommendations = fetch_spotify_recommendations(emotion)
        return html.Div(
            [
                html.P(f"Detected Emotion: {emotion}", style={"fontWeight": "bold"}),
                format_recommendations(recommendations, spotify_recommendations),
            ]
        )
    return html.P("Please enter text to analyze.", style={"color": "red"})

@app.callback(
    Output("voice-recommend-output", "children"),
    Input("record-voice-btn", "n_clicks"),
    prevent_initial_call=True,
)
def analyze_voice_and_recommend(n_clicks):
    emotion = detect_voice_emotion()
    recommendations = generate_recommendations(emotion)
    spotify_recommendations = fetch_spotify_recommendations(emotion)
    return html.Div(
        [
            html.P(f"Detected Emotion: {emotion}", style={"fontWeight": "bold"}),
            format_recommendations(recommendations, spotify_recommendations),
        ]
    )

@app.callback(
    Output("video-recommend-output", "children"),
    Input("video-detect-btn", "n_clicks"),
    prevent_initial_call=True,
)
def analyze_video_and_recommend(n_clicks):
    emotion = detect_face_emotion(duration=5)
    recommendations = generate_recommendations(emotion)
    spotify_recommendations = fetch_spotify_recommendations(emotion)
    return html.Div(
        [
            html.P(f"Detected Emotion: {emotion}", style={"fontWeight": "bold"}),
            format_recommendations(recommendations, spotify_recommendations),
        ]
    )


# Chatbot Handling: Retaining history and sending responses
@app.callback(
    [
        Output("chatbot-conversation", "children"),
        Output("chatbot-input", "value"),
    ],
    Input("send-chat-btn", "n_clicks"),
    State("chatbot-input", "value"),
    State("chatbot-conversation", "children"),
    prevent_initial_call=True,
)
def handle_chatbot_message(n_clicks, user_input, conversation):
    if not conversation:
        conversation = []

    if user_input:
        # Add user input to the conversation
        conversation.append(
            html.Div(f"You: {user_input}", style={"color": "#000", "marginBottom": "10px", "fontWeight": "bold"})
        )
        try:
            # Get bot response
            bot_response = chat_with_bot(user_input)
        except Exception as e:
            bot_response = f"Error: {str(e)}"

        # Add bot response to the conversation
        conversation.append(
            html.Div(
                f"Bot: {bot_response}",
                style={"color": "#007bff", "marginBottom": "10px", "fontWeight": "bold"},
            )
        )

    # Ensure the latest messages are visible
    return conversation, ""  # Clear the input field


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/text-detection":
        return text_detection_layout
    elif pathname == "/voice-detection":
        return voice_detection_layout
    elif pathname == "/video-detection":
        return video_detection_layout
    elif pathname == "/chatbot":
        return chatbot_layout
    


if __name__ == "__main__":
    app.run_server(debug=True)