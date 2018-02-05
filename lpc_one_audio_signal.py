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
from time import time

def get_signal_from_wav(file):
    signal_wave = wave.open("data/" + file)
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = signal_wave.getparams()

    fe = framerate

    [fs, a] = read("data/" + file)
    sig_in = np.array(a)

    nbytes_fen = fs * 0.03 # 480
    nbytes_pas = fs * 0.01 # 160

    signals = []

    for i in np.arange(0, len(sig_in), 160, dtype=int):
        signals.append(sig_in[i:i+480])

    return (signals, fe)


# Functions for lpc processing

def params_signal(signal, K):

    alpha = []
    k = []
    # a est un tableau de tableau (taille croissante)
    a = []

    alpha.append(phi(signal, 0))
    if (phi(signal, 0) == 0):
        if (phi(signal, 1) == 0):
            k.append(0)
        else:
            print("Possible issue here")
            k.append(0)
    else:
        k.append(-phi(signal, 1) / phi(signal, 0))
    a.append([-k[0]])

    for n in range(1, K):
        alpha_val = alpha[n-1] * (1 - (k[n-1]**2))
        alpha.append(alpha_val)
        sum_int = 0
        for p in range(0, n):
            sum_int += a[n-1][p] * phi(signal, n - p)
        int_val = (phi(signal, n) - sum_int)
        if (alpha_val == 0):
            if (int_val == 0):
                k.append(0)
            else:
                print("Possible issue here")
                k.append(0)
        else:
            k.append((-1/alpha_val) * int_val)
        a_array = []
        for q in range(0, n):
            int_a_val = a[n-1][q] + k[n] * a[n-1][n-q-1]
            a_array.append(int_a_val)
        a_array.append( -k[n])
        a.append(a_array)

    return (alpha, k, a)

def dsp_calculation(signal, K, a, nu, audiolazy): 
    sum_sigma = 0
    for i in range(0, K):
        if audiolazy == True:
            sum_sigma += a[i] * phi(signal, i)
        else:
            sum_sigma += a[K-1][i] * phi(signal, i)
    sigma_e = phi(signal, 0) - sum_sigma
    sum_den_dsp = 0
    for j in range(0, K):
        if audiolazy == True:
            sum_den_dsp += a[j] * cmath.exp(2 * cmath.pi * nu * j * 1j)
        else:
            sum_den_dsp += a[K-1][j] * cmath.exp(2 * cmath.pi * nu * j * 1j)
    den_dsp = (abs(1 - sum_den_dsp))**2
    dsp = 0
    if (den_dsp != 0 and sigma_e != 0):
        dsp = sigma_e / den_dsp
    return dsp

def phi(signal, k_ind):
    # phi est un estimateur de la fonction d'autocorrélation du signal
    N = len(signal)
    somme = 0
    for i in range(0, N - k_ind):
        somme += signal[i] * signal[i + k_ind]
    return (somme / N)

def plt_dsp(signals, K, audiolazy, fe):

    alpha_arr = []
    k_arr = []
    a_arr = []
    dsp_arr = []

    t = np.arange(0, 0.01 * len(signals), 0.01)
    f = range(0, 2000, 100)

    # Il faut boucler sur tous les échantillons de notre son (rappel, on a pris des fenêtres de 30ms)
    for i in range(0, len(signals)):
        # t2 = time()
        if audiolazy == True:
            filt = lpc.lpc.kautocor(signals[i], K)
            a = lpc.lsf(filt)
        else:
            [alpha, k, a] = params_signal(signals[i], K)
            alpha_arr.append(alpha)
            k_arr.append(k)
        a_arr.append(a)
        # t3 = time()
        dsp_int_arr = []
        for j in f:
            nu = j / fe
            dsp = dsp_calculation(signals[i], K, a, nu, audiolazy)
            dsp_int_arr.append(dsp)
        if audiolazy == True:
            dsp_arr.append(dsp_int_arr[::-1])
        else:
            dsp_arr.append(dsp_int_arr)
        # t4 = time()
        # print('Exec params signal {}'.format(t3-t2))
        # print('Exec dsp {}'.format(t4-t3))

    plt.pcolormesh(f, t, dsp_arr)
    plt.title('STFT Magnitude')
    plt.ylabel('Time [sec]')
    plt.xlabel('Frequency [Hz]')
    plt.show()


t0 = time()
K = 25
audiolazy = True
[signals, fe] = get_signal_from_wav("stop.wav")
plt_dsp(signals, K, audiolazy, fe)
t1 = time()
print('Executed in {}'.format(t1 - t0))
