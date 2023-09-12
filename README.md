HPWREN Webcam Video from Archived Images
===

A very crude script to get 24 hours worth of images from a camera like
https://hpwren.ucsd.edu/cameras/S/SD/stgo.html and compile the static images
into a video of your desired length.

Usage: `./run.sh https://hpwren.ucsd.edu/cameras/archive/stgo-w-mobo-c/large/20230911/ 60`

The above will generate a 60 second long video from the days worth of images
from the Santiago West camera.

Here is the result (in a lower quality)

https://github.com/steverobbins/HPWREN-video-maker/assets/3498562/a0e5ad39-7cf5-492d-a52d-3e5bb620470c

It works on my machine :man_shrugging:.  You'll probably be fine if you replace
`command-threader` with `bash` in `prep-images.py`, but it will take longer to
download all the images since it's not doing it in parallel.

Please be nice HPWREN and don't abuse their free badwidth.
