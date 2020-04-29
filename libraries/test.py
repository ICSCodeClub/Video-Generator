import os
from moviepy.editor import *
import moviepy.video.fx.all as vfx


#Make sure we can import base libraries
FILEPATH, filename = os.path.split(os.path.abspath(__file__))
sys.path.insert(1, FILEPATH)
import simple_tts as tts
import base.pixabay
import base.animate_image
import base.string_utils_rewrite

paths = ['C:\\Users\\leonl\\OneDrive\\Workspaces\\Python\\Video-Generator\\libraries\\base\\temp\\short script.webm',
         'C:\\Users\\leonl\\OneDrive\\Workspaces\\Python\\Video-Generator\\libraries\\base\\temp\\don.webm',
         'C:\\Users\\leonl\\OneDrive\\Workspaces\\Python\\Video-Generator\\libraries\\base\\temp\\man.webm']


totalDur = 0
clips = []
for path in paths:
    clip = VideoFileClip(path)
    clips.append(clip)
    totalDur += clip.duration

mwidth = clips[0].size[0]
mheight = clips[0].size[1]
for clip in clips:
    if clip.size[0] < mwidth:
        mwidth = clip.size[0]
    if clip.size[1] < mheight:
        mheight = clip.size[1]

#let's ignore this and just set the output
mwidth = 1280
mheight = 720

print("\n\n"+str(mwidth)+", "+str(mheight)+"\n\n")

croppedClips = []
for clip in clips:
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
vignette = vignette.resize((mwidth, mheight)).set_duration(totalDur)
        
print(clips)
# compose the clips and add vignette
concat_clip = concatenate_videoclips(croppedClips, method='compose').set_duration(totalDur)
final_clip = CompositeVideoClip([concat_clip, vignette]).set_duration(totalDur)
final_clip.write_videofile('test.webm', fps=20, bitrate='15000k')
