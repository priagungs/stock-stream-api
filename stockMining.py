import urllib.request as req
import json, time, math, random, pprint, copy, sys

# GLOBAL SECTION
WINDOW_SIZE = 1024  # banyaknya item stock yang diambil dari stream
CURSOR_UP_ONE = '\x1b[1A'
ERASE_LINE = '\x1b[2K'

# inisialisasi data pada program secara umum
def init():
    init_trade_stock_code()
    init_trade_stock_mask()
    get_baskets(800)

# mengambil 1 item stock dari stream
def get_stock_item(size=1):
    stock_url = "http://localhost:4992/getstream?size=" + str(size)
    with req.urlopen(stock_url) as url:
        data = json.loads(url.read().decode())
    return data

def print_progress(current, maxim):
    percentage = current * 100 / maxim + 1
    bar = percentage / 2
    print('Progress: ', str(int(percentage)), "% ", end="")
    print('#' * int(bar));

def clear_line(nb_line):
    for i in range(nb_line):
        sys.stdout.write(CURSOR_UP_ONE)
        sys.stdout.write(ERASE_LINE)

# SAMPLING SECTION
# mengambil sample sebanyak $percentage % dari stream yang diterima
def sampling_stock(percentage):
    sample = []
    for i in range(WINDOW_SIZE):
        stock = get_stock_item()[0]
        stock_hash = abs(hash(stock['kode_saham'])) % 100
        print('Stock code: ', stock['kode_saham'], end=" ")
        if (stock_hash < percentage):
            sample.append(stock)
            print('- Action: TAKE')
        else:
            print('- Action: DROP')
        print_progress(i,WINDOW_SIZE);
        clear_line(2)
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
def filtering_stock():
    for i in range(WINDOW_SIZE):
        stock = get_stock_item()[0]
        stock_code = stock['kode_saham']
        status = True
        for factor in range(1,NB_HASH_FUNCTION+1):
            idx = bloom_filter_hash(stock_code,factor)
            if (trade_stock_mask[idx] == 0):
                status = False
                break
        trade_stock = []
        not_trade_stock = []
        if (status):
            print("Stock code: ", stock_code, " - Sector: TRADE")
            trade_stock.append(stock)
        else:
            print("Stock code: ", stock_code, " - Sector: NON TRADE")
            not_trade_stock.append(stock)
        print_progress(i,WINDOW_SIZE)
        clear_line(2)
    return [trade_stock,not_trade_stock]


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
        print("Stock code: ", stock['kode_saham'], " - Current distinct: ", 2 ** maxTrailingZeros)
        print_progress(i,WINDOW_SIZE)
        clear_line(2)
    return 2**maxTrailingZeros


# COUNTING ITEMSET SECTION
MAX_BASKET_SIZE = 10    # maksimum banyaknya saham yang dapat dibeli pada waktu yang sama
SUPPORT_VALUE = 3       # support value untuk menentukan apakah item/itemset frequent
baskets = []

# mendapatkan transaksi saham pada waktu yang relatif sama dari datastream
def get_baskets(nb_basket):
    global baskets
    for i in range(nb_basket):
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
                    print_progress(i,len(old_frequent_items))
                    clear_line(1)
                    pair_items = [old_frequent_items[i],old_frequent_items[j]]
                    candidate_items.append(pair_items)
                    candidate_count.append(0)
                    for basket in baskets:
                        if set(pair_items) < set(basket):
                            candidate_count[-1] += 1
        else:
            for i in range(0,len(old_frequent_items)-1):
                for j in range(i+1,len(old_frequent_items)):
                    print_progress(i,len(old_frequent_items))
                    clear_line(1)
                    item1,item2 = old_frequent_items[i],old_frequent_items[j]
                    if (len(set(item1) & set(item2)) == 1):
                        pair_items = list(set(item1).union(item2))
                        status = True
                        for i in range(len(pair_items)):
                            sub_pair_items = pair_items[:i] + pair_items[i+1:]
                            if not set(sub_pair_items) < set(item1):
                                status = False
                                break
                        if (status):
                            candidate_items.append(pair_items)
                            candidate_count.append(0)
                            for basket in baskets:
                                if set(pair_items) < set(basket):
                                    candidate_count[-1] += 1
    for i in range(len(candidate_items)):
        if candidate_count[i] >= SUPPORT_VALUE:
            frequent_items.append(candidate_items[i])
            frequent_count.append(candidate_count[i])

        print_progress(i,len(candidate_items))
        clear_line(1)
    
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
            print('Current frequent items length: ', item_size)
            item_size += 1
            frequent_items = copy.copy(x)
        else:
            stop = True

    return frequent_items

if __name__ == '__main__':
    init()
    print("Stock datastream mining, choose action: ")
    print("1. Sampling")
    print("2. Filtering")
    print("3. Count distinct element")
    print("4. Count frequent itemsets")
    action = int(input("<< action: "))

    if (1 <= action and action <= 4):
        if (action == 1):
            percentage = int(input("<< input sampling percentage: "))
            print("\nSampling stock datastream start...")
            sample = sampling_stock(percentage)
            with open('sample.json', 'w') as file:
                parsed = json.loads(json.dumps(sample))
                file.write(json.dumps(parsed,indent=4))
            print("Sample has been wroten in sample.json")
        elif (action == 2):
            print("\nFiltering TRADE and NOT-TRADE stock datastream start...")
            trade_stock, not_trade_stock = filtering_stock()
            with open('stock_trade.json','w') as file:
                parsed = json.loads(json.dumps(trade_stock))
                file.write(json.dumps(parsed,indent=4))
            with open('stock_not_trade.json','w') as file:
                parsed = json.loads(json.dumps(not_trade_stock))
                file.write(json.dumps(parsed,indent=4))
            print("TRADE stock has been wroten in stock_trade.json")
            print("NON-TRADE stock has been wroten in not_stock_trade.json")
        elif (action == 3):
            print("Count distinct stock datastream start...")
            nb_distinct = counting_distinct_stock()
            print("There is",nb_distinct,"distinct stock found")
        else:
            print("Count frequent itemset stock datastream start...")
            frequent_items = counting_itemset_stock()
            print("Frequent itemset found: ", frequent_items)
    else:
        print("Failed, action input should be in range [1,4]")