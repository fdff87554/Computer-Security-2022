// gcc -o demo_BOF1 -fno-stack-protector -fno-pie -no-pie demo_BOF1.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


void backdoor() {
    printf("You have entered the backdoor");
    system("/bin/sh");
}


int main() {
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    char name[0x10];

    printf("What's your name: ");
    read(0, name, 0x100);

    return 0;
}
