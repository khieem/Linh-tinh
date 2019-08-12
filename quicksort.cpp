#include <vector>
#include <iostream>
#include <time.h>
#include <algorithm>
#include <iomanip>
using namespace std;

int partition(vector<int>& arr, int left, int right) {
   int final = (left+right)/2;
   int pivot = arr[final];
   while (left <= right) {
      while (arr[left] < pivot)
         left++;
      while (arr[right] > pivot)
         right--;
      if (left <= right) {
         if (left == final)
            final = right;
         else if (right == final)
            final = left;
         swap(arr[left],arr[right]);
         left++;
         right--;
      }
   }
   return final;
}

void quickSort(vector<int>& arr, int left, int right) {

      int i = left, j = right;

      int tmp;

      int pivot = arr[(left + right) / 2];



      /* partition */

      while (i <= j) {

            while (arr[i] < pivot)

                  i++;

            while (arr[j] > pivot)

                  j--;

            if (i <= j) {

                  tmp = arr[i];

                  arr[i] = arr[j];

                  arr[j] = tmp;

                  i++;

                  j--;

            }

      };



      /* recursion */

      if (left < j)

            quickSort(arr, left, j);

      if (i < right)

            quickSort(arr, i, right);

}

void print( vector<int>& arr) {
   for (int x : arr)
      cout << setfill('0') << setw(2) << x << " ";
   cout << endl;
}

int main() {
   srand( time(NULL) );
   size_t size = 10;
   vector<int> arr(size);
   generate( arr.begin(), arr.end(), [] () {
      return rand() % 100;
   } );
   print( arr );
   int f;
   cout << (f = partition( arr, 0, size-1 )) << endl;
   //quickSort( arr, 0, size-1 );
   //bubble_sort( arr );
   //sort( arr.begin(), arr.end() );
   print( arr );
   for (int i = 1; i <= f; ++i) {
      cout << "   ";
   }
   cout << "*\n";

}
