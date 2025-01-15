#include <stdio.h>


/**
 * Note about the syntax of this struct: it's called a tagged stuct because name precedes open brace.
 *
 * This now means the "struct " prefix, even though a different word, is kind of part of the name of the
 * type. Cannot do sizeof(PackedFlags), has to be sizeof(struct PackedFlags).
 *
 * This is as opposed to ....
 *
 * typedef struct {
 *  int a;
 *  int b;
 * } my_struct;
 *
 * In sucn case, typedef is creating an "alias" for the type so the new type name (my_struct) can be
 * used without the struct keyword. Some like explicitly putting "struct " though, for clarity. Both
 * methods may be combined a la:
 *
 * typedef cool_struct {
 *  int a;
 * } cool_struct;
 *
 */
struct PackedFlags {
  // If remove the `: N` from this (called bit field declarator; controls how many bits are occupied by the member,
  // is used specially for this case), then the size of the struct will be larger: 4 bytes, not 1, 
  // because it won't pack into single byte
  //
  unsigned char isActive: 1;
  unsigned char priority: 3;
  unsigned char type: 2;
  unsigned char reserved: 2;

};


int main() {
  // this syntax is known as a compound literal or structure initialized, it inits struct members in order of
  // declaration
  struct PackedFlags flags = {1, 5, 2, 0};

  // Size should be 1, because of packing
  // Note that %zu means unsigned size. 
  printf("Size of PF: %zu bytes\n", sizeof(struct PackedFlags));
  // also 1 of course
  printf("Size of flags: %zu bytes\n", sizeof(flags));

  printf("Active: %d\n", flags.isActive);
  printf("Priority: %d\n", flags.priority);
  printf("Type: %d\n", flags.type);
  printf("Reserved: %d\n", flags.reserved);


  flags.priority = 6; // if set to number larger than three bites, it 
                      // will not be accurate, and only set some bits that fit 
  printf("Set priority=6\n");


  printf("Active: %d\n", flags.isActive);
  printf("Priority: %d\n", flags.priority);
  printf("Type: %d\n", flags.type);
  printf("Reserved: %d\n", flags.reserved);
}
