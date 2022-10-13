#include <iostream>
#include <bitset>

#include <stdio.h>
#include <cstdlib>

using std::cout; using std::endl;
using std::string; using std::bitset;

#define N 16

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

  int i = 0;

  for(i=0;i<N;i++)
    {
      bitset<4> bs(i);
      cout << "(" << i << ")" << bs << endl;
    }

  return EXIT_SUCCESS;
}
