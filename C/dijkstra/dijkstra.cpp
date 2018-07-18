#include<stdio.h>
#include<string.h>
const int INF = 1000000000;
const int MAXN = 1000;

int n, m;
int v[MAXN], d[MAXN], G[MAXN][MAXN],fa[MAXN];

int main() {
		freopen("C:\\Users\\Administrator\\Desktop\\data_in.txt","r",stdin);
  scanf("%d%d", &n, &m);
  for(int i = 0; i < n; i++)
    for(int j = 0; j < n; j++)
      G[i][j] = INF;
  for(int i = 0; i < m; i++) {
    int u, v, w;
    scanf("%d%d%d", &u, &v, &w);
    G[u][v] = w; 
  }
  memset(v, 0, sizeof(v));
  for(int i = 0; i < n; i++) d[i] = (i==0 ? 0 : INF),fa[i]=i;
  for(int i = 0; i < n; i++) {
    int x, m = INF;
    for(int y = 0; y < n; y++) if(!v[y] && d[y]<=m) m = d[x=y];//找最小 
    v[x] = 1;
    for(int y = 0; y < n; y++)  
				{
					if(d[y]>d[x]+G[x][y])
					{
						d[y]=d[x]+G[x][y];
						fa[y]=x;
					} 
				}//d[y]=d[y]< (d[x] + G[x][y])?d[y]:(d[x]+G[x][y]);//更新 
  }
  for(int i = 0; i < n; i++)
    printf("%d\n", d[i]);
  for(int i = 1; i < n; i++)
  {
  	int j=i;printf("%d ",i);
  	while(fa[j])
  	{
  		printf("%d ",fa[j]);
  		j=fa[j];
			}
  	  printf("%d\n",fa[j]);
		}
  return 0;
}
