#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#define N 1e9
float function(float x)
{
	return x*x-1;
}
float call(float(*f)(float),float a,float b,float c,float d)
{
	int count=0;
	for(int i=0;i<N;i++)
	{
		float x=(float)rand()/RAND_MAX*(b-a)+a;
	 float y=(float)rand()/RAND_MAX*(d-c)+c;
	 float y0=f(x);
	 if(y>0&&y<y0) count++;
	 if(y<0&&y0<y) count--;
	}
	return count/N*(d-c)*(b-a);
}
int main()
{
			srand((unsigned int )time(NULL));
			float a=-2,b=2,c=-1,d=3;
			printf("result is %f\n",call(function,a,b,c,d));
		return 0;	
}





