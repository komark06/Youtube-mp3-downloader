import io
import os
from contextlib import redirect_stdout
from flask import (
    Flask,
    render_template,
    request,
    send_file,
)
from yt_dlp import YoutubeDL
from pydub import AudioSegment


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    youtube_url = request.form["youtube_url"]
    ydl_args = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "outtmpl": "-",
        "logtostderr": True,
    }
    ydl = YoutubeDL(ydl_args)
    info_dict = ydl.extract_info(youtube_url, download=False)
    title = info_dict["title"]
    ext = info_dict["ext"]
    if info_dict["duration"] > 1800:
        error_message = "Cannot download videos longer than 30 minutes."
        return render_template("index.html", error_message=error_message)
    buffer = io.BytesIO()
    with redirect_stdout(buffer):
        ydl.download([youtube_url])
    buffer.seek(0)
    audio = AudioSegment.from_file(buffer, format=ext)
    # Export the audio to MP3 format
    mp3_file = io.BytesIO()
    audio.export(mp3_file, format="mp3")
    mp3_file.seek(0)
    return send_file(
        mp3_file,
        as_attachment=True,
        download_name=title + ".mp3",
        mimetype="audio/mpeg",
    )


if __name__ == "__main__":
    app.run(port=5000)
