import math
import regex as re
import pickle
import os
dictionary = dict()
tfIdf = dict()
nbrOfFiles = 9

def index(text,filename):
    p = re.compile(r"\p{L}+")
    i = 0;
    for m in p.finditer(text.lower()):
        if (dictionary.get(m.group())== None):
            dictionary[(m.group())] = dict()
            tmplist = dictionary[m.group()]
            tmplist[filename] = [m.start()]
            dictionary[(m.group())] = tmplist
        elif(dictionary[m.group()].get(filename) == None):
            tmplist = dictionary[m.group()]
            tmplist[filename] = [m.start()]
            dictionary[(m.group())] = tmplist
        else:
            tmplist = dictionary[m.group()][filename]
            tmplist.append(m.start())
            dictionary[m.group()][filename] = tmplist

def get_files(dir, suffix):
    """
    Returns all the files in a folder ending with suffix
    :param dir:
    :param suffix:
    :return: the list of file names
    """
    files = []
    for file in os.listdir(dir):
        if file.endswith(suffix):
            files.append(file)
    return files

def get_nbrOfWords(filename):
    nbrOfWords =0
    for words in dictionary.values():
        positions = words.get(filename)
        if (positions != None):
            nbrOfWords += len(positions)
    return (nbrOfWords)

def tlfIdfValue(word,document,nbrOfWordsInDocument):
    try:
        return ((len(dictionary[word][document])/nbrOfWordsInDocument) * math.log10(nbrOfFiles/len(dictionary[word])))
    except:
        return 0.0

def vectorSpace(document):
    vector = {}
    nbrOfWords = get_nbrOfWords(document)
    for word in dictionary:
        vector[word] = tlfIdfValue(word,document,nbrOfWords)
    return vector

def cosCompare(document1,document2):
    sumd1d2 = 0
    sumd1sqr = 0
    sumd2sqr = 0
    for word in document1:
        sumd1d2 += document1[word]*document2[word]
        sumd1sqr += document1[word]*document1[word]
        sumd2sqr += document2[word] * document2[word]
    return ((sumd1d2)/(math.sqrt(sumd1sqr)*math.sqrt(sumd2sqr)))


"""
Starting main
"""
filenames = get_files("Selma","txt")
for filename in filenames:
    index(open("Selma/"+filename).read(),filename[:-4])

for filename in filenames:
    tfIdf[filename] = vectorSpace(filename[:-4])

for filname in filenames:
    values = " "
    for filname2 in filenames:
        values += str(cosCompare(tfIdf[filname],tfIdf[filname2])) + " "
    print(filname+ values)
print(dictionary["nils"]["kejsaren"])


pickle.dump(dictionary,open("indexer.idx","wb"))