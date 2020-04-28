from PyDictionary import PyDictionary
from numpy.random import choice
import numpy as np
import random, re, string, math

# Selects up to 3 random words from a line
# May return an empty selection if the line is rather short
# Returns a single string, ideal for queries
def selectWords(line):
    words = getPartOnly(line,'Noun') 
    if len(words) < 1:
        return ""
    maxSize = max([1,int(math.sqrt(len(words)))])
    size = maxSize
    if maxSize >= 2: #Can't generate random if maxSize one
        size = random.randrange(1,maxSize,1)
    
    selection = choice(words, size=size,replace=False)
    for word in selection:
        out = " "+str(word)
    if len(out) < 0:
        return ""
    return out[1:] #remove first space


# Deletes all words that aren't the designated part of speech,
# as dictated by PyDictionary. Returns these words as a list with no punctuation
DICTIONARY = PyDictionary()
def getPartOnly(line,partOfSpeech):
    partOfSpeech = '\''+str(partOfSpeech)+'\''
    words = re.sub('['+string.punctuation+']', '', str(line)).split()
    
    acceptedWords = []
    for word in words:
        meaning = ""
        with HiddenPrints():
            meaning = str(DICTIONARY.meaning(word))
        
        if not (meaning is "None") and len(meaning) > len(partOfSpeech):
            if partOfSpeech in meaning: #hacky, but works
                acceptedWords.append(word)
    return acceptedWords

def toFileName(s):
    file_name = "".join( x for x in s.lower() if (x.isalnum() or x in "_- ")).replace(' ','_').replace('.','')
    return file_name

# From https://stackoverflow.com/questions/8391411/suppress-calls-to-print-python
# PyDictionary LOVES to print garbage
import os, sys
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout
