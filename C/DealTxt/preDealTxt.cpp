#include<stdio.h>
#define MAXN 100

int  DealTxt(char *fname,int (*dataArray)[MAXN]) {
	FILE *fp;
	char s[MAXN];
	if((fp=fopen(fname,"r"))==NULL) {
		printf("打开文件%s错误\n",fname);
		return NULL;
	}
	int row=0;
	while(fgets(s,MAXN,fp)!=NULL) {
		int count=1,temp=0,num=0;
		bool neg=false;
		while(s[temp]!='\n'&&s[temp]!='\0') {
			if(s[temp]=='-')
				neg=true;
			else if(s[temp]>='0'&&s[temp]<='9') {
				num=num*10+s[temp]-'0';
			} else {
				dataArray[row][count]=(neg==true?-num:num);
				count++;
				neg=false;
				num=0;
				while((s[temp+1]<'0'||s[temp+1]>'9')&&s[temp]!='\n') {
					if(s[temp+1]=='-')
						neg=true;
					temp++;
				}
			}

			temp++;
		}
		dataArray[row][count]=(neg==true?-num:num);
		dataArray[row][0]=count;
		row++;
	}
	return row;
}

void disp(int (*dataArray)[MAXN],int rows) {
	int i,j;
	for(i=0; i<rows; i++)  {
		for(j=0; j<=dataArray[i][0]; j++) {
			printf("%d ",dataArray[i][j]);
		}
		printf("\n");
	}
}

int main() {
	char *fname="F:\\leetcode\\DealTxt\\dataIn.txt";
	int dataArray[MAXN][MAXN]= {0};
	int rows=DealTxt(fname,dataArray);
//	printf("%d",rows);
	disp(dataArray,rows);
	return 0;
}
