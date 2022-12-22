#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


int main() {
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    char buf[0x10];

    printf("Your libc: %p", printf);
    read(0, buf, 0x100);

    return 0;
}
