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

  for(int i = 0; i < 16; i++)
    list[i] = i;

  shuffle(list, 16);
  
  for (int i = 0; i < 16; i++) {
    // printf("%d \n", list[i]);
    std::bitset<4> bs(list[i]);
    std::cout << list[i] << ":" << bs << std::endl;
  }

  
  return 0;
  
}
