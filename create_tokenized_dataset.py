import copy
import io
import os
import pickle

CODES = {'<PAD>': 0, '<EOS>': 1, '<UNK>': 2, '<GO>': 3 }
TOKENISED_FILENAME = 'tokenized_input2.p'
INPUT_DATA_WRITE_PATH = 'input_data/'


def load_data(path):
    input_file = os.path.join(path)

    with io.open(input_file, 'r', encoding='utf-8') as f:
        data = f.read()

    return data


def get_source_and_target(
        source_path='input2.txt',
        target_path='output2.txt',
    ):
    source_text = load_data(INPUT_DATA_WRITE_PATH + source_path)
    target_text = load_data(INPUT_DATA_WRITE_PATH + target_path)
    return source_text, target_text


def create_lookup_tables(text):
    # make a list of unique words
    vocab = set(text.split())

    # (1)
    # starts with the special tokens
    vocab_to_int = copy.copy(CODES)

    # the index (v_i) will starts from 4 (the 2nd arg in enumerate() specifies the starting index)
    # since vocab_to_int already contains special tokens
    for v_i, v in enumerate(vocab, len(CODES)):
        vocab_to_int[v] = v_i

    # (2)
    int_to_vocab = {v_i: v for v, v_i in vocab_to_int.items()}

    return vocab_to_int, int_to_vocab


def text_to_ids(source_text, target_text, source_vocab_to_int, target_vocab_to_int):
    # empty list of converted sentences
    source_text_id = []
    target_text_id = []

    # make a list of sentences (extraction)
    source_sentences = source_text.split("\n")
    target_sentences = target_text.split("\n")

    max_source_sentence_length = max([len(sentence.split(" ")) for sentence in source_sentences])
    max_target_sentence_length = max([len(sentence.split(" ")) for sentence in target_sentences])

    # iterating through each sentences (# of sentences in source&target is the same)
    for i in range(len(source_sentences)):
        # extract sentences one by one
        source_sentence = source_sentences[i]
        target_sentence = target_sentences[i]

        # make a list of tokens/words (extraction) from the chosen sentence
        source_tokens = source_sentence.split(" ")
        target_tokens = target_sentence.split(" ")

        # empty list of converted words to index in the chosen sentence
        source_token_id = []
        target_token_id = []

        for index, token in enumerate(source_tokens):
            if (token != ""):
                print(token)
                source_token_id.append(source_vocab_to_int[token])

        for index, token in enumerate(target_tokens):
            if (token != ""):
                target_token_id.append(target_vocab_to_int[token])

        # put <EOS> token at the end of the chosen target sentence
        # this token suggests when to stop creating a sequence
        target_token_id.append(target_vocab_to_int['<EOS>'])

        # add each converted sentences in the final list
        source_text_id.append(source_token_id)
        target_text_id.append(target_token_id)

    return source_text_id, target_text_id


def preprocess_and_save_data(
        source_path=INPUT_DATA_WRITE_PATH + 'input2.txt',
        target_path=INPUT_DATA_WRITE_PATH + 'output2.txt',
        text_to_ids=text_to_ids
    ):
    # Preprocess

    source_text = load_data(source_path)
    target_text = load_data(target_path)

    # to the lower case
    source_text = source_text.lower()
    target_text = target_text.lower()

    # create lookup tables for Source and Targer
    source_vocab_to_int, source_int_to_vocab = create_lookup_tables(source_text)
    target_vocab_to_int, target_int_to_vocab = create_lookup_tables(target_text)

    # TODO: homogenise

    # create list of sentences whose words are represented in index
    source_text, target_text = text_to_ids(source_text, target_text, source_vocab_to_int, target_vocab_to_int)

    # Save data for later use
    pickle.dump((
        (source_text, target_text),
        (source_vocab_to_int, target_vocab_to_int),
        (source_int_to_vocab, target_int_to_vocab)), open(INPUT_DATA_WRITE_PATH + TOKENISED_FILENAME, 'wb'),
        protocol=2)


if __name__ == '__main__':
    preprocess_and_save_data()
