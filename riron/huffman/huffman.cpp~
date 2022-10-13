#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <algorithm>
#include <queue>
#include "get_distribution.hpp"
#include "initialize_huffman_tree.hpp"
#include "initialize_priority_queue.hpp"
#include "make_huffman_tree.hpp"
#include "huffman_tree_dfs.hpp"
using namespace std;

int main(){
    //üÍ
    string S;
    cin >> S;


    //@ ¶Ìo»pxðßé
    map<char, int> dist;
    get_distribution(S, dist);
    int N = dist.size();

    //íÞª1ÌêÍ_~[Ì¶ðüêéKvª é
    bool dummy_flag = false;
    if (N == 1){
        dummy_flag = true;
        N++;
        char dummy = (char) (S[0]+1);
        dist[dummy] = 0;
    }



    //A.@ e¶ÉÎ·ém[hð1Â¸Âìé
    vector<tuple<int, vector<int>, string> > T(2*N-1);
    initialize_huffman_tree(dist, T);


    //A.A eð½È¢m[hÌ¤¿Ao»pxª¬³¢2ÂÌm[hðIÔ
    priority_queue<pair<int, int>, vector<pair<int, int> >, greater<pair<int, int> > > pque;
    initialize_priority_queue(dist, pque);


    //A.B »Ì2ÂÌo»pxð«µí¹½m[hðV½Éìé
    //A.C V½Èm[hð»Ì2ÂÌm[hÌeÆ·é
    //A.D 2-4ÌèðSÄÌm[hªÂÈªêéÜÅJèÔ·
    make_huffman_tree(dist, T, pque);


    //B nt}ØÌeGbWÉ0Æ1ðÄÍßÄ¢­
    //C nt}ØÌª©ç¶ÜÅÌm[hðHÁÄÅ«½rbgñªêÆÈé
    huffman_tree_dfs(T, 2*N-2);


    //oÍ
    if (dummy_flag) N--;

    cout << N << endl;

    map<char, string> codeword;//ê
    int i = 0;
    for (auto itr : dist){
        if (i < N){
            cout << itr.first << " "  << get<2>(T[i]) << endl;
            codeword[itr.first] = get<2>(T[i]);
            i++;
        }
    }

    for (int i = 0; i < (int) S.length(); i++){
        cout << codeword[S[i]];
    }
    cout << endl;

    return 0;
}
