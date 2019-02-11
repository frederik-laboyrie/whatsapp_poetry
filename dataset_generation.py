""" Must be run using python2 as gutenberg relies on that
"""

import re

from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers

BOOKS = [
  # bookid, skip N lines
  (574, 15, 'Blake'),
]
MESSAGES_FILENAME = 'fwchat.txt'
INPUT_DATA_WRITE_PATH = 'input_data/'
WHATSAPP_FILLERS = ['media omitted']
USE_POETRY = True
OUT_PATH = 'raw_poetry.txt' if USE_POETRY else 'raw_whatsapp.txt'

def poetry_cleaner(
        poetry_books=BOOKS
    ):
    with open(INPUT_DATA_WRITE_PATH + 'raw_poetry.txt', 'w') as ofp:

        lineno = 0

        for (id_nr, toskip, title) in poetry_books:

            startline = lineno
            text = strip_headers(load_etext(id_nr)).strip()
            lines = text.split('\n')[toskip:]

            for line in lines:

                if 0 < len(line) < 50 and line.upper() != line and not re.match('.*[0-9]+.*', line):
                    cleaned = re.sub('[^a-z\'\-]+', ' ', line.strip().lower())
                    if lineno < 100:
                        ofp.write(cleaned)
                        ofp.write('\n')
                    lineno = lineno + 1

                else:
                    ofp.write('\n')

        print('Wrote lines {} to {} from {}'.format(startline, lineno, title))


def whatsapp_cleaner(
        whatsapp_fillers=WHATSAPP_FILLERS,
    ):

    with open(INPUT_DATA_WRITE_PATH + MESSAGES_FILENAME, 'r') as f, \
            open(INPUT_DATA_WRITE_PATH + OUT_PATH, 'a') as ofp:

        line_ct = 0
        message_history = list(f)[1:]
        for line in message_history:
            # colon followed by space is way of splitting message from name and date stub in whatsapp history
            message = line.split(": ", 1)[1]
            clean_message = re.sub(r'([^\s\w]|_)+', '', message).lower()[:-1] # TODO: don't have -1 indexing to get rid of ]n
            nb_words_clean = len(clean_message.split(" "))
            #import pdb; pdb.set_trace()
            if clean_message in whatsapp_fillers:
                continue

            elif nb_words_clean > 4:
                ofp.write(clean_message)
                ofp.write('\n')
                line_ct += 1

            else:
                ofp.write(clean_message + ' ')

    print('Wrote {} lines from message history'.format(line_ct))


def convert_to_source_and_target():
    with open(INPUT_DATA_WRITE_PATH + OUT_PATH, 'r') as rawfp, \
            open(INPUT_DATA_WRITE_PATH + 'input.txt', 'w') as infp, \
            open(INPUT_DATA_WRITE_PATH + 'output.txt', 'w') as outfp:
        prev_line = ''
        for curr_line in rawfp:
            curr_line = curr_line.strip()
            # poems break at empty lines, so this ensures we train only
            # on lines of the same poem

            if len(prev_line) > 0 and len(curr_line) > 0:
                infp.write(prev_line + '\n')
                outfp.write(curr_line + '\n')

            prev_line = curr_line

    print('Wrote messages and poetry to source and target')


def main():
    if USE_POETRY:
        poetry_cleaner()
    whatsapp_cleaner()
    convert_to_source_and_target()

if __name__ == '__main__':
    main()

