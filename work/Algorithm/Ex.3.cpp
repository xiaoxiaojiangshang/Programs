#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<string.h>
#define pi 3.1415926
#define N 10000

int Set[N]={0},visited[N]={0};

int setcount(int X_size)
{
	for(int temp=0;temp<N;temp++)
	 Set[temp]=0,visited[temp]=0;
	
	int count=0,rand_num=rand()%X_size;
	do{
		  count++;
		  visited[rand_num]=1;
		  rand_num=rand()%X_size;
	  }while(visited[rand_num]==0);
	  return int((float)(2*count*count)/pi);
}
int main()
{
			srand((unsigned int )time(NULL));
			int n;
			for(n=10;n<=N;n*=10)
			{
				int Count=0;
				for(int j=0;j<200;j++)
				{
					Count+=setcount(n);
				}
				printf("n=%d,estimate n is %d\n",n,Count/200);
			}
		return 0;	
}





