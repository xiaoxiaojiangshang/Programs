#include<stdio.h>
#include<stdlib.h>
#include<time.h>

void swap(int *a,int *b)
{
	int temp=*a;
	*a=*b;
	*b=temp;
}
void quick_sord(int *s,int start,int end)
{
	if(start<end)
	{
		int i=start;
		int j=end;
		while(i<j)
	 {
		  for(;j>i;j--)
		  {
		  	if(s[j]<s[i])
		  		{swap(&s[j],&s[i]);break;}
				}
				for(;i<j;i++)
				{
					if(s[i]>s[j])
		  		{swap(&s[j],&s[i]);break;}
	   }
	}
		quick_sord(s,start,i);
	 quick_sord(s,j+1,end);
}
}
void display(int *s,int maxn)
{
	for(int i=0;i<maxn;i++)
		printf("%d ",s[i]);
	printf("\n");
}
int main()
{
	srand((unsigned)time(NULL));
	int maxn=1000;
	int i,s[maxn],top_100[100],top=100;
	for(i=0;i<maxn;i++)
		s[i]=rand()%maxn;
	quick_sord(s,0,maxn-1);
	display(s,maxn);

	return 0; 
} 
