import socket
from piglatin import to_piglatin


HOST = '127.0.0.1'   # Standard loopback interface address (localhost)
PORT = 9000        # Port to listen on (non-privileged ports are > 1023)


# First pass at a pig latin server. What could go wrong?
def server_v1():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # associate socket to address and port
    serversocket.bind((HOST, PORT))
    # enable incoming connections
    serversocket.listen()
    # block and wait for incoming connection
    clientsocket, addr = serversocket.accept()
    print('Connected to by:', addr)

    bdata = clientsocket.recv(64)
    print('Received:', bdata)

    data = bdata.decode('ascii') # convert from bytes to ascii
    data_out = to_piglatin(data) # translate to Pig Latin
    bdata_out = data_out.encode('ascii') # back to bytes
    print('Sending back:', bdata_out)

    clientsocket.send(bdata_out)
    serversocket.close()


# A second attempt: receive, translate, and send bit by bit
def server_v2():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((HOST, PORT))
    serversocket.listen()
    clientsocket, addr = serversocket.accept()
    print('Connected to by:', addr)

    all_data = ''
    while True:
        bdata = clientsocket.recv(64)
        print('Received:', bdata)
        if not bdata:
            break

        data = bdata.decode('ascii')
        data_out = to_piglatin(data)
        bdata_out = data_out.encode('ascii') # back to binary string

        # print(bdata_out)
        i = 0
        while i < len(data_out):
            sent = clientsocket.send(bdata_out[i:])
            print('Sent %d bytes:'%sent, bdata_out[i:i+sent])
            i += sent

    serversocket.close()


def server_v3():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((HOST, PORT))
    serversocket.listen()
    clientsocket, addr = serversocket.accept()
    print('Connected by', addr)

    all_data = ''
    while True:
        bdata = clientsocket.recv(64) # here data is a bytes string
        print('Received:', bdata)
        if not bdata:
            break
        all_data += bdata.decode('ascii') # here it's a normal python string

    # do the thing
    data_out = to_piglatin(all_data)
    data_out = data_out.encode('ascii') # back to binary string

    i = 0
    while i < len(data_out):
        sent = clientsocket.send(data_out[i:])
        print('Sent %d bytes:'%sent, bdata_out[i:i+sent])
        i += sent

    serversocket.close()

# uses message length
def server_v4():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((HOST, PORT))
    serversocket.listen()
    clientsocket, addr = serversocket.accept()
    print('Connected by', addr)

    # pluck off message length
    first_chunk = clientsocket.recv(64)
    # split the first transmission to remove the length info
    len_info, all_data = first_chunk[:6].decode('ascii'), first_chunk[6:].decode('ascii')
    msg_len = int(len_info)
    print('Full message length: %d bytes' % msg_len)

    # receive the rest of the message
    while len(all_data) < msg_len:
        bdata = clientsocket.recv(64)
        print('Received:', bdata)
        all_data += bdata.decode('ascii')
    print("Full Message Received")

    # translate to pig latin
    data_out = to_piglatin(all_data)
    bdata_out = data_out.encode('ascii') # back to binary string
    print("Full Message Translated")

    # send the translation back
    i = 0
    while i < len(bdata_out):
        sent = clientsocket.send(bdata_out[i:])
        print('Sent %d bytes:'%sent, bdata_out[i:i+sent])
        i += sent
    print("Message Returned")
    
    clientsocket.close()
    serversocket.close()


if __name__ == '__main__':
    server_v2()
