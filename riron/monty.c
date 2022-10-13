#include <stdio.h>
#include<stdlib.h>
#include<time.h>
#define NUM_DOORS 3

int monty(int change)
{
    int i = 0, doors[NUM_DOORS] = {0};

    doors[rand()%NUM_DOORS] =1;
    int mychoice = rand()%NUM_DOORS;
    
    for(i = 0; i < NUM_DOORS; i++)
        if(doors[i] == 0 && i != mychoice)
        {
            doors[i] = -1;
            break;
        }

    if(change)
        for(i = 0; i < NUM_DOORS; i++)
            if(doors[i] != -1 && i  != mychoice)
            {
                mychoice = i;
                break;
            } 

    return (doors[mychoice] == 1); 
}

int main()
{
    int i = 0, num_win = 0;
    srand((unsigned)time(NULL));

    int *changed;
    int *no_changed;

    int N = 1000000;
    FILE *fp;

    changed = (int*)malloc(sizeof(int) * N);
    no_changed = (int*)malloc(sizeof(int) * N);

    num_win = 0;
    for(i = 0; i < N; i++) 
      {
	if(monty(0)) num_win++;
	changed[i] = num_win;
      }

    printf("変更無しの勝率は%.6f\n", (double)num_win / i);

    num_win = 0;
    for(i = 0; i < N; i++) 
      { 
	if(monty(1)) num_win++;
	no_changed[i] = num_win;
      }

    printf("変更ありの勝率は%.6f\n", (double)num_win / i);


    fp = fopen("no_changed.txt", "w");
    for(i = 0; i < N; i++) 
      fprintf(fp, "%.6f \n", (double)no_changed[i]/N);
    fclose(fp);

    fp = fopen("changed.txt", "w");
    for(i = 0; i < N; i++) 
      fprintf(fp, "%.6f \n", (double)changed[i]/N);
    fclose(fp);

    return 0;
}
