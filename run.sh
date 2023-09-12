#!/bin/bash

set -ex

exitHelp()
{
    echo "Usage: $0 [source] [videoRunTime=60]"
    echo "    source - The location of the images, e.g. https://hpwren.ucsd.edu/cameras/archive/stgo-w-mobo-c/large/20230911/"
    echo "    videoRunTime - How long the compiled video should be in seconds (default: 60)"
    exit 1
}

if [ -z "$1" ]; then
    exitHelp
fi

SOURCE_URL=$1
RUNTIME=60

if [[ $2 != '' ]]; then
    RUNTIME="$2"
fi

DATETIME=`date -u +"%Y%m%d%H%M%S"`

mkdir -p "result/$DATETIME"
cd "result/$DATETIME"

python3.7 ../../prep-images.py $SOURCE_URL > download-images.sh

command-threader download-images.sh 25

FILE_COUNT=$(ls -l *.jpg | wc -l)
FRAME_RATE=$((FILE_COUNT / RUNTIME))

ffmpeg -framerate "$FRAME_RATE" -pattern_type glob -i '*.jpg' video.mp4

cp video.mp4 "~/Downloads/$DATETIME.mp4"
