#include <stdio.h>

int main()
{
    unsigned long x = 0x12345678;
    unsigned long y = 2;
    short x1 = 0x1234;
    short y1 = 3;
    unsigned int x2 = 0x5678;
    unsigned int y2 = 7;
    printf("Hello, from an x64 machine!\n");
    printf("LONGS:\n");
    printf("%d\n", x+y);
    printf("%d\n", x-y);
    printf("%d\n", x/y);
    printf("%d\n", x*y);
    printf("%d\n", x%y);
    printf("%d\n", x&y);
    printf("%d\n", x|y);
    printf("%d\n", ~x);
    printf("%d\n", x<<y);
    printf("%d\n", x>>y);
    printf("%d\n", x+y);

    printf("SHORTS:\n");
    printf("%d\n", x1+y1);
    printf("%d\n", x1-y1);
    printf("%d\n", x1/y1);
    printf("%d\n", x1*y1);
    printf("%d\n", x1%y1);
    printf("%d\n", x1&y1);
    printf("%d\n", x1|y1);
    printf("%d\n", ~x1);
    printf("%d\n", x1<<y1);
    printf("%d\n", x1>>y1);
    printf("%d\n", x1+y1);

    printf("UNSIGNED INTS:\n");
    printf("%d\n", x2+y2);
    printf("%d\n", x2-y2);
    printf("%d\n", x2/y2);
    printf("%d\n", x2*y2);
    printf("%d\n", x2%y2);
    printf("%d\n", x2&y2);
    printf("%d\n", x2|y2);
    printf("%d\n", ~x2);
    printf("%d\n", x2<<y2);
    printf("%d\n", x2>>y2);
    printf("%d\n", x2+y2);
 
    printf("Done!\n");
    return 42;
}
