import socket

from dataset_generation import main as data_main
from model import main as model_main
from create_tokenized_dataset import preprocess_and_save_data

HOST = '127.0.0.1'
PORT = 8080
INPUT_DATA_DIR = 'input_data/'

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
conn, addr = s.accept()

print('Connected by', addr)


packet_ct = 0

while True:
    data = conn.recv(1024)
    if not data:
        break
    conn.sendall(data)

    if data and packet_ct > 0:  # ignore first packet which is just scoket info
        with open(INPUT_DATA_DIR + 'test.txt', 'a+') as f:
            f.write(data)

    packet_ct += 1
    print(packet_ct)

    if packet_ct > 100:  # TODO: do this whenevr there is long gap not just count
        data_main(input_file_path='test.txt')
        preprocess_and_save_data()
        model_main()

