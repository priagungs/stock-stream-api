import urllib.request as req
import json

get_stream_url = "http://localhost:4992/getstream"

# fungsi ini untuk mendapatkan json stock dari stream, size adalah banyak stock, default 1
def getStocks(size=1):    
    get_stocks_url = get_stream_url + "?size=" + str(size)
    with req.urlopen(get_stocks_url) as url:
        data = json.loads(url.read().decode())
        
    return data


if __name__ == "__main__":
    get_stocks(2)