HPWREN Webcam Video from Archived Images
===

A very crude script to get 24 hours worth of images from a camera like
https://www.hpwren.ucsd.edu/cameras/S/SD/mta.html?camera=stgo-e-mobo-c and
compile the static images into a video of your desired length.

Usage: `./run.sh stgo-w-mobo-c 20241027 60`

The above will generate a 60 second long video from the days worth of images
from the Santiago West camera.

Here is the result (in a lower quality)

https://github.com/steverobbins/HPWREN-video-maker/assets/3498562/a0e5ad39-7cf5-492d-a52d-3e5bb620470c

It works on my machine :man_shrugging:.  You'll probably be fine if you replace
`command-threader` with `bash` in `prep-images.py`, but it will take longer to
download all the images since it's not doing it in parallel.

Please be nice HPWREN and don't abuse their free bandwidth.
