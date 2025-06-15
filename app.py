from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import openai
import requests
import datetime
import json
import re

app = Flask(__name__, static_folder='static')

# API keys - should be moved to environment variables in production
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', '0b13e0b9b9c23448c6d4db706b006ecf')
NEWS_API_KEY = os.environ.get('NEWS_API_KEY', 'c9387526f67147c389ade503802a37eb')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')

# Initialize OpenAI client
try:
    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
except:
    openai_client = None

# Base URLs for API calls
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
NEWS_BASE_URL = "https://newsapi.org/v2/top-headlines"

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LEO Voice Assistant</title>
        <link rel="stylesheet" href="/static/css/style.css">
    </head>
    <body>
        <div class="container">
            <h1>🦁 LEO - Voice Assistant</h1>
            <h2>Your Intelligent Voice Companion</h2>
            
            <div class="voice-controls">
                <h3>Speak to LEO</h3>
                <p>Click the microphone and start speaking</p>
                <button id="micButton" class="mic-btn">🎤</button>
                <p id="status">Ready to listen...</p>
                
                <div class="response-area">
                    <p><strong>You:</strong> <span id="userQuery"></span></p>
                    <p><strong>LEO:</strong> <span id="assistantResponse">How can I help you today?</span></p>
                </div>
            </div>
            
            <div class="features">
                <h3>🌟 What I Can Do:</h3>
                <ul>
                    <li>🌤️ Weather Updates - "weather in New York" or "weather in London"</li>
                    <li>📰 Latest News - "news" for tech headlines</li>
                    <li>⏰ Time & Date - Ask for current time and date</li>
                    <li>🌐 Website Navigation - Open websites (limited in web version)</li>
                    <li>🤣 Random Jokes - "tell me a joke"</li>
                    <li>🤖 AI Conversations - Ask me anything!</li>
                </ul>
            </div>
            
            <p>For full functionality including offline mode, download the desktop application:</p>
            <a href="/download" class="download-btn">Download Desktop Version</a>
        </div>
        
        <script src="/static/js/voice.js"></script>
    </body>
    </html>
    """

@app.route('/download')
def download():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Download LEO Voice Assistant</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #2c3e50;
                color: #ecf0f1;
                text-align: center;
                padding: 50px;
            }
            h1 {
                color: #e67e22;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: #34495e;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.5);
            }
            .instructions {
                text-align: left;
                margin: 20px 0;
                padding: 15px;
                background-color: #2c3e50;
                border-radius: 5px;
            }
            .back-btn {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                margin-top: 20px;
                text-decoration: none;
                display: inline-block;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Download LEO Voice Assistant</h1>
            
            <div class="instructions">
                <h3>Installation Instructions:</h3>
                <ol>
                    <li>Clone the repository: <code>git clone https://github.com/yourusername/leo-voice-assistant.git</code></li>
                    <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
                    <li>Run the application: <code>python deploy.py</code></li>
                </ol>
                
                <h3>Requirements:</h3>
                <ul>
                    <li>Python 3.7 or higher</li>
                    <li>Microphone for voice recognition</li>
                    <li>Speakers for voice output</li>
                    <li>Internet connection for API features</li>
                </ul>
            </div>
            
            <p>For support or questions, please contact us at support@example.com</p>
            
            <a href="/" class="back-btn">Back to Home</a>
        </div>
    </body>
    </html>
    """

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "online", "version": "1.0.0"})

@app.route('/process-query', methods=['POST'])
def process_query():
    data = request.json
    query = data.get('query', '').lower()
    response = "I'm sorry, I couldn't process that request."
    
    # Process different types of queries
    if 'weather' in query:
        # Extract city name from query
        city_match = re.search(r'weather in ([a-zA-Z\s]+)', query)
        if city_match:
            city = city_match.group(1).strip()
            response = get_weather(city)
        else:
            response = "Please specify a city for weather information."
    
    elif 'news' in query:
        response = get_news()
    
    elif 'time' in query:
        now = datetime.datetime.now()
        response = f"The current time is {now.strftime('%I:%M %p')}."
    
    elif 'date' in query:
        now = datetime.datetime.now()
        response = f"Today is {now.strftime('%A, %B %d, %Y')}."
    
    elif 'joke' in query:
        response = get_joke()
    
    else:
        # Use OpenAI for general conversation
        response = get_ai_response(query)
    
    return jsonify({"response": response})

def get_weather(city):
    """Get weather information for a city"""
    try:
        params = {
            'q': city,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        response = requests.get(WEATHER_BASE_URL, params=params)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            condition = data['weather'][0]['description']
            humidity = data['main']['humidity']
            return f"In {city}, it's currently {temp}°C with {condition}. The humidity is {humidity}%."
        else:
            return f"Sorry, I couldn't find weather information for {city}."
    except Exception as e:
        print(f"Weather API error: {e}")
        return f"Sorry, there was an error getting weather information for {city}."

def get_news():
    """Get latest news headlines"""
    try:
        params = {
            'category': 'technology',
            'language': 'en',
            'apiKey': NEWS_API_KEY
        }
        response = requests.get(NEWS_BASE_URL, params=params)
        data = response.json()
        
        if response.status_code == 200 and data.get('articles'):
            articles = data['articles'][:3]  # Get top 3 articles
            news_text = "Here are the latest tech headlines: "
            for i, article in enumerate(articles, 1):
                news_text += f"{i}. {article['title']}. "
            return news_text
        else:
            return "Sorry, I couldn't fetch the latest news at the moment."
    except Exception as e:
        print(f"News API error: {e}")
        return "Sorry, there was an error getting the latest news."

def get_joke():
    """Get a random joke"""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "What do you call a fake noodle? An impasta!",
        "How do you organize a space party? You planet!",
        "Why don't eggs tell jokes? They'd crack each other up.",
        "What's the best thing about Switzerland? I don't know, but the flag is a big plus.",
        "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them.",
        "Why was the math book sad? Because it had too many problems.",
        "What do you call a parade of rabbits hopping backwards? A receding hare-line."
    ]
    import random
    return random.choice(jokes)

def get_ai_response(query):
    """Get response from OpenAI"""
    if not openai_client or not OPENAI_API_KEY:
        return "I'm sorry, AI conversation is not available at the moment."
    
    try:
        # Add the user's query to conversation history
        messages = [
            {"role": "system", "content": "You are LEO, a helpful and friendly voice assistant. Keep your responses conversational, helpful, and concise."},
            {"role": "user", "content": query}
        ]
        
        # Get response from OpenAI
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return "I'm sorry, I couldn't process that with my AI capabilities right now."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)