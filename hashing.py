import imagehash
import PIL
import main_features as mf

filename = "oki_doki_boomer_09.mp3"

def hash(feature):
    
    data =  PIL.Image.fromarray(feature,mode= 'RGB')
    songhash = imagehash.phash(data)
    return songhash

song ,sr = mf.load_sound(filename)

spect = mf.spectro(song, sr)

feature_1 = mf.feature_1(song, sr)

feature_2 = mf.feature_2(song, sr)

feature_3 = mf.feature_3(song, sr)

hash_spect = hash(spect)
print(hash_spect)


hash_f1 = hash(feature_1)
print(hash_f1)


hash_f2 = hash(feature_2)
print(hash_f2)


hash_f3 = hash(feature_3)
print(hash_f3)

