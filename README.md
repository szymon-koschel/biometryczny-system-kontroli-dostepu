# zsw
web intercom

## how to spawn?
uasge: `zsw.py [-h] [--lockfile LOCKFILE] index`
usage: `zsw.py [-h] [--button-file BUTTON_FILE] [--video-num VIDEO_NUM] [--capture-delay CAPTURE_DELAY] 

### how does it work?
When button is pushed (and `button_file` is created):
1. App is capturing photos via webcam under `video_num` with delay specified as `capture_delay`.
2. App is triggering relay if someone is recognized.


### how to add authorized users?
Add Image instance to authorized_images in `zsw.py`.
