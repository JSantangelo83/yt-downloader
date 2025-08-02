import os, yt_dlp,re
from flask import Flask, render_template, request,send_from_directory

def download_audio(link, output_path):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': False,
            'noplaylist': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
    except Exception as e:
        print(f"Failed to download {link}: {e}")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    links = re.findall(r"https?://\S+", request.form['links'])
    if(not links or len(links) < 1):
        return 'There has been an Error'
    
    os.system('rm -r out sounds.zip')
    
    output_dir = "out"
    os.makedirs(output_dir, exist_ok=True)

    for link in links:
        download_audio(link, output_dir)

    os.system('zip -r sounds.zip ./out')
    
    return send_from_directory('.', 'sounds.rar')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)