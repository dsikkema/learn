#ifndef HASH_TBL_H
#define HASH_TBL_H
#include "linked_list.h"

void m_set(node**, int, int);
int m_get(node** map, int, int*);
int m_unset(node**, int);
node** create_hashmap();
#endif
