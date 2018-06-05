#include<stdio.h>
#include<stdlib.h>
int n,m;

long max(long long a,long long b,long long c)
{
	if(a>b)
	return a>c?a:c;
	else
	return b>c?b:c;
}
int cmp1(const void* a,const void *b)
{

	return *(long long *)a - *(long long*)b; 
}
int cmp2(const void* a,const void *b)
{
	return *(long long *)b - *(long long*)a; 
}

int main()
{
	
	while(scanf("%d %d",&n,&m)==2)
	{
		int a[1000000]={0};
		int b[1000000]={0};
		for (int i=0;i<n;i++)
		  scanf("%d",&a[i]);
		for (int i=0;i<n;i++)
		  scanf("%d",&b[i]);
		qsort(a,n,sizeof(a[0]),cmp1);
		qsort(b,n,sizeof(b[0]),cmp2);
//		for(int i=0;i<n;i++)
//		  printf("%d %d\n",a[i],b[i]);
		long long happyValue=0;
		int i=0;
		for(i=0;i+3<n;i=i+3)
		{
			long long temp=b[i]+b[i+1]+b[i+2]-a[i]-a[i+1]-a[i+2]+m;
//			printf("%lld\n",temp);
			if (temp>0)
			   happyValue+=temp;
			 else
			  break;
		}
		long long temp2=max(b[i]-a[i],b[i]+b[i+1]-a[i]-a[i+1],0);
		printf("%lld\n",temp2+happyValue);
	}	
	return 0;
}
