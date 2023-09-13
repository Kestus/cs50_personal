// Implements a dictionary's functionality
#include "dictionary.h"
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>//strcpy, strcasecmp
#include <ctype.h>


// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 626;

// Hash table
node *table[N];

void free_node(node *n);
int word_count;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    //strcasecmp
    int h = hash(word);
    for (node *tmp = table[h]; tmp != NULL; tmp = tmp->next)
    {
        if (strcasecmp(word, tmp->word) == 0)
        {
            return true;
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash = 0;

    for (int i = 0, j = strlen(word); i < j; i++)
    {
        hash += (int)tolower(word[i]);
    }

    hash = (N - 1) % hash; //N - 1
    return hash;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{

    word_count = 0;
    char *buffer = malloc(45 * sizeof(char));

    //open file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }

    //read strings, one at a time
    while (fscanf(file, "%s", buffer) != EOF)
    {
        //create new node for each word
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            fclose(file);
            return false;
        }

        //copy string
        strcpy(new_node -> word, buffer);
        new_node -> next = NULL;

        //hash word to obtain a hash value
        int h = hash(buffer);

        //insert node into hash table at that location
        new_node -> next = table[h];
        table[h] = new_node;

        word_count++;
    }

    fclose(file);
    free(buffer);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return word_count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        free_node(table[i]);
    }
    return true;
}

void free_node(node *n)
{
    if (n == NULL)
    {
        return;
    }

    if (n->next != NULL)
    {
        free_node(n->next);
    }

    free(n);
}