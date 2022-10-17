#include <iostream>
#include "json.hpp"

// nlohmann/jsonðg¢â·­·é½ßGCAXì¬:
using json = nlohmann::json;

using namespace std;

int main(int argc, char* argv[]) {
    // eLg[ÈJSON¶ñðì¬:
    string jsonstr = R"({
        "str": "¢ëÍÉÙÖÆ",
        "hoge": "í·éæI",
        "num": 9999.9999,
        "isFoo": false,
        "person": {
            "firstname": "Taro",
            "surname": "YAMADA",
            "favorites": ["apple", "orange"]
        }
      })";
    // JSON¶ñðp[X:
    auto jobj = json::parse(jsonstr);
    // JSONIuWFNg©çJSON¶ñð_v:
    cout << "\nJSONð_v: " << jobj.dump() << endl; // ®`³µÅoÍ
    // JSONIuWFNg©çvpeBlðæ¾:
    cout << "\njobj[\"str\"]Ìlðæ¾: " << jobj["str"] << endl;
    // JSONIuWFNgÌvpeBlðXV:
    jobj["str"] = "¿èÊéð";
    jobj.erase("hoge"); // hogevpeBðí
    jobj["num"] = 999999.999999;
    jobj["isFoo"] = true;
    jobj["person"]["surname"] = "SUZUKI"; // person.surnameðÏX
    jobj["person"]["age"] = 20; // person.ageÆ¢¤Vµ¢vpeBðÇÁ
    jobj["person"]["favorites"].push_back("banana"); // zñÉlðÇÁ
    // JSONIuWFNg©çJSON¶ñð®`µÄ_v:
    cout << "\nlÏXãÌJSONð®`µÄ_v: " << jobj.dump(2) << endl;
}
