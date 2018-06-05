#include<stdio.h>
#include<stdlib.h>

int i,j,k,n,m;

typedef struct node node;
struct node
{
	char s[101];
	int sort_lenth=0;
	int order=0;
}Node[101];

int cmp(const void* a,const void *b)
{
	node *x=(node*)a;
	node *y=(node*)b;
	if (x->sort_lenth!=y->sort_lenth)
		return x->sort_lenth-y->sort_lenth; 
	else 
		return x->order-y->order;
}
int count_lenth(char * s) 
{
	int count=0;
	for(i=0;i<n;i++)
		for(j=i+1;j<n;j++)
			if(s[i]>s[j])
				count++; 
		return count;
}
char null;
int main()
{
	scanf("%d%d",&n,&m);
	for(k=0;k<m;k++)
	   {
	   scanf("%c",&null);
				scanf("%s",Node[k].s);
				Node[k].order=k+1;
				Node[k].sort_lenth=count_lenth(Node[k].s);
				} 
	qsort(Node,m,sizeof(Node[0]),cmp);
	for(i=0;i<m-1;i++)
		printf("%s\n",Node[i].s); 
	printf("%s",Node[m-1].s);
	return 0;
}
