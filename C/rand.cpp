#include<stdio.h>
#include<stdlib.h>
#include<time.h>
int main()
{
    int  a, i;
    srand((unsigned)time(NULL));
    for (i = 0; i < 100; ++i){
        a = rand()%100;
        printf ("%d\n", a);
    }
    return 0;
}
