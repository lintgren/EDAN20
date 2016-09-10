"""
Tokenizers
Usage: python tokenizer.py < corpus.txt
"""
__author__ = "Pierre Nugues"

import sys
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
    return tokens


if __name__ == '__main__':
    """text = sys.stdin.read()"""
    text = open("Selma.txt").read()
    """words = tokenize(text)
    for word in words:
        print(word)
    words = tokenize2(text)
    """
    words = tokenize3(text)
    newText = ""
    i = 0
    for word in words:
        newText += word+ " "
    sentence = ""
    hit = 0
    c = re.compile('[A-Z](\p{L}|,|\s)*.')
    for sentencee in c.finditer(newText):
        sentence +="<s> "+ sentencee.group().lower()+" </s> "
    p = re.compile(r"\p{L}+")
    print(len(p.findall(re.sub('\p{P}',"",sentence))))
    for word in words:
        if(hit == 0 and re.search('[A-Z]',word) != None):
            hit=1
            sentence +="<s> "+word
        elif hit == 1:
            sentence += " " +word
            if(word == '.'):
                newText+=re.sub('\p{P}','',sentence[:-2].lower())+" </s> "
                sentence= ""
                hit =0
"""    print(newText)"""
"""print(len(p.findall(newText)))"""
"""print(count.count_unigrams(count.tokenize(text)))"""