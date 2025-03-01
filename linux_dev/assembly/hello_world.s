.global _start

.text

_start:
    mov x8, #64             // 64: write syscall
    mov x0, #1              // file descriptor (1: stdout)
    adr x1, hello_str       // data address
    mov x2, #13             // buffer len, len(hello_str) == 13
    svc #0
    
    mov x0, #0              // Start exiting
    mov x8, #93
    svc #0

.data

hello_str:
    .ascii "Hello, world\n"
