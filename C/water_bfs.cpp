#include<stdio.h>
#include<string.h>
int Cap[3],need_cap;
int Vis[1000][1000]={0};
int ok=0;

typedef struct Node Node;
struct Node
{
	int cap[3];
	int father,dist;
}node[1000];

void print_path(int n)
{
	if(node[n].father!=0)   //source
	   print_path(node[n].father);
	 for(int i=0;i<3;i++)
	 	printf("%d ",node[n].cap[i]);
	 printf("\n");
}

int Min(int a,int b)
{
	if (a>b)
	return b;
	else return a;
}

void bfs()
{
  int front=0,rear=1;
		int i,j;
		node[0].cap[0]=Cap[0];
		node[0].cap[1]=node[0].cap[1]=node[0].father=node[0].dist=0; //initianization
		Vis[Cap[0]][0]=1; 
		while(front<rear)
		{
			Node &u=node[front];  //&引用 
			for(i=0;i<3;i++)
				if(u.cap[i]==need_cap)
						{ok=1;
						for(int i=0;i<3;i++)
	 	        printf("%d ",node[0].cap[i]);
	 	   printf("\n");
						print_path(front);
						printf("front =%d water times=%d\n",front,u.dist);
						return;}
				for(i=0;i<3;i++)
				 for(j=0;j<3;j++) if(i!=j)  //?不能将if写入for中判断 
				  {
				  	Node &v=node[rear];
				  	int accept_water_cap=Min(u.cap[i],(Cap[j]-u.cap[j])); //i向j倒水;
				  	for(int k=0;k<3;k++) v.cap[k]=u.cap[k];
							 v.cap[i]-=accept_water_cap;
							 v.cap[j]+=accept_water_cap;
				  	if(!Vis[v.cap[0]][v.cap[1]])
				  	{
				  		Vis[v.cap[0]][v.cap[1]]=1;
				  		v.father=front;
				  		v.dist=u.dist+1;
				  		rear++;
//				  		printf("%d %d %d\n", v.cap[0], v.cap[1], v.cap[2]);
							}
						}
			front++; 
		}	
}
int main()
{	
scanf("%d%d%d%d",&Cap[0],&Cap[1],&Cap[2],&need_cap);
memset(Vis, 0, sizeof(Vis));
bfs();
if(!ok) printf("it is impossible");
return 0;	
} 
