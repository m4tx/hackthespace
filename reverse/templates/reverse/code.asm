BITS        64
SECTION     .text
GLOBAL      check:function

check:
    xor eax, eax
    .len_calc:
    mov edx, eax
    mov rcx, rax
    add rax, 1
    cmp BYTE [rdi - 1 + rax], 0
    jne .len_calc

    cmp edx, {{ encoded_url|length }}
    je .after_inv_len

    .ret_false:
    xor eax, eax
    ret

    .after_inv_len:
    lea rax, [rdi-1+rcx]
    mov rdx, rdi
    cmp rdi, rax
    jnb .check_pw

    .rev_loop:
    mov cl, [rdx]
    mov sil, [rax]
    inc rdx
    dec rax
    mov [rdx - 1], sil
    mov [rax + 1], cl
    cmp rdx, rax
    jb .rev_loop

    .check_pw:
    xor eax, eax
    .pw_loop:
    mov dl, [rdi+rax]
    xor dl, [rel key + rax]
    cmp dl, [rel strx + rax]
    jne .ret_false
    add rax, 1
    cmp rax, {{ encoded_url|length }}
    jne .pw_loop

    mov eax, 1
    ret

strx:
    db {% load hexlist %}{{ encoded_url|hexlist }}
key:
    db {{ key|hexlist }}
