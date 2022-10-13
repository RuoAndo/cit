#include <stdio.h>
#include <string.h>
#include <iostream>

int main(int argc, char *argv[])
{
  int i = 0;

  char moji[100];
  int j = 0;

  int n = 0;
  int decimal;
  int binary[32];

  std::string mystring = argv[1];
  std::cout << mystring << std::endl;

  strcpy(moji,mystring.c_str());
  
  /* display ASCII code */ 
  while(moji[i])
    printf("%d " , moji[i++]);
  
  printf("\n");

  i = 0;
  while(moji[i])
    {
      n = (int)moji[i];

      for(j=0; n>0; j++){
	binary[j] = n % 2;
	n = n / 2;
      }
 
      while( j>0 ){
	printf("%d", binary[--j]);
      }
      printf(" ");

      i++;
    }

  
  printf("\n");
 
  return 0;
}

