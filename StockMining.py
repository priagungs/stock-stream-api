import urllib.request as req
import json, time, math

# GLOBAL SECTION
WINDOW_SIZE = 1000  # banyaknya item stock yang diambil dari stream

# inisialisasi data pada program secara umum
def init():
    init_property_stock_code()
    init_property_stock_mask()

# mengambil 1 item stock dari stream
def get_stock_item():
    stock_url = "http://localhost:4992/getstream?size=1"
    with req.urlopen(stock_url) as url:
        data = json.loads(url.read().decode())
    return data



# SAMPLING SECTION
# mengambil sample sebanyak $percentage % dari stream yang diterima
def sampling_stock(percentage):
    sample = []
    for i in range(WINDOW_SIZE):
        stock = get_stock_item()[0]
        stock_hash = abs(hash(stock['kode_saham'])) % 100
        if (stock_hash < percentage):
            sample.append(stock)
    return sample



# FILTER SECTION
BIT_MASK_SIZE = 1024        # ukuran memori tersedia untuk bit array bloom filter
NB_HASH_FUNCTION = 3        # banyaknya hash function digunakan pada bloom filter
property_stock_code = []    # daftar stock yang tergolong sector property
property_stock_mask = []    # bit array yang akan digunakan untuk bloom filter

# menginisialisasi stock yang tergolong sektor property dari data.json
def init_property_stock_code():
    global property_stock_code
    with open("data.json") as file:
        raw = file.read()
        data = json.loads(raw)
        for stock in data:
            if ('PROPERTY' in stock['sektoral']):
                property_stock_code.append(stock['kode_saham'])

# fungsi hash yang digunakan untuk bloom filter
def bloom_filter_hash(stock_code, factor):
    return (abs(hash(stock_code)) * factor) % BIT_MASK_SIZE

# menginisialisasi bit array dengan hash dari stock dalam property_stock_code
def init_property_stock_mask():
    global property_stock_mask
    property_stock_mask = [0 for x in range(BIT_MASK_SIZE)]
    for stock_code in property_stock_code:
        for factor in range(1,NB_HASH_FUNCTION+1):
            idx = bloom_filter_hash(stock_code,factor)
            property_stock_mask[idx] = 1

# filtering dengan bloom filter untuk menentukan apakah stock bersektor property atau tidak
def filtering_stock(stock_code):
    status = True
    for factor in range(1,NB_HASH_FUNCTION+1):
        idx = bloom_filter_hash(stock_code,factor)
        if (property_stock_mask[idx] == 0):
            status = False
            break
    return status



# COUNTING DISTINCT ELEMENT SECTION
# hash function yang digunakan untuk flajolet martin approach, keluaran berupa binary string
def flajolet_martin_hash(stock_code):
    modulo = math.ceil(math.log2(WINDOW_SIZE))
    hash_result = abs(hash(stock_code)) % (2**modulo)
    bin_hash_result = bin(hash_result)[2:]
    return '0' * (modulo-len(bin_hash_result)) + bin_hash_result

# menghitung banyaknya trailing zeros dari sebuah binary string
def trailing_zeros(binary_string):
    return len(binary_string) - len(binary_string.rstrip('0'))

# menghitung banyaknya kode saham unik dari window data stream
def counting_distinct_stock():
    maxTrailingZeros = -1
    for i in range(WINDOW_SIZE):
        stock = get_stock_item()[0]
        hash_result = flajolet_martin_hash(stock['kode_saham'])
        maxTrailingZeros = max(maxTrailingZeros,trailing_zeros(hash_result))
    return 2**maxTrailingZeros

def counting_itemset_stock():
    pass


if __name__ == '__main__':
    init()
    print(counting_distinct_stock())