#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Toodo: make an array of these
typedef struct  {
  char* name;
  int age;
} Person;

void print_person(Person* p) {
  // If you don't provide arguments for the placeholders, it will print.
  // Print... something, that is.
  printf("Name: %s, Age: %d\n", p->name, p->age);
}

Person* create_person(const char* name, int age) {
  Person* person = (Person*)malloc(sizeof(Person));

  if (person == NULL) {
    printf("malloc fail\n");
    return NULL;
  }

  person->name = (char*)malloc(strlen(name) + 1);
  if (person->name == NULL) {
    free(person); // See, a tricky catch here! Need to free previously allocated mem during error
                  // handling
    printf("malloc fail\n");
    return NULL;
  }

  // strcopy(dest, src)
  strcpy(person->name, name);
  person->age = age;
  print_person(person);
  return person;
}

void free_person(Person* person) {
  if (person != NULL) {
    free(person->name);
    free(person);
  }
}

void mistakes_to_avoid() {
  // use after free
  int * numbers = (int*)malloc(sizeof(int) * 3);
  numbers[0] = 1;
  free(numbers);
  numbers[0] = 2;
  printf("numbers[0] after free: %d (anyway, still bad)", numbers[0]);


  //double free
  free(numbers); // already freed above
  
  // memory leak (forget to free)
  int* leaked = (int*)malloc(sizeof(int) * 100);
  // and it just lurks around the atmosphere....
}


int main() {
  Person* person = create_person("Dale", 31);
  print_person(person);
  free_person(person);

  mistakes_to_avoid();

  // also, following loop will eventually get shut down by something (perhaps zsh) for using too much mem
  for (unsigned long i = 0; 1; i++) {
    int* lol = (int*)malloc(1024 * 1024);
    if (lol == NULL) {
      printf("malloc failed");
      break;
    }

    memset(lol, 1, 1024*1024);

    if (i % 1000) {
      printf(".");
    }
  }
  
  return 0;
}

