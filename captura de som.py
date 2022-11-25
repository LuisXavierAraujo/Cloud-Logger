# -*- coding: utf-8 -*-
"""
Created on Fri Nov 25 18:09:19 2022

@author: luise
"""

import sounddevice as sd
from scipy.io.wavfile import write
import librosa as lib
import numpy as np

fs = 44100
second = 3

record_voice = sd.rec( int( second * fs ) , samplerate = fs , channels = 2 )
sd.wait()
write("som.wav", fs , record_voice )

x, sr = lib.load("som.wav")

# cronograma 
espetro = lib.feature.chroma_stft(y=x, sr=sr)

# espetro de energia 
S = np.abs(lib.stft(x))
chroma = lib.feature.chroma_stft(S=S, sr=sr)