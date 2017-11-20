import wave
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fftpack
from scipy.io.wavfile import read

def get_folder():
    return "data/"

def get_files():
    files = []
        files.append({
        "filename": "enavant.wav",
        "class": "forward",
    })
    files.append({
        "filename": "enavant2.wav",
        "class": "forward",
    })
    files.append({
        "filename": "enavant3.wav",
        "class": "forward",
    })
    files.append({
        "filename": "enavant_1_paul.wav",
        "class": "forward",
    })
    files.append({
        "filename": "enavant_2_paul.wav",
        "class": "forward",
    })
    files.append({
        "filename": "enavant_3_paul.wav",
        "class": "forward",
    })
    files.append({
        "filename": "enavant_1_remi.wav",
        "class": "forward",
    })
    files.append({
        "filename": "enavant_2_remi.wav",
        "class": "forward",
    })
    files.append({
        "filename": "enavant_3_remi.wav",
        "class": "forward",
    })
    files.append({
        "filename": "adroite.wav",
        "class": "right",
    })
    files.append({
        "filename": "adroite2.wav",
        "class": "right",
    })
    files.append({
        "filename": "adroite3.wav",
        "class": "right",
    })
    files.append({
        "filename": "adroite_1_paul.wav",
        "class": "right",
    })
    files.append({
        "filename": "adroite_2_paul.wav",
        "class": "right",
    })
    files.append({
        "filename": "adroite_3_paul.wav",
        "class": "right",
    })
    files.append({
        "filename": "adroite_1_remi.wav",
        "class": "right",
    })
    files.append({
        "filename": "adroite_2_remi.wav",
        "class": "right",
    })
    files.append({
        "filename": "adroite_3_remi.wav",
        "class": "right",
    })
    files.append({
        "filename": "agauche.wav",
        "class": "left",
    })
    files.append({
        "filename": "agauche2.wav",
        "class": "left",
    })
    files.append({
        "filename": "agauche3.wav",
        "class": "left",
    })
    files.append({
        "filename": "agauche_1_paul.wav",
        "class": "left",
    })
    files.append({
        "filename": "agauche_2_paul.wav",
        "class": "left",
    })
    files.append({
        "filename": "agauche_3_paul.wav",
        "class": "left",
    })
    files.append({
        "filename": "agauche_1_remi.wav",
        "class": "left",
    })
    files.append({
        "filename": "agauche_2_remi.wav",
        "class": "left",
    })
    files.append({
        "filename": "agauche_3_remi.wav",
        "class": "left",
    })
    files.append({
        "filename": "stop.wav",
        "class": "stop",
    })
    files.append({
        "filename": "stop2.wav",
        "class": "stop",
    })
    files.append({
        "filename": "stop3.wav",
        "class": "stop",
    })
    files.append({
        "filename": "stop_1_paul.wav",
        "class": "stop",
    })
    files.append({
        "filename": "stop_2_paul.wav",
        "class": "stop",
    })
    files.append({
        "filename": "stop_3_paul.wav",
        "class": "stop",
    })
    files.append({
        "filename": "stop_1_remi.wav",
        "class": "stop",
    })
    files.append({
        "filename": "stop_2_remi.wav",
        "class": "stop",
    })
    files.append({
        "filename": "stop_3_remi.wav",
        "class": "stop",
    })
    return files

def apply_preemphasis_filter(data_signal):
    # Pre-Emphasis Filter
    pre_emphasis = 0.95
    emphasized_signal = np.append(data_signal[0], data_signal[1:] - pre_emphasis * data_signal[:-1])
    return emphasized_signal

def apply_stft(data_signal, nperseg, overlap, fs, NFFT):
    # FFT
    window = 'hamming'
    f, t, Zxx = signal.stft(x = data_signal, fs=fs, nperseg=nperseg, noverlap=overlap, nfft=NFFT, window=window)
    return f, t, Zxx

def apply_filter_banks(Zxx, fs, NFFT):
    # Filter Banks
    nfilt = 40
    low_freq_mel = 0
    high_freq_mel = (2595 * np.log10(1 + (fs / 2) / 700))  # Convert Hz to Mel
    mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilt + 2)  # Equally spaced in Mel scale
    hz_points = (700 * (10**(mel_points / 2595) - 1))  # Convert Mel to Hz
    bin = np.floor((NFFT + 1) * hz_points / fs)

    fbank = np.zeros((nfilt, int(np.floor(NFFT / 2 + 1))))
    for m in range(1, nfilt + 1):
        f_m_minus = int(bin[m - 1])   # left
        f_m = int(bin[m])             # center
        f_m_plus = int(bin[m + 1])    # right

        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
    filter_banks = np.dot(Zxx.T, fbank.T)
    filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)  # Numerical Stability
    filter_banks = 20 * np.log10(filter_banks)  # dB
    return filter_banks

def apply_mfcc(filter_banks):
    # MFCC
    num_ceps = 12
    mfcc = fftpack.dct(filter_banks, type=2, axis=1, norm='ortho')[:, 1 : (num_ceps + 1)]
    return mfcc

def process_file(filename):
    [fs, a] = read(filename)
    nperseg = math.floor(fs*2/100)
    overlap = math.floor(nperseg/2)
    NFFT = 2*nperseg
    data_signal = np.array(a,dtype=float)
    data_signal = apply_preemphasis_filter(data_signal)
    f, t, Zxx = apply_stft(data_signal, nperseg, overlap, fs, NFFT)
    filter_banks = apply_filter_banks(Zxx, fs, NFFT)
    mfcc = apply_mfcc(filter_banks)
    return mfcc

def altDTWDistance(s1, s2,w):
    DTW={}

    w = max(w, abs(len(s1)-len(s2)))

    for i in range(-1,len(s1)):
        for j in range(-1,len(s2)):
            DTW[(i, j)] = float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(s1)):
        for j in range(max(0, i-w), min(len(s2), i+w)):
            dist= np.sqrt(sum(np.abs((s1[i]-s2[j])**2)))
            DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)])

    return DTW[len(s1)-1, len(s2)-1]

def DTWDistance(s1, s2):
    DTW={}

    for i in range(len(s1)):
        DTW[(i, -1)] = float('inf')
    for i in range(len(s2)):
        DTW[(-1, i)] = float('inf')
    DTW[(-1, -1)] = 0

    for i in range(len(s1)):
        for j in range(len(s2)):
            dist= np.sqrt(sum(np.abs((s1[i]-s2[j]))**2))
            DTW[(i, j)] = dist + min(DTW[(i-1, j)],DTW[(i, j-1)], DTW[(i-1, j-1)])

    return DTW[len(s1)-1, len(s2)-1]

def diff_mfcc(s1, s2):
    diff = []
    for i in range(0, min(len(s1), len(s2))):
        current_diff = s1[i] - s2[i]
        diff.append(current_diff)
    plt.pcolormesh(np.real(diff))
    plt.show()
