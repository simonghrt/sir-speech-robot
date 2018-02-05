
# coding: utf-8

# # Obtaining LPC (Linear Prediction Coefficients) for speech command

import wave
import math
import cmath
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io.wavfile import read
from audiolazy import lazy_lpc as lpc

# Datasets creation

folder = "data/"

rossignol_set = []
rossignol_set.append({
    "filename": "enavant.wav",
    "class": "forward",
})
rossignol_set.append({
    "filename": "enavant2.wav",
    "class": "forward",
})
rossignol_set.append({
    "filename": "enavant3.wav",
    "class": "forward",
})
rossignol_set.append({
    "filename": "adroite.wav",
    "class": "right",
})
rossignol_set.append({
    "filename": "adroite2.wav",
    "class": "right",
})
rossignol_set.append({
    "filename": "adroite3.wav",
    "class": "right",
})
rossignol_set.append({
    "filename": "agauche.wav",
    "class": "left",
})
rossignol_set.append({
    "filename": "agauche2.wav",
    "class": "left",
})
rossignol_set.append({
    "filename": "agauche3.wav",
    "class": "left",
})
rossignol_set.append({
    "filename": "stop.wav",
    "class": "stop",
})
rossignol_set.append({
    "filename": "stop2.wav",
    "class": "stop",
})
rossignol_set.append({
    "filename": "stop3.wav",
    "class": "stop",
})

remi_set = []
remi_set.append({
    "filename": "enavant_1_remi.wav",
    "class": "forward",
})
remi_set.append({
    "filename": "enavant_2_remi.wav",
    "class": "forward",
})
remi_set.append({
    "filename": "enavant_3_remi.wav",
    "class": "forward",
})
remi_set.append({
    "filename": "adroite_1_remi.wav",
    "class": "right",
})
remi_set.append({
    "filename": "adroite_2_remi.wav",
    "class": "right",
})
remi_set.append({
    "filename": "adroite_3_remi.wav",
    "class": "right",
})
remi_set.append({
    "filename": "agauche_1_remi.wav",
    "class": "left",
})
remi_set.append({
    "filename": "agauche_2_remi.wav",
    "class": "left",
})
remi_set.append({
    "filename": "agauche_3_remi.wav",
    "class": "left",
})
remi_set.append({
    "filename": "stop_1_remi.wav",
    "class": "stop",
})
remi_set.append({
    "filename": "stop_2_remi.wav",
    "class": "stop",
})
remi_set.append({
    "filename": "stop_3_remi.wav",
    "class": "stop",
})


paul_set = []
paul_set.append({
    "filename": "enavant_1_paul.wav",
    "class": "forward",
})
paul_set.append({
    "filename": "enavant_2_paul.wav",
    "class": "forward",
})
paul_set.append({
    "filename": "enavant_3_paul.wav",
    "class": "forward",
})
paul_set.append({
    "filename": "adroite_1_paul.wav",
    "class": "right",
})
paul_set.append({
    "filename": "adroite_2_paul.wav",
    "class": "right",
})
paul_set.append({
    "filename": "adroite_3_paul.wav",
    "class": "right",
})
paul_set.append({
    "filename": "agauche_1_paul.wav",
    "class": "left",
})
paul_set.append({
    "filename": "agauche_2_paul.wav",
    "class": "left",
})
paul_set.append({
    "filename": "agauche_3_paul.wav",
    "class": "left",
})
paul_set.append({
    "filename": "stop_1_paul.wav",
    "class": "stop",
})
paul_set.append({
    "filename": "stop_2_paul.wav",
    "class": "stop",
})
paul_set.append({
    "filename": "stop_3_paul.wav",
    "class": "stop",
})


paul_set_reduce = []
paul_set_reduce.append({
    "filename": "enavant_1_paul.wav",
    "class": "forward",
})
paul_set_reduce.append({
    "filename": "adroite_1_paul.wav",
    "class": "right",
})
paul_set_reduce.append({
    "filename": "agauche_1_paul.wav",
    "class": "left",
})
paul_set_reduce.append({
    "filename": "stop_1_paul.wav",
    "class": "stop",
})


remi_set_reduce = []
remi_set_reduce.append({
    "filename": "enavant_1_remi.wav",
    "class": "forward",
})
remi_set_reduce.append({
    "filename": "adroite_1_remi.wav",
    "class": "right",
})
remi_set_reduce.append({
    "filename": "agauche_1_remi.wav",
    "class": "left",
})
remi_set_reduce.append({
    "filename": "stop_1_remi.wav",
    "class": "stop",
})


simon_set = []
simon_set.append({
    "filename": "enavant_1_simon.wav",
    "class": "forward",
})
simon_set.append({
    "filename": "enavant_2_simon.wav",
    "class": "forward",
})
simon_set.append({
    "filename": "enavant_3_simon.wav",
    "class": "forward",
})

# Functions for lpc processing

def phi(signal, k_ind):
    # phi est un estimateur de la fonction d'autocorrélation du signal
    N = len(signal)
    somme = 0
    for i in range(0, N - k_ind):
        somme += signal[i] * signal[i + k_ind]
    return (somme / N)

def dsp_calculation_audiolazy(signal, K, a, nu): 
    sum_sigma = 0
    for i in range(0, K):
        sum_sigma += a[i] * phi(signal, i)
    sigma_e = phi(signal, 0) - sum_sigma
    sum_den_dsp = 0
    for j in range(0, K):
        sum_den_dsp += a[j] * cmath.exp(2 * cmath.pi * nu * j * 1j)
    den_dsp = (abs(1 - sum_den_dsp))**2
    dsp = 0
    if (den_dsp != 0 and sigma_e != 0):
        dsp = sigma_e / den_dsp
    return dsp

# Process file getting lpc coefficients

def process_file(filename):
    signal_wave = wave.open(filename)
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = signal_wave.getparams()

    [fs, a] = read(filename)
    sig_in = np.array(a)

    nbytes_fen = fs * 0.03 # 480
    nbytes_pas = fs * 0.01 # 160

    signals = []

    for i in np.arange(0, len(sig_in), 160, dtype=int):
        signals.append(sig_in[i:i+480])
        
    K = 25
    a_arr = []
    dsp_arr = []
    t = np.arange(0, 0.01 * len(signals), 0.01)
    f = range(0, 2000, 100)

    # Il faut boucler sur tous les échantillons de notre son (rappel, on a pris des fenêtres de 30ms)
    for i in range(0, len(signals)):
        filt = lpc.lpc.kautocor(signals[i], K)
        # a = filt.numerator
        a = lpc.lsf(filt)
        a_arr.append(a)
        dsp_int_arr = []
        for j in f:
            nu = j / fs
            dsp = dsp_calculation_audiolazy(signals[i], K, a, nu)
            dsp_int_arr.append(dsp)
        dsp_arr.append(dsp_int_arr)
        
        
    dsp_arr_np = np.array(dsp_arr)
    return dsp_arr_np


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
        minDist = {'dist': 100000000000000000}
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


# ## Evaluating datasets
reference_set = compute_set(folder=folder, files=paul_set + rossignol_set)
test_set = compute_set(folder=folder, files=remi_set)
test_set = test_set_to_reference(test_set=test_set, reference_set=reference_set, verbose=False)

