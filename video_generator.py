import video_utils, entry_utils
import os

SCRIPTS_FOLDER = 'scripts'
OUTPUT_FOLDER = 'output'
def neuralClipGen():
    print('Generating Entries')
    entries = entry_utils.getAndParseOutput(40000)
    
    # Save all entries directly
    print('Saving entries')
    paths = []
    for entry in entries:
        file_name = str(entry.title)+" by "+str(entry.author)
        file_name = toFileName(file_name)

        os.makedirs(str(SCRIPTS_FOLDER), exist_ok=True)
        with open(SCRIPTS_FOLDER+'/Script '+file_name+'.txt', "w") as file:
            file.write("-\n "+entry.title+"\n"+entry.content)
            paths.append(SCRIPTS_FOLDER+'/Script '+file_name+'.txt')

    # Generate Videos
    for path in paths:
        genClipBasedOnFile(path)

def genClipBasedOnFile(path, title = ''):
    os.makedirs(str(OUTPUT_FOLDER), exist_ok=True)
    with open(path,'r') as file:
        for line in file.read().split('\n'):
            if len(line) > 5:
                if len(title) < 1:
                    title = line
                video_utils.addClipFromLine(line)
        video_utils.buildVideo(os.path.join(OUTPUT_FOLDER, title))

def toFileName(string):
    file_name = "".join( x for x in string if (x.isalnum() or x in "._- "))
    return file_name
        
genClipBasedOnFile("script.txt")

#First, we need to generate entries with entry_utils, then iterate through them
#Then, we need to split the entry up into a line

#using the line, we get an image (or queue it to add to the next line)
#Then, we speak the entire queued up line

#Now that we have a line audio file and a line image file, we combine them into a clip

#When we're totally done, we combine all the clips into a final video
