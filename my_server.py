from multiprocessing.managers import BaseManager
from multiprocessing import Queue

import sys


class QueueManager(BaseManager):
    pass


def main():
    ip = '127.0.0.1'
    port = 9001
    in_queue = Queue()
    out_queue = Queue()
    QueueManager.register('in_queue', callable=lambda: in_queue)
    QueueManager.register('out_queue', callable=lambda: out_queue)
    manager = QueueManager(address=(ip, int(port)), authkey=bytes("bla bla", "utf-8"))
    server = manager.get_server()
    server.serve_forever()


if __name__ == '__main__':
    main()
