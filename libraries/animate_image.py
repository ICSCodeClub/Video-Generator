import os, shutil, time
from moviepy.editor import *
import pixabay
from gtts import gTTS

THREADS = 1
SMOOTHNESS = 2.3

DIR = os.path.split(os.path.realpath(__file__))[0]
FOLDER = 'temp'

# Turns an image into a video by applying a nice zoom.
# Returns the resulting path
def renderImgZoom(imgPath, duration):
    os.makedirs(str(FOLDER), exist_ok=True)
    # First, get the file name without extension for saving later
    file_name = ""
    if '/' not in imgPath:
        file_name = imgPath[:imgPath.rfind('.')]
    else:
        file_name = imgPath[imgPath.rfind('/')+1:imgPath.rfind('.')]

    # Get the image clip and save its size
    imgClip = ImageClip(imgPath)
    orgSize = imgClip.size

    # Animate the clip
    imgClip = imgClip.resize(height=orgSize[1]*SMOOTHNESS).resize(lambda t : 1+0.008*t).set_position(('center', 'center')).set_duration(duration)
    imgClip = CompositeVideoClip([imgClip]).resize(width=orgSize[0])
    # Render the clip
    vid = CompositeVideoClip([imgClip.set_position(('center', 'center'))], size=orgSize)
    vid.write_videofile(DIR+'/'+FOLDER+'/'+file_name+'.webm',bitrate="15000k", fps=20,verbose=False, logger=None)
    # Return the location
    return DIR+'/'+FOLDER+'/'+file_name+'.webm'

# Returns the VideoClip that is the result of combining target video and audio files
def videoAudioCombine(vidPath, audioPath):
    videoclip = VideoFileClip(vidPath)
    audioclip = AudioFileClip(audioPath)

    new_audioclip = CompositeAudioClip([audioclip])
    
    #cut longer file short. should probably remove
    if new_audioclip.duration > videoclip.duration:
        videoclip = videoclip.set_audio(new_audioclip.set_duration(videoclip))
    else:
        videoclip = videoclip.set_duration(new_audioclip.duration).set_audio(new_audioclip)
    return videoclip

from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=THREADS)
asyncs = []

# Combines an image with audio immediately, animating the image in the process.
# Can easily take around 10 seconds for even short clips
def imageAudioCombine(imgPath, audioPath):
    audioclip = AudioFileClip(audioPath)
    
    videopath = renderImgZoom(imgPath, audioclip.duration)
    combinedclip = videoAudioCombine(videopath, audioPath)
    return combinedclip

# Combines two video files and adds the resulting processes to the file queue
# Get the results with getQueue(), which returns a list of VideoClips that have the audio added
def queueImageAudioCombine(imgPath, audioPath):
    global pool, asyncs
    
    async_result = pool.apply_async(imageAudioCombine, (imgPath, audioPath))
    asyncs.append(async_result)
    if THREADS == 1:
        async_result.get()
    return async_result
    
# Processes the entire file queue and returns its results
def getQueue():
    global asyncs

    returnValues = []
    for ttt in asyncs:
        returnValues.append(ttt.get())
    asyncs.clear()
    return returnValues

# Clears the temp folder
def clear():
    shutil.rmtree(DIR+'/'+FOLDER, ignore_errors=True, onerror=None)
    os.makedirs(str(FOLDER), exist_ok=True)


#videoclip = videoAudioCombine(DIR+"/temp/happy.webm",DIR+"/she is sad.wav")
#videoclip.write_videofile("new_filename.webm")

