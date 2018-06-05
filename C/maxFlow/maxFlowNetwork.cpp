//
// Created by Administrator on 2018/3/11.
// 默认从1作为源，流入到最大节点vertex。 
//

#include<stdio.h>
#include<queue>
#include <string.h>

#define MAX_VERTEXS 300
#define INF 1e8;
using namespace std;
queue<int> q;

int vertexs,edges;
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
    	printf("%d\n",vertexTemp);
    	q.pop();
    	for(int iVertex=1;iVertex<=vertexs;iVertex++)
    	   {
									 if(!visit[iVertex]&&graph[vertexTemp][iVertex]>0)
    	    	{
    	    		visit[iVertex]=true;
    	    		preNode[iVertex]=vertexTemp;
    	    		q.push(iVertex);
												if(iVertex==vertexs)
												{
													findPath=true;
													break;						
												}
//												else q.push(iVertex);						     
											}
							}
				}
		
	if(findPath)
	   {
	   	int vertexTemp=vertexs;
				 int currentMinWeight=INF;
					 while(preNode[vertexTemp])
	    {
	    	if(currentMinWeight>graph[preNode[vertexTemp]][vertexTemp])
	    	   currentMinWeight=graph[preNode[vertexTemp]][vertexTemp];
	    	   vertexTemp=preNode[vertexTemp];
					}
						vertexTemp=vertexs;
						while(preNode[vertexTemp])
						{
							graph[preNode[vertexTemp]][vertexTemp]-=currentMinWeight;
							graph[vertexTemp][preNode[vertexTemp]]+=currentMinWeight;
							vertexTemp=preNode[vertexTemp];
						}
						printf("currentMinWeight=%d\n",currentMinWeight);
						return currentMinWeight;				
}
	else return 0;
}

void deal_data()
{
    freopen("F:\Programs\C\maxFlowinput.txt","r",stdin);
    scanf("%d %d",&edges,&vertexs);
    memset(graph,0, sizeof(graph));
    int inFlow,outFlow,weight;
    for (int iEdge=1;iEdge<=edges;iEdge++)
    {
        scanf("%d %d %d",&inFlow,&outFlow,&weight);
        graph[inFlow][outFlow]+=weight;
    }
}
int main()
{
    deal_data();
    int maxFlow=0;
    int incFlow; 
    while(incFlow=argument())
        maxFlow+=incFlow;
    printf("maxFlow=%d\n",maxFlow);
    return 0;
}
