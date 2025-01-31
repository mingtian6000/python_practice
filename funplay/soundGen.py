from pydub import AudioSegment
import numpy as np

duration = 500 
sample_rate = 44100  
frequency = 1000 

t = np.linspace(0, duration / 1000, int(duration * sample_rate / 1000), False)
note = np.sin(frequency * 2 * np.pi * t)

print(note.dtype.itemsize)
audio = AudioSegment(
    note.astype(np.float32).tobytes(),
    frame_rate=sample_rate,
    sample_width=4,
    channels=1
)

audio.export("hit.wav", format="wav")

pop_duration = 100  
pop_frequency = 5000  

pop_t = np.linspace(0, pop_duration / 1000, int(pop_duration * sample_rate / 1000), False)
pop_note = np.sin(pop_frequency * 2 * np.pi * pop_t)

pop_audio = AudioSegment(
    pop_note.astype(np.float32).tobytes(),
    frame_rate=sample_rate,
    sample_width=4,
    channels=1
)

print(pop_note.dtype.itemsize)
pop_audio.export("pop.wav", format="wav")