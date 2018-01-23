import pickle
import speech_process as sp

folder = "../../../../../../sir-speech-robot/data/"

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


reference_set = rossignol_set + remi_set + paul_set + simon_set
reference_set = sp.compute_set(folder=folder, files=reference_set)
pickle.dump(reference_set, open('ref_set.pkl', 'wb'))
