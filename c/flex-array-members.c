#include <stdlib.h>
#include <stdio.h>

struct buffer {
  size_t size;
  char data[]; // if this were defined non-dynamically, it would tally into the size of the struct
               // and the bug wouldn't happen
} ;

int main() {
  int sz = 60;
  int malloc_add_sz = 0; // if this were equal to "sz" the program would work
  struct buffer* buf = malloc(sizeof(struct buffer)+malloc_add_sz);
  struct buffer* buf2 = malloc(sizeof(struct buffer)+malloc_add_sz);
  buf->size = sz;

  for(int i=0; i<buf->size; i++){
    buf->data[i] = 'A' + i;
    buf2->data[i] = 'A' + i;
  }


  for (int i=0; i<buf->size; i++) {
    // bug: we find that the writes onto buf1 have overridden buf2 because they're suparate by only 16 bytes of
    // address space, and thus, the (0-indexed) 16th character of buf1 starts overwriting buf2.
    // But this "separated by 16 bytes of address space" is likely an undefined behavior, machine-specific, etc.
    printf("i: %d, buf1: %c, buf2: %c \n", i, buf->data[i], buf2->data[i]);
  }

  free(buf);
  printf("\n");
  printf("Size of buf: %d", sizeof(struct buffer));
  printf("buf1 loc: %p, ", buf);
  printf("buf2 loc: %p", buf2);
  return 0;
}
