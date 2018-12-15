import random 
import json
from pprint import pprint

def printSamples(samples): 
    for i in range(len(samples)): 
        print(samples[i]) 
  
def samplingStreams(stream, n, k): 
        samples = [0]*k 
        for i in range(k): 
            samples[i] = stream[i]
          
        while(i < n): 
            j = random.randrange(i+1)
              
            if(j < k): 
                samples[j] = stream[i] 
            i+=1
           
        return samples
  
if __name__ == "__main__": 
    with open('../data.json') as f:
        data = json.load(f)
    n = len(data) 
    k = 5
    samples = samplingStreams(data, n, k)
    printSamples(samples)