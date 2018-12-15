import json, time
import stock_stream
from stock_stream import current_stock


# konstanta ini didapat dari data.json
nbStock = 632
nbSector = 13
sectorArr = ['property','trade','misc-ind','consumer','finance','infrastruc','agri','mining','basic-ind','lq45','kompas100','pefindo25','manufactur','delisting']


def thread_stock_stream():
    stock_stream.run_stream()


# def thread_mining():


# mengembalikan kode binary yang bersesuaian dengan sectorName
def sectorHash(sectorName):
    binResult = bin(sectorArr.index(sectorName.lower()))[2:]
    return '0' * (4-len(binResult)) + binResult


# menghitung trailing zeros dari sebuah binary string
def trailingZeros(binaryString):
    return len(binaryString)-len(binaryString.rstrip('0'))


# menghitung banyaknya elemen berbeda berdasarkan option, windowSize menyatakan banyak stream yang diambil
def countingDistinctElement(option, windowSize):
    maxTrailingZeros = -1
    for i in range(windowSize):
        currentStock = conn.getStocks()[0]
        print(currentStock)
        currentItem = currentStock[option][0]
        
        currentItemCode = ''
        if (option.lower() == 'sektoral'):
            currentItemCode = sectorHash(currentItem)
            
        print(currentItemCode)
        maxTrailingZeros = max(maxTrailingZeros,trailingZeros(currentItemCode))

        time.sleep(0.01)
    return 2 ** maxTrailingZeros


if __name__ == "__main__": 
    print(current_stock)
    # print(countingDistinctElement('sektoral',16))
    # with open('../data-sample.json') as f:
    #     data = json.load(f)
    # count = countUniqStreams(data)
    # print(count)

