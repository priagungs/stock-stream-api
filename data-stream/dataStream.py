from threading import Thread
import time

currentStock = None

def runStream():
    while(True):
        

a = 0

def thread1(threadname):
    # global a       # Optional if you treat a as read-only
    while a < 10:
        print a
        time.sleep(0.5)

def thread2(threadname):
    global a
    while True:
        a += 1
        time.sleep(1)

if __name__ == '__main__':
    thread1 = Thread( target=thread1, args=("Thread-1", ) )
    thread2 = Thread( target=thread2, args=("Thread-2", ) )
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
