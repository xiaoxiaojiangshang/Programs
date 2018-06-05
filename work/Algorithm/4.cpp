#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#define N RAND_MAX
#define REAPT_TIMES 10

int val[N+1]={0},ptr[N+1]={0};
int count,head;
long long countA=0,countB=0,countC=0,countD=0;

int Search(int x,int i)
{
    count =0;
    while(x>val[i])
    {
        i=ptr[i];
        count++;
    }
    return i;
}
int A(int x)
{
    return Search(x,head);
}
int D(int x)
{
  int i=rand()%N+1;
  int y=val[i];
  if(x<y) {countD++;return Search(x,head);}
  else if(y<x){countD++;return Search(x,ptr[i]);}
   return i;
}
int B(int x)
{
    int y,i=head;
    int max=val[i];
    for(int j=1;j*j<=N;j++)
    {
        countB++;
        y=val[j];
        if(max<y&&y<=x){i=j;max=y;}
    }
    return Search(x,i);
}
int C(int x)
{
    int y,i=head;
    int max=val[i];
    for(int j=1;j=N/6;j++)
    {
        y=val[j];
        if(max<y&&y<=x){i=j;max=y;}
    }
    return Search(x,i);
}
void Gen_Data()
{
    int index, pre;
    head = (rand()%N+1);
    val[pre=head] = 1;
    for(int i = 2;i<= N;)
    {
        index = rand()%N+1 ;
        if(0==val[index])
        {
            val[index] = i;
            ptr[pre] = index;
            pre = index;
            i++;
        }
    }
    ptr[index] = 0;
}
int main()
{
    srand((unsigned int )time(NULL));
    Gen_Data();
    int find_num;
    for(int i = 1; i <= REAPT_TIMES; i++)
    {
        find_num=rand()%N+1;
        A(find_num);
        countA += count;
        B(find_num);
        countB += count;
        C(find_num);
        countC += count;
        D(find_num);
        countD += count;
    }
    printf("countA = %lld\n",countA/REAPT_TIMES);
    printf("countB = %lld\n", countB/REAPT_TIMES );
    printf("countC = %lld\n",countC/REAPT_TIMES );
    printf("countD = %lld\n",countD/REAPT_TIMES);
    return 0;
}

