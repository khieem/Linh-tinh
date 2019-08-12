#include <iostream>
#include <map>
#include <vector>
#define INF 2000000000

using namespace std;

string find_lowest_cost_node( map< string, int >& costs, map<string,bool>& processed );

int main() {
   map< string, map< string, int > > graph;
   graph["nha"]["phuc"]   = 2;
   graph["nha"]["tuong"]  = 1;
   graph["phuc"]["kiet"]  = 0;
   graph["phuc"]["linh"]  = 7;
   graph["tuong"]["an"]   = 1;
   graph["tuong"]["linh"] = 3;
   graph["an"]["quang"]   = 2;
   graph["kiet"]["an"]    = 4;
   graph["kiet"]["quang"] = 2;
   graph["kiet"]["cun"]  = 4;
   graph["quang"]["cun"] = 3;
   graph["quang"]["dich"] = 0;
   graph["linh"]["quang"] = 1;
   graph["linh"]["lanEm"]   = 3;
   graph["cun"]["dich"]  = 1;
   graph["lanEm"]["dich"]   = 4;

   map< string, int> costs;
   costs["phuc"] = 2;
   costs["tuong"] = 1;
   costs["an"] = INF;
   costs["kiet"] = INF;
   costs["quang"] = INF;
   costs["linh"] = INF;
   costs["lanEm"] = INF;
   costs["cun"] = INF;
   costs["dich"] = INF;

   map< string, string > parents;
   parents["phuc"] = "nha";
   parents["tuong"] = "nha";

   map< string, bool> processed;

   string node = find_lowest_cost_node( costs, processed );
   while ( node != "") {
      int cost = costs[node];
      map<string, int> neighbors = graph[node];
      for ( map<string, int>::iterator it = neighbors.begin(); it != neighbors.end(); ++it ) {
         int new_cost = cost + neighbors[it->first];
         if ( costs[it->first] > new_cost ) {
            costs[it->first] = new_cost;
            parents[it->first] = node;
         }
      }
      processed[node] = true;
      node = find_lowest_cost_node( costs, processed );
   }
}

string find_lowest_cost_node( map< string, int >& costs, map< string, bool>& processed ) {
   int lowest_cost = INF;
   string lowest_cost_node;
   for ( map<string,int>::iterator it = costs.begin(); it != costs.end(); ++it ) {
      int cost = it->second;
      if ( cost < lowest_cost && processed[it->first] == false ) {
         lowest_cost = cost;
         lowest_cost_node = it->first;
      }
   }
   return lowest_cost_node;
}
