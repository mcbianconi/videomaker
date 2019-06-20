#!/usr/local/bin/python3

import cv2
import argparse
import os
from mutagen.mp3 import MP3
import ffmpeg

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

def get_files(folder, ext):
    files = []
    for f in os.listdir(folder):
        if f.endswith(ext):
            files.append(os.path.join(folder,f))
    return files

def create_video(image, music, output, fps=1):
    print("Fazendo video com %s e %s para salver em %s" % (image, music, output))

    img = cv2.imread(image)
    height, width, layers = img.shape
    size = (width,height)

    out = cv2.VideoWriter(output,get_codec(), fps, size)

    music_data = ffmpeg.probe(music)
    audio_length = music_data['format']['duration']
    
    for i in range(int(float(audio_length))):
        out.write(img)
    out.release()

    video_stream = ffmpeg.input(output)
    music_stream = ffmpeg.input(music)

    
    joined = ffmpeg.concat(video_stream, music_stream, v=1, a=1).node

    nout = ffmpeg.output(joined[0], joined[1], 'out.mp4')
    print(nout)
    nout.run()


def get_video_name(image, music):
    
    video_name = os.path.basename(image).strip().split()[-1] + os.path.basename(music).strip().split()[-1] + '.mp4'
    return video_name

def main():
    args = get_args()

    image_ext = args['imageext']
    image_folder = args['imagefolder']
    music_folder = args['musicfolder']
    music_ext = args['musicext']
    output_folder = args['output']

    images = get_files(folder=image_folder, ext=image_ext)
    musics = get_files(folder=music_folder, ext=music_ext)
    
    for image, music in zip(images, musics):
        location = os.path.join(output_folder, get_video_name(image, music))    
        create_video(image, music, location)

if __name__=="__main__":
    main()