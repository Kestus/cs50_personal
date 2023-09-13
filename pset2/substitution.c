#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>


bool valid(string x);

int main(int argc, string argv[])
{
    //check for command line arguments
    if (argc != 2)
    {
        printf("Usage: ./substitution KEY\n");
        return 1;
    }
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    //validate key
    if (valid(argv[1]) == true)
    {


        //get plaintext
        string plain = get_string("plaintext: ");

        //encipher text
        char cipher[strlen(plain) - 1];
        cipher[strlen(plain)] = '\0';
        //alphabet reference
        string ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

        //start encryption
        for (int i = 0, n = strlen(plain); i < n; i++)
        {
            if (isalpha(plain[i]))
            {
                for (int j = 0; j < 26; j++)
                {
                    if (isupper(plain[i]) && plain[i] == ALPHA[j])
                    {
                        cipher[i] = toupper(argv[1][j]);
                        break;
                    }
                    else if (toupper(plain[i]) == (ALPHA[j]))
                    {
                        cipher[i] = tolower(argv[1][j]);
                        break;
                    }
                }
            }
            else
            {
                cipher[i] = plain[i];
            }
        }

        //print result
        printf("%lu", strlen(plain));
        printf("ciphertext: %s\n", (string)cipher);
        return 0;
    }
    else
    {
        return 1;
    }
}




bool valid(string x)
{
    bool valid = false;
    for (int i = 0, n = strlen(x); i < n; i++)  //check each character in a key
    {

        if (!isalpha(x[i])) //check if that (i) character is alphabetical
        {
            printf("Key must contain alphabeitic characters.\n");
            return valid;
        }

        for (int j = i + 1; j < n; j++) //compare each character (i) to each subsequent character (j = i + 1)
        {
            if (toupper(x[i]) == toupper(x[j]))
            {
                printf("Key must not contain repeated characters.\n");
                return valid;
            }

        }
    }
    valid = true;
    return valid;
}
