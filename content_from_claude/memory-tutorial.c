#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Let's create a simple structure to work with
struct Person {
    char* name;
    int age;
};

// Function to demonstrate proper memory allocation and deallocation
struct Person* create_person(const char* name, int age) {
    // malloc returns a void pointer that we cast to our desired type
    // sizeof(struct Person) calculates the exact size needed for our structure
    struct Person* person = (struct Person*)malloc(sizeof(struct Person));
    
    if (person == NULL) {
        // Always check if malloc succeeded
        printf("Memory allocation failed!\n");
        return NULL;
    }

    // Now we need to allocate memory for the name string
    // strlen() + 1 accounts for the null terminator
    person->name = (char*)malloc(strlen(name) + 1);
    
    if (person->name == NULL) {
        // If second malloc fails, we need to free the first allocation
        // This prevents memory leaks
        free(person);
        printf("Memory allocation failed for name!\n");
        return NULL;
    }

    // strcpy is used to copy the string into our allocated memory
    strcpy(person->name, name);
    person->age = age;

    return person;
}

// Function to free all allocated memory for a person
void free_person(struct Person* person) {
    if (person != NULL) {
        // Free the name first (inner allocation)
        free(person->name);
        // Then free the structure itself
        free(person);
    }
}

// Function to demonstrate common memory mistakes
void memory_mistakes(void) {
    // Mistake 1: Using memory after freeing it (use-after-free)
    printf("\nMistake 1: Use after free\n");
    int* numbers = (int*)malloc(sizeof(int) * 3);
    numbers[0] = 1;
    free(numbers);
    // BAD: numbers[0] = 2; // This could crash or cause undefined behavior
    
    // Mistake 2: Double free
    printf("Mistake 2: Double free\n");
    int* more_numbers = (int*)malloc(sizeof(int) * 3);
    free(more_numbers);
    // BAD: free(more_numbers); // This would cause a double-free error
    
    // Mistake 3: Memory leak (forgetting to free)
    printf("Mistake 3: Memory leak\n");
    int* leaked = (int*)malloc(sizeof(int) * 100);
    // Program ends without freeing 'leaked' - memory is lost until program ends
}

int main() {
    // Create a person with proper memory management
    struct Person* alice = create_person("Alice", 30);
    if (alice != NULL) {
        printf("Created person: %s, age %d\n", alice->name, alice->age);
    }

    // Demonstrate memory mistakes
    memory_mistakes();

    // Proper cleanup
    free_person(alice);

    // Let's also demonstrate realloc
    printf("\nDemonstrating realloc:\n");
    int* array = (int*)malloc(sizeof(int) * 3);
    for (int i = 0; i < 3; i++) {
        array[i] = i + 1;
    }

    // Resize the array to be larger
    // realloc preserves existing data and adds more space
    int* new_array = (int*)realloc(array, sizeof(int) * 5);
    if (new_array != NULL) {
        array = new_array;  // If realloc succeeds, update our pointer
        array[3] = 4;
        array[4] = 5;
        
        for (int i = 0; i < 5; i++) {
            printf("%d ", array[i]);
        }
        printf("\n");
    }

    free(array);  // Don't forget to free the reallocated memory
    return 0;
}
