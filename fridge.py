#!/bin/python3

# parse arguments
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('audio')
parser.add_argument('background')
parser.add_argument('output')
parser.add_argument('--speed', '-s', type=float, default=1)
parser.add_argument('--reverb', '-r', type=bool, default=False)
parser.add_argument('--fps', type=int, default=30)
parser.add_argument('--bitrate', type=str, default='12000k')
parser.add_argument('--margin-left', type=int, default=0)
parser.add_argument('--margin-right', type=int, default=0)
args = parser.parse_args()

# we import everything we need here for performance
from moviepy.editor import *
from pysndfx import AudioEffectsChain
from math import trunc

# apply effects to audio
fx = AudioEffectsChain().speed(args.speed)

if args.reverb:
    fx = fx.reverb()

fx(args.audio, 'slowed.mp3')

# check if the background is a gif
is_gif = args.background.endswith('.gif')

# load the background and the audio
audio = AudioFileClip('slowed.mp3')
image = VideoFileClip(args.background) if is_gif else ImageClip(args.background)
image = image.margin(left=args.margin_left, right=args.margin_right)

# set loop times
if is_gif:
    loops = trunc(audio.duration / image.duration)
    image = image.loop(n=loops)
    
# compose it
final = CompositeVideoClip([image], size=image.size)
final = final.set_audio(audio)
final = final.set_duration(audio.duration)

# render it
final.write_videofile(args.output, fps=args.fps, codec='mpeg4', bitrate=args.bitrate)
