import wave
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io.wavfile import read

spf = wave.open('data/enavant.wav','r')

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')


#If Stereo
if spf.getnchannels() == 2:
    print("Just mono files")
    sys.exit(0)

plt.figure(1)
plt.title('Signal Wave')
plt.plot(signal)

plt.show()
