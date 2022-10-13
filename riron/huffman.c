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
  //入力
  string S;
  cin >> S;


  //① 文字の出現頻度を求める
  map<char, int> dist;
  get_distribution(S, dist);
  int N = dist.size();

  //種類数が1の場合はダミーの文字を入れる必要がある
  bool dummy_flag = false;
  if (N == 1){
    dummy_flag = true;
    N++;
    char dummy = (char) (S[0]+1);
    dist[dummy] = 0;
  }



  //②.① 各文字に対応するノードを1つずつ作る
  vector<tuple<int, vector<int>, string> > T(2*N-1);
  initialize_huffman_tree(dist, T);


  //②.② 親を持たないノードのうち、出現頻度が小さい2つのノードを選ぶ
  priority_queue<pair<int, int>, vector<pair<int, int> >, greater<pair<int, int> > > pque;
  initialize_priority_queue(dist, pque);


  //②.③ その2つの出現頻度を足し合わせたノードを新たに作る
  //②.④ 新たなノードをその2つのノードの親とする
  //②.⑤ 2-4の手順を全てのノードがつながれるまで繰り返す
  make_huffman_tree(dist, T, pque);


  //③ ハフマン木の各エッジに0と1を当てはめていく
  //④ ハフマン木の根から文字までのノードを辿ってできたビット列が符号語となる
  huffman_tree_dfs(T, 2*N-2);


  //出力
  if (dummy_flag) N--;

  cout << N << endl;

  map<char, string> codeword;//符号語
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
