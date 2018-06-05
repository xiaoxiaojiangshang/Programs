import random
import numpy as np
import math

def PrintPrimes():
    list=[2,3]
    for n in range(5,10000,2):
        if RepeatMillRab(n,(int)(math.log(n,2))):
            list.append(n)
    return list
def RepeatMillRab(n,k):
    for i in range(1,k+1):
       if MillRob(n)==False:
           return False
    return True

def MillRob(n):
    a=random.randint(2,n-2)
    return Btest(a,n)
def Btest(a,n):
    s=0
    t=n-1
    while(t%2==1):
        s=s+1
        t=t/2
    x=a**t%n
    if (x==1)|(x==n-1):
        return True
    for i in range(1,s):
        x=x*x%n
        if x==n-1:
            return True
    return False
def prime():
    list=[2,3]
    for i in range(5,10000,2):
        flag=0
        for j in range(2,(int)(np.sqrt(i))+1):
            if i%j==0:
                flag=1
        if flag==0:
            list.append(i)
    return list
if __name__ == "__main__":
    list_certer=prime()
    count=0;
    for i in range(100):
        list_uncerter = PrintPrimes()
        for j in list_uncerter:
            if j not in list_certer:
                count+=1
    print(count)
