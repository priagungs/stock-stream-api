import urllib.request as req
import json, time, math, random, pprint, copy, sys

# GLOBAL SECTION
WINDOW_SIZE = 1000  # banyaknya item stock yang diambil dari stream

# inisialisasi data pada program secara umum
def init():
    init_trade_stock_code()
    init_trade_stock_mask()

# mengambil 1 item stock dari stream
def get_stock_item(size=1):
    stock_url = "http://localhost:4992/getstream?size=" + str(size)
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

        b = "Progress: " + str(i) + "/" + str(WINDOW_SIZE)
        print (b, end="\r")
    return sample


# FILTER SECTION
BIT_MASK_SIZE = 1024        # ukuran memori tersedia untuk bit array bloom filter
NB_HASH_FUNCTION = 3        # banyaknya hash function digunakan pada bloom filter
trade_stock_code = []       # daftar stock yang tergolong sector trade
trade_stock_mask = []       # bit array yang akan digunakan untuk bloom filter

# menginisialisasi stock yang tergolong sektor property dari data.json
def init_trade_stock_code():
    global trade_stock_code
    with open("data.json") as file:
        raw = file.read()
        data = json.loads(raw)
        for stock in data:
            if ('TRADE' in stock['sektoral']):
                trade_stock_code.append(stock['kode_saham'])

# fungsi hash yang digunakan untuk bloom filter
def bloom_filter_hash(stock_code, factor):
    return (abs(hash(stock_code)) * factor) % BIT_MASK_SIZE

# menginisialisasi bit array dengan hash dari stock dalam trade_stock_code
def init_trade_stock_mask():
    global trade_stock_mask
    trade_stock_mask = [0 for x in range(BIT_MASK_SIZE)]
    for stock_code in trade_stock_code:
        for factor in range(1,NB_HASH_FUNCTION+1):
            idx = bloom_filter_hash(stock_code,factor)
            trade_stock_mask[idx] = 1

# filtering dengan bloom filter untuk menentukan apakah stock bersektor trade atau tidak
def filtering_stock(stock_code):
    status = True
    for factor in range(1,NB_HASH_FUNCTION+1):
        idx = bloom_filter_hash(stock_code,factor)
        if (trade_stock_mask[idx] == 0):
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


# COUNTING ITEMSET SECTION
MAX_BASKET_SIZE = 10    # maksimum banyaknya saham yang dapat dibeli pada waktu yang sama
SUPPORT_VALUE = 10      # support value untuk menentukan apakah item/itemset frequent
baskets = []

# mendapatkan transaksi saham pada waktu yang relatif sama dari datastream
def get_baskets():
    global baskets
    for i in range(WINDOW_SIZE):
        basket_size = random.randrange(MAX_BASKET_SIZE) + 1
        stocks = get_stock_item(basket_size)
        basket = []
        for stock in stocks:
            if (stock['kode_saham'] not in basket):
                basket.append(stock['kode_saham'])
        baskets.append(basket)


# mendapatkan frequent_items dengan ukuran frequent_items sebesar item_size
def get_frequent_items(item_size):
    global baskets
    frequent_items = []
    frequent_count = []
    candidate_items = []
    candidate_count = []

    if (item_size == 1):
        for basket in baskets:
            for stock_code in basket:
                if stock_code in candidate_items:
                    idx = candidate_items.index(stock_code)
                    candidate_count[idx] += 1
                else:
                    candidate_items.append(stock_code)
                    candidate_count.append(1)
    else:
        old_frequent_items,old_frequent_count = get_frequent_items(item_size-1)
        if (item_size == 2):
            for i in range(0,len(old_frequent_items)-1):
                for j in range(i+1,len(old_frequent_items)):
                    pair_items = [old_frequent_items[i],old_frequent_items[j]]
                    candidate_items.append(pair_items)
                    candidate_count.append(0)
                    for basket in baskets:
                        if set(pair_items) < set(basket):
                            candidate_count[-1] += 1
        else:
            for i in range(0,len(old_frequent_items)-1):
                for j in range(i+1,len(old_frequent_items)):
                    item1,item2 = old_frequent_items[i],old_frequent_items[j]
                    if (len(set(item1) & set(item2)) == 1):
                        pair_items = list(set(item1).union(item2))
                        candidate_items.append(pair_items)
                        candidate_count.append(0)
                        for basket in baskets:
                            if set(pair_items) < set(basket):
                                candidate_count[-1] += 1

    for i in range(len(candidate_items)):
        if candidate_count[i] >= SUPPORT_VALUE:
            frequent_items.append(candidate_items[i])
            frequent_count.append(candidate_count[i])

    return frequent_items,frequent_count

# mendapatkan maximum frequent itemset
def counting_itemset_stock():
    item_size = 1
    frequent_items = []
    frequent_count = []

    stop = False
    while not stop:
        x,y = get_frequent_items(item_size)
        if len(x) > 0:
            item_size += 1
            frequent_items = copy.copy(x)
            print(item_size)
        else:
            stop = True

    return frequent_items

if __name__ == '__main__':
    init()
    print("Mining data stream, choose action: ")
    print("1. Sampling datastream")
    print("2. Filtering datastream")
    print("3. Count distinct element")
    print("4. Count frequent itemsets")
    action = int(input("<< action: "))

    if (1 <= action and action <= 4):
        if (action == 1):
            percentage = int(input("<< percentage: "))
            print("Sampling stock datastream start...")
            sample = sampling_stock(percentage)
            with open('sample.json', 'w') as file:
                parsed = json.loads(json.dumps(sample))
                file.write(json.dumps(parsed,indent=4))
            print("Sample has been write in sample.json")
    else:
        print("Failed, action input should be in range [1,4]")