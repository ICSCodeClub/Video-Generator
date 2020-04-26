import urllib.request, json, shutil
from requests import get  # to make GET request
from numpy.random import choice # for advanced choices


#https://pixabay.com/api/docs/

KEY = '13233745-b436d2a4655df3612ec66cf71'
FOLDER = 'temp'
RANDOM_CHANCE = 0.7

DEFAULT_PIC = 'https://cdn.pixabay.com/photo/2020/03/02/22/04/poppies-4897100_1280.jpg' #must be .jpg

def getPicsJSON(query):
    #print(str(query).replace(" ","+"))
    with urllib.request.urlopen('https://pixabay.com/api/?'+
                                'key='+KEY+
                                '&q='+str(query).replace(" ","+")+
                                #basic safety settings
                                '&image_type=photo&orientation=horizontal&min_height=700&safesearch=true&'+
                                #try and get the most liked results
                                '&page=1&per_page=10&order=popular') as url:
        data = json.loads(url.read().decode())
        #print(data['hits'])
        return data

def getRandomSinglePicURL(query):
    data = getPicsJSON(query)
    if int(data['totalHits']) <= 0:
        return

    # Weigh each entry by their likes, downloads, and favorites
    weights = []
    for hit in data['hits']:
        weights.append(int(hit['downloads'])+3*int(hit['likes'])+8*int(hit['favorites']))
    normalized = [float(i)/sum(weights) for i in weights]

    # Average the weights with random weights for increased variation
    finalWeights = averageLists(normalized, generateWeights(len(normalized)))
    finalWeights = [float(i)/sum(finalWeights) for i in finalWeights]

    # Return a random choice from numpy
    return choice(data['hits'],  size=1, p=finalWeights)[0]['largeImageURL']

def downloadPicFromUrl(url):
    url = str(url)
    file_name = url[url.rfind('/')+1:len(url)]
    download(url, FOLDER+'/'+file_name)
    return FOLDER+'/'+file_name

def downloadPicFromQuery(query):
    if len(query) < 3:
        query = "uplifting"
    url = str(getRandomSinglePicURL(query))+"";
    file_ext = url[url.rfind('.'):len(url)]
    if len(url) > 2:
        download(url, FOLDER+'/'+query.replace(".","")+file_ext)
        return FOLDER+'/'+query.replace(".","")+file_ext
    else:
        return 'default.jpg'
        

def getFolder():
    return FOLDER+'/'

def downloadFromQuery(query):
    url = getRandomSinglePicURL(query)
    downloadPicFromUrl(url)

def download(url, file_name):
    if url is None:
        return 'default.jpg'
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)

# Generates weights for use in numpy's random choice
# Output looks somewhat like this: [0.41957572502685286, 0.2517454350161117, 0.15104726100966703, 0.09062835660580021, 0.05437701396348013, 0.03262620837808808 ...]
# The output will always sum to 1
def generateWeights(size):
    weights = [RANDOM_CHANCE]
    for i in range(size-1):
        weights.append(weights[i]*RANDOM_CHANCE)
    normalized = [float(i)/sum(weights) for i in weights]
    return normalized

# Averages the values of two lists
def averageLists(l1,l2):
    outlist = []
    for i in range(min([len(l1),len(l2)])):
        outlist.append((l1[i]+l2[i])/2)
    return outlist

#downloads the default pic in the root folder
download(DEFAULT_PIC,'default.jpg')
