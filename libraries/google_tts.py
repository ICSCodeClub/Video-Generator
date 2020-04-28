# Google's CLOUD TEXT-TO-SPEECH https://cloud.google.com/text-to-speech/
# https://googleapis.dev/python/texttospeech/latest/gapic/v1beta1/api.html?highlight=enums#google.cloud.texttospeech_v1beta1.TextToSpeechClient.enums


from google.cloud import texttospeech
import os, re, string

# Creating the client
# ===================
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r''+os.path.dirname(os.path.realpath(__file__))+'\\google-key.json'
client = texttospeech.TextToSpeechClient()

FOLDER = 'base\\temp'
DIR = os.path.split(os.path.realpath(__file__))[0]

#print("\n"+str(client.list_voices())+"\n")

# ===================

def synthSpeech(line):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=line)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.types.VoiceSelectionParams(language_code='en-US',
                                                    ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE) #Wavenet A with speed 0.8 seems the best, or wavenet F with -2.8 pitch and 0.6 speed

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16,
                                                  speaking_rate=0.8)
    #print("\n"+str(audio_config)+"\n")
    
    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # Save the file, then return the path
    return writeOutputWithName(response.audio_content, str(line))

def writeOutput(audio):
    return writeOutputWithName(audio, "file_output_speech")
        
def writeOutputWithName(audio, name):
    # Shorten the name (in case it's too long)
    concatText = toFileName(name)
    while len(concatText) > 40 and '_' in concatText:
        concatText = concatText[0:concatText.rfind('_')]
    if len(concatText) > 40:
        concatText = concatText[0:40]
        
    # Then write the file
    os.makedirs(getFolder()+os.path.dirname(name), exist_ok=True)
    with open(getFolder()+concatText+'.wav', 'wb') as out:
        out.write(audio)

    # Now, return the path
    return getFolder()+concatText+'.wav'
def getFolder():
    return DIR+'\\'+FOLDER+'\\'
def toFileName(s):
    file_name = "".join( x for x in s.lower() if (x.isalnum() or x in "_- ")).replace(' ','_').replace('.','')
    return file_name
