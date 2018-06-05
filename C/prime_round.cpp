#include<stdio.h>
int N,vis[100]={0},A[100]={0},prime_array[1000]={0};
int is_prime(int n)
{
  for(int i=2;i<n;i++)
  	if(n%i==0)
  		return 0;
  return 1;
}
void gen_prime_array(int *A)
{
for(int i=3;i<1000;i++)
  if(is_prime(i))
   A[i]=1;	
}
void dfs(int cur)
{
	if(cur==N&&prime_array[A[0]+A[N-1]])
	  {for(int i=0;i<N;i++)
	    printf("%d ",A[i]);
	  printf("\n");
	  }
	else for(int i=2;i<=N;i++)
	    if(!vis[i]&&prime_array[A[cur-1]+i])
	    {
	    	A[cur]=i;
	    	vis[i]=1;
	    	dfs(cur+1);
	    	vis[i]=0;
		}
}
int main()
{
int i;
prime_array[2]=1; //first prime is 2
gen_prime_array(prime_array);
//for(i=1;i<1000;i++)
//if(prime_array[i])printf("%d ",i);
scanf("%d",&N);
A[0]=1,vis[1]=1;// Ê×Î»ÊÇ1 
dfs(1); 
return 0;	
} 
