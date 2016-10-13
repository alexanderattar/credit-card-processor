import sys
from time import process_time

from processor.processor import Processor
from processor.utils import setup_logger

log = setup_logger('logger')


def main():
    """
    Usage:
        python3 app.py input.txt' or 'python3 < input.txt'
    """
    log.info('Begin processing...')
    t = process_time()
    processor = Processor()

    # Accept input from two types of sources:
    # a filename passed in command line arguments or STDIN.
    with open(sys.argv[1], 'r') if len(sys.argv) > 1 else sys.stdin as f:
        for line in f:
            processor.parse_event(line)

    log.info('Finished processing in {0:.3f} seconds'.format(process_time() - t))
    summary = processor.generate_summary()
    processor.write_output(summary)

if __name__ == "__main__":
    main()
