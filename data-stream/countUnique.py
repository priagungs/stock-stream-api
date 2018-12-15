import json

def countUniqStreams(stream): 
    count = 0
    streamArr = []
    for i in range(len(stream)): 
        if stream[i]['kode_saham'] not in streamArr:
            streamArr.append(stream[i]['kode_saham'])
            count += 1
    return count
  
if __name__ == "__main__": 
    with open('../data-sample.json') as f:
        data = json.load(f)
    count = countUniqStreams(data)
    print(count)