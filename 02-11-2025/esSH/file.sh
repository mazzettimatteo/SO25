# hello_world.c e' il solito hello world
gcc -o hello_world hello_world.c 
./hello_world
# funziona ...  ma gcc non e' il compilatore, invoca l'intera toolchain
# preprocessore - compilatore - ottimizzatore - assemblatore - linker
# cosi' si vedono i passi
  gcc -v -o hello_world hello_world.c 
# ma i comandi hanno tantissimi parametri non si capisce
# la regola e' che gcc puo' interrompere la catena di tool con un parametro.
# -E esegue solo il preprocessore (e manda l'output in stdout)
  $  gcc -E hello_world.c
# -S genera i ferma dopo il compilatore e l'ottimizzatore, quindi produce assembler
  $  gcc -S hello_world.c
# ecco l'assembler
  $  cat hello_world.s
# -c non chiama il linker quindi genera il file oggetto .o
  $  gcc -c hello_world.c
# cosi' si vedono i tipi dei file
  $  file hello_world*
# per completare il percorso di compilazioone a partire da un risultato intermedio
        basta dare in input un file col suffisso giusto
# questo genera l'eseguibile a partire dal sogente assembler
  $  gcc hello_world.s
# funziona
  $  ./a.out
# cancelliamo a.out
        $  rm a.out
# questo chiama solo in linker:
  $  gcc hello_world.o
  $  ./a.out

######## proviamo a fare a meno della libreria
42.c contiene:
        int main() {
                return 42;
        }
########
  $  gcc -o 42 42.c 
  $  ./42
#funziona ma sembra non far nulla
  $  echo $?
# ecco dove e' finito, viene assegnato a una variabile della shell
# aggiungiamo 2 righe a 42.c
        int main() {
                int i;
                for (i = 0; i< 1000000000; i++)
                        ;
                return 42;
        }

  $  gcc -o 42 42.c 
  $  ./42
# ora aspetta un po'.
  $  gcc -S 42.c
  $  cat 42.s
# si vede nell'assembler il loop di attesa
  $  ls
# chiediamo all'ottimizzatore di eliminare il codice inutile.
  $  gcc -O2 -o 42 42.c 
  $  ./42
# ora e' velocissimo
  $  gcc -O2 -S 42.c 
  $  cat 42.s
#infatti nell'assembler e' sparito il loop
  $  gcc -O2 -S 42.c 
  $  cat 42.s
# se vogliamo che il compilatore mantenga il loop anche ottimizzando il codice dobbiamo
# dire che non puo' fare assunzioni sulla variabile i che puo' essere modificata da agenti
# esterni, fuori dalla portata del codice generato dal compilatore... quindi la variabile i
# deve essere definita: "volatile int i:". Se lo si fa:
  $  gcc -O2 -S 42.c 
  $  cat 42.s
# ora il loop e' rimasto (ma altre parti con codice inutile sarebbero state ottimizzate,
# quindi spetta al programmatore dire al compilatore cosa puo' essere ottimizzato e cosa no.
        $ gcc 42.c
        $ a.out
# l'attesa c'e'
# ora pero' vi faccio vedere che la libreria c'e' anche se non la usiamo.
# compiliamo in modo statico (senza librerie dinamiche)
  $  gcc -static 42.c
        $  ls -l a.out
# gia' la ampiezza del file fa presagire che non c'e' solo un loop e un return.
# con nm si vedono i simboli contenuti
  $  nm a.out
# infatti ce ne sono tanatissimi compresi printf e scanf che non abbiamo utilizzato.
# se proviamo a compilare e linkare "a mano"
  $  gcc -c 42.c
  $  ld 42.o
#l'errore che otteniamo e' che manca "_start". Per Linux il progrmma principale e' _start 
# e non main... la libreria C fra le altre cose implementa uno start che chiama main e
# quando main ritorna il controllo chiama la system call exit (infatti i processi
# non muoiono mai di morte naturale, o vengono uccisi o si suicidano).
# ho preparato un esempio di codice start in assembler:
  $  cat > crt0r.S
# o in altro modo generiamo il file crt0r.S col contenuto seguente
---------------
.text
  
.globl _start

