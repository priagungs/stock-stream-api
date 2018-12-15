import urllib.request as req
import json

current_stock = None
get_stream_url = "http://localhost:4992/getstream"

# fungsi ini untuk mendapatkan json stock dari stream, size adalah banyak stock, default 1
def get_stocks(size=1):    
    get_stocks_url = get_stream_url + "?size=" + str(size)
    with req.urlopen(get_stocks_url) as url:
        data = json.loads(url.read().decode())
    return data

# fungsi ini digunakan untuk mensimulasikan data stream stock
def run_stream():
    global current_stock
    while(True):
        current_item = get_stocks()
        print(current_item)
        print("--------------------------------------------")
        print()

if __name__ == "__main__":
    run_stream()