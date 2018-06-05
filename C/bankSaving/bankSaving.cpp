#include<stdio.h>

double money[21]={0};
float r1,r2,r3,r5;
int n,year[4]={1,2,3,5};
double temp[6]={0};

double max(double a,double b)
{
	return a>b?a:b;
}

bool inA(int c)
{
	for(int j=0;j<4;j++)
		if (c==year[j])
			return true;
		return false;	
}

double power(float a,int n)
{
	double b=1;
	for(int i=0;i<n;i++)
			b*=(a+1);
	return b;
}

void dymic(int n)
{
	 money[0]=1;
	 money[1]=1+r1;
		money[2]=(1+r2)*(1+r2);
		money[3]=(1+r3)*(1+r3)*(1+r3);
		for(int i=4;i<=20;i++)
			for(int j=0;j<4;j++)
			{
				  if(inA(year[j]))
				  {	
				  	money[i]=max(money[i],money[i-year[j]]*temp[year[j]]);
						}
				   
			}
}
int main()
{
	
	while(scanf("%d %f %f %f %f",&n,&r1,&r2,&r3,&r5)==5)
	{
		temp[1]=1+r1;
		temp[2]=power(r2,2);
		temp[3]=power(r3,3);
		temp[5]=power(r5,5);
		dymic(n);
		printf("%.5f\n",money[n]);
	}	
}
