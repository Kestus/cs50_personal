#include <cs50.h>
#include <stdio.h>


int main(void)
{
    //get the name from user
    string answer = get_string("name? ");
    //print formatted string, adding hello to a name
    printf("hello, %s", answer);
}
