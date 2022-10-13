#include <stdio.h>
#include <stdlib.h>    /* exit(  ) で必要 */
#include <string.h>

#define BYTE 256
int alpha[BYTE];       /* 関数の外で宣言 */

void PrintResult(void)
{
  int c;

  for (c = 'a'; c <= 'z'; c++) 
    printf("%c:%d ",  c, alpha[c]); 
  printf("\n\n");
  for (c = 'A'; c <= 'Z'; c++)   
    printf("%c:%d ",  c, alpha[c] ); 
  printf("\n");
}

int main(int argc, char *argv[])
{
  int i;
  int c;
  
  char moji[100];
  strcpy(moji, argv[1]);
  // printf("%s", moji);
  
  while (moji[i])
    {
      c = (int)moji[i];

      if ( c >= 'a' && c <= 'z' || c >= 'A' && c <= 'Z')
	alpha[c]++;

      i++;
    }

  PrintResult();

}
