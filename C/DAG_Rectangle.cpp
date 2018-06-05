#include<stdio.h>
int rectangle[100][2]={0},d[100]={0},G[100][100]={0};
int n; // the number of rectangle 
void swap(int *a,int *b)
{
	int temp=*a;
	*a=*b;
	*b=temp;
}
int max(int a,int b)
{
	if(a>b) return a;
	else return b;
}
int dp(int i)
{
	int &ans=d[i];
	if(ans>0) return ans;
	ans=1;
 for(int j=0;j<n;j++) if(G[i][j]) ans=max(ans,dp(j)+1);
	return ans;
}
int path[100];
void print_all(int cur,int i)
{
	path[cur]=i+1;
	if (d[i]==1) 
	 {
	 	printf("%d",path[0]);
	 	for(int j=1;j<n;j++)
	     if(path[j])printf("-->%d",path[j]);
	   printf("\n");
		}
		for(int j=0;j<n;j++)
   if(G[i][j]&&d[j]==d[i]-1)
     print_all(cur+1,j);
}
int main()
{
	 int i,j;
	 scanf("%d",&n);
	 for(i=0;i<n;i++)
	  {
	  	scanf("%d%d",&rectangle[i][0],&rectangle[i][1]);
	  	  if(rectangle[i][0]>rectangle[i][1])
	  	     swap(&rectangle[i][0],&rectangle[i][1]);
			} 
	 for(i=0;i<n;i++)
	   for(j=0;j<n;j++)
	   {
	   	 if(rectangle[i][0]<rectangle[j][0]&&rectangle[i][1]<rectangle[j][1])
	   	     G[i][j]=1;
				}
	 int ans=0;
	 for(i=0;i<n;i++)
	 	ans=max(ans,dp(i));
	  printf("%d\n",ans);
		for(i=0;i<n;i++) if(d[i]==ans) print_all(0,i); 
	return 0;
}
