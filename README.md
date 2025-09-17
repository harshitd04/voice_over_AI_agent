# Voice over AI Agent

A demo web application that converts text to speech using ElevenLabs TTS API and makes calls using Exotel API.

## Features

-  Text-to-Speech conversion using ElevenLabs API
-  Multiple voice selection options
-  Phone call integration with Exotel API
-  Audio preview before making calls
-  Responsive web interface
-  Minimal JavaScript usage (beginner-friendly)

## Project Structure

```
voice-ai-agent/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your actual environment variables (create this)
├── templates/
│   └── index.html        # Frontend HTML template
└── static/
    └── audio/            # Generated audio files (created automatically)
```

## Prerequisites

- Python 3.7+
- ElevenLabs account and API key
- Exotel account and API credentials (optional for demo)

## Setup Instructions

### 1. Clone/Download the Project

Create a new folder for your project and save all the provided files in the correct structure.

### 2. Install Python Dependencies

```bash
# Navigate to your project directory
cd voice-ai-agent

# Install required packages
pip install -r requirements.txt
```

### 3. Get API Keys

#### ElevenLabs API Key:
1. Go to [ElevenLabs](https://www.elevenlabs.io/)
2. Create a free account
3. Go to your profile settings
4. Copy your API key from the "API Key" section

#### Exotel API Credentials (Optional):
1. Go to [Exotel Developer Portal](https://developer.exotel.com/)
2. Create an account
3. Get your API Key, API Token, and Account SID

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit the `.env` file and add your API keys:
```bash
# ElevenLabs API Configuration
ELEVENLABS_API_KEY=your_actual_elevenlabs_api_key

# Exotel API Configuration (optional)
EXOTEL_API_KEY=your_actual_exotel_api_key
EXOTEL_API_TOKEN=your_actual_exotel_api_token
EXOTEL_SID=your_actual_exotel_sid
```

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## How to Use

1. **Enter Text**: Type the message you want to convert to speech
2. **Select Voice**: Choose from available ElevenLabs voices
3. **Generate Speech**: Click "Generate Speech" to create the audio
4. **Preview Audio**: Listen to the generated audio using the built-in player
5. **Enter Phone Number**: Add the phone number you want to call (with country code)
6. **Make Call**: Click "Make Call" to initiate the phone call

## APIs Used

### ElevenLabs TTS API
- **Endpoint**: `https://api.elevenlabs.io/v1/`
- **Purpose**: Convert text to natural-sounding speech
- **Features**: Multiple voice options, high-quality audio generation

### Exotel API (Optional)
- **Endpoint**: `https://api.exotel.com/v1/`
- **Purpose**: Make phone calls and play generated audio
- **Features**: Call management, audio streaming

## File Connections

### Backend (app.py)
- Handles API requests to ElevenLabs and Exotel
- Manages audio file storage
- Serves the HTML template
- Provides REST endpoints for frontend

### Frontend (templates/index.html)
- User interface for text input and voice selection
- Audio player for preview
- AJAX calls to backend endpoints
- Minimal JavaScript for interactivity

### Static Files
- `static/audio/` - Stores generated audio files
- Audio files are automatically created and served

## Limitations and Assumptions

1. **Audio Storage**: Audio files are stored locally in `static/audio/`
2. **Call Simulation**: If Exotel credentials are not provided, calls are simulated
3. **Audio Format**: Uses MP3 format for generated audio
4. **Public URL**: For real Exotel calls, audio files need to be publicly accessible
5. **Rate Limits**: Subject to ElevenLabs and Exotel API rate limits

## Troubleshooting

### Common Issues:

1. **"Error loading voices"**
   - Check your ElevenLabs API key
   - Ensure internet connection

2. **"Failed to generate speech"**
   - Verify API key is correct
   - Check if you have API credits

3. **"Call simulated"**
   - This is normal if Exotel credentials are not configured
   - Add real Exotel credentials to make actual calls

4. **Audio files not playing**
   - Check if `static/audio/` directory exists
   - Ensure proper file permissions

### Logs and Debugging:
- Check the console output for error messages
- Enable Flask debug mode (already enabled in the code)
- Check browser developer tools for JavaScript errors

## Deployment Considerations

For production deployment:
1. Set `debug=False` in `app.py`
2. Use a production WSGI server (like Gunicorn)
3. Serve static files through a web server (like Nginx)
4. Use environment variables for all sensitive data
5. Implement proper error handling and logging

## Demo Video/Screenshots

Since this is a functional web application, you can:
1. Take screenshots of each step
2. Record a short video showing the complete flow
3. Include these in your submission

## Security Notes

- Never commit API keys to version control
- Use environment variables for sensitive data
- Implement rate limiting for production use
- Validate all user inputs
- Use HTTPS in production

## Support

If you encounter any issues:
1. Check the troubleshooting section
2. Review the API documentation for ElevenLabs and Exotel
3. Ensure all dependencies are installed correctly
4. Verify your API keys are valid and have sufficient credits

---

**Created for internship assignment - Voice over AI Agent Demo**