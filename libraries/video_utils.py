import os
from moviepy.editor import *


#Make sure we can import base libraries
FILEPATH, filename = os.path.split(os.path.abspath(__file__))
sys.path.insert(1, FILEPATH)
import simple_tts as tts
import base.pixabay
import base.animate_image
import base.string_utils_rewrite




class VideoBuilder():
    def __init__(self):
        self.totalDur = 0
        self.clips = []
        self.queuedLine = ""
    def addClipFromLine(self, line):
        if len(self.queuedLine) > 0:
            line = str(self.queuedLine)+str(line)
            
        queries = base.string_utils_rewrite.get_phrases(str(line))
        imgPath = None
        
        # Go through all queries
        for query in queries:
            if imgPath is None and query is not None:
                print("q: "+str(query))
                imgPath = base.pixabay.downloadPicFromQuery(str(query))

        # If it failed
        if imgPath is None:
            # If the queue is too big, just go for it with any uplifting picture
            if len(self.queuedLine) > 200:
                query = "uplifting"
                imgPath = base.pixabay.downloadPicFromQuerySafe(str(query))
            else: #else, return to try again later
                queuedLine = str(self.queuedLine) + str(line) #try adding to queue
                return
            
        self.addImgWithAudio(imgPath, tts.synthSpeech(str(line)))
        queuedLine = "" # Reset Queue
    
    def addImgWithAudio(self, imgPath, audioPath):
        base.animate_image.queueImageAudioCombine(imgPath, audioPath)
        
    def addClip(self, clip):
        self.totalDur += clip.duration
        self.clips.append(clip)
        
    def build(self, name):
        # pop the queued line
        if len(self.queuedLine) > 0:
            addImgWithAudio(pixabay.downloadPicFromQuerySafe("uplifting"), tts.synthSpeech(queuedLine))
            self.queuedLine = ""
        
        # get image queue
        additionalClips = base.animate_image.getQueue()
        for clip in additionalClips:
            self.addClip(clip)

        # resize all clips to the lowest width and height
        mwidth = self.clips[0].size[0]
        mheight = self.clips[0].size[1]
        for clip in self.clips:
            if clip.size[0] < mwidth:
                mwidth = clip.size[0]
            if clip.size[1] < mheight:
                mheight = clip.size[1]

        #let's ignore this and just set the output resultion
        mwidth = 1280
        mheight = 720

        croppedClips = []
        for clip in self.clips:
            # first scale it up
            croppedClip = clip.resize(width=mwidth)
            if mheight > mwidth:
                croppedClip = clip.resize(height=mheight)

            # then crop it down
            (w, h) = croppedClip.size
            croppedClip = vfx.crop(croppedClip, width=mwidth, height=mheight, x_center=w/2, y_center=h/2)
            croppedClips.append(croppedClip.set_duration(clip.duration))

        # prepare vignette overlay
        vignette = ImageClip(base.pixabay.downloadPicFromUrl('http://i.stack.imgur.com/UsSV9.png'))
        vignette = vignette.resize((mwidth, mheight)).set_duration(self.totalDur)
        
        # compose the clips and add vignette
        concat_clip = concatenate_videoclips(croppedClips, method='compose').set_duration(self.totalDur)
        final_clip = CompositeVideoClip([concat_clip, vignette]).set_duration(self.totalDur)
        final_clip.write_videofile(str(name)+'.webm', fps=20, bitrate='15000k')

        # reset globals
        self.totalDur = 0
        self.clips.clear()
        #base.animate_image.clear()
    
def toFileName(s):
    file_name = "".join( x for x in s.lower() if (x.isalnum() or x in "_- ")).replace(' ','_').replace('.','')
    return file_name
