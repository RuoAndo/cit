#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <queue>

void huffman_tree_dfs(vector<tuple<int, vector<int>, string> > &T, int v) {
    vector<int> temp1 = {};
    if (get<1>(T[v]) != temp1){
        for (int i = 0; i < 2; i++) {
            string temp2 = get<2>(T[v]) + (char) (i+'0');
            int idx = get<1>(T[v])[i];
            T[idx] = make_tuple(get<0>(T[idx]), get<1>(T[idx]), temp2);
            huffman_tree_dfs(T, idx); //ÄA
        }
    }
}
