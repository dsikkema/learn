#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct hashmap {
  int size;
  int storage[];
} hashmap;

hashmap* create_hashmap(int size) {
  hashmap* result = (hashmap*)malloc(sizeof(hashmap));
  result->size = size;
}

uint32_t hash(int val) {
  unsigned int a = (unsigned int) val;
  a = (a ^ 61) ^ (a >> 16);
  a = a + (a << 3);
  a = a ^ (a >> 4);
  a = a * 0x27d4e2b2d;
  a = a ^ (a >> 15);
  return a;
}

int main() {
  for (int i=0; i<32; i++) {
    printf("%u\n", hash(i));
  }
}
