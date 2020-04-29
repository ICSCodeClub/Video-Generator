# Google's CLOUD TEXT-TO-SPEECH https://cloud.google.com/text-to-speech/
# https://googleapis.dev/python/texttospeech/latest/gapic/v1beta1/api.html?highlight=enums#google.cloud.texttospeech_v1beta1.TextToSpeechClient.enums


from gtts import gTTS
import os, re, string


FOLDER = 'base\\temp'
DIR = os.path.split(os.path.realpath(__file__))[0]


# ===================

def synthSpeech(line):
    filename = str(line)
    if len(filename) > 15:
        filename = filename[0:15]
    
    audio_created = gTTS(text=line, lang='en',
                         slow=True)
    audio_created.save(toFileName(getFolder()+filename))
    return toFileName(getFolder()+filename)
def getFolder():
    return DIR+'\\'+FOLDER+'\\'
def toFileName(s):
    file_name = "".join( x for x in s.lower() if (x.isalnum() or x in "_- ")).replace(' ','_').replace('.','')
    return file_name
