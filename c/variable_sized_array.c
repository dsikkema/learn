#include <stdio.h>
int n=3, c = 5; // they don't need to be static even
const int U=2, V=2;
int main() {
  int arr[n][c];
  // below will fail: cannot initialize variable size array
  // int arr[n][c] = {0};

  // this works, though: the sizes are consts so it's a fixed size array
  int arr2[U][V] = {0}; 

  arr[2][4] = 9;
  printf("arr[2][4] = %d\n", arr[2][4]);
}
