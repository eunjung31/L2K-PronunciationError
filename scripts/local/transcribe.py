import os
from sys import argv
from transformers import AutoProcessor, AutoModelForCTC
import torch
import librosa
import pandas as pd
from tqdm import tqdm
from jiwer import wer

print("")
print("Decoding using Phoneme Recognizer...")

processor = AutoProcessor.from_pretrained("slplab/wav2vec2-xls-r-300m_phone-mfa_korean")
model = AutoModelForCTC.from_pretrained("slplab/wav2vec2-xls-r-300m_phone-mfa_korean")
model.to("cuda")

results = []
dataFolder = argv[1]

for r, d, files in os.walk(dataFolder):
    for fn in tqdm(files):
        if fn.endswith(".wav"):
          result = {}
          result["fileName"] = fn
          fpath = os.path.join(r, fn)
          speech_array, sampling_rate = librosa.load(fpath, sr=16000)
          input_values = processor(speech_array, sampling_rate = sampling_rate, return_tensors="pt", padding="longest").input_values.to("cuda")
          with torch.no_grad():
            logits = model(input_values).logits
            predicted_ids = torch.argmax(logits, dim=-1)
            transcription = processor.batch_decode(predicted_ids)
            trans = transcription[0]
          tpath = fpath.split(".")[0] + ".textgrid"
          f = open(tpath, "r")
          for line in f.readlines():
            ref = line.strip()

          result["transcription"] = trans
          result["reference"] = ref
          print(result)
          results.append(result)

print(len(results))
df = pd.DataFrame(results)
df.to_csv("transcription.csv")
