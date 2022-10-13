#include <iostream>

#include <fstream>
#include <vector>
#include <string>
#include <boost/tokenizer.hpp>



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

int main(void)
{
  int counter = 0;
  int column_counter = 0;
  int row_counter = 0;

  std::vector<int> value;

  const auto cells = parse_csv("G.csv");
  for (const auto& rows : cells) {
    for (const auto& cell : rows) {
      std::cout << cell << ",";
      value.push_back(atoi(cell.c_str())) ;
      counter++; 
    }
    column_counter++;
    std::cout << std::endl;
  }

  row_counter = counter / column_counter;
  std::cout << row_counter << std::endl;
  std::cout << column_counter << std::endl;
  std::cout << std::endl;

  int** arr = NULL;
  int i, j;

  int input[4];

  for(i=0;i<4;i++)
    scanf("%d",&input[i]);

  for(i=0;i<4;i++)
    printf("%d",input[i]);

  printf("\n");
  
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

  for(i = 0; i < column_counter; i++){
    for(j = 0; j < row_counter; j++){
      printf("%d ", arr[i][j]) ;
    }
    printf("\n");
  }

  printf("\n");

  int xored;
  for(i = 0; i < row_counter; i++){
    xored = 0;
    for(j = 0; j < column_counter; j++){
      printf("%d %d \n", arr[j][i], input[j]);
      xored = xored + arr[j][i] * input[j]; 
    }
    printf("%d \n", xored);
  }
  
  /*
    for (i=0;i<row_counter;i++) {
	free(arr[i]);
    }
    
    free(arr);
  */
  
    // free(arr);
 
  return 0;
}
