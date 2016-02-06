import re

from processor.processor import Processor


# store users in hash
# {
# 'Tom': {'card_number': '4111111111111111', 'balance': 1000, 'limit': 2000}
# 'Lisa': {'card_number': '4111111111111111', 'balance': 1000, 'limit': 2000}
# }
#


def main():

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

    processor.write_output()

if __name__ == "__main__":
    main()
