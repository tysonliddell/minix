#include <stdio.h>

int main(argc, argv)
char **argv;
{
    int i;

    printf("arg count: %d\n", argc);
    for (i=0; i < argc; i++) {
        printf("arg %d: %s\n", i, argv[i]);
    }

    return 42;
}
