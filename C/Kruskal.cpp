#include<stdio.h>
#include<stdlib.h>
#define maxn 100
#define INF 10e9

struct Graph
{
	int edge_num;
	int vertex_num;
};
struct Edge
{
	int begin;
	int end;
	int weight;
}edge[maxn];
int cmp(const void *a,const void *b)
{
	Edge *x=(Edge*)a;
	Edge *y=(Edge*)b;
	return (*x).weight-(*y).weight;
}

int p[maxn];
int find(int x)
{
	return p[x]==x?x:find(p[x]);
}
int main()
{
	for(int temp=0;temp<maxn;temp++)
		  p[temp]=temp;
	freopen("C:\\Users\\Administrator\\Desktop\\data_in.txt","r",stdin);
	int i,j,k; //for loop
	Graph *PGraph;
	int w_temp,v1_temp,v2_temp; // for temp
	if((PGraph=(Graph*)malloc(sizeof(Graph)))==NULL)
		  return NULL;
	int &E=PGraph->edge_num;
	int &V=PGraph->vertex_num;// for quote;
	scanf("%d%d",&E,&V);
		for(i=0;i<E;i++)
    scanf("%d%d%d",&edge[i].begin,&edge[i].end,&edge[i].weight);
	qsort(edge,E,sizeof(edge[0]),cmp);
	int sum=0;
	for(i=0;i<E;i++)
	  {
	  	int x=find(edge[i].begin);
	  	int y=find(edge[i].end);
	  	if(x!=y)
	  	{
	  		p[x]=y;
	  		printf("(%d->%d),%d\n",edge[i].begin,edge[i].end,edge[i].weight);
	  		sum+=edge[i].weight;
				}
			}
			 printf("sum=%d\n",sum);
	return 0;
}

