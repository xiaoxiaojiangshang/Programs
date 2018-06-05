#include<stdio.h>

int return_number(int x)
{
	int count=1;
	while(x>0)
	{
		x=x/10;
		if(x>0)count++;
	}
	return count;
}
int mul(int y)
{
	int x=1;
	for(int j=0;j<y;j++)
			x=x*10;
		return x;
}
int main()
{
	int i,j,n,count=0,s[100000]={0};
	scanf("%d",&n);
	for(i=0;i<n;i++)
	scanf("%d",&s[i]);
	for(i=0;i<n;i++)
		{
		  for(j=0;j<n&&i!=j;j++)
				{
					int a=return_number(s[i]);
					int b=return_number(s[j]);
					if((s[i]*mul(b)+s[j])%7==0)  
						count++;
					if((s[j]*mul(a)+s[i])%7==0)
					  count++;
				}
		} 
		printf("%d",count);
		return 0;
}
