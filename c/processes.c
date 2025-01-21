#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
// #include <signal.h>

void signal_handler(int signum) {
  printf("\nCaught signal %d\n", signum);
  exit(0);
}

int main() {
  signal(SIGINT, signal_handler);
  printf("My PID is %d. Press ctrl+c to exit...\n", getpid()); // getpid in unistd
  while(1) {
    sleep(1); // sleep in unistd
  }

  return 0;
}
