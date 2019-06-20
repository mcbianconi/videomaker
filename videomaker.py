#!/usr/local/bin/python3

import cv2
import argparse
import os
from mutagen.mp3 import MP3
from datetime import datetime
import moviepy.editor as mpe

def get_args():
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-I", "--imagefolder", required=False, default='./images', help="Image folder. default is './images'")
    ap.add_argument("-M", "--musicfolder", required=False, default='./musics', help="Music folder. default is './music'")
    ap.add_argument("-ie", "--imageext", required=False, default='jpg', help="Image extension name. default is 'png'.")
    ap.add_argument("-me", "--musicext", required=False, default='mp3', help="Music extension name. default is 'mp3'.")
    ap.add_argument("-O", "--output", required=False, default='./output', help="Output Video folder")

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
    print("Image: %s + Audio: %s > %s" % (image, music, output))
    img = cv2.imread(image)
    height, width, layers = img.shape
    size = (width,height)

    
    out = cv2.VideoWriter(output,get_codec(), fps, size)

    # find the duration of the music and put a frame of the video
    # vor every second of it
    audio_length = get_music_length(music)
    iterations = int(audio_length)
    for i in range(iterations):
        out.write(img)
    out.release()

    # try to open the video, if its not ok itll raise an error
    # common mistake: image too large for an mp4 video
    try:
        video = mpe.VideoFileClip(output)
        video.write_videofile(output, audio=music)
    except OSError as error:
        print("Could not create the video, check the image file dimensions")
        print(error)
    

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
    image_ext = args['imageext']
    image_folder = args['imagefolder']
    music_folder = args['musicfolder']
    music_ext = args['musicext']
    output_folder = args['output']

    # all images from the folder
    images = get_files(folder=image_folder, ext=image_ext)

    # all music from the folder
    musics = get_files(folder=music_folder, ext=music_ext)
    
    # create a video made of 1 image with soundtrack made of 1 music
    for image, music in zip(images, musics):
        location = os.path.join(output_folder, get_video_name(image, music))    
        create_video(image, music, location)

if __name__=="__main__":
    main()