#From https://gist.github.com/karimkhanp/4b7626a933759d0113d54b09acef24bf

import nltk

nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

from nltk.corpus import stopwords


sentence_re = r'(?:(?:[A-Z])(?:.[A-Z])+.?)|(?:\w+(?:-\w+)*)|(?:\$?\d+(?:.\d+)?%?)|(?:...|)(?:[][.,;"\'?():-_`])'
lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()
grammar = r"""
    NBAR:
        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns
        
    NP:
        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...
        {<NBAR>}
"""
chunker = nltk.RegexpParser(grammar)
stopwords = stopwords.words('english')

def leaves(tree):
    for subtree in tree.subtrees(filter = lambda t: t.label()=='NP'):
        yield subtree.leaves()

def normalise(word):
    word = word.lower()
    word = lemmatizer.lemmatize(word)
    return word

def get_terms(tree):
    for leaf in leaves(tree):
        term = [ normalise(w) for w,t in leaf ]
        yield term

# The method to call to get a list of all noun phrases
def get_phrases(text):
    toks = nltk.regexp_tokenize(text, sentence_re)
    postoks = nltk.tag.pos_tag(toks)
    tree = chunker.parse(postoks)
    
    terms = get_terms(tree)
    phrases = [" ".join(term) for term in terms]
    return phrases



