#include<stdio.h>
#include<string.h>
#include<math.h>
#define INF 1e10
#define maxn 20

int n,S;
double d[1<<maxn];
struct Node
{
	double x,y,z;
}node[maxn+1];

void init()
{
	int i;
	scanf("%d",&n);
	for(i=0;i<n;i++)
			scanf("%lf%lf%lf",&node[i].x,&node[i].y,&node[i].z);
	S=1<<n;
	d[0]=0;
}
double dist(Node a,Node b)
{
	return sqrt((a.x-b.x)*(a.x-b.x)+(a.y-b.y)*(a.y-b.y)+(a.z-b.z)*(a.z-b.z));
}
double min(double a,double b)
{
	return a>b?b:a;
}
void solve()
{
	int s,i,j;
	for(s=1;s<S;s++)  //S-1代表全选的时候 
	 {
    d[s]=INF;
    for(i=n-1;i>=0;i--)   //  0代表左移0位，代表第一个数，n-1代表第n位置。 
		  if(s&(1<<i)) break;
				for(j=i-1;j>=0;j--)
			   if(s&1<<j)   d[s]=min(d[s],dist(node[i],node[j])+d[s^(1<<i)^(1<<j)]);   
	 }
}
int main()

{
  freopen("C:\\Users\\Administrator\\Desktop\\data_in.txt","r",stdin);
  init();
  solve();
  printf("%.3lf\n",d[S-1]);
  return 0;
}
