#!/usr/bin/env python3
import sys
import html
from google.cloud import translate

DEST_LANGUAGE = "fr"

class Scene:
    def __init__(self, num, time, text):
        self.num = num
        self.time = time
        self.text = text
    def toFile(self):
        return(self.num+"\n"+self.time+"\n"+self.text+"\n\n")
    def __repr__(self):
        return (self.num+" "+self.time+" "+self.text+"\n")

def getScenes(filename):
    scenes = []
    try:
        f = open(filename, "r")#, encoding="ISO-8859-1")
    except:
        sys.exit("This file doesn't exist.")
    txt = f.read()
    for inter in (txt.split("\n\n")):
        inter = inter.split("\n")
        scenes.append(Scene(inter[0], inter[1], " ".join(inter[2:])))
    return (scenes)

def convToFile(scenes):
    global DEST_LANGUAGE
    file = open(sys.argv[1].replace(".srt", "-"+DEST_LANGUAGE+".srt"), "w+")
    for scene in scenes:
        file.write(scene.toFile())
    file.close()

def translateScenes(scenes):
    global DEST_LANGUAGE
    translate_client = translate.Client()
    text = " | ".join([scene.text for scene in scenes])
    translation = translate_client.translate(text, target_language=DEST_LANGUAGE)
    divi = html.unescape(translation['translatedText']).split(" | ")
    
    for i in range(len(scenes)):
        scenes[i].text = divi[i]
    convToFile(scenes)

def manageParams():
    global DEST_LANGUAGE
    if (len(sys.argv) == 2 and sys.argv[1] == "-h"):
        print("SubtitleTranslator.py <file.srt> <target_language:default fr>\nex: Mr.Robot.srt fr")
        sys.exit(84)
    elif (len(sys.argv) == 3):
        DEST_LANGUAGE = sys.argv[2]
    elif (len(sys.argv) != 2):
        sys.exit("Bad parameters.")

def main():
    manageParams()
    scenes = getScenes(sys.argv[1])
    translateScenes(scenes)


if (__name__ == "__main__"):
    main()
