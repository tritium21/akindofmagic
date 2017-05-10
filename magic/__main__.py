import argparse
import sys

import magic

parser = argparse.ArgumentParser(prog='pyfile')
parser.add_argument('filename', metavar='FILE')
parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(magic.__version__))
parser.add_argument('-i', '--mime', action='store_true', help='output MIME type strings')

def main(args=None):
    args = parser.parse_args(args)
    try:
        print(magic.from_file(args.filename, mime=args.mime))
    except FileNotFoundError as e:
        return e

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))