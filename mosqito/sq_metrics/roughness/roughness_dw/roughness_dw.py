# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 10:34:04 2020

@author: wantysal
"""

# Standard imports
import numpy as np
import math
from numpy.fft import fft

# Local imports
from mosqito.sq_metrics.roughness.roughness_dw._roughness_dw_main_calc import _roughness_dw_main_calc 
from mosqito.sq_metrics.roughness.roughness_dw._gzi_weighting import _gzi_weighting
from mosqito.sq_metrics.roughness.roughness_dw._H_weighting import _H_weighting


def roughness_dw(signal, fs, freqs=[], overlap=0):
    """Roughness calculation of a signal sampled at 48kHz.

    The code is based on the algorithm described in "Psychoacoustical roughness:
    implementation of an optimized model" by Daniel and Weber in 1997.
    The roughness model consists of a parallel processing structure that is made up
    of successive stages and calculates intermediate specific roughnesses R_spec,
    which are summed up to determine the total roughness R.

    Parameters
    ----------
    signal :numpy.array
        time signal values or frequency spectrum in dB
    fs : integer
        sampling frequency if signal given in time domain. 
    freqs : np.array
        if signal is given in frequency domain, freqs is the correcponding frequency axis. Default is []
    overlap : float
        overlapping coefficient for the time windows of 200ms

    Outputs
    -------
    R : numpy.array
        roughness
    time : numpy.array
           time axis

    """

    if len(freqs) == 0:
    # Creation of overlapping frames of 200 ms from the input time signal

        # Number of points within each frame according to the time resolution of 200ms
        n = int(0.2 * fs)
    
        # Number of frames according to the given overlap proportion
        nb_frame = math.ceil(len(signal) / ((1 - overlap) * n)) - 1
        
        # # Zero padding for the last segment
        # pad = nb_frame * int(n*(1-overlap))
        # signal = np.append(signal, np.zeros(()))

        # reshaping of the signal according to the overlap and time proportions
        sig = np.zeros((nb_frame,n))
        for i_frame in range(nb_frame):
            sig[i_frame, :] = signal[i_frame * int(n * (1 - overlap)): i_frame * int(n * (1 - overlap)) + n]
        
        # Creation of the corresponding time axis
        time = np.linspace(0, len(signal) / fs, num=nb_frame)
        
        # Calculate Blackman analysis window
        window = np.blackman(n)
        window = window / sum(window)

        # Creation of the spectrum by FFT using the Blackman window
        spectrum = fft(sig * window) * 1.42
        # Frequency axis in Hertz
        freq_axis = np.arange(1, n//2 + 1, 1) * (fs / n)


    else :
        spectrum = signal     
        freq_axis = freqs
        if len(spectrum.shape)>1:
            n = signal.shape[1]
            nb_frame = signal.shape[0]
            fs = int(n * (freqs[0,1] - freqs[0,0]))
            
        else:
            n = len(signal)
            nb_frame = 1
            fs = int(n * (freqs[1] - freqs[0]))
            
    # Initialization of the weighting functions H and g
    hWeight = _H_weighting(n, fs)
    # Aures modulation depth weighting function
    gzi = _gzi_weighting(np.arange(1, 48, 1) / 2)

    R = np.zeros((nb_frame))
    if len(spectrum.shape)>1:   
        for i_frame in range(nb_frame):
            R[i_frame] = _roughness_dw_main_calc(spectrum[i_frame,:], freq_axis, fs, gzi, hWeight)
    else:
        R = _roughness_dw_main_calc(spectrum, freq_axis, fs, gzi, hWeight)


    if len(freqs) == 0:
        return R, time
    else:
        return R
