import json
import urlConnection as conn

# konstanta ini didapat dari data.json
nbStock = 632
nbSector = 13
sectorArr = [
    'property',
    'trade',
    'misc-ind',
    'consumer',
    'finance',
    'infrastruc',
    'agri',
    'mining',
    'basic-ind',
    'lq45',
    'kompas100',
    'pefindo25',
    'manufactur']

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
        currentItem = currentStock[option][0]
        currentItemCode = sectorHash(currentItem)
        print(currentItemCode)
        maxTrailingZeros = max(maxTrailingZeros,trailingZeros(currentItemCode))

    return 2 ** maxTrailingZeros


def countUniqStreams(stream): 
    count = 0
    streamArr = []
    for i in range(len(stream)): 
        if stream[i]['kode_saham'] not in streamArr:
            streamArr.append(stream[i]['kode_saham'])
            count += 1
    return count
  

if __name__ == "__main__": 
    print(countingDistinctElement('sektoral',16))
    # with open('../data-sample.json') as f:
    #     data = json.load(f)
    # count = countUniqStreams(data)
    # print(count)

