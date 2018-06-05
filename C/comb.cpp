#include<stdio.h>

void comb(int *a,int m, int k,int count) 
{
	int i,j;
	for(i=m;i>=k;i--)
	{
		a[k]=i;
		if(k>1) comb(a,i-1,k-1,count);
		else {
			for(j=count;j>=1;j--)
		 	printf("%d ",a[j]);
		printf("\n");
		}
	}
}
int main()
{
 int i,a[10];
 for(i=1;i<=5;i++)
    comb(a,5,i,i);
	return 0;
}
