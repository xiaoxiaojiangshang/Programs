#include<stdio.h>
#include<stdlib.h>
#include<string.h> 
#include<time.h>
int m=50,p=47;
int vis[50]={0},count=0;

int hash(int n)
{
	int v=n*n%p;
	count++;
	while(vis[v]!=0)
	{
		v=(v+1)%m;
		count++;
	}
	return v;
}
int main() 
{
	int i,s1[25]={0},s2[m];
	memset(s2,-1,sizeof(s2));
 srand((unsigned)time(NULL));	 
 for(i=0;i<25;i++)
 	s1[i]=rand()%100;
 int u;
 for(i=0;i<25;i++)
 {
 	u=hash(s1[i]);
 	s2[u]=s1[i];
 	vis[u]=1;
	}
	for(int i=0;i<25;i++)
		printf("%d ",s1[i]);
	printf("\n");	
	printf("一共查找了%d次\n",count);
	for(int i=0;i<m;i++)
		printf("%d ",s2[i]);
	printf("\n");
	int find_num;
	while(scanf("%d",&find_num)==1)
	{
		u=(find_num*find_num)%p;
		while(s2[u]!=find_num)
		{
			u=(u+1)%m;
		}
		printf("%d %d\n",s2[u],u);
	}
	return 0;
}
