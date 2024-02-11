from sys import argv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from seaborn import heatmap
from sklearn.metrics import confusion_matrix


def toCM(sentList):
    phoneList = []
    for sent in sentList:
        phones = sent.split(" ")
        nSplits = []
        for p in phones:
            p = p.replace("spn", "***")
            p = p.replace("OE", "oE")
            p = p.replace("UE", "oE")
            p = p.replace("AE", "E")
            nSplits.append(p)
        phoneList += nSplits
    return phoneList


def genCM(CV, CV_ipa, ref, hyp, country, fn):  # cons,vowels
    cm = confusion_matrix(ref, hyp, labels=CV)
    cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
    cm = cm * 100

    fig, ax = plt.subplots(figsize=(10, 10))
    ax = heatmap(
        cm,
        annot=True,
        cmap="Blues",
        fmt=".2f",
        linewidth=0.2,
        cbar=False,
        xticklabels=CV_ipa,
        yticklabels=CV_ipa,
        annot_kws={"size": 5},
    )
    ax.set(xlabel="Realized Phone (Non-native)", ylabel="Canonical Phone (Native)")
    fig.savefig(f"result/{fn}{country}.pdf", bbox_inches="tight")
    df = pd.DataFrame(cm, index=CV, columns=CV)
    df.to_csv(f"result/{fn}{country}.csv")

    return cm


def phoneAnalysis(cm, CV, country, fn):
    diag = cm.diagonal()
    avg = np.average(diag)
    filter1 = diag < avg
    newarr = diag[filter1]
    index = np.argwhere(filter1 == True).tolist()
    phoneList = []
    errorLists = []
    for i in index:
        phoneList.append((CV[i[0]], round(diag[i][0], 2)))
        _pattern = cm[i[0]]
        filter2 = _pattern > 0.01
        index2 = np.argwhere(filter2 == True).tolist()
        errorList = []
        for j in index2:
            if i != j:
                errorList.append((CV[i[0]], CV[j[0]], round(_pattern[j][0], 2)))
        errorLists.append(errorList)
    print("***Phones for Analysis***")
    print(phoneList)
    f = open(f"result/{fn}_phones{country}.txt", "w")
    for phone, val in phoneList:
        f.write("%s\t%s\n" % (phone, val))
    f.close()

    print("\n***Error Patterns for Analysis***")
    print(errorLists)
    g = open(f"result/{fn}_errorPatterns{country}.txt", "w")
    for error in errorLists:
        for a, b, val in error:
            g.write("%s\t%s\t%s\n" % (a, b, val))
    g.close()


def chi2Analysis(CV, country, fn):
    df = pd.read_csv(f"result/{fn}{country}.csv", index_col=0)

    pass


if __name__ == "__main__":
    cons_ipa = ["p", "p͈", "pʰ", "t", "t͈", "tʰ", "k", "k͈", "kʰ", "s", "s͈", "h", "tɕ", "tɕ͈", "tɕʰ", "m", "n", "l", "ɾ", "ŋ", "p̚", "k̚", "t̚", "*"]
    cons = ["B", "BB", "Ph", "D", "DD", "Th", "G", "GG", "Kh", "S", "SS", "H", "J", "JJ", "CHh", "M", "N", "L", "R", "NG", "p", "k", "t", "***"]
    vowels_ipa = ["ɐ", "jɐ", "wɐ", "ɛ", "jɛ", "wɛ", "i", "wi", "ɰi", "o", "jo", "u", "ju", "ʌ", "jʌ", "wʌ", "ɯ", "*"]
    vowels = ["A", "iA", "oA", "E", "iE", "oE", "I", "uI", "euI", "O", "iO", "U", "iU", "EO", "iEO", "uEO", "EU", "***"]
    country = ""  # ZH, VN, TH, JP, EN for each L1 language group, "" for all

    df = pd.read_csv("result/dataforCM.csv", index_col=False)
    refs = df["new_reference"].to_list()
    hyps = df["new_transcription"].to_list()

    ref = toCM(refs)
    hyp = toCM(hyps)
    cCM = genCM(cons, cons_ipa, ref, hyp, country, "cons")
    vCM = genCM(vowels, vowels_ipa, ref, hyp, country, "vowels")

    phoneAnalysis(cCM, cons, country, "cons")
    phoneAnalysis(vCM, vowels, country, "vowels")

    chi2Analysis(cons, country, "cons")
