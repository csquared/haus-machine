from transformers import AutoProcessor, MusicgenForConditionalGeneration 
from celery import Celery
import scipy
import hashlib

celery = Celery('tasks', broker='redis://localhost:6379/0', include=['api.tasks'])

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

    scipy.io.wavfile.write("wavs/musicgen_out_" + audio_digest[0:20] + ".wav", rate=sampling_rate, data=audio_values[0, 0].numpy())