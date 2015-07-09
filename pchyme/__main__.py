import argparse
import pkgutil
import random
import subprocess
import sys

from . import *

def main():
    parser = argparse.ArgumentParser(prog='pchyme')
    parser.add_argument('--instrument')
    parser.add_argument('--list-instruments', action='store_true')
    parser.add_argument('--seed')
    parser.add_argument('--output-file')
    args = parser.parse_args()

    instruments = [
        high, metal, rhodes, tiny, tuna, wood
    ]

    words = pkgutil.get_data('pchyme', 'english.txt').decode().splitlines()

    if args.list_instruments:
        print('\n'.join(i.name for i in instruments))
        return

    if args.instrument:
        instrument = next(i for i in instruments if i.name == args.instrument)
    else:
        instrument = random.choice(instruments)

    seed = args.seed or random.choice(words)

    print('{} "{}"'.format(instrument.name, seed), file=sys.stderr)
    canvas = instrument.jingle(seed=seed)
    if args.output_file:
        canvas.export(args.output_file, format='wav')
        return
    else:
        file = canvas.export(format='wav')
        p = subprocess.Popen(['mplayer', '-'], stdin=file,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return p.wait()

if __name__ == '__main__':
    sys.exit(main())
