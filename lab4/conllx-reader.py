"""
CoNLL-X and CoNLL-U file readers and writers
"""
__author__ = "Pierre Nugues"

import os
import itertools
import operator


def get_files(dir, suffix):
    """
    Returns all the files in a folder ending with suffix
    Recursive version
    :param dir:
    :param suffix:
    :return: the list of file names
    """
    files = []
    for file in os.listdir(dir):
        path = dir + '/' + file
        if os.path.isdir(path):
            files += get_files(path, suffix)
        elif os.path.isfile(path) and file.endswith(suffix):
            files.append(path)
    return files


def read_sentences(file):
    """
    Creates a list of sentences from the corpus
    Each sentence is a string
    :param file:
    :return:
    """
    f = open(file).read().strip()
    sentences = f.split('\n\n')
    return sentences


def split_rows(sentences, column_names):
    """
    Creates a list of sentence where each sentence is a list of lines
    Each line is a dictionary of columns
    :param sentences:
    :param column_names:
    :return:
    """
    new_sentences = []
    root_values = ['0', 'ROOT', 'ROOT', 'ROOT', 'ROOT', 'ROOT', '0', 'ROOT', '0', 'ROOT']
    start = [dict(zip(column_names, root_values))]
    for sentence in sentences:
        rows = sentence.split('\n')
        sentence = [dict(zip(column_names, row.split())) for row in rows if row[0] != '#']
        sentence = start + sentence
        new_sentences.append(sentence)
    return new_sentences


def save(file, formatted_corpus, column_names):
    f_out = open(file, 'w')
    for sentence in formatted_corpus:
        for row in sentence[1:]:
            # print(row, flush=True)
            for col in column_names[:-1]:
                if col in row:
                    f_out.write(row[col] + '\t')
                else:
                    f_out.write('_\t')
            col = column_names[-1]
            if col in row:
                f_out.write(row[col] + '\n')
            else:
                f_out.write('_\n')
        f_out.write('\n')
    f_out.close()

def verb_subject_freq(corpus):
    rootWord = None
    subject = None
    freq = {}
    count = 0
    for sentence in corpus:
        for word in sentence:
            if(word['deprel'] == 'SS'):
                try:
                    freq[((sentence[int(word['head'])])['form'].lower(),word['form'].lower())] += 1
                except:
                    freq[((sentence[int(word['head'])])['form'].lower(),word['form'].lower())] = 1

                count +=1
    print(count)
    return freq

def verb_subject_object_freq(corpus):
    freq = {}
    count = 0
    sentenceNbr = 0
    for sentence in corpus:
            sentenceNbr += 1
            objectIdxes = list(index for (index, d) in enumerate(sentence) if d["deprel"] == "OO")
            objectDict = {}
            for objectidx in objectIdxes:
                objectDict[objectidx] = (sentence[objectidx])['head'].lower()
            for word in sentence:
                if (word['deprel'].lower() == 'ss' and word['head'].lower() in objectDict.values()):
                    gen = ((v, k) for k, v in objectDict.items() if v==word['head'])
                    for k,v in gen:
                        count +=1
                        try:
                            freq[(((sentence[int(word['head'])])['form']).lower(),
                                (word['form']).lower(),
                                ((sentence[int(v)])['form']).lower())] += 1
                        except:
                            freq[(((sentence[int(word['head'])])['form']).lower(), (word['form']).lower(),
                                ((sentence[int(v)])['form']).lower())] = 1

    print(count)
    return freq

def verb_subject_object_freq2(corpus):
    rootWord = None
    subject = None
    freq = {}
    count = 0
    for sentence in corpus:
            objectIdxes = list(index for (index, d) in enumerate(sentence) if d["deprel"].lower() == "dobj")
            objectDict = {}
            for objectidx in objectIdxes:
                objectDict[objectidx] = (sentence[objectidx])['head'].lower()
            for word in sentence:
                if (word['deprel'].lower() == 'nsubj' and word['head'].lower() in objectDict.values()):
                    gen = ((v, k) for k, v in objectDict.items() if v==word['head'])
                    for k,v in gen:
                        count +=1
                        try:
                            freq[(((sentence[int(word['head'])])['form']).lower(),
                                (word['form']).lower(),
                                ((sentence[int(v)])['form']).lower())] += 1
                        except:
                            freq[(((sentence[int(word['head'])])['form']).lower(), (word['form']).lower(),
                                ((sentence[int(v)])['form']).lower())] = 1
    print(count)

    return freq




if __name__ == '__main__':
    column_names_2006 = ['id', 'form', 'lemma', 'cpostag', 'postag', 'feats', 'head', 'deprel', 'phead', 'pdeprel']

    train_file = 'swedish_talbanken05_train.conll'
    # train_file = 'test_x'
    test_file = 'swedish_talbanken05_test.conll'

    sentences = read_sentences(train_file)
    formatted_corpus = split_rows(sentences, column_names_2006)
    #print(formatted_corpus[0])
    #print(train_file, len(formatted_corpus))
    sorteed = sorted(((v, k) for k, v in verb_subject_freq(formatted_corpus).items()), reverse=True)
    for v, k in sorteed[:5]:
        print(str(v) + ' ' + str(k))

    sorteed = sorted(((v, k) for k, v in verb_subject_object_freq(formatted_corpus).items()), reverse=True)
    for v, k in sorteed[:5]:
        print(str(v) + ' ' + str(k))

    column_names_u = ['id', 'form', 'lemma', 'upostag', 'xpostag', 'feats', 'head', 'deprel', 'deps', 'misc']

    files = get_files('ud-treebanks-v1.3/', 'train.conllu')
    for train_file in files:
        sentences = read_sentences(train_file)
        formatted_corpus = split_rows(sentences, column_names_u)
        print(train_file, len(formatted_corpus))
        #print(formatted_corpus[0])
        for sentences in formatted_corpus:
            for idx,word in enumerate(sentences):
                if '-' in word['id']:
                    sentences.remove(word)
        myDict = sorted(((v, k) for k, v in verb_subject_object_freq2(formatted_corpus).items()), reverse=True)
        for v, k in myDict[:5]:
            print(str(v) + ' ' + str(k))
        #sorted(for key, value in myDict.items())