_start: # _start is the entry point known to the linker
        xor %ebp, %ebp            # effectively RBP := 0, mark the end of stack frames
        mov (%rsp), %edi          # get argc from the stack (implicitly zero-extended to 64-bit)
        lea 8(%rsp), %rsi         # take the address of argv from the stack
        lea 16(%rsp,%rdi,8), %rdx # take the address of envp from the stack
        xor %eax, %eax            # per ABI and compatibility with icc
        call main                 # %edi, %rsi, %rdx are the three args (of which first two are C standard) to main

        xor  %rdi, %rdi   # clean rdi
        mov  %eax, %edi   # copy eax to edi (syscall first arg)
        mov  $60, %eax    # exit
        syscall
---------------
# cancelliamo a.out
  $  rm a.out
# usiamo l'assemblatore per generare l'oggetto
  $  as -o crt0r.o crt0r.S
  $  ld -o a.out crt0r.o 42.o
  $  ./a.out
  $  echo $?
# sembra funzionare
#ora la libc non c'e'
  $  nm a.out
# start definisce _start ma ha necessita' (U-ndefined) main
  $  nm crt0r.o 
# e in 42.o c'e' main
  $  nm 42.o
# ora facciamo una prova col file hw6 che contiene:
--------------------
long mystrlen(char *s) {   // lunghezza di una stringa
        long len;
        for (len = 0; *s != 0; len++)
                s++;
        return len;
}

long mywrite(char *s) { //stampa una stringa
        long addr = (long) s; //addr e' l'indirizzo della stringa
        long len = mystrlen(s); // e len e' la lunghezza
        register long r_syscallno asm("rax") = 1; // mette nel registro rax il numero della syscall 1=write
                                                  // l'elenco completo in /usr/include/x86_64-linux-gnu/asm/unistd_64.h
                                                  // mutatis mutandis se usare un'altra architetttura di processore
        register long r_arg1 asm("rdi") = 1;      // da "man 2 write" si vede che il 1' paramentro e' il fd. 1 e' stdout
        register long r_arg2 asm("rsi") = addr;   // secondo parametro l'indirizzo del buffer da mettere in output
        register long r_arg3 asm("rdx") = len;    // terzo parametro e' la lunghezza
        register long r_retvalue asm("rax");      // chiamo r_retvalue il registro rax, dove le syscall mettono il valore di rit.
        asm("syscall");                           // genera la trap per "svegliare" il kernel
        return r_retvalue;                        // restituisco il valore di ritorno
}

void myexit(long value) {                   // termina il chiamante
        register long r_syscallno asm("rax") = 60;  // la ssytem call 60 e' _exit
        register long r_arg1 asm("rdi") = value;   // ed ha un solo parametro: il valore di ritorno
        asm("syscall");
}

void _start(void) {
        long retvalue;
        retvalue = mywrite("hello world\n"); // stampa la famosa stringa
        myexit(retvalue);                    // e resituisci come exit status il valore di ritorno della write
                                             // e' il numero dei caratteri stampati (o il codice di erroe in negativo).
}
  $  gcc -c hw6.c
  $  ld hw6.o
# ora non e' servito nulla
  $  ./a.out
  $  echo $?
# e funziona

# ora facciamo un altro esperimento. scriviamo questo programma che chiamiano noSO.c:
-----------------
typedef unsigned char uint8_t;
#define DDRC (*(volatile uint8_t *) 0x27)
#define PORTC (*(volatile uint8_t *) 0x28)

int main(void)
{
        volatile int i;
        DDRC |= 1 << 5;
        for (;;) {
                for (i=0; i < 32767; i++)
                        ;
                PORTC ^= 1 << 5;
        }
}
-----------------
Convertendo interi (0x27 e' il numero 27 esadecimale, cioè 39) in puntatori
accediamo alle periferiche (memoria o altro) "sparando" sul bus indirizzi ciò che piu' ci piace.

# proviamo a compilarlo
 $ gcc noSO.c
 $ ./a.out
# il risultato e' segmentation fault, perché gli indirizzi non sono legali per un processo in esecuzione in linux.
# compiliamolo per l'architetture avr atmel/atmega: (occorre il compilatore)
 $ avr-gcc -mmcu=atmega168 -Os -o noSO noSO.c
# l'eseguibile ottenurto non e' per intel:
  $  file noSO
# generiamo il file .hex (perché l'utility di trasferimento lo vuole così)
  $ avr-objcopy -O ihex noSO noSO.hex
# ... carichiamo il file sul microcontrollore atmega168
        $ avrdude -p m168 -c stk500v2 -P /dev/ttyUSB0 -U flash:w:noSO.hex 
# (occorre il chip, il programmatore ed un circuito quale quello descritto qui:
# http://tuxgraphics.org/electronics/200904/avr-c-programming.shtml

# il led lampeggia. potere del software.