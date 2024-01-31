from flask import Flask
from tasks import gen_audio

app = Flask(__name__)

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/python/gen_audio")
def generate_audio():
    return str(gen_audio.delay())