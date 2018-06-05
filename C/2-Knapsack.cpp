#include<stdio.h>
#define c 10
#define n 5

int max_val= 0;
int w[10]={0,2,2,6,5,4};
int v[10]={0,6,3,4,5,6};
int b[10];
int m[n+1][c+1]={0};

void comb(int *a,int m, int k,int count) 
{
	int i,j;
	for(i=m;i>=k;i--)
	{
		a[k]=i;
		if(k>1) comb(a,i-1,k-1,count);
		else 
		{
			int sum_w=0,sum_v=0;
		 for(j=count;j>=1;j--)
		 	{
		 		 sum_w+=w[a[j]];
						sum_v+=v[a[j]];	
				}
		if(sum_w<=c&&sum_v>max_val)
		     {
		     	max_val=sum_v;
		     	for(int temp=1;temp<=5;temp++)  //注意使用不同的变量，否则出错 
 		 							b[temp]=a[temp];
						 	} 
		}
	}
}

int max(int a,int b)
{
	if(a>b)return a;
	else return b;
}
void dynamic() 
{
	int i,j;  //都是从1开始
	for(j=c;j>=1;j--)
	 if(w[n]<=j) m[n][j]=v[n];
		else  m[n][j]=0;
	for(i=n-1;i>=1;i--)
	  for(j=1;j<=c;j++)
	  {
	  	if (j<w[i]) m[i][j]=m[i+1][j];
				else m[i][j]=max(m[i+1][j],(m[i+1][j-w[i]]+v[i]));
			}
}
int main()
{
	int i,j,a[10]={0};
 for(i=1;i<=5;i++)
    comb(a,5,i,i);
 printf("violence solve by combination max_val is %d\n",max_val);
 printf("one selcet things is:");
 for(i=1;i<=5;i++)
 		if(b[i]) printf("%d ",b[i]);
 	 printf("\n");
	dynamic();
	max_val=m[1][c];
	printf("Dynamic solve max_val is %d\n",m[1][c]);
	printf("selcet things is:");
	int is_choose[6]={0}; 
	for(j=1;j<=c;j++)
	  if(m[1][j]==max_val) break;
	for(i=1;i<=n-1;i++)
	 {
	 	if (m[i][j]==m[i+1][j]) continue;
	 	else {
	 		       is_choose[i]=1;  //选中
											j=j-w[i]; 
			     }
		}
		if(m[i][j]!=0)  is_choose[i]=1;
		for(i=1;i<=5;i++)
 		 if(is_choose[i]) printf("%d ",i);
 	 printf("\n");
			
	for(i=1;i<=n;i++)
	  {
			for(j=1;j<=c;j++)
	  	 printf("%d ",m[i][j]);
	  	 printf("\n");
			 } 	
	return 0;
}
