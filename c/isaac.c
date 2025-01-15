#include <stdio.h>
#include <stdint.h>
#include <stddef.h>

typedef struct dale_struct
{
    uint8_t a_byte;
    uint32_t b_int;
    uint32_t *c_int_ptr;
    uint64_t d_long;
} Dale;

int main()
{
    uint32_t my_array[3] = {1000, 1001, 1002};

    Dale my_dale = {
        1,
        2000,
        my_array,
        3000000000,
    };

    Dale *my_dale_ptr = &my_dale;

    printf(
        "Size: %lu\nOffsets: {\n\ta_byte: %u,\n\tb_int: %u,\n\tc_int_ptr: %u,\n\td_long: %u\n}\n",
        sizeof(Dale),
        offsetof(Dale, a_byte),
        offsetof(Dale, b_int),
        offsetof(Dale, c_int_ptr),
        offsetof(Dale, d_long));

    printf("a_byte: %d == %d\n", my_dale_ptr->a_byte, *((uint8_t *)(((void *)my_dale_ptr) + 0)));
    printf("b_int: %d == %d\n", my_dale_ptr->b_int, *((uint32_t *)(((void *)my_dale_ptr) + 4)));
    printf("c_int_ptr: %p == 0x%llx\n", my_dale_ptr->c_int_ptr, *((uint32_t **)(((void *)my_dale_ptr) + 8)));
    printf("d_long: %llu == %llu\n", my_dale_ptr->d_long, *((uint64_t *)(((void *)my_dale_ptr) + 16)));

    return 0;
}
