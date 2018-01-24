import wave
import math
import time
import numpy as np
from scipy import signal, fftpack
from scipy.io.wavfile import read

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

def get_k_nn(distance, k):
    classes = [0, 0, 0, 0]
    for i in range(k):
        minDist = {'dist': 1000000000}
        for j in range(len(distance)):
            dist = distance[j]['dtw']
            if dist == 0:
                continue
            elif dist < minDist.get('dist'):
                minDist = {'dist': dist, 'class': distance[j]['class'], 'idx': j}
        distance.pop(minDist.get('idx'))
        if minDist.get('class') == 'forward':
            classes[0] = classes[0] + 1
        elif minDist.get('class') == 'right':
            classes[1] = classes[1] + 1
        elif minDist.get('class') == 'left':
            classes[2] = classes[2] + 1
        elif minDist.get('class') == 'stop':
            classes[3] = classes[3] + 1
    return classes

def compute_set(folder, files):
    for fileIdx in range(len(files)):
        filename = files[fileIdx].get('filename')
        mfcc = process_file(folder + filename)
        files[fileIdx]['mfcc'] = mfcc
    return files

def test_set_to_reference(test_set, reference_set, verbose=False):
    good_predictions = [0,0,0,0]
    for fileIdx1 in range(len(test_set)):
        file1 = test_set[fileIdx1]
        dtw_distance = []
        for fileIdx2 in range(len(reference_set)):
            file2 = reference_set[fileIdx2]
            dtw_distance.append({'class': file2.get('class'), 'dtw': altDTWDistance(file1.get('mfcc'), file2.get('mfcc'), 15)})
        if verbose:
            print(file1.get('filename') + ':')
        classes = get_k_nn(dtw_distance, 1)
        if(max(classes) == classes[0]):
            if(file1.get('class') == 'forward'):
                if verbose:
                    print('TRUE')
                good_predictions[0] += 1
            else:
                if verbose:
                    print('FALSE')
            test_set[fileIdx1]['prediction'] = 'forward'
        elif(max(classes) == classes[1]):
            if(file1.get('class') == 'right'):
                if verbose:
                    print('TRUE')
                good_predictions[1] += 1
            else:
                if verbose:
                    print('FALSE')
            test_set[fileIdx1]['prediction'] = 'right'
        elif(max(classes) == classes[2]):
            if(file1.get('class') == 'left'):
                if verbose:
                    print('TRUE')
                good_predictions[2] += 1
            else:
                if verbose:
                    print('FALSE')
            test_set[fileIdx1]['prediction'] = 'left'
        elif(max(classes) == classes[3]):
            if(file1.get('class') == 'stop'):
                if verbose:
                    print('TRUE')
                good_predictions[3] += 1
            else:
                if verbose:
                    print('FALSE')
            test_set[fileIdx1]['prediction'] = 'stop'   
        if verbose:
            print(classes)
    print('\nGood Predictions:')
    print(good_predictions)
    print('\nAccuracy:')
    print(str(math.floor(sum(good_predictions)/(len(test_set))*100)) + '%')
    return test_set

def predict(test_set, reference_set, verbose=False):
    test_file = test_set[0]
    dtw_distance = []
    for ref_idx in range(len(reference_set)):
        ref_file = reference_set[ref_idx]
        dtw_distance.append({'class': ref_file.get('class'), 'dtw': altDTWDistance(test_file.get('mfcc'), ref_file.get('mfcc'), 15)})
    classes = get_k_nn(dtw_distance, 1)
    if verbose:
        print(test_file.get('filename') + ':')
        if(max(classes) == classes[0]): print("Prediction: Forward") 
        elif(max(classes) == classes[1]): print("Prediction: Right") 
        elif(max(classes) == classes[2]): print("Prediction: Left") 
        elif(max(classes) == classes[3]): print("Prediction: Stop")
    if(max(classes = classes[0])):
        return "forward"
    elif(max(classes = classes[1])):
        return "right"
    elif(max(classes = classes[2])):
        return "left"
    elif(max(classes = classes[3])):
        return "stop"
    return None
