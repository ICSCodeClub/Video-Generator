#https://www.grammarbot.io/quickstart
from grammarbot import GrammarBotClient
from numpy.random import choice

# Creating the client
# ===================
client = GrammarBotClient()

#API key is optional
client = GrammarBotClient(api_key='KS9C5N3Y')

# ===================
RANDOM_CHANCE = 0.6

# Generates weights for use in numpy's random choice
# Output looks somewhat like this: [0.41957572502685286, 0.2517454350161117, 0.15104726100966703, 0.09062835660580021, 0.05437701396348013, 0.03262620837808808 ...]
# The output will always sum to 1
def generateWeights(size):
    weights = [RANDOM_CHANCE]
    for i in range(size-1):
        weights.append(weights[i]*RANDOM_CHANCE)
    normalized = [float(i)/sum(weights) for i in weights]
    return normalized

# Calls the grammarbot api to correct text
def grammarCheck(text):
    if text is None or len(text) < 3:
        text = ""
        return ""
    #print(str(text))
    res = client.check(str(text))
    changedLength = 0
    for match in res.matches:
        offset = match.replacement_offset + changedLength #get corrected offset
        if match.replacements is not None and len(match.replacements) > 0:
            replacement = choice(match.replacements,  size=1, p=generateWeights(len(match.replacements)), replace=False)[0] #get a random correction
            text = text.replace(text[offset:offset+match.replacement_length],replacement,1) #replace whatever's there with the correction
            changedLength += len(str(replacement)) - match.replacement_length #track changes to string length
    return text

# Recursively grammar check multiple times
# Ideal for long text where certain corrections could cause issues
def grammarCheckWithPasses(text, passes):
    if(int(passes) == 0):
        return text
    else:
        try:
            return grammarCheckWithPasses(grammarCheck(text), int(passes)-1)
        except:
            return text

'''
text = 'By mocking basic human nature, Twain\'s legendary commentary retains its significance deep into the 21st century. The overall point of the book, that minorities are just as human as everyone else and deserve just as many rights as everyone else, is still a 21st century goal. However, possibly Twain\'s most pertinent criticism is the irony of Pap\'s "You call this a government" speech. In it, Pap argues that the government is so outrageous, he might as well not vote. In the trying times of 2016 and the upcoming 2020 election, this is the exact mindset of many Americans. How has Twain predicted so far ahead? Through a cunning analysis of human nature: while he couldn\'t have known the names of the candidates, he knew the mindset of the country and the commonfolk which form it. While his caricature of Pap is obviously wrong, we start debating when we talk about modern politics, even though the paralells are so clear. This was Twain\'s true genious and the reason behind writing his novels.'
text = grammarCheck(text)
print(text)
'''
