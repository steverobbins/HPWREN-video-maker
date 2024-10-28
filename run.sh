#!/bin/bash

set -ex

exitHelp()
{
    echo "Usage: $0 [camera] [date] [videoRunTime=60]"
    echo "    camera - The camera to pull images from, e.g. stgo-e-mobo-c"
    echo "    date - The date to pull images from, 20240101"
    echo "    videoRunTime - How long the compiled video should be in seconds (default: 60)"
    exit 1
}

if [ -z "$1" ]; then
    exitHelp
fi

CAMERA=$1
DATE=$2
RUNTIME=60

if [[ $3 != '' ]]; then
    RUNTIME="$3"
fi

DATETIME=`date -u +"%Y%m%d%H%M%S"`

mkdir -p "result/$DATETIME"
cd "result/$DATETIME"

python3.11 ../../prep-images.py $CAMERA $DATE > download-images.sh

if [ -f ~/bin/command-threader ]; then
    # This is parallel-ish script on my machine to run commands asyncronously.
    # Replace with whatever works for you, or download them one at a time
    #
    # https://www.gnu.org/software/parallel/parallel_tutorial.html
   ~/bin/command-threader download-images.sh 25
else
   bash download-images.sh
fi

FILE_COUNT=$(ls -l *.jpg | wc -l)
FRAME_RATE=$((FILE_COUNT / RUNTIME))

ffmpeg -framerate "$FRAME_RATE" -pattern_type glob -i '*.jpg' video.mp4

cp video.mp4 ~/Downloads/$DATETIME.mp4
