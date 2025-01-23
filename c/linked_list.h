#ifndef LINKED_LIST_H
#define LINKED_LIST_H


typedef struct node { 
  struct node* next;
  int val;
} node;

node* create_node(int val);

node* create_ll();


void ll_add(node* ll, int val);


int ll_get(node* ll, int idx, int* result);


int ll_del(node* ll, int idx);


int ll_del_homeaway(node* ll, int idx);
#endif
