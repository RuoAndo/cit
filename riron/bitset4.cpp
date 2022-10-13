#include <iostream>
#include <bitset>

using std::cout; using std::endl;
using std::string; using std::bitset;

int main(int argc, char *argv[])
{
  string bset_string = argv[1];
  cout << bset_string << endl;

  bitset<8> bset(bset_string);
  // cout << bset << endl;
  
  cout << "# of 1:" << int(bset.count()) << endl; 

  /*
  int parity;
  parity =  int(bset.count()) % 2;
  cout << parity << endl;
  */
  
  return 0;
}
