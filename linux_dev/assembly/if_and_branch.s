.global _start
func:
    mov x1, #5
    mov x2, #20
    add x0, x1, x2
    mov x8, #93     // 93 == 'exit' syscall
    svc #0          // exit, sum in status
_start:
    mov x1, #3      // x1 <- literal 3
    mov x2, #4      // x2 <- literal 4
    cmp x1, x2      // if not equal, then branch to func
    bne func

