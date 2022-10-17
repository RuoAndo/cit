#include <fstream>
#include <cstdlib>
#include <iostream>
#include "json.hpp"

using json = nlohmann::json;
using namespace std;

int main()
{
  std::ifstream ifs("person.json");
  json j = json::parse(ifs);

  std::map<string,int> age;  
  
  for (auto it : j)
    {
    // "it" is of type json::reference and has no key() member
    // std::cout << it["age"] << '\n';

    age.insert(make_pair(it["name"], it["age"]));
    
    }

  for(auto itr = age.begin(); itr != age.end(); ++itr) {
        std::cout << "key = " << itr->first
		  << ", val = " << itr->second << "\n";    // lð\¦
    }
  

  /*
  for (auto& [key, val] : j.items())
    {
      for (auto& [key2, val2] : val.items())
	std::cout << val2 << '\n';
    }
  */
  
}
