; This file is an 

global _start

section .text

_start:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg1
    mov rdx, msglen1
    syscall

    mov rax, 1
    mov rdi, 1
    mov rsi, msg2
    mov rdx, msglen2
    syscall

    mov rax, 60
    mov rdi, 0
    syscall

section .rodata
    msg1: db "Goodbye, Mars!", 10
    msglen1: equ $ - msg1

    msg2: db "Hello, world!", 10
    msglen2: equ $ - msg2