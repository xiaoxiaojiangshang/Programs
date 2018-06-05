#include<stdio.h>

int main()
{
	int a,b,c;
	double l_interest=0,h_interest=100;
	scanf("%d%d%d",&a,&b,&c);
	while(h_interest-l_interest>0.00001)
	{
		double m=(l_interest+h_interest)/2;
		double f=a;
		for(int i=0;i<b;i++) f+=f*m/100-c;
		if(f<0)l_interest=m;
		else h_interest=m;
	}
	printf("%.3lf%%\n",l_interest);
	return 0;
}
