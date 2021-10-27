"""
Take in a file to digest and convert to text


"""
import wave, math, contextlib
import speech_recognition as sr
from moviepy.editor import AudioFileClip
import time
import uuid
import os
import moviepy.editor
import mimetypes
import textract


def checkIfVideo(inputfile):
    if mimetypes.guess_type(inputfile)[0].startswith('video'):
        return True
    return False


def checkIfAudio(inputfile):
    if mimetypes.guess_type(inputfile)[0].startswith('audio'):
        return True
    return False


def audioFromVideo(inputvideo):
    videodata=moviepy.editor.VideoFileClip(inputvideo)
    audiodata=videodata.audio
    outputname=inputvideo.split(inputvideo.split('.')[-1])[0]+".wav"
    audiodata.write_audiofile(outputname)
    return outputname

#Okay so a universal sound based audio transcriber:
def transcribe_audio(audiofile):
    temp_audio_file_name=str(uuid.uuid4())+".wav"
    audioclip = AudioFileClip(audiofile)
    audioclip.write_audiofile(temp_audio_file_name)
    with contextlib.closing(wave.open(temp_audio_file_name, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    total_duration = math.ceil(duration / 60)
    r = sr.Recognizer()
    finaloutputtext=""
    for i in range(0, total_duration):
        time.sleep(1)
        with sr.AudioFile(temp_audio_file_name) as source:
            audio = r.record(source, offset=i * 60, duration=60)
            # r.recognize_google(audio) is failing -- trying bing
        try:
            transcriptiontext = r.recognize_google(audio, language='en-US')
            finaloutputtext+=" "+transcriptiontext.upper()
        except Exception as e:
            print(e)
            #return None
    os.remove(temp_audio_file_name)
    return finaloutputtext

def extractToText(inputfile):
    returntext=textract.process(inputfile).decode("utf-8")
    return returntext

def convertToText(inputfile):
    #print("Checking if it's a video...")
    if checkIfVideo(inputfile):
        audiofile=audioFromVideo(inputfile)
        return transcribe_audio(audiofile)
    #print("checking if its an audio...")
    if checkIfAudio(inputfile):
        return transcribe_audio(inputfile)
    #print("None of those, going to do standard text extraction...")
    return(extractToText(inputfile))