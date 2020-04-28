from collections import namedtuple

import neuralnet.rnn_generate as gen
import spell_check as spell
import random


CHANCE_TO_RANDOMISE = 0.0
SPELL_CHECK_PASSES = 1

Entry = namedtuple('Entry', 'title content author')

# Parses entry based on training data
def parseData(entry):
    entryByLine = entry.split('\n')
    title = ''
    try:
        title = entryByLine[0].title()
    except:
        return Entry("Error", "No body generated", gen.getAuthorName())
    
    body = ''
    for i in range(len(entryByLine)):
        if i > 0 and len(entryByLine[i]) >= 3:
            body = body + entryByLine[i]+'\n'
    if len(body) < 10:
        body = "No body generated"
    return Entry(title, body, gen.getAuthorName())

# Generates new output and automatically parses it
# Returns a list of Entries that are all spell-and-grammar-checked
def getAndParseOutput(numChars):
    if random.random() < CHANCE_TO_RANDOMISE:
        gen.randomNN()

    rawEntries = gen.getOutput(numChars)
    entries = []
    for raw in rawEntries:
        if len(raw) > 10 :
            #spell check the data twice
            parsed = parseData(raw)
            correctedCont = spell.grammarCheckWithPasses(parsed.content, SPELL_CHECK_PASSES)
            entries.append(Entry(parsed.title, correctedCont, parsed.author))
    return entries
