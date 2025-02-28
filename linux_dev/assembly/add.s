.global _start
_start:
    mov x1, #3      // x1 <- literal 3
    mov x2, #4      // x2 <- literal 4

    // when the program exits, the value inside register 0 is the exit code. This program returns the sum in its
    // exit code.
    // ./assemble_link_run.sh add.s
    // Exited with code: 7
    add x0, x1, x2  // x0 <- x1 + x2

    // to do a syscall: put syscall number into register 8...
    mov x8, #93     // 93 == 'exit' syscall
    // then the 'svc' instruction, given argument 0, surrenders control to the kernel so it can execute syscall
    svc #0
