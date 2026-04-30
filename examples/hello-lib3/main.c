#include <stdio.h>

int main()
{
	char buf[100];

    printf("Enter your name: ");
    scanf("%s", buf);
    printf("Hi %s!\n", buf);
    
    return 123;
}
