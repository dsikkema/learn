#include <stdio.h>

int main() {
  int val = 777;
  int* ptr = &val;
  int** double_ptr = &ptr;

  printf("Double reference: %p -> %p -> %d\n", double_ptr, *double_ptr, **double_ptr);
  
  // can put the asterisk wherever
  int *ptr_b = ptr;
  int      *      ptr_c = ptr;
  printf("Asterisks wherever you want: %d, %d\n", *ptr_b, *ptr_c);

  printf("When declaring multiple vars on same line, it gets tricky!\n");
  int* a, b;
  a=ptr; // it's a pointer
  b=val; // it's an int
  printf("a=%p, b=%d\n", a, b); 

}
