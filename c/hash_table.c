#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "linked_list.h"
#define is_debug 0
/**
 * I left the "extreme nulls" implementation in the 
 * linked list api. so just don't ever use ll_del_homeaway() otherwise this code, which directly gets 
 * into the guts of the linkedlist's pointers (for fun, for fastness, for
 * danger) will be un-memory safe by doing list mutation without properly handling the "extreme null"
 * sentinels. Also, you can't put 0 keys or values into the hashmap if also using extreme nulls lol.
 */

uint32_t hash(int val) {
  unsigned int a = (unsigned int) val;
  a = (a ^ 61) ^ (a >> 16);
  a = a + (a << 3);
  a = a ^ (a >> 4);
  a = a * 0x27d4e2b2d;
  a = a ^ (a >> 15);
  return a;
}

void dbg(char* s) {
  if (is_debug) {
    printf("%s\n", s);
  }
}

void dbg2(char* s, int n) {
  if (is_debug) {
    printf("%s %d\n", s, n);
  }
}

// Was going to structure this program using entry struct,
// and possibly as 2d array, but ending up not using the 
// struct and using array of linkedlists instead. But
// keeping the old code here just as later reference for 2d
// arrays and arrays of structs
typedef struct entry {
  int key;
  int val;
} entry;


void demo_2darr() {
  int nrows = 5, ncols = 5;
  entry* arr[nrows][ncols];
  for (int r = 0; r<nrows; r++) {
    for (int c = 0; c<ncols; c++) {
      entry* st = (entry*)malloc(sizeof(entry));
      st->key = r;
      st->val = c;
      arr[r][c] = st;
    }
  }

  for (int r = 0; r<nrows; r++) {
    printf("\n");
    for (int c = 0; c<ncols; c++) {
      printf(" %d,%d ", r, c);
    }
  }
  printf("\n");
}

const static int storage_size = 1024;

int get_map_idx(int key) {
  return hash(key) % storage_size;
}

void m_set(node** map, int key, int val) {
  dbg("enter mset");
  dbg2("key", key);
  dbg2("val", val);
  int map_idx = get_map_idx(key);
  node* val_ls = map[map_idx];
  if (val_ls == NULL) {
    val_ls = create_ll();
    map[map_idx] = val_ls;
  }

  node* cur = val_ls->next;
  node* prev = val_ls;
  while (cur != NULL) {
    dbg("in loop");
    if (cur->val == key) {
      dbg("hit val");
      cur->next->val = val;
      return;
    }
    prev = cur->next;
    cur = cur->next->next;
  }
  dbg("out loop");

  prev->next = create_node(key);
  prev->next->next = create_node(val);

}

int m_get(node** map, int key, int* result) {
  dbg2("enter m_get: key", key);
  int map_idx = get_map_idx(key);
  node* val_ls = map[map_idx];

  if (val_ls == NULL) {
    dbg("exit m_get, null ls");
    return -1;
  }

  node* cur = val_ls->next;
  while (cur != NULL) {
    dbg("m_get enter loop");
    if (cur->val == key) {
      *result = cur->next->val;
      dbg2("m_get hit val", cur->next->val);
      return 0;
    }
    cur = cur->next->next;
  }
  dbg("m_get exit loop");
  return -1;
}

int m_unset(node** map, int key) {
  int map_idx = get_map_idx(key);
  node* val_ls = map[map_idx];

  node* cur = val_ls->next;
  node* prev = val_ls;
  while (cur != NULL) {
    if (cur->val == key) {
      prev->next = cur->next->next;
      free(cur->next);
      free(cur);
      return 0;
    }
    prev = cur->next;
    cur = cur->next->next;
  }
  return -1;
}

node** create_hashmap() {
  // calloc will 0 all the mem, effectively initializing the whole array to NULLs
  return (node**)calloc(storage_size, sizeof(node*));
}


void demo_hashmap() {
  node** hashmap = create_hashmap();
  int k=9;
  int v=99;
  int result;
  m_set(hashmap, k, v);
  m_get(hashmap, k, &result);
  printf("get %d:%d\n", k, result);
}

int lolmain() {
  //demo_2darr();
  demo_hashmap();
  return 0;
}
