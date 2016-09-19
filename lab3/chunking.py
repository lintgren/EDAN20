
import regex as re

def tokenize4(text):
    """uses the punctuation and symbols to break the text into words
    returns a list of words"""
    spaced_tokens = re.sub('([\p{S}\p{P}])', r' \1 ', text)
    one_token_per_line = re.sub('\s+', '\n', spaced_tokens)
    tokens = one_token_per_line.split()
    i = 0
    return tokens



text = open("Selma.txt").read()
tokens =tokenize4(text)
hit = 0
for token in tokens:
    if(re.search('\p{Lu}',token) != None) and hit == 0:
        print(token)
        hit= 1


