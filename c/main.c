#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>

/**
 * Here's the final part I needed to break down after building the circular buffer, regarding doing 'magic' with the pointers, that Isaac helped me with.

  CircularBuffer* cb = create_buffer(5);
  write_to_buffer(cb, 7);
  void* coerced_cb = (void*)cb;
  void* coerced_ptr_to_read_ptr = coerced_cb + 8;
  int** ptr_to_read_ptr = (int**)coerced_ptr_to_read_ptr;
  int* derived_read_ptr = *ptr_to_read_ptr;
  int read_val = *derived_read_ptr;
  printf("Value to read next: %d\n", read_val);

I was fundamentally dealing with a pointer to a pointer. cb was already a pointer, and while what it "had" was a pointer to an int, I shifted "pointer to cb" to "the right" so that it became "pointer to (pointer to int)", hence needed to "de-coerce" into a int**. This becomes readily apparent when I see what the arrow operator hides:

  int direct_read_val = *(*cb).read_ptr;

The two different asterisks there show everything you need to know--pointer to a pointer.

Isaac also showed me how to treat an array as a pointer.


 */

typedef struct {
  int* buffer; 
  int* read_ptr;
  int* write_ptr;
  int size;
  int count;
} CircularBuffer;

CircularBuffer* create_buffer(int size) {
  CircularBuffer* cb = (CircularBuffer*)malloc(sizeof(CircularBuffer));
  cb->buffer = (int*)malloc(size * sizeof(int));
  cb->read_ptr = cb->buffer;
  cb->write_ptr = cb->buffer;
  cb->size = size;
  cb->count = 0;

  return cb;
}

int read_from_buffer(CircularBuffer* cb, int* result) {
  if (cb->count == 0) {
    return -1;
  } 
  
  *result = *(cb->read_ptr);
  cb->read_ptr++;

  if (cb->read_ptr >= cb->buffer + cb->size) {
    cb->read_ptr = cb->buffer;
  } 

  cb->count--;
  return 0;
}

int write_to_buffer(CircularBuffer* cb, int val) {
  if (cb->count == cb->size) {
    return -1;
  }

  *(cb->write_ptr) = val;
  cb->write_ptr++;
  
  if (cb->write_ptr >= cb->buffer + cb->size) {
    cb->write_ptr = cb->buffer;
  }

  cb->count++;
  return 0;
}

int test_buffer() {
  CircularBuffer* cb = create_buffer(5);

  printf("Writing loop\n");
  for (int i=0; i<7; i++) {
    // just for lols
    if (i==3) {
      int lmao;
      read_from_buffer(cb, &lmao);
      printf("Read val: %d, Count: %d\n", lmao, cb->count);
    }

    int result = write_to_buffer(cb, i);
    
    if (result == 0) {
      printf("Write val: %d, Count: %d\n", i, cb->count);
    } else {
      printf("Buffer full; couldn't write. Count=%d\n", cb->count);
    }
  }

  printf("Reading loop\n");
  for (int i=0; i<7; i++) {
    // just for lols
    if (i==3) {
      int lmao = 99;
      write_to_buffer(cb, lmao);
      printf("Wrote val: %d, Count: %d\n", lmao, cb->count);
    }
    int read_val;
    int result = read_from_buffer(cb, &read_val);
    if (result == 0) {
      printf("Read val: %d, Count: %d\n", read_val, cb->count);
    } else {
      printf("Buffer empty; couldn't read. Count=%d\n", cb->count);
    }
  }

  free(cb->buffer);
  free(cb);
  return 0;
}

int main() {
  // here is how to get offset
  // printf("Offset of buffer: %lu\n", offsetof(CircularBuffer, buffer));
  CircularBuffer* cb = create_buffer(5);
  write_to_buffer(cb, 7);
  // int val = *cb->read_ptr;
  // int* val = *((int**)(((void*)cb) + 8));
  void* coerced_cb = (void*)cb;
  void* coerced_ptr_to_read_ptr = coerced_cb + 8;
  int** ptr_to_read_ptr = (int**)coerced_ptr_to_read_ptr;
  int* derived_read_ptr = *ptr_to_read_ptr;
  int read_val = *derived_read_ptr;
  int direct_read_val = *(*cb).read_ptr;
  printf("Value to read next: %d\n", read_val);
  printf("Value to read next (direct): %d\n", direct_read_val);
}
