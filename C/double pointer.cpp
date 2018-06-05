#include<stdio.h>

typedef struct node node;
struct node
{
  int c;
  node * pnext=NULL;
  node * pre=NULL;
  
} Node[50000];

int main()
{
	int i,a,b;
	scanf("%d %d",&a,&b);
	Node[0].pnext=&Node[1];
	for(i=1;i<=a;i++)
	{
		Node[i].c=i;
		Node[i].pnext=&Node[i+1];
		Node[i].pre=&Node[i-1];
	}
	char Ins,null;
	int num1,num2;
	for(i=0;i<b;i++)
	{
		scanf("%c",&null);  //accpte null or /n
		scanf("%c%d%d",&Ins,&num1,&num2);
//		printf("%c %d %d\n",Ins,num1,num2);
		if(Ins=='A')   //left
		{
/*  	if (num1==Node[1].a)
		  		{Node[0].pnext=&Node[num2];}  */
		  	(*Node[num2].pre).pnext=Node[num2].pnext;
		  	(*Node[num2].pnext).pre=Node[num2].pre;  /* 删除 */
					(*Node[num1].pre).pnext=&Node[num2];
					Node[num2].pre=Node[num1].pre;
					Node[num2].pnext=&Node[num1];
					Node[num1].pre=&Node[num2];      /*  重新插入 */
		}  
		else       /*right*/
		{
				(*Node[num1].pre).pnext=Node[num1].pnext;
		  	(*Node[num1].pnext).pre=Node[num1].pre;  /* 删除Node[num1] */ 
					(*Node[num2].pnext).pre=&Node[num1];
					Node[num1].pnext=Node[num2].pnext;
					Node[num2].pnext=&Node[num1];
					Node[num1].pre=&Node[num2];        /*  重新插入  */
		}
	}
	node *c=Node[0].pnext;
	for(i=0;i<a;i++)
	{
		printf("%d",(*c).c);
		c=(*c).pnext;
	}
	return 0;
}
