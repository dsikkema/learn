.global _start

.text

_start:
    mov x8, #64             // 64: write syscall
    mov x0, #1              // file descriptor (1: stdout)
    adr x1, hello_str       // data address
    mov x2, #1              // buffer len of 1

begin_loop:
    ldr w3, [x1]
    cmp w3, 0x00
    beq end_loop
    svc #0
    add x1, x1, #1          // increment mem ctr
    b begin_loop

end_loop:

mov x0, #0              // Start exiting
mov x8, #93
svc #0

.data

hello_str:
    .asciz "Hello, World\n"
