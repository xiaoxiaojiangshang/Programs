#include<stdio.h>
#include<stdlib.h>
#include<time.h>

void swap(int *a,int *b)
{
	int temp=*a;
	*a=*b;
	*b=temp;
}

void get_top_n(int* s,int start,int end,int top_n)
{
		int i=start,j=end;
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
		if(end-j==top_n-1)
	    		return ;  //last top_n is we need
	 else if(end-j<top_n-1)  //right
		 get_top_n(s,start,j-1,top_n-(end-j+1));  //include j
		else                    //left
			get_top_n(s,j+1,end,top_n);
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
	int num_rand=1000,top_n=100;
	int a,i,s[num_rand],s1[num_rand];
	for(i=0;i<num_rand;i++)
		{
			a=rand()%num_rand;
			s[i]=a,s1[i]=a;
		}
	get_top_n(s,0,num_rand-1,top_n);
	for(i=num_rand-1;i>num_rand-100;i--)
		printf("%d ",s[i]);
	printf("\n");
	quick_sord(s1,0,num_rand-1);
	for(i=num_rand-1;i>num_rand-100;i--)
		printf("%d ",s1[i]);
	printf("\n");
	return 0; 
} 
