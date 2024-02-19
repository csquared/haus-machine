from transformers import AutoProcessor, MusicgenForConditionalGeneration 
from celery import Celery
import boto3
import scipy
import hashlib
import os

celery = Celery('tasks', 
                broker=os.getenv('REDIS_SERVER') + '/0', 
                backend=os.getenv('REDIS_SERVER') + '/1', 
                include=['api.tasks'])

s3 = boto3.client('s3',
                  aws_access_key_id=os.getenv('BUCKETEER_AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.getenv('BUCKETEER_AWS_SECRET_ACCESS_KEY'))

bucket_name = os.getenv('BUCKETEER_BUCKET_NAME')

@celery.task(name="api.tasks.gen_audio")
def gen_audio():
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small") 
    inputs = processor(
        text="EDM indie dance track with a four on the floor beat, funky bassline, and groovy synth lead.",
        padding=True,
        return_tensors="pt"
    )
    audio_values = model.generate(**inputs, max_new_tokens=256)
    sampling_rate = model.config.audio_encoder.sampling_rate
    audio_digest = hashlib.sha256(audio_values[0, 0].numpy().tobytes()).hexdigest()
    file_name = "/wavs/musicgen_out_" + audio_digest[0:20] + ".wav"
    file_loc = "public" + file_name
    scipy.io.wavfile.write(file_loc, rate=sampling_rate, data=audio_values[0, 0].numpy())
    s3.upload_file(file_loc, bucket_name, file_loc)
    s3_file_name = f"https://{bucket_name}.s3.amazonaws.com/{file_loc}"
    return s3_file_name