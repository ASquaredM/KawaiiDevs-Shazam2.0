import librosa
from scipy import signal

filename = "01.mp3"

def load_sound(filename):
    
    data, sr = librosa.load(filename,duration=60.0)
    return [data,sr]

def spectro(song,sr):
    f, t, sxx = signal.spectrogram(song, sr)
    return sxx


def feature_1(song,sr):
    centroid = librosa.feature.spectral_centroid(y=song, sr=sr)
    return centroid

def feature_2(song,sr):
    spect_bw = librosa.feature.spectral_bandwidth(y=song, sr=sr)
    return spect_bw

