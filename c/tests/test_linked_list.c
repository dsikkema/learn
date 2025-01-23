#include "unity/unity.h"
#include "linked_list.h"


void setUp(void) {}
void tearDown(void) {}

static int (*current_delete)(node*, int);

void test_delete_first_node(void) {
   node* list = create_ll();
   ll_add(list, 10);
   ll_add(list, 20);
   
   TEST_ASSERT_EQUAL_INT(0, current_delete(list, 0));
   
   int result;
   TEST_ASSERT_EQUAL_INT(0, ll_get(list, 0, &result));
   TEST_ASSERT_EQUAL_INT(20, result);
   TEST_ASSERT_EQUAL_INT(-1, ll_get(list, 1, &result));
}

void test_delete_middle_node(void) {
   node* list = create_ll();
   ll_add(list, 10);
   ll_add(list, 20);
   ll_add(list, 30);
   
   TEST_ASSERT_EQUAL_INT(0, current_delete(list, 1));
   
   int result;
   TEST_ASSERT_EQUAL_INT(0, ll_get(list, 0, &result));
   TEST_ASSERT_EQUAL_INT(10, result);
   TEST_ASSERT_EQUAL_INT(0, ll_get(list, 1, &result));
   TEST_ASSERT_EQUAL_INT(30, result);
}

void test_delete_last_node(void) {
   node* list = create_ll();
   ll_add(list, 10);
   ll_add(list, 20);
   
   TEST_ASSERT_EQUAL_INT(0, current_delete(list, 1));
   
   int result;
   TEST_ASSERT_EQUAL_INT(0, ll_get(list, 0, &result));
   TEST_ASSERT_EQUAL_INT(10, result);
   TEST_ASSERT_EQUAL_INT(-1, ll_get(list, 1, &result));
}

void test_multi_add_and_delete(void) {
   node* list = create_ll();

   // add to list...
   ll_add(list, 10);
   ll_add(list, 20);
   int result;

   // get them...
   TEST_ASSERT_EQUAL_INT(0, ll_get(list, 0, &result));
   TEST_ASSERT_EQUAL_INT(10, result);
   TEST_ASSERT_EQUAL_INT(0, ll_get(list, 1, &result));
   TEST_ASSERT_EQUAL_INT(20, result);
   
   // delete it out...
   TEST_ASSERT_EQUAL_INT(0, current_delete(list, 1));
   // while still getting something when there's just 1 node left...
   TEST_ASSERT_EQUAL_INT(0, ll_get(list, 0, &result));
   TEST_ASSERT_EQUAL_INT(10, result);
   // finish emptying it
   TEST_ASSERT_EQUAL_INT(0, current_delete(list, 0));

   // try to get things that don't exist..
   TEST_ASSERT_EQUAL_INT(-1, ll_get(list, 0, &result));
   TEST_ASSERT_EQUAL_INT(-1, ll_get(list, 1, &result));
   TEST_ASSERT_EQUAL_INT(-1, ll_get(list, 2, &result));

   // delete what doesn't exist...
   TEST_ASSERT_EQUAL_INT(-1, current_delete(list, 0));
   TEST_ASSERT_EQUAL_INT(-1, current_delete(list, 1));
   TEST_ASSERT_EQUAL_INT(-1, current_delete(list, 2));
}

void test_empty_list(void) {
   node* list = create_ll();
   int result;
   TEST_ASSERT_EQUAL_INT(-2, ll_get(list, -1, &result));
   TEST_ASSERT_EQUAL_INT(-1, ll_get(list, 0, &result));
   TEST_ASSERT_EQUAL_INT(-1, ll_get(list, 1, &result));
}

void test_add_after_deletion(void) {
   node* list = create_ll();
   ll_add(list, 10);
   ll_add(list, 20);
   
   current_delete(list, 1);
   ll_add(list, 30);
   
   int result;
   TEST_ASSERT_EQUAL_INT(0, ll_get(list, 0, &result));
   TEST_ASSERT_EQUAL_INT(10, result);
   TEST_ASSERT_EQUAL_INT(0, ll_get(list, 1, &result));
   TEST_ASSERT_EQUAL_INT(30, result);
}

void test_invalid_indices(void) {
   node* list = create_ll();
   ll_add(list, 10);
   
   int result;
   TEST_ASSERT_EQUAL_INT(-2, ll_get(list, -1, &result));
   TEST_ASSERT_EQUAL_INT(-1, ll_get(list, 1, &result));
   TEST_ASSERT_EQUAL_INT(-1, current_delete(list, 1));
   TEST_ASSERT_EQUAL_INT(-1, current_delete(list, -1));
}

int main(void) {
   UNITY_BEGIN();
   
   RUN_TEST(test_empty_list);
   
   printf("\nTesting with standard delete:\n");
   current_delete = ll_del;
   RUN_TEST(test_delete_first_node);
   RUN_TEST(test_delete_middle_node);
   RUN_TEST(test_delete_last_node);
   RUN_TEST(test_multi_add_and_delete);
   RUN_TEST(test_add_after_deletion);
   RUN_TEST(test_invalid_indices);
   
   printf("\nTesting with homeaway delete:\n");
   current_delete = ll_del_homeaway;
   RUN_TEST(test_delete_first_node);
   RUN_TEST(test_delete_middle_node);
   RUN_TEST(test_delete_last_node);
   RUN_TEST(test_multi_add_and_delete);
   RUN_TEST(test_add_after_deletion);
   RUN_TEST(test_invalid_indices);
   
   return UNITY_END();
}
