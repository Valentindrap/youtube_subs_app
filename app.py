from flask import Flask, request, render_template, Response
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
import re

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    url = request.form['youtube_url']
    video_id = extract_video_id(url)

    try:
        # Idiomas preferidos (probando en orden)
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=['es', 'en', 'es-ES', 'en-US', 'en-GB']
        )
        # Solo el texto de los subtítulos, sin timestamps
        plain_text = "\n".join([entry['text'] for entry in transcript])
        return Response(
            plain_text,
            mimetype='text/plain',
            headers={"Content-Disposition": "attachment;filename=subtitulos.txt"}
        )

    except NoTranscriptFound:
        return "<p>No se encontraron subtítulos en los idiomas soportados (es, en).</p>"

    except TranscriptsDisabled:
        return "<p>Este video tiene los subtítulos desactivados.</p>"

    except Exception as e:
        return f"<p>Error inesperado: {e}</p>"

def extract_video_id(url):
    # Soporta formatos de URLs comunes de YouTube
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

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
