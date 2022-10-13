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

    if (bset1.any())
        cout << "bset1 has some bit set.\n";
  
    if (bset2.any())
        cout << "bset2 has some bit set.\n";

   // bset.set() sets all bits
    cout << "biset1.set():" << bset1.set() << endl;
  
    // bset.set(pos, b) makes bset[pos] = b
    cout << "bitset1.set(4,0):" << bset1.set(4, 0) << endl;
  
    // bset.set(pos) makes bset[pos] = 1
    cout << "bset2.set(4):" << bset2.set(4) << endl;

    // makes all bits 0
    cout << "bset1.reset():" << bset1 << endl;
    cout << "bset2.reset():" << bset2 << endl;
  
    // flip function flips all bits 
    cout << "bset1.flip(2):" << bset1.flip(2) << endl;
    cout << "bset2.flip():" << bset2.flip() << endl;
    
  return 0;
}
