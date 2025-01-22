#include <stdio.h>
#include <stdlib.h>

/**
 * Something important going on here. sizeof will get total bytes of the arr, not length. So divide by the size
 * of an element to get the length. But you cannot do this inside a function for the very reason that we're 
 * calculating length here in the first place! Because then size information will be erased.
 *
 * Hence we are doing it as a macro.
 */
#define ARRAY_LENGTH(arr)  (sizeof(arr) / sizeof(arr[0]))

void sayHello() {
  printf("Hello\n"); 
}

int multiply(int a, int b) {
  return a * b;
}

int square(int a) {
  return a * a;
}

int weird_funcptr_demo() {
  printf("\nThis part of the demo will showcase crazy function pointer declarations and casting\n"); 

  // This was my first line; it's a problem because it's a memory leak! Immediately overwritten malloc'd space.
  // void* arbitrary_ptr = malloc(sizeof(size_t));  
  void* arbitrary_ptr;  

  int (*proper_multiply_func_ptr)(int, int) = multiply; // This is the right way to declare func ptr to multiply()
  arbitrary_ptr = (void*) multiply; // I can also cast it to void*, though.

  printf("Implicitly, void fn is converted to other types. Call multiply:\n");
  int (*func_ptr)(int, int);
  func_ptr = arbitrary_ptr; // ... and then assign it, with coercion, into the proper type again
  int res = func_ptr(2, 3); // ... and call it.
  printf("result=%d\n", res);

  //
  printf("Doesn't exactly work the other way: must explicitly cast non-void func ptr to void\n");
  int (*int_fn_ptr_with_args)(int, char, long, long, long, size_t);
  int_fn_ptr_with_args = (int (*)(int, char, long, long, long, size_t))sayHello;
  // int_fn_ptr_with_args(); // won't work, expects args

  // By the way, this won't work either: it's the wrong syntax. Casting to a void pointer is not the same
  // as casting to a function pointer:

  // ((void*)int_fn_ptr_with_args)(); 

  // This actually does work, and says hello
  ((void (*)())int_fn_ptr_with_args)();

  printf("Can use typedef to \"shortcut\" the argless void function ptr type, and cast to that too:\n");
  typedef void (*void_fn_ptr)(void);
  ((void_fn_ptr)sayHello)();
}

// void transform_arr(int arr[1]) {
// void transform_arr(int* arr) {
void transform_arr(int arr[], size_t len, int(*callback)(int)) {
  /**
   * BTW, in the signature, notice how I have to pass size as a separate param. arr is just a pointer, it contains
   * no size information, and there's no built-in NULL terminator or equivalent to int arrays (unlike strings).
   *
   * In the local declaration of an array, the array variable represents the actual array object, with baked-in size
   * information, so sizeof() can work on it. Here, sizeof() won't work. So we have to call it at the local declaration
   * and pass the information in.
   *
   * The alternative would be to define some kind of sentinel value like -1, but that would become a problem is an "expected"
   * value in the array ever happend to be the sentinal.
   */
  for (int i = 0; i < len; i++) {
    arr[i] = callback(arr[i]);
  } 
}

void print_arr(int* arr, size_t len) {
  for (int i=0; i < len; i++) {
    printf("%d, ", arr[i]);
  }
  printf("\n");
}

int demo_array_callback() {
  printf("\nNow we're going to see a classic callback example\n");
  int arr[] = {-4, -2, -1, 0, 1, 2, 4, 8};

  size_t len=ARRAY_LENGTH(arr);
  printf("len: %zu\n", len);
  printf("Array before transform with callback (square):\n");
  print_arr(arr, len);
  transform_arr(arr, len, square);
  printf("...and after:\n");
  print_arr(arr, len);

  return 0;
}


int main() {
  weird_funcptr_demo();
  demo_array_callback();
}

