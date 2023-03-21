import logging
import platform
import shutil
import tempfile

from .ffmpeg import compile_video
from .osx import capture as osx_capture
from .gphoto import capture as gphoto_capture
from .pi import capture as pi_capture
if platform.system() == 'Darwin':
    from .osx import capture as auto_capture
else:
    from .pi import capture as auto_capture


logger = logging.getLogger()


def create_timelapse(duration, interval, filename, capturer=None,  persistent_photos_dir=None):
    logger.info('recording timelapse (duration: {}, interval: {}, filename: {})'.format(
        duration, interval, filename))

    if persistent_photos_dir is None:
        photos_dir = tempfile.mkdtemp(suffix='_golden-hour')
    else:
        photos_dir = persistent_photos_dir

    # keeping old functionality of auto picking osx/pi based on OS
    is_osx = platform.system() == 'Darwin'
    capture_func = None
    photos_extension = 'png'
    # TODO create constants to validate/pass this value
    capturer = capturer.upper() if capturer is not None else None
    print("capturer:" + str(capturer))
    if capturer is None and is_osx or capturer == 'OSX':
        capture_func = osx_capture
    elif capturer is None and not is_osx or capturer == "PI":
        capture_func = pi_capture
    elif capturer == "GPHOTO":
        capture_func = gphoto_capture
        photos_extension = 'jpg'

    capture_func(photos_dir, duration, interval)
    compile_video(photos_dir, filename, photos_extension=photos_extension)

    if persistent_photos_dir is None:
        shutil.rmtree(photos_dir)
