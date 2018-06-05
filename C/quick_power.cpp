#include<stdio.h>
// http://blog.csdn.net/ltyqljhwcm/article/details/53043646
int deal(int a,int j,int p)
{
	int s=1;
	a=a%p;
	while(j>0)
	{
		if(j%2!=0) 
			s=s*a%p;
			a=a*a%p;
			j=j/2;
	}
	return s;
}
int main()
{
	int a=3,j=36,p=37;
	for (int k=1;k<=j;k++)
  	printf("k=%d,%d\n",k,deal(a,k,p));
	return 0;
}
