section .data
    msg db "Hello, World! (From Assembly)", 0xa
    len equ $ - msg

    input_msg db "Say Hi: "
    len_input_msg equ $ - input_msg

    HI db "Hi"
    len_HI equ $ - HI

    quit db "Quit"
    len_quit equ $ - quit

    msg_quit db "See you later!",10
    len_msg_quit equ $ - msg_quit

    msg_HI db "Hello!",10
    len_msg_HI equ $ - msg_HI

    Inncorrect db "Inncorrect",10
    len_Inncorrect equ $ - Inncorrect

    buf times 32 db 0
    buflen equ $ - buf

section .text
    global _start

_start:
    mov rsi, msg
    mov rdx, len
    call print

loop_:
    mov rsi, input_msg
    mov rdx, len_input_msg
    call print

    mov rsi, buf
    mov rdx, 10
    call read

    dec rax
    mov byte [buf+rax], 0

    mov rsi, buf
    mov rdi, HI
    mov rcx, len_HI

.compare_hi:
    test rcx, rcx
    jz .correctHi

    mov al, [rsi]
    mov bl, [rdi]
    cmp al, bl
    jne .check_quit

    inc rsi
    inc rdi
    dec rcx
    jmp .compare_hi

.check_quit:
    mov rsi, buf
    mov rdi, quit
    mov rcx, len_quit
    jmp .compare_quit

.compare_quit:
    test rcx, rcx
    jz .correctQuit

    mov al, [rsi]
    mov bl, [rdi]
    cmp al, bl
    jne .inncorrectA

    inc rsi
    inc rdi
    dec rcx
    jmp .compare_quit

.correctHi:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg_HI
    mov rdx, len_msg_HI
    syscall
    jmp loop_

.correctQuit:
    jmp .done

.inncorrectA:
    mov rax, 1
    mov rdi, 1
    mov rsi, Inncorrect
    mov rdx, len_Inncorrect
    syscall
    jmp loop_

.done:
    mov rax, 1
    mov rdi, 1
    mov rsi, msg_quit
    mov rdx, len_msg_quit
    syscall

    mov rax, 60
    xor rdi, rdi
    syscall

print:
    mov rax, 1
    mov rdi, 1
    syscall
    ret

read:
    mov rax, 0
    mov rdi, 0
    syscall
    ret
