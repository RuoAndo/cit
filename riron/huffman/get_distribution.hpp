#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <queue>

using namespace std;

void get_distribution(string S, map<char, int> &dist){
    for (int i = 0; i < (int) S.length(); i++) {
        dist[S[i]]++;
    }
}
