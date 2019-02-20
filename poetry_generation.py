import pickle

import tensorflow as tf

INPUT_SENTENCE = 'happy bday faye'

BATCH_SIZE = 16


def load_params():
    with open('/opt/app/config/params.p', mode='rb') as in_file:
        return pickle.load(in_file)


def load_preprocess():
    with open("/opt/app/input_data/tokenized_input.p", mode='rb') as in_file:
        return pickle.load(in_file)


def sentence_to_seq(sentence, vocab_to_int):
    results = []
    for word in sentence.split(" "):
        if word in vocab_to_int:
            results.append(vocab_to_int[word])
        else:
            results.append(vocab_to_int['<UNK>'])

    return results


def generate_next_sentence(
        input_sentence_non_token=INPUT_SENTENCE,
        batch_size=BATCH_SIZE
    ):
    _, (source_vocab_to_int, target_vocab_to_int), (source_int_to_vocab, target_int_to_vocab) = load_preprocess()

    input_sentence = sentence_to_seq(input_sentence_non_token, source_vocab_to_int)

    load_path = load_params()

    loaded_graph = tf.Graph()

    with tf.Session(graph=loaded_graph) as sess:
        # Load saved model
        loader = tf.train.import_meta_graph(load_path + '.meta')
        loader.restore(sess, load_path)

        input_data = loaded_graph.get_tensor_by_name('inputs:0')
        logits = loaded_graph.get_tensor_by_name('predictions:0')
        target_sequence_length = loaded_graph.get_tensor_by_name('target_sequence_length:0')
        keep_prob = loaded_graph.get_tensor_by_name('keep_prob:0')

        translate_logits = sess.run(logits, {input_data: [input_sentence] * batch_size,
                                             target_sequence_length: [len(input_sentence) * 2] * batch_size,
                                             keep_prob: 0.5})[0]

    print('Input')
    print('  Word Ids:      {}'.format([i for i in input_sentence]))
    print('  Input Words: {}'.format([source_int_to_vocab[i] for i in input_sentence]))

    print('\nPrediction')
    print('  Word Ids:      {}'.format([i for i in translate_logits]))
    print('  Output Words: {}'.format(" ".join([target_int_to_vocab[i] for i in translate_logits])))

    return [target_int_to_vocab[i] for i in translate_logits]


def generate_x_lines(input_sentence_non_token=INPUT_SENTENCE):
    print(input_sentence_non_token)
    input_sentence = input_sentence_non_token
    sentence_ct = 0
    while sentence_ct < 10:
        print('input: {}'.format(input_sentence))
        output_sentence = generate_next_sentence(input_sentence_non_token=input_sentence)
        print('output: {}'.format(' '.join(output_sentence)))
        input_sentence = ' '.join(output_sentence)
        sentence_ct += 1


if __name__ == '__main__':
    generate_x_lines()