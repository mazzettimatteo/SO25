#!/bin/bash
# ================================================================
# Dimostrazione completa della toolchain di compilazione in C
# Preprocessore → Compilatore → Ottimizzatore → Assemblatore → Linker
# ================================================================

echo "== Compilazione e esecuzione base =="
cat > hello_world.c <<'EOF'
#include <stdio.h>
int main() {
    printf("Hello, world!\n");
    return 0;
}
EOF

gcc -o hello_world hello_world.c
./hello_world

echo
echo "== Mostriamo i passi che gcc esegue internamente (modalità verbose) =="
gcc -v -o hello_world hello_world.c

echo
echo "== Preprocessore: -E genera l'output preprocessato su stdout =="
gcc -E hello_world.c | head -20   # mostra solo le prime righe

echo
echo "== Compilatore: -S genera il codice assembler =="
gcc -S hello_world.c
echo "--- Contenuto di hello_world.s ---"
head -20 hello_world.s

echo
echo "== Assemblatore: -c genera il file oggetto (no linking) =="
gcc -c hello_world.c
file hello_world.o

echo
echo "== Linker: creiamo l'eseguibile a partire dal file oggetto =="
gcc hello_world.o -o hello_world_linked
./hello_world_linked

# ---------------------------------------------------------------
# ESEMPIO MINIMALE SENZA I/O
# ---------------------------------------------------------------
echo
echo "== Programma minimale che restituisce 42 =="
cat > 42.c <<'EOF'
int main() {
    return 42;
}
EOF

gcc -o 42 42.c
./42
echo "Codice di uscita: $?"

# ---------------------------------------------------------------
# LOOP OTTIMIZZABILE
# ---------------------------------------------------------------
echo
echo "== Aggiungiamo un loop inutile =="
cat > 42.c <<'EOF'
int main() {
    int i;
    for (i = 0; i < 1000000000; i++)
        ;
    return 42;
}
EOF

echo "Compilo senza ottimizzazione (il loop resta)"
gcc -o 42 42.c
time ./42

echo
echo "Compilo con ottimizzazione -O2 (il loop sparisce)"
gcc -O2 -o 42 42.c
time ./42

echo
echo "== Verifica nell'assembly (loop sparito) =="
gcc -O2 -S 42.c
grep -A5 main 42.s

echo
echo "== Manteniamo il loop con 'volatile' =="
cat > 42.c <<'EOF'
int main() {
    volatile int i;
    for (i = 0; i < 1000000000; i++)
        ;
    return 42;
}
EOF
gcc -O2 -S 42.c
grep -A5 main 42.s

# ---------------------------------------------------------------
# LIBRERIA C E STATIC LINKING
# ---------------------------------------------------------------
echo
echo "== Compilazione statica: includiamo la libc dentro l'eseguibile =="
gcc -static 42.c
ls -lh a.out
echo "Controllo simboli in a.out:"
nm a.out | head -20

# ---------------------------------------------------------------
# COMPILAZIONE E LINKING “A MANO”
# ---------------------------------------------------------------
echo
echo "== Tentiamo di linkare manualmente (manca _start) =="
gcc -c 42.c
ld 42.o || echo "(manca _start!)"

echo
echo "== Creiamo un piccolo startup crt0r.S in assembly =="
cat > crt0r.S <<'EOF'
.text
.globl _start
_start:
    xor %ebp, %ebp
    mov (%rsp), %edi
    lea 8(%rsp), %rsi
    lea 16(%rsp,%rdi,8), %rdx
    xor %eax, %eax
    call main
    mov %eax, %edi
    mov $60, %eax
    syscall
EOF

as -o crt0r.o crt0r.S
ld -o a.out crt0r.o 42.o
./a.out
echo "Codice di uscita: $?"

# ---------------------------------------------------------------
# SYS CALL DIRETTE: niente libc
# ---------------------------------------------------------------
echo
echo "== Programma che usa solo syscall dirette (hw6.c) =="
cat > hw6.c <<'EOF'
long mystrlen(char *s) {
    long len;
    for (len = 0; *s != 0; len++)
        s++;
    return len;
}

long mywrite(char *s) {
    long addr = (long) s;
    long len = mystrlen(s);
    register long r_syscallno asm("rax") = 1;
    register long r_arg1 asm("rdi") = 1;
    register long r_arg2 asm("rsi") = addr;
    register long r_arg3 asm("rdx") = len;
    register long r_retvalue asm("rax");
    asm("syscall");
    return r_retvalue;
}

void myexit(long value) {
    register long r_syscallno asm("rax") = 60;
    register long r_arg1 asm("rdi") = value;
    asm("syscall");
}

void _start(void) {
    long retvalue;
    retvalue = mywrite("hello world\n");
    myexit(retvalue);
}
EOF

gcc -c hw6.c
ld hw6.o
./a.out
echo "Codice di uscita: $?"

# ---------------------------------------------------------------
# MICROCONTROLLER AVR
# ---------------------------------------------------------------
echo
echo "== Esempio finale: accesso diretto all’hardware (noSO.c) =="
cat > noSO.c <<'EOF'
typedef unsigned char uint8_t;
#define DDRC (*(volatile uint8_t *) 0x27)
#define PORTC (*(volatile uint8_t *) 0x28)

int main(void) {
    volatile int i;
    DDRC |= 1 << 5;
    for (;;) {
        for (i = 0; i < 32767; i++)
            ;
        PORTC ^= 1 << 5;
    }
}
EOF

echo "Se lo compili per Linux, fallirà:"
gcc noSO.c && ./a.out || echo "(Segmentation fault previsto)"

echo
echo "Compilazione per microcontrollore AVR (richiede avr-gcc):"
echo "  avr-gcc -mmcu=atmega168 -Os -o noSO noSO.c"
echo "  avr-objcopy -O ihex noSO noSO.hex"
echo "  avrdude -p m168 -c stk500v2 -P /dev/ttyUSB0 -U flash:w:noSO.hex"
echo "Caricare il firmware su un ATmega168 per far lampeggiare un LED."
# ================================================================
echo
echo "== Fine dimostrazione =="
# ================================================================
