#!/bin/python3

# parse arguments
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('audio')
parser.add_argument('background')
parser.add_argument('output')
args = parser.parse_args()

# we import everything we need here for performance
from moviepy.editor import *
from pysndfx import AudioEffectsChain
from math import trunc

# apply effects to audio
fx = AudioEffectsChain().speed(0.9).reverb()
fx(args.audio, 'slowed.mp3')

# check if the background is a gif
is_gif = background_path.endswith('.gif')

# load the background and the audio
audio = AudioFileClip('slowed.mp3')
image = VideoFileClip(args.background) if is_gif else ImageClip(background_path)
image = image.margin(left=100, right=100)

# set loop times
if is_gif:
    loops = trunc(audio.duration / image.duration)
    image = image.loop(n=loops)
    
# compose it
final = CompositeVideoClip([image], size=image.size)
final = final.set_audio(audio)
final = final.set_duration(audio.duration)

# render it
final.write_videofile(args.output, fps=30, codec='mpeg4', bitrate='12000k')