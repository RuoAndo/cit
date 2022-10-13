#include <iostream>
#include <bitset>

using std::cout; using std::endl;
using std::string; using std::bitset;

string toBinary(int n)
{
  string r;
  while (n != 0){
    r += ( n % 2 == 0 ? "0" : "1" );
    n /= 2;
  }
  return r;
}

int main() {
  
  int number = 0;

  printf("input integer = ");
  scanf("%d", &number);
  
  bitset<8> bs2(number);
  cout << "binary:  " << bs2 << endl;

  unsigned long number2 = bs2.to_ulong();

  cout << "integer: " << number2 << endl;
    
  return EXIT_SUCCESS;
}
