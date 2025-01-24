#include "unity/unity.h"
#include "linked_list.h"
#include "hash_table.h"
#include <stdlib.h>

node** map;

void setUp(void) {
  map = create_hashmap();
}
void tearDown(void) {
  free(map);
}

/**
 * This is structured as one test because I like testing the data structure
 * by doing lots of operations in sequence and in different combinations.
 * I'm more likely to find an edge case by deleting something both before and
 * after lots of other operations have caused many internal changes to the
 * internal structure of the hashmap.
 */
void test_set_get(void) {
  int k=1, v=11;
  m_set(map, k, v);
  int result;

  // initial set
  m_get(map, k, &result);
  TEST_ASSERT_EQUAL_INT(v, result);

  // reset
  m_set(map, k, 111);
  m_get(map, k, &result);
  TEST_ASSERT_EQUAL_INT(111, result);

  // unset
  int status;
  TEST_ASSERT_EQUAL_INT(0, m_unset(map, k));
  TEST_ASSERT_EQUAL_INT(-1, m_get(map, k, &result));

  // set a bunch...
  int n_entries=100000;
  for (int i=0; i<n_entries; i++) {
    //printf("test set i=%d\n", i);
    m_set(map, i, i*1000);
  }

  // check they're all set...
  for (int i=0; i<n_entries; i++) {
    //printf("test get i=%d\n", i);
    char msg[100];
    snprintf(msg, sizeof(msg), "i=%d", i);
    /**
     * Note: custom assertion messages here, very good
     */
    TEST_ASSERT_EQUAL_INT_MESSAGE(0, m_get(map, i, &result), msg);
    TEST_ASSERT_EQUAL_INT_MESSAGE(i*1000, result, msg);
  }

  // unset a bunch (odd indexes)...
  for (int i=1; i<n_entries; i += 2) {
    TEST_ASSERT_EQUAL_INT(0, m_unset(map, i));
  }
  
  // verify they're gone...
  for (int i=1; i<n_entries; i += 2) {
    TEST_ASSERT_EQUAL_INT(-1, m_get(map, i, &result));
  }

  // the rest remain (even indexes)
  for (int i=0; i<n_entries; i += 2) {
    TEST_ASSERT_EQUAL_INT(0, m_get(map, i, &result));
  }

  // reset the remaining...
  for (int i=0; i<n_entries; i += 2) {
    m_set(map, i, i*2);
  }

  // the removed ones are still gone
  for (int i=1; i<n_entries; i += 2) {
    TEST_ASSERT_EQUAL_INT(-1, m_get(map, i, &result));
  }

  // but the reset ones are still reset
  for (int i=0; i<n_entries; i += 2) {
    TEST_ASSERT_EQUAL_INT(0, m_get(map, i, &result));
    TEST_ASSERT_EQUAL_INT(i*2, result);
  }
}

int main(void) {
  UNITY_BEGIN();
   
  RUN_TEST(test_set_get);
   
  return UNITY_END();
}
