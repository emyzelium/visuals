#!/bin/sh

ffmpeg -framerate 12 -i frames/frame_%03d.png -filter_complex "[0:v] palettegen=max_colors=48 [pal];[0:v][pal] paletteuse=dither=none" anim_entities.gif
