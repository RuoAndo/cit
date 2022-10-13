#include <iostream>
#include <bitset>

using std::cout; using std::endl;
using std::string; using std::bitset;

int main(int argc, char *argv[])
{
  string bset_string_1 = argv[1];
  cout << "bitset1:" << bset_string_1 << endl;

  string bset_string_2 = argv[2];
  cout << "bitset2:" << bset_string_2 << endl;
  
  bitset<8> bset1(bset_string_1);
  bitset<8> bset2(bset_string_2);

  cout << endl;
  
  // comparison operator
  cout << "(bset1 == bset2):" << (bset1 == bset2) << endl;
  cout << "(bset1 != bset2):" << (bset1 != bset2) << endl; 
  
  // left and right shifting
  cout << "(bset1 <<= 2):" << (bset1 <<= 2) << endl; 
  cout << "(bset1 >>= 1):" << (bset1 >>= 1) << endl; 
  
  // not operator
  cout << "(~bset2):" << (~bset2) << endl; // 1100
  
  // bitwise operator
  cout << "(bset1 & bset2)" << (bset1 & bset2) << endl; // 0010
  cout << "(bset1 | bset2)" << (bset1 | bset2) << endl; // 0111
  cout << "(bset1 ^ bset2)" << (bset1 ^ bset2) << endl; // 0101

  // bitwise operation and assignment
  cout << endl;
  cout << "(bset1 ^= bset2):" << (bset1 ^= bset2) << endl; // 1010
  
  /*
  cout << "(bset1 &= bset2)" << (bset1 &= bset2) << endl; // 0010
  cout << "(bset1 |= bset2)" << (bset1 |= bset2) << endl; // 0011
  */
  
  return 0;
}
