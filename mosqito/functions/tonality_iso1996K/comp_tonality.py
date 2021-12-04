# -*- coding: utf-8 -*-
"""
    Author: Cristina Taboada (TinaTabo)
    Start date: 17/11/2021
"""

# Local imports
from mosqito.functions.oct3filter.comp_third_spectrum import comp_third_spec
from mosqito.functions.shared.load import load


def comp_tonality(signal, fs):
    """
    <Descirption in english ;-)>

    Parameters
    ----------
    signal : numpy.array
        time signal values
    fs : integer
        sampling frequency

    Outputs
    -------
    prominent_tones: dictionary
        dictionary with {fc:Lp_mean} pairs where prominent tones are detected.
    """

    third_spec = comp_third_spec(is_stationary=True, signal=signal, fs=fs)

    # -- Obtain the lists of the central frequencies and the average Lp
    fc = third_spec["freqs"]
    Lp_mean = third_spec["values"]

    # -- Length of the lists, the 2 have the same length.
    Lp_len = len(Lp_mean)

    # -- List where the indexes corresponding to the positions where there is 
    # -- a prominent tone will be stored.
    index_tone_list = []

    for x in range(0, Lp_len):
        if x > 0 and x < 27:  # dirty correction, to be improved
            # -- Variables to compare
            Lp_prev = int(Lp_mean[x - 1])
            Lp = int(Lp_mean[x])
            Lp_post = int(Lp_mean[x + 1])

            # -- calculate the difference
            Lp_diff_prev = Lp - Lp_prev
            Lp_diff_post = Lp - Lp_post

            # -- Compare levels to determine if it is a prominent tone.
            if x > 0 and x < 9:
                # -- "LOW FREQUENCY --> difference 15 dB".
                if Lp_diff_prev >= 15 and Lp_diff_post >= 15:
                    # -- there is a tone in x, we store its value.
                    index_tone_list.append(x)

            elif x > 8 and x < 14:
                # -- "HALF FREQUENCY --> difference 8 dB"
                if Lp_diff_prev >= 8 and Lp_diff_post >= 8:
                    # -- there is a tone in x, we store its value.
                    index_tone_list.append(x)
            elif x > 13 and x < 30:
                # -- "HIGH FREQUENCY --> 5 dB difference".
                if Lp_diff_prev >= 5 and Lp_diff_post >= 5:
                    # -- there is a tone in x, we store its value.
                    index_tone_list.append(x)

    # -- Dictionary in which the data corresponding to the prominent tones 
    # -- will be stored, i.e. {fc : Lp_mean}
    prominent_tones = {}

    for i in range(0, len(index_tone_list)):
        index = index_tone_list[i]
        key = fc[index]
        value = Lp_mean[index]
        prominent_tones[key] = value

    # -- Return of the function.
    return prominent_tones

#-- Main call to the function for its execution.
if __name__ == "__main__":
    sig, fs = load(True, "tests/input/1KHZ60DB.WAV", calib=1)
    tones = comp_tonality(sig, fs)
    pass