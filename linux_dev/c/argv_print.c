#include <stdio.h>

int main(int argc, char* argv[]) {
    printf("Argument count: %d\n", argc);
    while (*argv) { // null terminated array
        printf("%s\n", *(argv)); // starts by printing the 0th arg: the command used to invoke the program (e.g. target/argv_print)
        argv++; // yes, this can go directly in the line above
    }
} 
