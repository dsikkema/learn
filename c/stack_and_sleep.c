#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>


void demonstrateStack() {
  printf("\ndemonstrateStack()\n");
  int num = 7;
  char arr[4];
  // It's common to see the stack addresses decrease as more vars are declared. "Growing downward."
  printf("stack var address: %p\n", &num);
  printf("stack var address: %p\n", &arr);
}
int main() {
  demonstrateStack();
  printf("\nmain var printing:()\n");
  int num = 7;
  char arr[4] = "lmao";
  long another_num = 77;

  // Yes I opened another terminal tab, ran ipython, and counted the length of the
  // string. What about it? Everyone knows C is written in Python anyway.
  //
  // Update (several minutes later). This was a bad idea. Python said the length
  // was 1406. C says the length is 1413. Life comes at you fast, but in C, it 
  // comes at you even faster.
  char to_be[1413] = "To be, or not to be, that is the question:\nWhether 'tis nobler in the mind to suffer\nThe slings and arrows of outrageous fortune,\nOr to take arms against a sea of troubles\nAnd by opposing end them. To die—to sleep,\nNo more; and by a sleep to say we end\nThe heart-ache and the thousand natural shocks\nThat flesh is heir to: 'tis a consummation\nDevoutly to be wish'd. To die, to sleep;\nTo sleep, perchance to dream—ay, there's the rub:\nFor in that sleep of death what dreams may come,\nWhen we have shuffled off this mortal coil,\nMust give us pause—there's the respect\nThat makes calamity of so long life.\nFor who would bear the whips and scorns of time,\nTh'oppressor's wrong, the proud man's contumely,\nThe pangs of dispriz'd love, the law's delay,\nThe insolence of office, and the spurns\nThat patient merit of th'unworthy takes,\nWhen he himself might his quietus make\nWith a bare bodkin? Who would fardels bear,\nTo grunt and sweat under a weary life,\nBut that the dread of something after death,\nThe undiscovere'd country, from whose bourn\nNo traveller returns, puzzles the will,\nAnd makes us rather bear those ills we have\nThan fly to others that we know not of?\nThus conscience doth make cowards of us all,\nAnd thus the native hue of resolution\nIs sicklied o'er with the pale cast of thought,\nAnd enterprises of great pith and moment\nWith this regard their currents turn awry\nAnd lose the name of action.\n";
  long yet_another_num = 77;
  printf("stack var address: %p\n", &num);
  printf("stack var address: %p\n", &arr);
  demonstrateStack();

  // lol is a pointer I'll use to scan the stack outside the range of the starting point array
  void* lol = &arr;

  /**
   * This loop will print some of the Prince of Denmark's sad soliloquy. But before and after 
   * doing so, it will spatter junk onto the terminal, because we're scanning other memory
   * that wasn't "meant" to be interpretted as character data.
   */
  for (int i=-100; i<2000; i++) {
    // Following line also works (even with the negative indexes)
    // printf("%c", ((char*)lol)[i]);

    // May be necessary to flush stdout buffer before sleep, because sleep
    // will prevent buffer from being flushed, or something, until
    // "enough" has been printed
    //
    // Problem does not always reproduce.
    fflush(stdout);

    // usleep takes microseconds as an arg. Comes from unistd.h
    usleep(1000 * 1);
    printf("%c", *(char*)(lol + i));
  }
}
