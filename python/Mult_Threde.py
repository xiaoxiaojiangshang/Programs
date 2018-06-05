import  multiprocessing as mp
import  threading as td
import  time
import queue

list_td, list_name =[],[]
list_mp=[]
def job1(list,j):
    res=0
    for i in range(1000000):
        if i%4==j:
            res +=(i +i*i+i**3)
    list.append(res)
    print (list)

def job2():
    res = 0
    for i in range(1000000):
        res += (i + i * i+i**3)
    print ('res=',res)

if __name__=="__main__":
    max_pro,max_td=4,4
    sum_mp,sum_td,sum=0,0,0
    a=time.clock()
    for i in range(max_pro):
        P=mp.Process(target=job1,args=(list_mp,i))
        P.start()
        list_name.append(P)
    for i in list_name:
        i.join()
    for i in list_mp:
        sum_mp +=i
    print('sum_mp=',sum_mp)
    print ('M-process spend_time=',time.clock()-a)
    a=time.clock()
    list_name=[]
    for i in range(max_td):
        T=td.Thread(target=job1,args=(list_td,i))
        T.start()
        list_name.append(T)
    for i in list_name:
        i.join()
    for j in list_td:
        sum_td +=j
    print('sum_td=',sum_td)
    print ('threade spend_time=',time.clock()-a)
    a=time.clock()
    job2()
    print('normal spend_time=', time.clock() - a)




