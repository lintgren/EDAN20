"""
Tokenizers
Usage: python tokenizer.py < corpus.txt
"""
__author__ = "Pierre Nugues"

import sys
import itertools
import math
import regex as re
"""from lab2 import count"""
text = """Tell me, O muse, of that ingenious hero who
travelled far and wide after he had sacked the famous
town of Troy. ASDGASF ny mening eller nå."""


"""def tokenize(text):
    uses the nonletters to break the text into words
    returns a list of words
    # words = re.split('[\s\-,;:!?.’\'«»()–...&‘’“”*—]+', text)
    # words = re.split('[^a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ’\-]+', text)
    # words = re.split('\W+', text)
    words = re.split('\P{L}+', text)
    words.remove('')
    return words
"""


def tokenize2(text):
    """uses the letters to break the text into words
    returns a list of words"""
    # words = re.findall('[a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ’\-]+', text)
    # words = re.findall('\w+', text)
    words = re.findall('\p{L}+', text)
    return words


def tokenize3(text):
    """uses the punctuation and nonletters to break the text into words
    returns a list of words"""
    # text = re.sub('[^a-zåàâäæçéèêëîïôöœßùûüÿA-ZÅÀÂÄÆÇÉÈÊËÎÏÔÖŒÙÛÜŸ’'()\-,.?!:;]+', '\n', text)
    # text = re.sub('([,.?!:;)('-])', r'\n\1\n', text)
    text = re.sub(r'[^\p{L}\p{P}]+', '\n', text)
    text = re.sub(r'(\p{P})', r'\n\1\n', text)
    text = re.sub(r'\n+', '\n', text)
    return text.split()


def tokenize4(text):
    """uses the punctuation and symbols to break the text into words
    returns a list of words"""
    spaced_tokens = re.sub('([\p{S}\p{P}])', r' \1 ', text)
    one_token_per_line = re.sub('\s+', '\n', spaced_tokens)
    tokens = one_token_per_line.split()
    i = 0
    return tokens

def count_unigrams(words):
    freq = {}
    for word in words.split():
        try:
            freq[word.lower()] +=1
        except:
            freq[word.lower()] = 1
    return freq

def count_bigrams(text):
    """word_pair = zip(text,text[1:])"""
    word_pairs = {}
    words = text.split()
    bigrams = {}
    for idx, word in enumerate(words):
        if idx+1 <len(words):
            try:
                bigrams[(word,words[idx+1])] += 1
            except:
                bigrams[(word, words[idx + 1])] = 1
    return bigrams




if __name__ == '__main__':
    text = open("Selma.txt").read()
    words = tokenize4(text)
    newText = ""
    text2 = ""
    c = re.compile('\p{Lu}[^\.]*')
    for sentence in c.finditer(text):
        sentence = re.sub(r'\p{P}+','',sentence.group())
        sentence = re.sub(r'\n','',sentence)
        text2 +="<s> "+ sentence.lower()+" </s> "
    unigrams = count_unigrams(text2)
    bigrams = count_bigrams(text2)
    p = re.compile(r"\p{L}+")
    nbrOfWords = len(p.findall(re.sub('\p{P}',"",text2)))
    print("nbr of words: "+ str(nbrOfWords))
    nbrOfWords2 = 0
    for nbr in unigrams.values():
        nbrOfWords2 +=nbr
    print("nbrofwords2: "+str(nbrOfWords2))

    sentence = "<s> det var en gång en katt som hette nils </s>"
    uniProb = 0
    words = sentence.split()
    total_prob = 1
    for word in re.finditer(r'\p{L}+|<s>|</s>',sentence):
        print(word.group() + ":\t" +str(unigrams[word.group()])+"\t"+ str(unigrams[word.group()]/nbrOfWords))
        total_prob *= unigrams[word.group()]/nbrOfWords
    print("unigram prob: " + str(total_prob))
    entropy = (-math.log(total_prob)) / 10
    print("Entropy: " + str(entropy))
    print("perplexity: " + str(math.pow(2, entropy)))


    print()
    total_prob = 1
    for idx, word in enumerate(words):
        if idx + 1 < len(words):
            try:
                bi_prob = (bigrams[(word,words[idx+1])])/(unigrams[word])
                print(word+","+words[idx+1] + "\t" + str(bigrams[(word,words[idx+1])]) +"\t"+ str(unigrams[word]) + "\t"+ str(bi_prob))
                total_prob *= bi_prob
            except:
                print(word + "," + words[idx + 1] + "\t" +"0" + "\t" + str(unigrams[word])+"\t"+str(unigrams[words[idx+1]]/nbrOfWords))
                total_prob *= unigrams[words[idx+1]]/nbrOfWords

    print("bigram prob: " + str(total_prob))
    entropy = (-math.log(total_prob))/10
    print("Entropy: " + str(entropy))
    print("perplexity: " + str(math.pow(2,entropy)))