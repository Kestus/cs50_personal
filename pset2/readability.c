#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>


int count_letters(string x);
int count_words(string x);
int count_sentences(string x);

int main(void)
{
    //get text from user
    string text = get_string("Text: ");

    //count letters/word/sentences in text
    float letters = count_letters(text);
    float words = count_words(text);
    float sentences = count_sentences(text);

    //calculate number of average letters and sentences
    float L = (letters / words) * 100;
    float S = (sentences / words) * 100;

    //calculate index
    float index = (0.0588 * L) - (0.296 * S) - 15.8;
    int i = (int)round(index);

    //print result
    if(i < 1)
    {
        printf("Before Grade 1\n");
    }
    else if(i >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", i);
    }

}


int count_letters(string x)
{
    int letters = 0;

    for(int i = 0, n = strlen(x); i < n; i++)
    {
        if ((x[i] >= 65 && x[i] <= 90) || (x[i] >= 97 && x[i] <= 122))
        {
            letters++;
        }
    }
    return letters;
}

int count_words(string x)
{
    int words = 1;

    for(int i = 0, n = strlen(x); i < n; i++)
    {
        if(x[i] == 32)
        {
            words++;
        }
    }
    return words;
}

int count_sentences(string x)
{
    int sentences = 0;

    for(int i = 0, n = strlen(x); i < n; i++)
    {
        if(x[i] == 46 || x[i] == 33 || x[i] == 63)
        {
            sentences++;
        }
    }
    return sentences;
}

