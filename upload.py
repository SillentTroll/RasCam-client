import argparse

from camera_worker import upload


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Upload images.')
    parser.add_argument("-f", help="the filename of the image", dest='filename', required=True)
    parser.add_argument("-e", help="the event", dest='event')
    parser.add_argument("-t", help="the thread number (camera)", dest='camera')
    parser.add_argument("-d", help="the date", dest='date')
    parser.add_argument("-r", help="indicates whether to remove the file after successful upload", dest='remove')

    args = parser.parse_args()

    if args.filename:
        upload.delay(args.filename, args.date, args.remove)
    print "Filename %s done" % args.filename



