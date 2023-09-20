from flask import Flask, request, jsonify, Response
from moviepy.editor import VideoFileClip
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/convert', methods=['POST'])
def convert_mp4_to_mp3():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo foi enviado'}), 400

        file = request.files['file']

        if not file.filename.endswith('.mp4'):
            return jsonify({'error': 'O arquivo deve ser um MP4'}), 400
        
        temp_mp4 = '/tmp/temp.mp4'
        file.save(temp_mp4)

        video = VideoFileClip(temp_mp4)

        audio = video.audio

        temp_mp3 = '/tmp/temp.mp3'
        audio.write_audiofile(temp_mp3)

        with open(temp_mp3, 'rb') as mp3_file:
            mp3_binary = mp3_file.read()

        audio.close()
        video.close()
        os.remove(temp_mp4)
        os.remove(temp_mp3)

        return Response(mp3_binary, content_type='audio/mpeg')
    
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='localhost', port=8085, debug=True)