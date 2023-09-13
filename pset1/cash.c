#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    float dollars;
    //get input number of change
    do
    {
        dollars = get_float("change owed: ");
    }
    while (dollars <= 0);

    //set value of cents and start count for number of coins
    int cents = round(dollars * 100);
    int coins = 0;
    
    //add coin to coins while there is more then 25 cents
    while (cents >= 25)
    {
        cents = cents - 25;
        coins++;
    }
    
    //do the same for 10 etc.
    while (cents >= 10)
    {
        cents = cents - 10;
        coins++;
    }
    while (cents >= 5)
    {
        cents = cents - 5;
        coins++;
    }
    while (cents >= 1)
    {
        cents = cents - 1;
        coins++;
    }

    printf("%i\n", coins);
}