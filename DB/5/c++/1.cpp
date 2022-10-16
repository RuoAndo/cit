#include <fstream>
#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>

#include "rapidjson/document.h"
#include "rapidjson/istreamwrapper.h"

using namespace rapidjson;
using namespace std;

int main(int, char **)
{
    std::ifstream ifs("person.json");
    IStreamWrapper isw(ifs);

    Document doc;
    doc.ParseStream(isw);

    rapidjson::Value& s = doc["age"];
    //cout << doc["age"] << endl;
 
    
}

