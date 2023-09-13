#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int start_pop;
    int end_pop;
    int brn;
    int pass;
    int years = 0;


    // TODO: Prompt for start size
    do
    {
        start_pop = get_int("Start size: ");
    }
    while (start_pop < 9);

    // TODO: Prompt for end size
    do
    {
        end_pop = get_int("End size: ");
    }
    while (end_pop < start_pop);

    // TODO: Calculate number of years until we reach threshold
    while (start_pop < end_pop)
    {
        brn = start_pop / 3;
        pass = start_pop / 4;
        start_pop = start_pop + brn - pass;
        years++;
    }


    // TODO: Print number of years
    printf("Years: %i\n", years);


}