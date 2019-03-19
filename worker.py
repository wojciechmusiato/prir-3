from multiprocessing.managers import BaseManager
from multiprocessing import Process
from multiprocessing import Queue
import math, sys, time
import queue


class QueueManager(BaseManager):
    pass


def worker_main(X, inqueue, outqueue):
    while True:
        try:
            data = inqueue.get(True, 0.05)
        except queue.Empty:
            print('spierdalaj')
            break
        A = data[0]
        nr = data[1]
        print(nr)
        nrows = len(A)
        ncols = len(A[0])
        y = []
        for i in range(nrows):
            s = 0
            for c in range(0, ncols):
                s += A[i][c] * X[c][0]
            # time.sleep(0.1)
            y.append(s)
        outqueue.put([y, nr])


def main():
    n = 4
    QueueManager.register('in_queue')
    QueueManager.register('out_queue')
    m = QueueManager(address=('127.0.0.1', 9001), authkey=bytes("bla bla", "utf-8"))
    m.connect()
    inqueue = m.in_queue()
    outqueue = m.out_queue()
    X = inqueue.get()
    start = time.time()
    jobs = []
    for i in range(0, n):
        jobs.append(Process(target=worker_main, args=(X, inqueue, outqueue)))
        jobs[i].start()
    for i in range(0, n):
        jobs[i].join()
    end = time.time()
    print(end - start)
    print('amdahl:')

    print(1/((1-0.43)+0.43/n))

if __name__ == '__main__':
    main()
