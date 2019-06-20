#!/usr/bin/python3

import cv2
import argparse
import os
from mutagen.mp3 import MP3
from datetime import datetime
import logging
import subprocess

def get_args():
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-I", "--imagefolder", required=False, default='./images', help="Image folder. default is './images'")
    ap.add_argument("-M", "--musicfolder", required=False, default='./musics', help="Music folder. default is './music'")
    ap.add_argument("-ie", "--imageext", required=False, default='jpg', help="Image extension name. default is 'png'.")
    ap.add_argument("-me", "--musicext", required=False, default='mp3', help="Music extension name. default is 'mp3'.")
    ap.add_argument("-O", "--output", required=False, default='./output', help="Output Video folder")
    ap.add_argument("-v","--verbose", help="increase output verbosity", action="store_true")

    args = vars(ap.parse_args())
    return args

# Define the codec
def get_codec():
    return cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case

# Get files from a folder that match the extension
def get_files(folder, ext):
    files = []
    for f in os.listdir(folder):
        if f.endswith(ext):
            files.append(os.path.join(folder,f))
    return files


# create the video
# image and music = full path to files
# output = full path of the new video (path/to/folder/video_name.mp4)
#
def create_video(image, music, output, fps=1):
    logging.info("Creating Video: image: %s + audio: %s @ %s" % (image, music, output))
    img = cv2.imread(image)
    height, width, layers = img.shape
    size = (width,height)
    logging.debug("Vide Size: %s" % str(size))

    
    out = cv2.VideoWriter(output,get_codec(), fps, size)
    logging.debug("VideoWriter: %s" % out)

    # find the duration of the music and put a frame of the video
    # vor every second of it
    audio_length = get_music_length(music)
    logging.debug("Video Lenght: %s seconds" % audio_length)

    iterations = int(audio_length)
    for i in range(iterations):
        out.write(img)
    out.release()

    add_audio(output, music)

def add_audio(video_file, audio_file):
    # add audio to the original video, trim either the audio or video depends on which one is longer
    subprocess.call(['ffmpeg', '-i', video_file, '-i', audio_file, '-shortest', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-y', video_file+"_with_audio.mp4"]) 

# get the music duration in seconds
def get_music_length(music):
    mp3_file = MP3(music)
    return mp3_file.info.length

# function to create the video name, now its the exactly time of its creation
def get_video_name(image, music):
    return str(datetime.today().timestamp()) + ".mp4"


# Main function
def main():

    # just set the parameters to variables
    args = get_args()
    if args['verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    image_ext = args['imageext']
    image_folder = args['imagefolder']
    music_folder = args['musicfolder']
    music_ext = args['musicext']
    output_folder = args['output']

    # all images from the folder
    images = get_files(folder=image_folder, ext=image_ext)
    logging.debug("Found %s images on %s" % (len(images), image_folder))

    # all music from the folder
    musics = get_files(folder=music_folder, ext=music_ext)
    logging.debug("Found %s musics on %s" % (len(musics), music_folder))
    
    # create a video made of 1 image with  soundtrack made of 1 music
    for image, music in zip(images, musics):
        location = os.path.join(output_folder, get_video_name(image, music))    
        create_video(image, music, location)

if __name__=="__main__":
    main()
    