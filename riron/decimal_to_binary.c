#include <stdio.h>
#include <math.h>
 
int main(void)
{
  int i = 0;
  int j = 0;
  int n = 0;

  int binary[32];

  printf("input integer = ");
  scanf("%d", &i);

  for(j=0; i>0; j++){
    binary[j] = i % 2;
    i = i / 2;
  }

  // printf("%d \n",j);
  n = j;
  while( j>0 ){
    printf("%d", binary[--j]);
  }
  printf("\n");

  double w = 0;
  for(i=0; i<n; i++){
    printf("%d %d (%d) ", binary[i], i, (int)(pow(2,(double)i)));
    w = w + pow(2,(double)i)*(double)binary[i];
    printf("\n");
  }

  short int w_i = 0;

  printf("short intに変換\n");
  w_i = (short int)w;

  printf("%d \n", w_i);

  printf("%d << 1 = %d\n", w_i, w_i << 1);
  printf("%d >> 1 = %d\n", w_i, w_i >> 1);

}
