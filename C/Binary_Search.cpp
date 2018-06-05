#include<stdio.h>
#include<stdlib.h>
#include<time.h>
int count;

int b_search(int n,int *s,int low,int high)
{
	while(low<high)
	{
		int m=(low+high)/2;
		count+=1;
		if(s[m]==n) return m;
		else if(s[m]<n) low=m+1;
		else high=m;
		printf("%d ",m);
	}
	printf("it do not exit");
	return -1;
}

int main()
{
	srand((unsigned)time(NULL));
	int s[10000]={0},i,find_num;
	for(i=0;i<10000;i++)
			s[i]=i;
	while(scanf("%d",&find_num)==1)
	{
		count=0;
		int a=b_search(find_num,s,0,9999);
		printf("\n %d %d count=%d",s[a],a,count);
	}
return 0;
}
