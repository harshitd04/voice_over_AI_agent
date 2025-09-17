from flask import Flask, render_template, request, jsonify, send_file
import requests
import os
from datetime import datetime
import io
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configuration
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', 'your_elevenlabs_api_key_here')
EXOTEL_API_KEY = os.getenv('EXOTEL_API_KEY', 'your_exotel_api_key_here')
EXOTEL_API_TOKEN = os.getenv('EXOTEL_API_TOKEN', 'your_exotel_api_token_here')
EXOTEL_SID = os.getenv('EXOTEL_SID', 'your_exotel_sid_here')

print(f"ElevenLabs API Key configured: {'Yes' if ELEVENLABS_API_KEY != 'your_elevenlabs_api_key_here' else 'No'}")

# ElevenLabs API endpoints
ELEVENLABS_BASE_URL = "https://api.elevenlabs.io/v1"
VOICES_URL = f"{ELEVENLABS_BASE_URL}/voices"
TTS_URL = f"{ELEVENLABS_BASE_URL}/text-to-speech"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_voices', methods=['GET'])
def get_voices():
    """Fetch available voices from ElevenLabs"""
    try:
        # Check if API key is configured
        if ELEVENLABS_API_KEY == 'your_elevenlabs_api_key_here' or not ELEVENLABS_API_KEY:
            print("ElevenLabs API key not configured, returning demo voices")
            # Return demo voices for testing
            demo_voices = [
                {'voice_id': 'demo_voice_1', 'name': 'Demo Voice 1', 'category': 'Demo'},
                {'voice_id': 'demo_voice_2', 'name': 'Demo Voice 2', 'category': 'Demo'}
            ]
            return jsonify({'success': True, 'voices': demo_voices})
        
        headers = {
            "Accept": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        print(f"Fetching voices from: {VOICES_URL}")
        response = requests.get(VOICES_URL, headers=headers, timeout=10)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            voices_data = response.json()
            # Simplify the voice data for the frontend
            voices = []
            for voice in voices_data.get('voices', []):
                voices.append({
                    'voice_id': voice['voice_id'],
                    'name': voice['name'],
                    'category': voice.get('category', 'Unknown')
                })
            print(f"Successfully fetched {len(voices)} voices")
            return jsonify({'success': True, 'voices': voices})
        else:
            print(f"Error response: {response.text}")
            return jsonify({'success': False, 'error': f'API returned status {response.status_code}'})
    
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return jsonify({'success': False, 'error': f'Network error: {str(e)}'})
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({'success': False, 'error': f'Unexpected error: {str(e)}'})

@app.route('/generate_speech', methods=['POST'])
def generate_speech():
    """Generate speech from text using ElevenLabs TTS"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        voice_id = data.get('voice_id', '')
        
        if not text or not voice_id:
            return jsonify({'success': False, 'error': 'Text and voice_id are required'})
        
        # Check if using demo voices
        if voice_id.startswith('demo_voice_'):
            print("Demo mode - simulating speech generation")
            # Create a dummy audio file for demo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"demo_audio_{timestamp}.mp3"
            filepath = os.path.join('static', 'audio', filename)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # Create an empty file (in real scenario, this would be actual audio)
            with open(filepath, 'wb') as f:
                f.write(b'')  # Empty file for demo
            
            return jsonify({
                'success': True, 
                'audio_file': filename,
                'audio_url': f'/static/audio/{filename}',
                'demo_mode': True,
                'message': 'Demo mode - no actual audio generated'
            })
        
        # Check if API key is configured
        if ELEVENLABS_API_KEY == 'your_elevenlabs_api_key_here' or not ELEVENLABS_API_KEY:
            return jsonify({'success': False, 'error': 'ElevenLabs API key not configured'})
        
        # ElevenLabs TTS API call
        url = f"{TTS_URL}/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        print(f"Generating speech for text: {text[:50]}...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"Speech generation response: {response.status_code}")
        
        if response.status_code == 200:
            # Save the audio file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audio_{timestamp}.mp3"
            filepath = os.path.join('static', 'audio', filename)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"Audio saved to: {filepath}")
            return jsonify({
                'success': True, 
                'audio_file': filename,
                'audio_url': f'/static/audio/{filename}'
            })
        else:
            print(f"Error generating speech: {response.text}")
            return jsonify({'success': False, 'error': f'Speech generation failed: {response.status_code}'})
    
    except requests.exceptions.RequestException as e:
        print(f"Request error in speech generation: {e}")
        return jsonify({'success': False, 'error': f'Network error: {str(e)}'})
    except Exception as e:
        print(f"Unexpected error in speech generation: {e}")
        return jsonify({'success': False, 'error': f'Unexpected error: {str(e)}'})

@app.route('/make_call', methods=['POST'])
def make_call():
    """Make a call using Exotel API or simulate the call"""
    try:
        data = request.get_json()
        phone_number = data.get('phone_number', '')
        audio_file = data.get('audio_file', '')
        
        if not phone_number:
            return jsonify({'success': False, 'error': 'Phone number is required'})
        
        # Check if we have valid Exotel credentials
        if (EXOTEL_API_KEY == 'your_exotel_api_key_here' or 
            EXOTEL_API_TOKEN == 'your_exotel_api_token_here' or
            EXOTEL_SID == 'your_exotel_sid_here'):
            
            # Simulate call since no real Exotel credentials
            return jsonify({
                'success': True,
                'message': 'Call simulated successfully! (No real Exotel credentials provided)',
                'call_id': f'simulated_call_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                'status': 'simulated'
            })
        
        # Real Exotel API call
        exotel_url = f"https://api.exotel.com/v1/Accounts/{EXOTEL_SID}/Calls/connect.json"
        
        # Audio file URL (you'll need to make this publicly accessible for Exotel)
        audio_url = f"https://yourdomain.com/static/audio/{audio_file}"  # Replace with your actual domain
        
        payload = {
            'From': '09513886363',  # Replace with your Exotel virtual number
            'To': phone_number,
            'Url': audio_url,  # URL to your audio file
            'CallType': 'trans'
        }
        
        response = requests.post(
            exotel_url,
            data=payload,
            auth=(EXOTEL_API_KEY, EXOTEL_API_TOKEN)
        )
        
        if response.status_code == 200:
            call_data = response.json()
            return jsonify({
                'success': True,
                'message': 'Call initiated successfully!',
                'call_id': call_data.get('Call', {}).get('Sid', ''),
                'status': call_data.get('Call', {}).get('Status', '')
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to initiate call'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/call_status/<call_id>')
def call_status(call_id):
    """Check the status of a call"""
    try:
        if call_id.startswith('simulated_call_'):
            return jsonify({
                'success': True,
                'status': 'completed',
                'message': 'Simulated call completed'
            })
        
        # Real Exotel status check
        exotel_url = f"https://api.exotel.com/v1/Accounts/{EXOTEL_SID}/Calls/{call_id}.json"
        
        response = requests.get(
            exotel_url,
            auth=(EXOTEL_API_KEY, EXOTEL_API_TOKEN)
        )
        
        if response.status_code == 200:
            call_data = response.json()
            return jsonify({
                'success': True,
                'status': call_data.get('Call', {}).get('Status', ''),
                'duration': call_data.get('Call', {}).get('Duration', '0')
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to get call status'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/audio', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    print("🎤 Voice AI Agent Starting...")
    print("📁 Created necessary directories")
    print(f"🔑 ElevenLabs API Key: {'Configured' if ELEVENLABS_API_KEY != 'your_elevenlabs_api_key_here' else 'NOT CONFIGURED'}")
    print("🌐 Server will start at: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)