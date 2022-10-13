#include <stdio.h>
#include <stdlib.h>
#define ROW 6
#define COL 5
int main(){
    int** arr = NULL;
    int i, j;
    
    arr = (int**)malloc(sizeof(int*) * ROW);
    if(arr == NULL){
        return -1;
    }
    for(i = 0; i < ROW; i++){
        arr[i] = (int*)malloc(sizeof(int) * COL);
        if(arr[i] == NULL){
            return -1;
        }
    }    
    for(i = 0; i < ROW; i++){
        for(j = 0; j < COL; j++){
            arr[i][j] = i * j;
        }
    }
    for(i = 0; i < ROW; i++){
        for(j = 0; j < COL; j++){
            printf("%d ", arr[i][j]) ;
        }
        printf("\n");
    }    
            
    return 0;
}
