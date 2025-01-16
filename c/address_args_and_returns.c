#include <stdio.h> // for printf
#include <stdlib.h> // for malloc, sizeof

int* dangerousStackReturn() {
  int num = 7;
  printf("Return address to an int holding number 7\n");
  return &num;
}

void demoStackReturnProblem() {
  printf("\nGoing to demonstrate returning stack addresses and pitfalls associated therewith\n\n");
  int* danger_ptr = dangerousStackReturn();
  printf("This may appear to work because stack hasn't changed much since getting pointer: %d\n", *danger_ptr);

  int a = 99;
  int b = 99;
  int c = 99;
  printf("Now try again, after declaring some other ints...\n");
  printf("Does this look like the number 7 to you? %d\n", *danger_ptr);
}

void takePassByRef(int* ref) {
  int replace = 99;
  printf("Received %d, will replace its value with %d\n", *ref, replace);
  *ref = replace;
}

void demoPassByRef() {
  printf("\nNow will demo pass by ref\n");
  int var = 1;
  printf("Initial value = %d\n", var);
  takePassByRef(&var);
  printf("New value = %d\n", var);
}


int main() {
  demoStackReturnProblem();
  demoPassByRef();

  // also, just because I don't know where else to put this, here is sprintf
  char* charArr = (char*)malloc(6 * sizeof(char) + 1); // length of "lmao N" + 1 for null terminator
  sprintf(charArr, "lmao %c", '7');
  printf("%s", charArr);
}
