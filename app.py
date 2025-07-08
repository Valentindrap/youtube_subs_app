from flask import Flask, request, render_template, Response
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
import re
import os

app = Flask(__name__)

@app.route('/extract', methods=['POST'])
def extract():
    url = request.form['youtube_url']
    video_id = extract_video_id(url)

    try:
        # Usar proxy gratuito
        proxies = {
            'http': 'http://38.147.98.190:8080',
            'https': 'http://38.147.98.190:8080'
        }

        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=['es', 'en', 'es-ES', 'en-US'],
            proxies=proxies
        )

        plain_text = "\n".join([entry['text'] for entry in transcript])
        return Response(
            plain_text,
            mimetype='text/plain',
            headers={"Content-Disposition": "attachment;filename=subtitulos.txt"}
        )

    except Exception as e:
        return f"<p>Error inesperado: {e}</p>"


def extract_video_id(url):
    patterns = [
        r"youtu\.be/([^\?&]+)",
        r"youtube\.com/watch\?v=([^\?&]+)",
        r"youtube\.com/embed/([^\?&]+)"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("No se pudo extraer el ID del video")

# Para desarrollo local o compatibilidad con Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
