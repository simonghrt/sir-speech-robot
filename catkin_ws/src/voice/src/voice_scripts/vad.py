import math
import numpy as np

def is_noise(frame, threshold=1000):
    local_mean = sum(frame) / len(frame)
    local_var = math.sqrt(sum((frame - local_mean)**2) / len(frame))
    if abs(local_var) > threshold:
        return False
    return True

def simulate_real_time(signals, threshold):
    signal_clean = []
    first_voiced = -1
    last_voiced = -1
    frame_duration = 30
    last_frame = []
    previous_last_voiced = -1
    previous_signal_clean = []
    for [signal, frequency] in signals:
        length_frames = math.floor(frame_duration * frequency / 1000)
        for i in range(0, math.floor(len(signal)/length_frames)):
            if (i+1) * length_frames > len(signal):
                max_range = len(signal) - 1
            else:
                max_range = (i+1) * length_frames
            frame = signal[i * length_frames:max_range]
            if is_noise(frame, threshold):
                if last_voiced == -1:
                    previous_signal_clean = signal_clean
                    last_voiced = max_range
                    last_frame = frame
            else:
                if first_voiced == -1:
                    first_voiced = i * length_frames
                if last_voiced != -1:
                    previous_last_voiced = last_voiced
                    last_voiced = -1
            if last_voiced != -1 and (last_voiced / length_frames) - (first_voiced / length_frames) < 5:
                last_voiced = -1
                first_voiced = -1
            if last_voiced == -1 and first_voiced != -1:
                signal_clean.extend(frame)
            if last_voiced != -1 and (last_voiced / length_frames) - (previous_last_voiced / length_frames) < 3:
                signal_clean = previous_signal_clean
    return signal_clean
