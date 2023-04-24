import argv
import pandas as pd
from seaborn import heatmap
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

def toCM(sentList):
    phoneList = []
    for sent in sentlist:
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

def genCM(CV): #cons,vowels
    cm = confusion_matrix(ref, hyp,labels=CV)
    cm = cm.astype('float') / cm.sum(axis=1)[:,np.newaxis]
    fig,ax = plt.subplots(figsize=(10,10))
    ax = heatmap(cm, annot=True, cmap="Blues", fmt='.2f',
            linewidth=.2, cbar=False,
            xticklabels=CV,
            yticklabels=CV,
            annot_kws={"size":5},
            )
    ax.set(xlabel='hyp', ylabel='ref')
    fig.savefig({}.format(CV) + ".pdf", bbox_inches='tight')
    return cm

def phoneAnalysis(cm,CV):
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
    print("***Phonesfor Analysis***")
    print(phoneList)
    print("\n***Error Patterns for Analysis***")
    print(errorLists)


if __name__ == '__main__':
    cons = ['B','BB', 'Ph','D','DD','Th','G', 'GG','Kh','S','SS','H','J','JJ', 'CHh','M','N','L','R','NG','p', 'k', 't', '***']
    vowels = ['A','iA','oA','E','iE','oE','I', 'uI','O', 'iO','U','iU','EO', 'iEO', 'uEO','EU','euI','***' ]

    csvFile = sys.argv[1]
    df = pd.read_csv(csvFile,index_col=False)

    refs = df["reference"].to_list()
    hyps = df["transcription"].to_list()
    ref = toCM(refs)
    hyp = toCM(hyps)

    cCM = genCM(cons)
    vCM = genCM(vowels)

    phoneAnalysis(cCM,cons)
    phoneAnalysis(vCm,vowles)
