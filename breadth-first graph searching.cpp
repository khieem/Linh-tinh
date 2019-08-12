#include <iostream>
#include <vector>
#include <map>
#include <deque>

using namespace std;

void print( vector<string>& arr ) {
   for ( string x : arr )
      cout << x << " ";
   cout << endl;
}

void print( deque<string>& queue ) {
   for ( string s : queue )
      cout << s << " ";
   cout << endl;
}

int main() {
   map< string, vector<string> > graph;
   graph["khiem"] = {"an", "tuong", "kiet"};
   graph["an"] = {"quang"};
   graph["quang"] = {"phuc"};
   graph["phuc"] = {"quang", "kiet", "linh", "DICH"};
   graph["kiet"] = {"khiem", "linh"};
   graph["tuong"] = {"linh"};
   graph["linh"] = {"DICH"};
   graph["DICH"] = {};

   deque<string> queue;
   map<string, bool> visited;
   queue.push_back( "khiem" );
   while ( !queue.empty() ) {
      string name = queue[0];
      queue.pop_front();
      if ( !visited[name] ) {
         if ( name == "DICH" ) {
            cout << "DA DEN DICH";
            return 0;
         } else {
            queue.insert( queue.end(), graph[name].begin(), graph[name].end() );
            visited[name] = 1;
         }
      }
   }
}
