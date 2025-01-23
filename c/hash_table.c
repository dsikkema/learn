#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef struct hashmap {
  int storage_sz;
  int** storage[];
} hashmap;

hashmap* create_hashmap(int storage_sz) {
  hashmap* result = (hashmap*)malloc(sizeof(hashmap));
  result->storage_sz = storage_sz;
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

}
