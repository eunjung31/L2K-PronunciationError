from tqdm import tqdm
import pandas as pd
import sys

def createDict():
    f = open("per_utt", "r")
    refs, hyps = [], []
    dataList = []
    for i , line in enumerate(tqdm(f.readlines())):
        line = line.strip()
        split_ = line.split(" ")
        splits = [v for v in splits_ if v]
        fn = splits[0]
        index = splits[1]
        if index == 'ref':
            data = {}
            data["fileName"] = fn
            data["new_reference"] = " ".join(splits[2:])
        elif index == 'hyp':
            data["new_transcription"] = " ".join(splits[2:])

        if (i ==0) or (i % 4 == 0):
            dataList.append(data)
        return dataList

def results(dataDict):
    dataList = []
    for i in tqdm(range(len(dataDict))):
        result = {}
        result["fileName"] = dataDict[i]["fileName"]
        result["new_reference"] = dataDict[i]["new_reference"]
        result["new_transcription"] = dataDict[i]["new_transcription"]

        dataList.append(result)
    return dataList

dataDict = createDict()
results = results(dataDict)

df = pd.DataFrame.from_dict(results)
df.to_csv("dataforCM.csv",index=False)
