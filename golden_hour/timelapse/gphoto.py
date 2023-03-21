import argparse
import logging
import os
import subprocess
import platform

from golden_hour.timelapse.ffmpeg import compile_video


logger = logging.getLogger()


def capture(output_dir, duration, interval):
    logger.info('capturing one photo every {interval} seconds for {duration} seconds'.format(
        duration=duration,
        interval=interval,
    ))
    capture_count = int(duration/interval)
    output_pattern = '{}/image%05n.jpg'.format(output_dir)

    # kill PTPCamera on Mac OS
    if platform.system() == 'Darwin':
        try:
            subprocess.check_call([
                'pkill',
                'PTPCamera',
            ])
        except subprocess.CalledProcessError as error:
            logger.error('Error killing PTPCamera', exc_info=True)

    try:
        subprocess.check_call([
            'gphoto2',
            '--capture-image-and-download',
            '--interval', str(interval),
            '--frames', str(capture_count),
            '--filename', output_pattern,
        ])
    except subprocess.CalledProcessError as error:
        logger.error('Error encountered while capturing using gphoto', exc_info=True)


def main():
    parser = argparse.ArgumentParser(description='Record a timelapse.')
    parser.add_argument('--duration', metavar='minutes', required=True, type=int, help='total duration of timelapse capture in minutes')
    parser.add_argument('--interval', metavar='seconds', required=True, type=int, help='number of seconds between photo captures')
    parser.add_argument('--photos-per-second', type=int, default=30, help='number of photos displayed per second in video')
    args = parser.parse_args()
    logger.debug(args)

    # capture and compile timelapse
    if not os.path.exists('photos'):
        os.makedirs('photos')
    photos_dir = os.path.abspath('photos')
    output_filename = "timelapse.mp4"
    logger.info('created {}'.format(photos_dir))
    capture(photos_dir, args.duration, args.interval)
    compile_video(photos_dir, output_filename, args.photos_per_second, photos_extension='jpg')
    # TODO clean up temp dir


if __name__ == '__main__':
    main()
