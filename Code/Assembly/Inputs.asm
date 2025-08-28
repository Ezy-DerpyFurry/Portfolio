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

    Math_input db "Math"
    len_Math_input equ $ - Math_input

    msg_math db "Please enter number: "
    len_msg_math equ $ - msg_math

    msg_HI db "Hello!",10
    len_msg_HI equ $ - msg_HI

    Inncorrect db "Inncorrect",10
    len_Inncorrect equ $ - Inncorrect

    buf times 32 db 0
    buflen equ $ - buf

    math_buf times 32 db 0
    math_buf_len equ $ - math_buf

    math_buf2 times 32 db 0
    math_buf2_len equ $ - math_buf2

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
    jne .check_math

    inc rsi
    inc rdi
    dec rcx
    jmp .compare_quit

.check_math:
    mov rsi, buf
    mov rdi, Math_input
    mov rcx, len_Math_input
    jmp .compare_math

.compare_math:
    test rcx, rcx
    jz .mathloop

    mov al, [rsi]
    mov bl, [rdi]
    cmp al, bl
    jne .inncorrectA

    inc rsi
    inc rdi
    dec rcx
    jmp .compare_math

.mathloop:
    mov rsi, msg_math
    mov rdx, len_msg_math
    call print

    mov rsi, math_buf
    mov rdx, math_buf_len
    call read

    mov rsi, msg_math
    mov rdx, len_msg_math
    call print

    mov rsi, math_buf2
    mov rdx, math_buf2_len
    call read

    ; I don't know assembly math yet :<

    jmp loop_

.correctHi:
    mov rsi, msg_HI
    mov rdx, len_msg_HI
    call print
    jmp loop_

.correctQuit:
    jmp .done

.inncorrectA:
    mov rsi, Inncorrect
    mov rdx, len_Inncorrect
    call print
    jmp loop_

.done:
    mov rsi, msg_quit
    mov rdx, len_msg_quit
    call print

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
