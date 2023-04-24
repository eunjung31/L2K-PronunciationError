from sys import argv
import numpy as np
import pandas as pd
from seaborn import heatmap
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt


def toCM(sentList):
    phoneList = []
    for sent in sentList:
        phones = sent.split(" ")
        nSplits = []
        for p in phones:
            p = p.replace("spn", "***")
            p = p.replace("OE","oE")
            p = p.replace("UE","oE")
            p = p.replace("AE","E")
            nSplits.append(p)
        phoneList += nSplits
    return phoneList

def genCM(CV,ref,hyp,fn): #cons,vowels
    cm = confusion_matrix(ref, hyp,labels=CV)
    cm = cm.astype('float') / cm.sum(axis=1)[:,np.newaxis]
    fig,ax = plt.subplots(figsize=(10,10))
    ax = heatmap(cm, annot=True, cmap="Blues", fmt='.2f',
            linewidth=.2, cbar=False,
            xticklabels=CV,
            yticklabels=CV,
            annot_kws={"size":5})
    ax.set(xlabel='hyp', ylabel='ref')
    fig.savefig('result/'+  fn + ".pdf", bbox_inches='tight')
    return cm

def phoneAnalysis(cm,CV,fn):
    diag = cm.diagonal()
    avg = np.average(diag)
    filter1 = diag > avg
    newarr = diag[filter1]
    index = np.argwhere(filter1==True).tolist()
    phoneList = []
    errorLists = []
    for i in index:
        phoneList.append((CV[i[0]],round(diag[i][0],2)))
        _pattern = cm[i[0]]
        filter2 = _pattern > 0.01
        index2 = np.argwhere(filter2==True).tolist()
        errorList = []
        for j in index2:
            if i != j:
                errorList.append((CV[i[0]],CV[j[0]],round(_pattern[j][0],2)))
        errorLists.append(errorList)
    print("***Phones for Analysis***")
    print(phoneList)
    f = open('result/' + fn + "_phones.txt", "w")
    for (phone,val) in phoneList:
        f.write("%s\t%s\n" % (phone,val))
    f.close()

    print("\n***Error Patterns for Analysis***")
    print(errorLists)
    g = open('result/' + fn + "_errorPatterns.txt", "w")
    for error in errorLists:
        for (a,b,val) in error:
            g.write("%s\t%s\t%s\n" % (a,b,val))
    g.close()

if __name__ == '__main__':
    cons = ['B','BB', 'Ph','D','DD','Th','G', 'GG','Kh','S','SS','H','J','JJ', 'CHh','M','N','L','R','NG','p', 'k', 't', '***']
    vowels = ['A','iA','oA','E','iE','oE','I', 'O', 'iO','U','iU','EO', 'iEO', 'uEO','EU','euI','***' ]

    df = pd.read_csv("result/dataforCM.csv",index_col=False)
    refs = df["new_reference"].to_list()
    hyps = df["new_transcription"].to_list()

    ref = toCM(refs)
    hyp = toCM(hyps)
    cCM = genCM(cons,ref,hyp,"cons")
    vCM = genCM(vowels,ref,hyp,"vowels")

    phoneAnalysis(cCM,cons, "cons")
    phoneAnalysis(vCM,vowels, "vowels")
