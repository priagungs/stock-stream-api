import random 

def printArray(stream,n): 
    for i in range(n): 
        print(stream[i]) 
  
def selectKItems(stream, n, k): 
        i=0;  

        samples = [0]*k 
        for i in range(k): 
            samples[i] = stream[i]
          
        while(i < n): 
            j = random.randrange(i+1)
              
            if(j < k): 
                samples[j] = stream[i] 
            i+=1
           
        printArray(samples, k)
  
if __name__ == "__main__": 
    