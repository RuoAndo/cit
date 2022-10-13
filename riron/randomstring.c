#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <bitset>
#include <time.h>

void shuffle(int array[], int size) {
    for(int i = 0; i < size; i++) {
      srand((unsigned int)time(NULL));
      int j = rand() % size;
        // int j = rand()%size;
      int t = array[i];
      array[i] = array[j];
      array[j] = t;
    }
}

int main(void){

  int *list;
  
  list = (int*)malloc(sizeof(int) * 16);

  srand((unsigned int)time(NULL));
  for(int i = 0; i < 16; i++)
    {
      list[i] = 65 + (int)(rand() * (90 - 65 + 1.0) / (1.0 + RAND_MAX));
    }
  
  shuffle(list, 16);
  
  for (int i = 0; i < 16; i++) {
    printf("%c", list[i]);
  }

  printf("\n");
  
  return 0;
  
}
