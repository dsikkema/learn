/**
 * TOODO:
 *  - support 0 vals in array (that don't conflict with EXTREME NULL)
 *
 * List is structured so that empty list always has a head, 0th value is always stored 
 * in head->next->val, not head->val.
 *
 * A "linked list" is simply a reference to the head node.
 *
 * Example: [0, 1, 2]. h( ) is "head" which contains no real val data.
 * index:         0      1      2
 * node:  ( ) -> (7) -> (9) -> (4) -> NULL
 *
 * Example: empty list. h( ) is "head" which contains no real val data.
 * index: (no indexes)        
 * node:  ( ) -> NULL
 */
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

#define debug_enabled 0

void debug(char* str) {
  if (debug_enabled) {
    printf("(debug) %s\n", str);
  }
}

/**
 * this syntax: typedef, with struct name before and after struct body, 
 * is necessary to allow struct to have pointer to itself
 */
typedef struct node { 
  struct node* next;
  int val;
} node;


node* create_node(int val) {
  node* result = (node*)malloc(sizeof(node));
  result->val = val;
  result->next = NULL;
  return result;
}

void free_list(node* ll) {
  node* cur = ll;
  node* nxt = NULL;
  while (cur != NULL) {
    nxt = cur->next;
    free(cur);
    cur = nxt;
  }
}

/**
 * Todo: extreme null needs to be a once-randomly generated sequence of bytes,
 * all-zeroes is actually plausible for real struct (if val = 0)
 */
int set_extreme_null(node* ptr) {
  if (ptr == NULL) {
    return -1;
  }
  for (size_t i=0; i<sizeof(node); i++) {
    *(((char*)ptr) + i) = 0;
  }

  return 0;
}

/**
 * This is a toy concept, not suppoed to be safe, to push the limits of weird
 * memory mgmt with C. It turns the memory address into kind of sentinel value
 * so that other pointers, even without being NULL, can be interpretted like
 * NULL if they point to an address filled with this data.
 */
int extreme_null(node* ptr) {
  if (ptr == NULL) {
    return 0;
  }
  for (size_t i=0; i<sizeof(node); i++) {
    if (*(((char*)ptr) + i) != 0) {
      return 0;
    }
  }
  return 1;
}

void ll_add(node* ll, int val) {
  debug("Enter ll_add");
  node* cur = ll;
  while (cur->next != NULL && !extreme_null(cur->next)) {
    debug("In loop");
    cur = cur->next;
  }
  debug("Out loop");

  if (extreme_null(cur->next)) {
    debug("is extreme null");
    free(cur->next);
  }

  debug("set cur->next to create node");
  cur->next = create_node(val);
}

node* create_ll() {
  return create_node(-1); // the linked list is just the head
}

node* ll_retrieve_node(node* ll, int idx) {
  int i = 0;
  node* cur = ll->next;
  
  if (cur == NULL || extreme_null(cur)) {
    return NULL; // empty list, no indexes will exist
  }

  while (i < idx && cur->next != NULL && (!extreme_null(cur->next))) {
    cur = cur->next;
    i++;
  } 

  if (i < idx) {
    return NULL;
  } else {
    return cur;
  }
}

/**
 * return -1 for idx doesn't exist
 */
int ll_get(node* ll, int idx, int* result) {
  debug("enter ll_get");
  if (idx < 0) {
    debug("return -2 ll_get");
    return -2;
  }

  node* cur = ll_retrieve_node(ll, idx);
  if (cur == NULL) {
    debug("return -1 ll_get");
    return -1;
  }
  *result = cur->val;
  debug("return 0 ll_get");
  return 0;
  
}

/**
 * return -1 for idx doesn't exist
 */
int ll_del(node* ll, int idx) {
  node* prev;
  if (idx < 0) {
    return -1;
  } else if (idx == 0) {
  // } else if (idx = 0) { // lmao bug alert, I actually did this, and it ran - just caused wrong node to be deleted.
    prev = ll;
  } else {
    prev = ll_retrieve_node(ll, idx - 1);

    // the index before the one to delete doesn't exist, hence the idx to delete doesn't exist
    if (prev == NULL) {
      return -1;
    }
  }

  node* to_rm = prev->next;
  if (to_rm == NULL || extreme_null(to_rm)) {
    return  -1; // the idx in need of removal doesn't exist (it's one index past the list's end)
  }
  prev->next = to_rm->next;
  free(to_rm);
  return 0;
}

/**
 * Works for all but deleting the last node. 
 *
 * It's called a homeaway delete because an interviewer told me about this trick during
 * an interview for HomeAway (that job was cool).
 *
 * return -1 for non-existent index
 */
