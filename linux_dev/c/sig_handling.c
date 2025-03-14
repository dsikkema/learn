#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <time.h>
#include <string.h>

// for reference tutorial: https://claude.ai/chat/0f947089-7e85-4cb1-8974-d484f1c65aba

/**
 * volatile keyword: prevent compiler optimizations around a var. Needed for when hardware, another
 * thread, or a signal handler (my case) uses that variable.
 */
volatile sig_atomic_t signal_recv = 0;
volatile sig_atomic_t signal_ct = 0;

/**
 * A callback that gets registered, so to speak
 */
void signal_handler(int sig) {
    signal_recv = sig;
    signal_ct++;
}


int main() {
    struct sigaction act;

    act.sa_handler = signal_handler;
    // "A global signal mask defines the set of signals currently blocked from delivery to a process."
    // Seems to handle the case where, if a signal is being handled, this mask makes sure the same signal
    // cannot be processed until it finishes being handled the first time.
    sigemptyset(&act.sa_mask);

    // settings configurable in these bit-flags
    act.sa_flags = 0;

    // the third argument is oact, a reference that if given as non-zero, is also a sigaction struct meant to now return
    // to the user the previous signal handling action that was in place before registering the new one, &act.
    sigaction(SIGINT, &act, NULL); 
    sigaction(SIGTERM, &act, NULL); 
    sigaction(SIGUSR1, &act, NULL); 

    /**
     * Instructions
     */
    int pid = getpid();
    printf("Process ID: %d\n", pid);
    printf("In another terminal, run the following to see signal handling in this process:\n");
    printf("  kill -SIGINT %d (equivalent to ctrl+c)\n", pid);
    printf("  kill -SIGTERM %d \n", pid);
    printf("  kill -SIGUSR1 %d\n", pid);
    printf("\nTo actually kill the process, can send SIGKILL (unhandlable) or SIGQUIT (simply not handled)\n");
    printf("(\"SIG\" prefix optional: e.g., SIGINT, INT, and the signal number (2) are interchangeable)\n");
    printf("Running... Press Ctrl+c or send signals to interact\n");
    printf("Ctrl+\\ to quite (sends SIGQUIT)\n");

    char* signame;
    time_t start_time = time(NULL);
    while (1) {
        if (signal_recv) {
            time_t current_time = time(NULL);

            switch (signal_recv) {
                case SIGINT:
                    signame = strdup("SIGINT");
                    break;
                case SIGTERM:
                    signame = strdup("SIGINT");
                    break;
                case SIGUSR1:
                    signame = strdup("SIGINT");
                    break;
                default:
                    printf("Error: unknown signal handled, %d", signal_recv);
                    exit(-1);
            }

            printf("\n[%ld seconds elapsed] Received signal %d (%s), count: %d\n",
                current_time - start_time,
                signal_recv,
                signame,
                signal_ct
            );

            signal_recv = 0;
        }
        printf(".");
        fflush(stdout); // fflush takes a file and flushes it - so even without newline, the dot won't be stuck in buffer but will print.
        sleep(2);
    }
    
}