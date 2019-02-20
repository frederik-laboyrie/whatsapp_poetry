import logging
import pickle

import numpy as np

from predict_client.prod_client import ProdClient


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

# In each file/module, do this to get the module name in the logs
logger = logging.getLogger(__name__)

HOST = '0.0.0.0:9000'
# a good idea is to place this global variables in a shared file
MODEL_NAME = 'test'
MODEL_VERSION = 5

client = ProdClient(HOST, MODEL_NAME, MODEL_VERSION)
INPUT_SENTENCE = 'deep in the chill'

def sentence_to_seq(sentence, vocab_to_int):
    results = []
    for word in sentence.split(" "):
        if word in vocab_to_int:
            results.append(vocab_to_int[word])
        else:
            results.append(vocab_to_int['<UNK>'])
    return results

def load_preprocess():
    with open("input_data/tokenized_input.p", mode='rb') as in_file:
        return pickle.load(in_file)


_, (source_vocab_to_int, target_vocab_to_int), (source_int_to_vocab, target_int_to_vocab) = load_preprocess()

input_sentence = sentence_to_seq(INPUT_SENTENCE, source_vocab_to_int)

req_data = [
    {'in_tensor_name': 'inputs', 'in_tensor_dtype': 'DT_INT32', 'data': np.array([input_sentence] * 8)},
    {'in_tensor_name': 'target_sequence_length', 'in_tensor_dtype': 'DT_INT32', 'data': 4},
    {'in_tensor_name': 'keep_prob', 'in_tensor_dtype': 'DT_FLOAT', 'data': 1.0},
]

prediction = client.predict(req_data, request_timeout=10)

print([target_int_to_vocab[i] for i in prediction['predictions'][0]])
