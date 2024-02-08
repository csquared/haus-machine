import sys
import os
from flask import Flask, jsonify, request, send_from_directory
from api.tasks import gen_audio, celery

app = Flask(__name__, static_folder='../public', static_url_path='')

@app.route("/")
def home():
    public_dir = os.path.join(app.root_path, '..', 'public')
    return send_from_directory(public_dir, 'index.html')

@app.route("/api/v1/gen_audio", methods=['POST'])
def generate_audio():
    job_id = str(gen_audio.delay())
    return {"id": job_id}

@app.route("/api/v1/gen_audio_progress", methods=['GET'])
def check_progress():
    job_id = request.args.get('id')
    if not job_id:
        return jsonify({"error": "Missing job_id parameter"}), 400

    task = celery.AsyncResult(job_id)
    if task.state == 'PENDING':
        # Job did not start yet
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.status,
            'result': task.result
        }
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'status': str(task.info),  # this is the exception raised
        }

    return jsonify(response)