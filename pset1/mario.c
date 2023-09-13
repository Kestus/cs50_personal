#include <cs50.h>
#include <stdio.h>



int main(void)
{
    int height;

    do
    {
        height = get_int("Height: ");
    }
    while (height <= 0 || height >= 9);


    for (int i = 0; i < height; i++)
    {
        for (int space = 0; space < height - i - 1; space++)
        {
            printf(" ");
        }
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        printf("\n");
    }

}