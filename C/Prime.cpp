#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#define maxn 100
#define INF 10e8

struct Graph
{
	int edge_num;
	int vertex_num;
 int weight[maxn][maxn];
};

void Prime(int N,Graph* P)
{
	int lowcost[N];  
	int i,j;//for loop
	bool visit[N];
	memset(visit,false,sizeof(visit));
	visit[0]=true;
	for(i=0;i<N;i++)
		lowcost[i]=P->weight[0][i];  //just one point,that is 'o';
	int k,sum=0;  //k for record,sum for result;
	for(i=0;i<N-1;i++)// find point
			{
				int min=INF;
						for(j=0;j<N;j++)
							{
								  if(lowcost[j]<min&&!visit[j])
								    {min=lowcost[j];k=j;}
							}
		 visit[k]=true;
			printf("%d->%d\n",k,min);
			sum+=min;
		for(j=0;j<N;j++)
		{if(lowcost[j]>P->weight[k][j]&&!visit[j])
					 lowcost[j]=P->weight[k][j];}		
 }
 printf("sum=%d\n",sum);
}
int main()
{
	freopen("C:\\Users\\Administrator\\Desktop\\data_in.txt","r",stdin);
	int i,j,k; //for loop
	Graph *PGraph;
	int w_temp,v1_temp,v2_temp; // for temp
	if((PGraph=(Graph*)malloc(sizeof(Graph)))==NULL)
		  return NULL;
	int &E=PGraph->edge_num;
	int &V=PGraph->vertex_num;// for quote;
	scanf("%d%d",&E,&V);
	for(i=0;i<V;i++)  //pre_deal
	   for(j=i;j<V;j++)
	   {
	   	 if(j==i) PGraph->weight[i][j]=0;
	   	 else PGraph->weight[i][j]=PGraph->weight[j][i]=INF;
				}
		for(i=0;i<E;i++)
		{
			scanf("%d%d%d",&v1_temp,&v2_temp,&w_temp);
			PGraph->weight[v1_temp][v2_temp]=PGraph->weight[v2_temp][v1_temp]=w_temp;
		}
	Prime(V,PGraph);
	return 0;
}

