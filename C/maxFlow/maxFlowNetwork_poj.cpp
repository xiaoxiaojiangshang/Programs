#include<stdio.h>
#include<queue>
#include <string.h>

#define MAX_VERTEXS 201
#define INF 1e8;
using namespace std;
queue<int> q;

int M,N;
int graph[MAX_VERTEXS][MAX_VERTEXS];
int preNode[MAX_VERTEXS];
bool visit[MAX_VERTEXS];

int argument()
{
    memset(preNode,0, sizeof(preNode));
    memset(visit,0, sizeof(visit));
    q.push(1);
    visit[1]=1;
    bool findPath=false;
    while(!q.empty())
    {
    	int vertexTemp=q.front();

    	q.pop();
    	int iVertex;
    	for(iVertex=1;iVertex<=M;iVertex++)
    	   {
									 if(!visit[iVertex]&&graph[vertexTemp][iVertex]>0)
    	    	{
    	    		visit[iVertex]=true;
    	    		preNode[iVertex]=vertexTemp;
    	    		q.push(iVertex);
											if(iVertex==M)
												{
													findPath=true;
													break;						
												}				     
											}
							}
				}
		
	if(findPath)
	   {
	   	int vertexTemp=M;
				 int currentMinWeight=INF;
					 while(preNode[vertexTemp])
	    {
	    	if(currentMinWeight>graph[preNode[vertexTemp]][vertexTemp])
	    	   currentMinWeight=graph[preNode[vertexTemp]][vertexTemp];
	    	   vertexTemp=preNode[vertexTemp];
					}
						vertexTemp=M;
						while(preNode[vertexTemp])
						{
							graph[preNode[vertexTemp]][vertexTemp]-=currentMinWeight;
							graph[vertexTemp][preNode[vertexTemp]]+=currentMinWeight;
							vertexTemp=preNode[vertexTemp];
						}
						return currentMinWeight;				
}
	else return 0;
}

int main()
{
	while(scanf("%d %d",&N,&M)==2)
	{
		memset(graph,0, sizeof(graph));
    int inFlow,outFlow,weight,iEdge;
    for (iEdge=1;iEdge<=N;iEdge++)
    {
        scanf("%d %d %d",&inFlow,&outFlow,&weight);
        graph[inFlow][outFlow]+=weight;
    }
		  int maxFlow=0;
    int incFlow; 
    while(incFlow=argument())
        maxFlow+=incFlow;
    printf("%d\n",maxFlow);
	}
    return 0;
}
