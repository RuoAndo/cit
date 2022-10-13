#include <iostream>

#include <fstream>
#include <vector>
#include <string>
#include <boost/tokenizer.hpp>

#include <stdio.h>
#include <string.h>

std::vector < std::vector< std::string > > parse_csv(const char* filepath)
{
  std::vector< std::vector< std::string > > cells;
  std::string line;
  std::ifstream ifs(filepath);

  // csvを走査
  while (std::getline(ifs, line)) {

    std::vector< std::string > data;

    // 1行を走査
    boost::tokenizer< boost::escaped_list_separator< char > > tokens(line);
    for (const std::string& token : tokens) {
      data.push_back(token);
    }

    // 1行読み込んだ結果を入れる
    cells.push_back(data);
  }

  return cells;
}

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
	
	// printf("%s %d \n", argv[1], i);
	strlen = i;

	strcpy(input0, argv[1]);
	// printf("%s \n", input0);
	
	for (i = 0 ; i < strlen; i++ )
	{
	  // printf("%d\n", ctoi(input0[i]));
	  input[i] = ctoi(input0[i]);
	}

	int counter = 0;
	int column_counter = 0;
	int row_counter = 0;

	std::vector<int> value;

	const auto cells = parse_csv("G.csv");
	for (const auto& rows : cells) {
	  for (const auto& cell : rows) {
	    // std::cout << cell << ",";
	    value.push_back(atoi(cell.c_str())) ;
	    counter++; 
	  }
	  column_counter++;
	  // std::cout << std::endl;
	}

	row_counter = counter / column_counter;
	/*
	std::cout << row_counter << std::endl;
	std::cout << column_counter << std::endl;
	std::cout << std::endl;
	*/

	int** arr = NULL;
	int j;

	arr = (int**)malloc(sizeof(int*) * column_counter);
	if(arr == NULL){
	  return -1;
	}
  
	for(i = 0; i < column_counter; i++){
	  arr[i] = (int*)malloc(sizeof(int) * row_counter);
	  if(arr[i] == NULL){
	    return -1;
	  }
	}

	counter = 0;
	for(i = 0; i < column_counter; i++){
	  for(j = 0; j < row_counter; j++){
	    arr[i][j] = value[counter];
	    // std::cout << value[counter];
	    counter++;
	  }
	} 

	/*
	for(i = 0; i < column_counter; i++){
	  for(j = 0; j < row_counter; j++){
	    printf("%d ", arr[i][j]) ;
	  }
	  printf("\n");
	}
	*/

	int xored;

	for(i = 0; i < row_counter; i++){
	  xored = 0;
	  for(j = 0; j < column_counter; j++){
	    // printf("%d %d \n", arr[j][i], input[j]);
	    xored = xored xor (arr[j][i] * input[j]);
	  }
	  printf("%d", xored);

	}

	printf("\n");

	return 0;
}
