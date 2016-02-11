import re
from time import process_time

from processor.processor import Processor
from processor.utils import setup_logger

log = setup_logger('logger')


def main():
    t = process_time()

    input = """ Add Tom 4111111111111111 $1000
    Add Lisa 5454545454545454 $3000
    Add Quincy 1234567890123456 $2000
    Charge Tom $500
    Charge Tom $800
    Charge Lisa $7
    Credit Lisa $100
    Credit Quincy $200
    """.replace('\n', ' ').strip()

    events = re.split(r'\s(?=(?:Add|Charge|Credit)\b)', input)
    processor = Processor()

    for e in events:
        processor.parse_event(e)

    log.info((
        'Finished processing in {0:.3f} seconds\n\n'
        '==================== [SUMMARY] ===================='.format(
            process_time() - t)
    ))

    summary = processor.generate_summary()
    processor.write_output(summary)

if __name__ == "__main__":
    main()
