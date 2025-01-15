#include <stdio.h>
#include <stddef.h>
#include <limits.h>

void section(const char* title) {
  printf("\n ##### %s ##### \n", title);
}

int main() {

  section("The Basics");
  
  printf("float %%f: %f\n", 2.3);
  printf("signed (int, default),  %%d: %d\n", -1);
  printf("unsigned (int, default),  %%u: %u\n", 4294967295);
  printf("unsigned (same as above but typed in code as \"-1)\",  %%u: %u\n", 4294967295);
  printf("signed (long),  %%ld: %ld\n", LONG_MAX);
  printf("unsigned (long),  %%lu: %lu\n", ULONG_MAX);
  char mychar = 1;
  printf("signed char, %%hhd: %hhd\n", mychar);

  section("Size");

  printf("Size of size_t: %zu\n", sizeof(size_t));
  printf("Size of sizeof(sizeof((1))): %zu\n", sizeof(sizeof((1)))); // This and prev may be 8 for 64 bit systems.
  printf("Size of int: %zu\n", sizeof(int)); // 4

  char array[50];
  // note how below, I can (and should, must really, for safety) use size_t as the iterator type, so
  // it has no danger of overflowing in case sizeof returns something larger than an int (64 bit 
  // systems have 8 bytes not 4 for sizes)
  for (size_t i = 0; i < sizeof(array); i++) {
    array[i] = 'A' + i;
  }

  section("Max limits of signed vs. unsigned");
  // Silly me, this was confusing for a moment: this is just casting -1 to size_t.
  // Of course to get the (unsigned) max, what you generally do is interpret a signed -1 as unsigned
  printf("What the heck? (size_t)-1 = %zu\n", (size_t)-1);

  int max_int = INT_MAX;
  unsigned int max_uint = UINT_MAX;
  printf("INT_MAX: %d\n", max_int);
  printf("UINT_MAX, printed with %%d: %d\n", max_uint);
  printf("UINT_MAX (%%u): %u, literal '-1' interpretted as unsigned int :%u\n", max_uint, -1); 
}

