// gcc -o demo_ROP -fno-stack-protector -fno-pie -no-pie demo_ROP.c
#include <stdio.h>
#include <unistd.h>


int main () {
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);

    char buf[0x10];

    printf("Here is your \"/bin/sh\": %p\n", "/bin/sh");
    printf("Give me your ROP: ");
    read(0, buf, 0x400);

    return 0;
}
