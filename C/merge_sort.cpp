#include<stdio.h>
#include<time.h>
#include<stdlib.h>
int  maxn= 100;

void Merge(int *s,int low,int high) {
	int mid=(high+low)/2;
	int i=low,j=mid+1;  //[i,mid],[mid+1,high]
	int k=0,temp[high-low+1]= {0};
	while(i<=mid&&j<=high) {
		if(s[i]<s[j])
			temp[k++]=s[i],i++;
		else 	temp[k++]=s[j],j++;
	}
	if(i==mid+1) {
		for(; j<=high; j++)
			temp[k++]=s[j];
	} else for(; i<=mid; i++)
			temp[k++]=s[i];
	k=0;
	for(i=low; i<=high; i++)
		s[i]=temp[k++];
}
void merge_sort(int *s,int low,int high) {
	if(low<high) {
		int mid=(high+low)/2;
		merge_sort(s,low,mid);
		merge_sort(s,mid+1,high);   //·Ö
		Merge(s,low,high);   //²¢
	}
}
void display(int *s,int maxn) {
	for(int i=0; i<maxn; i++)
		printf("%d ",s[i]);
	printf("\n\n\n");
}
int main() {
	srand((unsigned)time(NULL));
	int i,s[maxn];
	for(i=0; i<maxn; i++)
		s[i]=rand()%maxn;
	display(s,maxn);
	merge_sort(s,0,maxn-1);
	display(s,maxn);
	return 0;
}
