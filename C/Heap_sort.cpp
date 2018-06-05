#include<stdio.h>
#include<time.h>
#include<stdlib.h>
int maxn=1001;

void swap(int *a,int *b)
{
	int temp=*a;
	*a=*b;
	*b=temp;
}
void Heap_adjust(int *s,int i,int n)
{
	 int left=i*2;
	 int right=left+1;
		int max=i;   //巧妙的设计可以判断有没有调整； 
		if(left<=n&&s[left]>s[i])
		    max=left;
		if(right<=n&&s[right]>s[max])
		    max=right;
		if(max!=i)
		    swap(&s[i],&s[max]),Heap_adjust(s,max,n);
}
void Build_heap(int *s,int n)
{
  	for(int i=n/2;i>=1;i--)
      Heap_adjust(s,i,n);
}
void Heap_sort(int *s,int n)
{
	Build_heap(s,n);
	for(int i=n;i>=1;i--)
	   swap(&s[1],&s[i]),Heap_adjust(s,1,i-1);
}
void display(int *s,int maxn)
{
	for(int i=1;i<maxn;i++)
		printf("%d ",s[i]);
	printf("\n\n\n");
}

int main()
{
srand((unsigned)time(NULL));
	int i,s[maxn];
	for(i=1;i<maxn;i++)
	  s[i]=rand()%maxn;
	display(s,maxn);
	Heap_sort(s,1001);
	display(s,maxn);  
return 0;
}
