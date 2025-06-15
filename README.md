# LEO Voice Assistant

LEO is an intelligent voice assistant built with Python that can perform various tasks through voice commands.

## Features

- 🌤️ Weather Updates - Get current weather for any city
- 📰 Latest News - Fetch tech headlines
- ⏰ Time & Date - Ask for current time and date
- 🌐 Website Navigation - Open websites like YouTube, Google, GitHub
- 🤣 Random Jokes - Ask for jokes
- 🤖 AI Conversations - Powered by OpenAI

## Deployment

This project is configured for deployment on Render.com.

### Local Development

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the desktop application:
   ```
   python deploy.py
   ```

3. Run the web version:
   ```
   python app.py
   ```

### Deploying to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Render will automatically detect the configuration in `render.yaml`
4. Deploy!

## Requirements

- Python 3.7+
- For desktop version: microphone and speakers
- OpenAI API key (for AI conversation features)

## License

MIT