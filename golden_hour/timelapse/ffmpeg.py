import logging
import subprocess


logger = logging.getLogger()


def compile_video(photos_dir, output_filename, photos_per_second=4, photos_extension=None):
    photos_extension = 'png' if photos_extension is None else photos_extension
    logger.info('compiling timelapse (photos per second: {photos_per_second})'.format(
        photos_per_second=photos_per_second,
    ))
    # TODO ensure output_filename ends with .mp4
    photos_pattern = '{}/image%05d.{}'.format(photos_dir, photos_extension)
    try:
        subprocess.check_call([
            'ffmpeg',
            '-loglevel', 'warning',
            '-framerate', str(photos_per_second),
            '-i', photos_pattern,
            '-c:v', 'libx264',
            '-s:v', '4k',
            '-r', '30',
            '-pix_fmt', 'yuv420p',
            output_filename,
        ])
    except subprocess.CalledProcessError as error:
        logger.error('Error encountered while generating video using ffmpeg', exc_info=True)
