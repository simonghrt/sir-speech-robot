from scipy.io.wavfile import read
import vad
import matplotlib.pyplot as plt
import sounddevice as sd

threshold = 2500

[fs_avant, avant] = read('../../../../../data/enavant.wav')
[fs_noise, noise] = read('../../../../../data/noise.wav')

signal_noisy = []
signal_noisy.append([noise, fs_noise])
signal_noisy.append([avant, fs_avant])
signal_noisy.append([noise, fs_noise])

signal_clean = vad.simulate_real_time(signal_noisy, threshold)

sd.play(signal_clean, fs_avant)
sd.wait()

plt.figure(1)
plt.subplot(211)
plt.plot(signal_clean, 'b')
plt.subplot(212)
plt.plot(avant, 'r')
plt.show()
