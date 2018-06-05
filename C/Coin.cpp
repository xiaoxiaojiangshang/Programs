#include<stdio.h>
#include<string.h>
#define maxn 100
#define INF 99999999
int record_min[maxn]={0},record_max[maxn]={0},v[maxn]={0};
int n,change_coin;
void display(int a,int *b)
{
	printf("%d=",a);
	while(a)
	   {
	   	printf("%d-->",v[b[a]]);  //选择的物品 
	   	a=a-v[b[a]];  //剩下的物品 
	   }
}
int main()
{
	scanf("%d%d",&n,&change_coin);
	int i,j;
	for(i=1;i<=n;i++)
	  scanf("%d",&v[i]);
	int min[maxn],max[maxn];
	memset(min,-1,sizeof(min));
	memset(max,-1,sizeof(max));
	min[0]=0;max[0]=0;
	for(i=1;i<=change_coin;i++)
	  {int ans_min=INF,ans_max=-INF,flag1=0,flag2=0;  // variable's location is important 
			for(j=1;j<=n;j++)
	  {
	  	if(i>=v[j])
	  	  {
	  	  	if(ans_min>min[i-v[j]]+1 && min[i-v[j]]!=-1)  //大且可达
							  {
									   ans_min=min[i-v[j]]+1;
									   record_min[i]=j;
									   flag1=1;
									}
							if(ans_max<max[i-v[j]]+1 && max[i-v[j]]!=-1)  //小且可达
							  {
									   ans_max=max[i-v[j]]+1;
									   record_max[i]=j;
									   flag2=1;
									} 
						}
					}
						if(flag1) min[i]=ans_min;
						if(flag2) max[i]=ans_max;
			}
   if(max[change_coin]==-1){printf("impossible");return 0;}
			printf("sum_max=%d,sum_min=%d\n",max[change_coin],min[change_coin]);
			display(change_coin,record_min);
			printf("\n");
			display(change_coin,record_max);
			printf("\n");
			return 0;
}
