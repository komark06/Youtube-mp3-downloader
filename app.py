from flask import Flask, render_template, request, send_from_directory
import os
import subprocess

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    youtube_url = request.form["youtube_url"]

    ydl_command = [
        "yt-dlp",
        "--no-playlist",
        "--format",
        "bestaudio/best",
        "--extract-audio",
        "--audio-format",
        "mp3",
        "--output",
        "downloads/%(title)s.%(ext)s",
        youtube_url,
    ]
    filename = None
    try:
        subprocess.run(ydl_command, check=True)
        filename = get_downloaded_filename(youtube_url)
        return send_from_directory("downloads", filename, as_attachment=True)
    finally:
        if filename:
            os.remove(f"downloads/" + filename)


def get_downloaded_filename(youtube_url):
    ydl_command = [
        "yt-dlp",
        "--get-filename",
        "--no-playlist",
        "--output",
        "%(title)s.%(ext)s",
        youtube_url,
    ]
    result = subprocess.run(ydl_command, capture_output=True, text=True)
    filename = result.stdout.strip()
    filename = os.path.splitext(filename)[0] + ".mp3"  # Change the extension to .mp3
    return filename


if __name__ == "__main__":
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)
    app.run(port=5000)
