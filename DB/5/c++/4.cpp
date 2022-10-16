#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iterator>
#include "picojson.h"

int main(void)
{
    // JSONf[^ÌÇÝÝB
    std::ifstream ifs("person.json", std::ios::in);
    if (ifs.fail()) {
        std::cerr << "failed to read test.json" << std::endl;
        return 1;
    }
    const std::string json((std::istreambuf_iterator<char>(ifs)), std::istreambuf_iterator<char>());
    ifs.close();

    // JSONf[^ððÍ·éB
    picojson::value v;
    const std::string err = picojson::parse(v, json);
    if (err.empty() == false) {
        std::cerr << err << std::endl;
        return 2;
    }

    /*
    std::cout << "¢Á½ñ·×ÄðoÍµÄÝéB" << std::endl;
    std::cout << v << std::endl;
    std::cout << std::endl;
    */

    picojson::object& obj = v.get<picojson::object>();
    picojson::array& ary = obj["array"].get<picojson::array>();
    for (const auto& e : ary) {  // vectorðrange-based-forÅÜíµÄ¢éB
        std::cout << e.get<std::string>() << " ";
    }
    std::cout << "\n\n";

    /*
    picojson::object& obj = v.get<picojson::object>();
    std::cout << "[vðÜíµÄÝéB" << std::endl;
    for (const auto& p : obj) { // mapðrange-based-forÅÜíµÄ¢éB
      std::cout << p.first << ": " << p.second.to_str() << std::endl;
    }
    */
    
}
