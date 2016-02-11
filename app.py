from time import process_time

from processor.processor import Processor
from processor.utils import setup_logger

log = setup_logger('logger')


def main():
    log.info('Begin processing...')
    t = process_time()
    processor = Processor()
    events = processor.read_input()

    for e in events:
        processor.parse_event(e)

    log.info('Finished processing in {0:.3f} seconds'.format(process_time() - t))
    summary = processor.generate_summary()
    processor.write_output(summary)

if __name__ == "__main__":
    main()
