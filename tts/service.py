from flask import Flask, request, send_file
from gtts import gTTS
import os
import tempfile

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200


@app.route('/synthesize', methods=['POST'])
def synthesize_speech():
    text = request.json.get('text', '')
    if not text:
        return 'No text provided', 400

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        tts = gTTS(text=text, lang='en')
        tts.save(temp_file.name)
        temp_file_path = temp_file.name

    return send_file(temp_file_path, mimetype='audio/mp3')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)