#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

char name[0x80];

int main() {
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    char buf[0x10];

    printf("Give me your name: ");
    read(0, name, 0x80);

    printf("Give me your ROP: ");
    read(0, buf, 0x20);

    return 0;
}
