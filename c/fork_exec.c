#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/syscall.h>

int demo_fork() {
  printf("\nDemoing fork:\n\n");
  pid_t pid = fork();

  if (pid < 0) {
      perror("Fork failed");
  } else if (pid == 0) {
    printf("Child: pid=%d\n", getpid());
    execl("/bin/ls", "ls", "-l", NULL); // if I put -lzzz as the third arg, it will exit status 256, printed by parent proc.
    perror("execl failed");
    exit(1);
  } else {
    printf("Parent: pid=%d, child_pid=%d\n", getpid(), pid);
    int _unused;
    int status;
    wait(&status); // this works because wait() will wait until the child is finished, and populate its exit status
                   // into the memory address given as a pass by ref.
    printf("Child process finished, status=%d\n", status);
  }

  return 0;
}

void demo_syscall() {
  printf("\nDemo syscall:\n\n");
  pid_t pid = syscall(SYS_getpid);
  printf("PIDs: direct syscall = %d, lib = %d", pid, getpid());
}

int main() {
  demo_fork();
  demo_syscall();
}
