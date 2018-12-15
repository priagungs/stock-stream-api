import json, time
import stock_stream
from threading import Thread

# konstanta ini didapat dari data.json
nb_stock = 632
max_trailing_zeros = -1


def stock_hash_binary(stock_name):
    bin_result = bin(hash(stock_name) % (nb_stock+1))[2:]
    return hash(stock_name) % (nb_stock + 1)


def thread_mining(threadname):
    while(True):
        print(count_distinct(100))

# mengembalikan kode binary yang bersesuaian dengan sector_name
def sector_hash(sector_name):
    bin_result = bin(sector_arr.index(sector_name.lower()))[2:]
    return '0' * (4-len(bin_result)) + bin_result

# menghitung trailing zeros dari sebuah binary string
def trailing_zeros(binary_string):
    return len(binary_string)-len(binary_string.rstrip('0'))

# menghitung banyaknya sector berbeda, window_size menyatakan banyak stream yang diambil
def count_distinct(window_size):
    global max_trailing_zeros
    for i in range(window_size):
        if (stock_stream.current_stock == None):
            continue
        else:
            current_stock = stock_stream.current_stock[0]
            current_item = current_stock['sektoral'][0]
            current_item_code = sector_hash(current_item)
            max_trailing_zeros = max(max_trailing_zeros,trailing_zeros(current_item_code))

    return 2 ** max_trailing_zeros

if __name__ == "__main__": 
    thread1 = Thread(target=stock_stream.thread_streaming, args=("Thread-1", )) 
    thread2 = Thread(target=thread_mining, args=("Thread-2", ))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

