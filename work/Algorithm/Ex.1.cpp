#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#define N 1e9
//#define RAND_MAX 1000
int main()
{
		float x,y;
		int s[10]={1e4,1e5,1e6,1e7,1e8,1e9};
		for(int j=0;j<6;j++)
		{
			int count=0;
			srand((unsigned int )time(NULL));
			for(int i=0;i<s[j];i++)
			{
				x=(float)rand()/RAND_MAX;
				y=(float)rand()/RAND_MAX;
				if(x*x<1-y*y) count++;
				}	
			printf("N=%d\nresult is %f\n",s[j],4.0*count/s[j]);
		}
		return 0;	
}
