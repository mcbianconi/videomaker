#!/usr/bin/python3

import cv2
import argparse
import os
from mutagen.mp3 import MP3
from datetime import datetime
import logging
import subprocess
import PIL.Image
import numpy as np

def get_args():
    # Construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-I", "--imagefolder", required=False, default='./images', help="Image folder. default is './images'")
    ap.add_argument("-M", "--musicfolder", required=False, default='./musics', help="Music folder. default is './music'")
    ap.add_argument("-ie", "--imageext", required=False, default='jpg', help="Image extension name. default is 'png'.")
    ap.add_argument("-me", "--musicext", required=False, default='mp3', help="Music extension name. default is 'mp3'.")
    ap.add_argument("-O", "--output", required=False, default='./output', help="Output Video folder")
    ap.add_argument("-ve", "--videoext", required=False, default='mp4', help="Output Video Fomart")
    ap.add_argument("-v","--verbose", help="increase output verbosity", action="store_true")

    args = vars(ap.parse_args())
    return args

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
def create_video(image, music, video_ext ,location_folder):
    output = os.path.join(location_folder, get_video_name(image, music))
    if not video_ext.startswith('.'):
        video_ext = '.' + video_ext
    subprocess.call(["ffmpeg", "-loop","1" ,"-y","-i", image, "-i", music, "-acodec", "copy", "-vcodec", "mpeg4", "-shortest", output+video_ext])

# function to create the video name, now its the exactly time of its creation
def get_video_name(image, music):
    name, ext = os.path.basename(music).split('.')
    return name


# Main function
def main():

    # just set the parameters to variables
    args = get_args()
    if args['verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.DEBUG)

    image_ext = args['imageext']
    image_folder = args['imagefolder']
    music_folder = args['musicfolder']
    music_ext = args['musicext']
    output_folder = args['output']
    video_extension = args['videoext']

    # all images from the folder
    images = get_files(folder=image_folder, ext=image_ext)
    logging.debug("Found %s images on %s" % (len(images), image_folder))
    
    cimages = []
    for f in build_images(image_folder, image_ext):
        cimages.append(f)

    # all music from the folder
    musics = get_files(folder=music_folder, ext=music_ext)
    logging.debug("Found %s musics on %s" % (len(musics), music_folder))
    
    # create a video made of 1 image with  soundtrack made of 1 music
    for image, music in zip(images, musics):
        create_video(image, music, video_extension ,output_folder)

def build_images(basedir, ext):
    for root, dirs, fnames in os.walk(basedir):
        imgs = []
        for f in fnames:
            if f.endswith(ext):
                imgs.append(PIL.Image.open(os.path.join(root, f)))
        if len(imgs) == 1:
            yield imgs[0]
            
        min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
        img_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )                
        dest_dir = os.path.join(root,'after')
        if not os.path.exists(dest_dir):
            logging.info('Criando Diretorio: %s' % dest_dir)
            os.mkdir(dest_dir)
        
        img_name = os.path.join(dest_dir, 'combined.' + ext) 
        logging.info('Salvando Imagem: %s' % img_name)
        img_comb = PIL.Image.fromarray( img_comb)
        img_comb.save(img_name)
        yield img_name

if __name__=="__main__":
    main()
    