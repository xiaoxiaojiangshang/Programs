#include<stdio.h>
#include<stdlib.h>
#define maxn 100
int top=-1;

struct tree_node
{
	char operater;
	int number;
	tree_node *pleft;
	tree_node *pright;
};

tree_node* pop(tree_node** pstack)
{
	tree_node* data=pstack[top];
	top--;
	return data;
}
void push(tree_node *p,tree_node** pstack)
{
	top++;
	pstack[top]=p;
}
tree_node* creat_express_tree(char *s,tree_node **p_stack)
{
	tree_node *p;
	int i=0;
	while(s[i])
	{
		if('0'<=s[i]&&s[i]<='9')
				{
					p=(tree_node*)malloc(sizeof(tree_node));
					p->number=s[i]-'0';
					p->pleft=p->pright=NULL;
					push(p,p_stack); 
					printf("push=%d,%c\n",top,p_stack[top]->number);
				}
		 else
					{
						p=(tree_node*)malloc(sizeof(tree_node));
						p->operater=s[i];
						p->pleft=pop(p_stack);	
						p->pright=pop(p_stack);
						push(p,p_stack);	
						printf("top=%d,%c\n",top,p_stack[top]->operater);
					} 
			i++;
	}
	return p_stack[top];
}
int  visit(tree_node* p)
{
	if(p->pleft==NULL&&p->pright==NULL)
	   printf("%d ",p->number);
	else printf("%c ",p->operater);
	return 0;
}
void pre_order(tree_node* p)
{
	if(p)
	{
		visit(p);
		pre_order(p->pleft);
		pre_order(p->pright);
	}
}
void In_order(tree_node* p)
{
	if(p)
	{
		In_order(p->pleft);
		visit(p);
		In_order(p->pright);
	}
}
void Post_order(tree_node* p)
{
	if(p)
	{
		Post_order(p->pleft);
		Post_order(p->pright);
		visit(p);
	}
}

int main()

{
 char buf[maxn];
	scanf("%s",buf);
	tree_node **p_stack;
	tree_node* root;
	p_stack=(tree_node**)malloc(sizeof(tree_node*)*maxn); //stack
	root=creat_express_tree(buf,p_stack);
	pre_order(root);
	printf("\n");
	In_order(root);
	printf("\n");
	Post_order(root);
	return 0;
}


