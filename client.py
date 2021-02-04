#!/usr/bin/env python3

import socket

GENESIS = '''
    [1:1] In the beginning when God created the heavens and the earth,
    [1:2] the earth was a formless void and darkness covered the face of the deep, while a wind from God swept over the face of the waters.
    [1:3] Then God said, "Let there be light"; and there was light.
    [1:4] And God saw that the light was good; and God separated the light from the darkness.
    [1:5] God called the light Day, and the darkness he called Night. And there was evening and there was morning, the first day.
    [1:6] And God said, "Let there be a dome in the midst of the waters, and let it separate the waters from the waters."
    [1:7] So God made the dome and separated the waters that were under the dome from the waters that were above the dome. And it was so.
    [1:8] God called the dome Sky. And there was evening and there was morning, the second day.
    [1:9] And God said, "Let the waters under the sky be gathered together into one place, and let the dry land appear." And it was so.
    [1:10] God called the dry land Earth, and the waters that were gathered together he called Seas. And God saw that it was good.
    [1:11] Then God said, "Let the earth put forth vegetation: plants yielding seed, and fruit trees of every kind on earth that bear fruit with the seed in it." And it was so.
    [1:12] The earth brought forth vegetation: plants yielding seed of every kind, and trees of every kind bearing fruit with the seed in it. And God saw that it was good.
    [1:13] And there was evening and there was morning, the third day.
    [1:14] And God said, "Let there be lights in the dome of the sky to separate the day from the night; and let them be for signs and for seasons and for days and years,
    [1:15] and let them be lights in the dome of the sky to give light upon the earth." And it was so.
    [1:16] God made the two great lights - the greater light to rule the day and the lesser light to rule the night - and the stars.
    [1:17] God set them in the dome of the sky to give light upon the earth,
    [1:18] to rule over the day and over the night, and to separate the light from the darkness. And God saw that it was good.
    [1:19] And there was evening and there was morning, the fourth day.
    [1:20] And God said, "Let the waters bring forth swarms of living creatures, and let birds fly above the earth across the dome of the sky."
    [1:21] So God created the great sea monsters and every living creature that moves, of every kind, with which the waters swarm, and every winged bird of every kind. And God saw that it was good.
    [1:22] God blessed them, saying, "Be fruitful and multiply and fill the waters in the seas, and let birds multiply on the earth."
    [1:23] And there was evening and there was morning, the fifth day.
    [1:24] And God said, "Let the earth bring forth living creatures of every kind: cattle and creeping things and wild animals of the earth of every kind." And it was so.
    [1:25] God made the wild animals of the earth of every kind, and the cattle of every kind, and everything that creeps upon the ground of every kind. And God saw that it was good.
    [1:26] Then God said, "Let us make humankind in our image, according to our likeness; and let them have dominion over the fish of the sea, and over the birds of the air, and over the cattle, and over all the wild animals of the earth, and over every creeping thing that creeps upon the earth."
    [1:27] So God created humankind in his image, in the image of God he created them; male and female he created them.
    [1:28] God blessed them, and God said to them, "Be fruitful and multiply, and fill the earth and subdue it; and have dominion over the fish of the sea and over the birds of the air and over every living thing that moves upon the earth."
    [1:29] God said, "See, I have given you every plant yielding seed that is upon the face of all the earth, and every tree with seed in its fruit; you shall have them for food.
    [1:30] And to every beast of the earth, and to every bird of the air, and to everything that creeps on the earth, everything that has the breath of life, I have given every green plant for food." And it was so.
    [1:31] God saw everything that he had made, and indeed, it was very good. And there was evening and there was morning, the sixth day.
'''.encode('ascii')

HELLO = 'Hello, world!'.encode('ascii')


HOST = '127.0.0.1'  # The server's hostname or IP address
# HOST = '209.6.119.75'
PORT = 9000         # The port used by the server


# First pass at a client which sends messages to be translated, then receives
def client_v1():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOST, PORT))

    msg = HELLO
    #msg = GENESIS
    sent = clientsocket.send(msg)
    print('Message sent, %d/%d bytes transmitted' % (sent, len(msg)))

    print('Received:')
    data = clientsocket.recv(64)
    print(data)

    clientsocket.close()


# ... but send and recv are buffers
def client_v2():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOST, PORT))

    #msg = HELLO
    msg = GENESIS

    # this is basically sendall():
    sent_total = 0
    while sent_total < len(msg):
        # send returns the number of bytes which it sends
        sent = clientsocket.send(msg[sent_total:]) # send remaining portion of message
        sent_total += sent
    print('Message sent, %d/%d bytes transmitted' % (sent_total, len(msg)))

    while True:
        data = clientsocket.recv(64)
        if not data: # this detects when the server has closed.
            break
        print('Received:', data)

    clientsocket.close()

# Finally we try with baked in message length (v4 corresponds to server v4)
def client_v4():
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((HOST, PORT))

    #msg = HELLO
    msg = GENESIS

    # send message length, padded with zeros (eg. '000481')
    bmsg_len = ('%06d' % len(msg)).encode('ascii')
    clientsocket.send(bmsg_len) # send message length
    print('Message length sent: %s', bmsg_len)

    # this is basically sendall():
    sent_total = 0
    while sent_total < len(msg):
        # send returns the number of bytes which it sends
        sent = clientsocket.send(msg[sent_total:]) # send remaining portion of message
        sent_total += sent
    print('Message sent, %d/%d bytes transmitted' % (sent_total, len(msg)))

    while True:
        data = clientsocket.recv(1024)
        if not data: # this detects when the server has closed.
            break
        print('Received:', data)

    clientsocket.close()


if __name__ == '__main__':
    client_v2()
