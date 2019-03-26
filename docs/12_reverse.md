# reverse: `ayeayepatch/`

The page contains a function named  `check` written in x86_64 assembly.

![Screenshot of the reverse puzzle](images/12_reverse.png)

The goal is to reverse engineer it and guess what input will make it return
`true`.

```nasm
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

    cmp edx, 17
    je .after_inv_len

    .ret_false:
    xor eax, eax
    ret

    .after_inv_len:
    lea rax, [rdi - 1 + rcx]
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
    mov dl, [rdi + rax]
    xor dl, [rel key + rax]
    cmp dl, [rel strx + rax]
    jne .ret_false
    add rax, 1
    cmp rax, 17
    jne .pw_loop

    mov eax, 1
    ret

strx:
    db 0xb0, 0xb5, 0x53, 0x01, 0xd9, 0x25, 0xce, 0xab, 0x26, 0x97, 0xa5, 0x92, 0x78, 0x14, 0xf2, 0x27, 0x13
key:
    db 0x9f, 0xd0, 0x27, 0x60, 0xab, 0x4c, 0xbe, 0xcf, 0x43, 0xe7, 0xd0, 0xe0, 0x1c, 0x75, 0x87, 0x56, 0x3c
```

Short analysis of the code:

* The first part, after `.len_calc` label, checks if the input length is 17
* `.after_inv_len` checks if the computed length is equal to 1 (which of course
  is never true at that moment), and if so, skips the next step
* `.rev_loop` is responsible for reversing the input string
* `.check_pw` XORs the string with corresponding bytes from `key` and checks
  if they are equal to `strx`

Since XOR is reversible (using XOR), getting the valid password is as easy
as XORing the `strx` and `key` arrays and reversing the output. An example of
how to do this using Python:

```python
>>> strx = 0xb0, 0xb5, 0x53, 0x01, 0xd9, 0x25, 0xce, 0xab, 0x26, 0x97, 0xa5, 0x92, 0x78, 0x14, 0xf2, 0x27, 0x13
>>> key = 0x9f, 0xd0, 0x27, 0x60, 0xab, 0x4c, 0xbe, 0xcf, 0x43, 0xe7, 0xd0, 0xe0, 0x1c, 0x75, 0x87, 0x56, 0x3c
>>> ''.join(chr(x ^ y) for x, y in zip(strx, key))[::-1]
'/quadrupedpirate/'
```
