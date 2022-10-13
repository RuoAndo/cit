#include <iostream>

#include <fstream>
#include <vector>
#include <string>
#include <boost/tokenizer.hpp>

#include <stdio.h>
#include <string.h>

int ctoi(char c) {
	switch (c) {
		case '0': return 0;
		case '1': return 1;
		case '2': return 2;
		case '3': return 3;
		case '4': return 4;
		case '5': return 5;
		case '6': return 6;
		case '7': return 7;
		case '8': return 8;
		case '9': return 9;
		default: return 0;
	}
}

int main(int argc, char** argv)
{
	int strlen;
	int i;

	char input0[4];
	int input[4];
	
	for(i=0; argv[1][i]!='\0'; ++i);
	
	printf("%s %d \n", argv[1], i);
	strlen = i;

	strcpy(input0, argv[1]);
	printf("%s \n", input0);
	
	for (i = 0 ; i < strlen; i++ )
	{
	  printf("%d\n", ctoi(input0[i]));
	  input[i] = ctoi(input0[i]);
	}

	return 0;
}
