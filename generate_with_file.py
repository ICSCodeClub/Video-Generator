import os
from libraries.video_utils import VideoBuilder


SCRIPTS_FOLDER = 'scripts'
OUTPUT_FOLDER = 'output'

def genClipBasedOnFile(path, title = ''):
    videoBulder = VideoBuilder()
    os.makedirs(str(OUTPUT_FOLDER), exist_ok=True)
    with open(path,'r') as file:
        for line in file.read().split('\n'):
            if len(line) > 5:
                if len(title) < 1:
                    title = line
                print('"'+str(line)+'"')
                videoBulder.addClipFromLine(str(line))
        videoBulder.build(os.path.join(OUTPUT_FOLDER, title))
    return os.path.join(OUTPUT_FOLDER, title)

def toFileName(string):
    file_name = "".join( x for x in string if (x.isalnum() or x in "._- "))
    return file_name

path = genClipBasedOnFile("script.txt", title='script')
print(path)

#First, we need to generate entries with entry_utils, then iterate through them
#Then, we need to split the entry up into a line

#using the line, we get an image (or queue it to add to the next line)
#Then, we speak the entire queued up line

#Now that we have a line audio file and a line image file, we combine them into a clip

#When we're totally done, we combine all the clips into a final video
