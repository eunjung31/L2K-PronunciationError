import pandas as pd

df = pd.read_csv("result/transcription.csv",index_col=False)

fnList = df["fileName"].tolist()
refList = df["reference"].tolist()
transList = df["transcription"].tolist()

f = open("ref", "w")
for i in range(len(refList)):
    f.write("%s\t%s\n"%(fnList[i], refList[i]))
f.close()

g = open("hyp", "w")
for j in range(len(transList)):
    g.write("%s\t%s\n"%(fnList[j], transList[j]))
g.close()
