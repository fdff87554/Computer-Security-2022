// gcc -o demo_BOF2 -fstack-protector-all -fno-pie -no-pie demo_BOF2.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


void backdoor() {
    printf("You have entered the backdoor\n");
    system("/bin/sh");
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    char name[0x10];
    char phone[0x10];

    printf("Enter your name: ");
    read(0, name, 0x100);
    printf("Hello, %s !", name);

    printf("Enter your phone number: ");
    read(0, phone, 0x100);

    return 0;
}
