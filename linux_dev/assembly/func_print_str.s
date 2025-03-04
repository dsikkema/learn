.global _start

.text

write_null_term_str:
    // x0 arg: "passes" straight to syscall, the file descriptor
    // x1 arg: "passes" straight to syscall x1, the address to write

    mov x8, #64                 // 64: write syscall
    mov x2, #1                  // buffer len of 1
    
    begin_loop:
        ldrb w3, [x1]            // w3 <- memory @ address stored in x1
        cmp w3, 0x0             // stores comparison result (less than, eq, greater than) in a dedicated register
        beq end_loop            // interrogate comparison result and if equal, then jump to end_loop location
        svc #0
        add x1, x1, #1          // increment mem ctr
        b begin_loop
    
    end_loop: 
    ret
    

_start:
    // args for first write_null_term_str call
    mov x0, #1                  // file descriptor (1: stdout)
    adr x1, hello_str           // data address
    bl write_null_term_str
    
    // args for second write_null_term_str call
    mov x0, #1                  // file descriptor (1: stdout)
    adr x1, goodbye_str           // data address
    bl write_null_term_str

    mov x0, #0              // Start exiting
    mov x8, #93
    svc #0
.data

hello_str:
    .asciz "Hello, World\n"

lol_str:
    .asciz "lol, this should never be printed (detect bad null checks)\n"


goodbye_str:
    .asciz "It was lovely to meet you\n"

lmao_str:
    .asciz "lmao, another check to make sure null checks work, do not print me.\n"
