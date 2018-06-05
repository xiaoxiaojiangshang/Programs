#include<stdio.h> 
#include<stdlib.h> 
#include<time.h> 
#include<sys/time.h> 
#include<stack> 
//#define CHESS_SIZE 20
#define REAPT_TIMES 64 
using namespace std; 
int CHESS_SIZE;
int chess[21]; int stepVegas; 
stack<int> st; 
bool is_legal(int row, int col);
bool backtrace(int k); 
bool QueenLV(); 
void Print_ChessBoard(int, int);
bool is_legal(int row, int col) 
{ 
if(row >= 2)
for(int m = 1; m < row; m++)
	if( (col+row)==(chess[m]+m) || (col-row)==(chess[m]-m) || (col == chess[m]) ) 
       return false;
  return true; 
}

bool backtrace(int k) 
{  
  int i = k + 1; int j = 1; 
while( i <= CHESS_SIZE && i >= k + 1 ) 
{ for(; j <= CHESS_SIZE; j++)
  if(is_legal(i, j)) 
		{chess[i] = j; st.push(j); i = i + 1;  j = 1; break;}
	 if( j == CHESS_SIZE + 1 ) 
		{ i = i - 1;  if(i <= k) return false; j = st.top() + 1; st.pop(); } 
 }
 if( i <= k) return false; 
	return true; 
	}
bool QueenLV() 
{ 
 int i, j, nb, k = 0; 
if(stepVegas == k) return backtrace(k); 
while(true) 
{  nb = 0; /* number of open positions for the (k+1)th queen */ 
for(i = 1; i <= CHESS_SIZE; i++)
 if(is_legal(k+1, i)){nb += 1; if( (rand()%nb + 1) == 1 ) j = i;} 
  if(nb > 0){k = k + 1; chess[k] = j;} 
if( nb == 0 || k == stepVegas ) break;
  } 
if(nb > 0) return backtrace(k); return false; 
}

/* Print the first num_of_row rows of the chess board */ 
void Print_ChessBoard(int num_of_row, int num_of_column) 
{ 
for(int i = 1; i <= num_of_row; i++)
{
	for(int j = 1; j <= num_of_column; j++) 
	if(chess[i]==j) printf("@ ");
	else printf("* "); printf("\n"); 
}
}

/* get program run time */ 
double get_time() { 
struct timeval tv_start, tv_end; gettimeofday(&tv_start, NULL); 
for(int i = 1; i <= REAPT_TIMES; i++)
 while(!QueenLV()); gettimeofday(&tv_end, NULL);
 return ( (tv_end.tv_sec - tv_start.tv_sec) + 1.0e-6*(tv_end.tv_usec - tv_start.tv_usec) ) / REAPT_TIMES; 
} 
int main() 
{
for(CHESS_SIZE=12;CHESS_SIZE<=20;CHESS_SIZE++)
{
 
srand((unsigned)time(NULL));
printf("\nCHESS_SIZE = %d\n",CHESS_SIZE); 
for(stepVegas = 0; stepVegas <= CHESS_SIZE; stepVegas++) 
printf("%lf  ", get_time());
while(!st.empty()) st.pop();
}
return 0; 
}



  
  
