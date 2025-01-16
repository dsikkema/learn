#include <stdio.h>
#include <stdlib.h>
// #include <unistd.h> // if I want usleep
// #include <string.h> // for strlen probably

void demonstrateHeap() {
  // contrast addresses of stack mem with heap mem
  int* heap_num = (int*)malloc(sizeof(int));
  *heap_num=7;
  int stack_num = 9;

  printf("I do have two variables on the stack, a pointer and a plain int:\n");
  printf("heap_num is at: %p\n", &heap_num);
  printf("stack_num is at: %p\n", &stack_num);

  printf("But the value of the pointer is to a far away address:\n");
  printf("heap_num pointer val: %p\n", heap_num);

  printf("But heap vars declared by each other may be close in memory (albeit with possible \
buffer in between):\n");
  int* heap_2 = (int*)malloc(sizeof(int));
  int* heap_3 = (int*)malloc(sizeof(int));
  int* heap_4 = (int*)malloc(sizeof(int));
  *heap_2 = 1;
  *heap_3 = 1;
  *heap_4 = 1;
  printf("Three heap addresses: %p, %p, %p\n", heap_2, heap_3, heap_4);

  printf("Now freeing heap mem declared; good practice!\n");
  free(heap_num);
  free(heap_2);
  free(heap_3);
  free(heap_4);
}

int main() {
  demonstrateHeap();
  return 0;
}
