#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Toodo: make an array of these
typedef struct  {
  char* name;
  int age;
} Person;

void print_person(Person* p) {
  printf("Name: %s, Age: %d\n");
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
  print_person(person);
  print_person(person);
  print_person(person);
  print_person(person);
  print_person(person);
  print_person(person);
  print_person(person);
  return person;
}

void free_person(Person* person) {
  if (person != NULL) {
    free(person->name);
    free(person);
  }
}




int main() {
  Person* person = create_person("Dale", 31);
  print_person(person);
  free_person(person);
  

  return 0;
}
