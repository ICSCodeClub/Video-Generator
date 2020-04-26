import os
from moviepy.editor import *
import pixabay, animate_image, string_utils, google_tts

totalDur = 0
clips = []

queuedLine = ""
def addClipFromLine(line):
    global queuedLine

    if len(queuedLine) > 0:
        line = str(queuedLine)+str(line)
        
    query = string_utils.selectWords(str(line))
    imgPath = pixabay.downloadPicFromQuery(str(query))

    # If it failed
    if imgPath is None:
        queuedLine = str(queuedLine) + str(line) #try adding to queue
        # If the queue is too big, just go for it with any uplifting picture
        if len(query) > 200:
            query = "uplifting"
            imgPath = pixabay.downloadPicFromQuery(str(query))
        else: #else, return to try again later
            return
        
    addImgWithAudio(imgPath, google_tts.synthSpeech(str(line)))
    queuedLine = ""

def addImgWithAudio(imgPath, audioPath):
    animate_image.queueImageAudioCombine(imgPath, audioPath)
    
def buildVideo(name):
    global totalDur, clips, queuedLine

    # pop the queued line
    if len(queuedLine) > 0:
        addImgWithAudio(pixabay.downloadPicFromQuery("uplifting"), google_tts.synthSpeech(queuedLine))
    
    # get image queue
    additionalClips = animate_image.getQueue()
    for clip in additionalClips:
        totalDur += clip.duration
        clips.append(clip)

    # resize all clips to the lowest width and height
    mwidth = clips[0].size[0]
    mheight = clips[0].size[1]
    for clip in clips:
        if clip.size[0] < mwidth:
            mwidth = clip.size[0]
        if clip.size[1] < mheight:
            mheight = clip.size[1]
    for clip in clips:
        clip.crop(width=mwidth, height=mheight, x_center=clip.size[0]/2.0-1 , y_center=clip.size[1]/2.0-1)

    # prepare vignette overlay
    vignette = ImageClip(pixabay.downloadPicFromUrl('http://i.stack.imgur.com/UsSV9.png'))
    vignette = vignette.resize((mwidth+2, mheight+2))
    
    # compose the clips and add vignette
    concat_clip = concatenate_videoclips(clips, method="compose").set_duration(totalDur)
    final_clip = CompositeVideoClip([concat_clip, vignette]).set_duration(totalDur)
    final_clip.write_videofile(name+'.avi',fps=20, codec='mpeg4', bitrate='15000k')

    # reset globals
    totalDur = 0
    clips.clear()
    animate_image.clear()