int ll_del_homeaway(node* ll, int idx) {
  debug("enter homeaway");
  if (idx < 0) {
    return -1;
  }
  node* to_rm = ll_retrieve_node(ll, idx);
  debug("ha got node");
  if (to_rm == NULL) {
    return -1;
  }

  if (extreme_null(to_rm->next)) {
    debug("ha is ext null");
    free(to_rm->next);
    to_rm->next = NULL;
  }
  if (to_rm->next != NULL) {
    debug("ha cur->next is not null");
    to_rm->val = to_rm->next->val;
    node* old_next = to_rm->next; 
    to_rm->next = to_rm->next->next;
    /**
     * Note: bug bait here! I was originally freeing to_rm->next without capturing the old value
     * first, hence I was freeing the wrong node - freeing the one to_rm is supposed to point to
     * and which is actually still in the list, while leaving unfree'd the dangling node that
     * is being taken out of the list's topology.
     */
    free(old_next);
  } else {
    debug("ha cur->next is null, set ext null");
    set_extreme_null(to_rm);
  }
  debug("ha return");
  return 0;
}

void print_ll(node* ll) {
  debug("enter print");
  int result;
  int status;
  int i = 0;
  printf("[");
  status = ll_get(ll, i, &result);
  while (status == 0) {
    char buf[50];
    sprintf(buf, "print loop: %d", i);
    debug(buf);
    if (i > 0) {
      printf(", ");
    }
    printf("%d", result);
    i++;
    status = ll_get(ll, i, &result);
    strcpy(buf, "");
    sprintf(buf, "status: %d", status);
    debug(buf);
  }
  printf("]\n");
  debug("exit print");
}

void demo_ll() {
  printf("\n\nDemo of LL\n");

  node* n = create_node(7);
  printf("Created node, value %d\n", n->val);

  node* ll = create_ll();
  // 1, 2, 4, 8, 16, 32...
  int power = 1;
  for (int i = 0; i < 6; i++) {
    ll_add(ll, power);
    power = power << 1;
  }
  printf("Populated linked list: \n");
  print_ll(ll);

  int result;
  int status;
  int non_existent_idx = 6;
  status = ll_get(ll, non_existent_idx, &result);
  if (status < 0) {
    printf("Task failed successfully: couldn't get index=%d, status=%d\n", non_existent_idx, status);
  } else {
    printf("Problem! Shouldn't have succeeded.\n");
  }

  printf("Delete idx = 3...\n");
  status = ll_del(ll, 3);
  if (status < 0) {
    printf("Failed to delete");
  }
  print_ll(ll);
  
  printf("Delete too-large index 99\n");
  status = ll_del(ll, 99);
  if (status < 0) {
    printf("Successful: Failed to delete\n");
  } else {
    printf("Something went wrong: this delete should have failed\n");
  }
  print_ll(ll);


  printf("Added another number...\n");
  ll_add(ll, 7);
  print_ll(ll);

  printf("And do a homeaway style deletion, idx = 4\n");
  status = ll_del_homeaway(ll, 4);
  if (status < 0) {
    printf("Failed to delete");
  }
  print_ll(ll);
  printf("Try another homeaway delete for last index (4 again)\n");
  status = ll_del_homeaway(ll, 4);
  print_ll(ll);

  printf("(Homeaway version) Delete too-large index 99\n");
  status = ll_del_homeaway(ll, 99);
  if (status < 0) {
    printf("Successful: Failed to delete\n");
  } else {
    printf("Something went wrong: this delete should have failed\n");
  }
  print_ll(ll);


  printf("But now delete from the middle again, idx=2\n");
  ll_del_homeaway(ll, 2);
  print_ll(ll);
  free_list(ll);

  printf("Done\n");

}



void debug_mem(node* n) {
  unsigned char* ptr = (unsigned char*)n;
  for(size_t i = 0; i < sizeof(node); i++) {
    /**
     * 0 - flag for zeropadding up to minwidth
     * 2 - the minwidth
     * x - hex (inherently unsigned, no need for u specifier)
     */
    printf("%02x ", ptr[i]);
  }
  printf("\n");
}

void demo_extreme_nulls() {
  printf("\n\nDemoing extreme nulls!\n");
  node* ptr = create_node(9);
  printf("Before set\n");
  debug_mem(ptr);
  printf("Is extreme? %d\n", extreme_null(ptr));

  set_extreme_null(ptr);
  printf("After set\n");
  debug_mem(ptr);
  printf("Is extreme? %d\n", extreme_null(ptr));
  free_list(ptr);
}


int do_demos() {
  demo_extreme_nulls();
  demo_ll();
  return 0;
}

// int main() {
//   do_demos();
//   return 0;
// }
