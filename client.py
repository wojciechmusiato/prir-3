from multiprocessing.managers import BaseManager
import math, sys, time


class QueueManager(BaseManager):
    pass

def splitdata(dane):
    A = dane[0]
    n = dane[1]
    zakresy = []
    for i in range(0, n):
        zakresy.append(int(i*len(A)/n))
    zakresy.append(int(len(A)))
    return zakresy


def read(fname):
    f = open(fname, "r")
    nr = int(f.readline())
    nc = int(f.readline())

    A = [[0] * nc for x in range(nr)]
    r = 0
    c = 0
    for i in range(0, nr * nc):
        A[r][c] = float(f.readline())
        c += 1
        if c == nc:
            c = 0
            r += 1

    return A


def main():
    start = time.time()


    QueueManager.register('in_queue')
    QueueManager.register('out_queue')
    m = QueueManager(address=('127.0.0.1', 9001), authkey=bytes("bla bla", "utf-8"))
    m.connect()
    inqueue = m.in_queue()
    outqueue = m.out_queue()

    ncpus = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    fnameA = sys.argv[2] if len(sys.argv) > 2 else "A.dat"
    fnameX = sys.argv[3] if len(sys.argv) > 3 else "X.dat"

    A = read(fnameA)
    X = read(fnameX)

    inqueue.put(X)
    zakresy = splitdata([A, ncpus])

    for i in range(0, len(zakresy)-1):
        print(zakresy[i],zakresy[i+1])
        inqueue.put([A[zakresy[i]:zakresy[i+1]],i])
        print('ok')
    R=[len(A)]
    i=0
    while i<ncpus:
        print(i)
        O = outqueue.get()
        R[zakresy[O[1]]:zakresy[O[1]+1]-1] = O[0]
        i += 1
    print(R)
    end = time.time()
    print(end - start)

if __name__ == '__main__':
    main()
