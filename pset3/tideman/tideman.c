#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)           //check each candidate
    {
        if(strcmp(candidates[i], name) == 0)            //if name of the candidate == name in the input
        {
            ranks[i] = rank;
            return true;                                //Set input number to rank i (ranks[i] correlates with candidates[i])
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    int cand_num = 0;
    for (int i = 0; i < candidate_count; i++)              //Compare candidate i
    {
        for (int j = i + 1; j < candidate_count - 1; j++)      //To next candidate
        {
            if (ranks[i] < ranks[j])                    //If rank of candidate i higher then candidate j
            {
                preferences[cand_num][j]++;                    //Add score
            }
        }
    }
    cand_num++;
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for(int i = 0; i < candidate_count; i++)           //pair compare candidate i
    {
        for(int j = i + 1; j < candidate_count - 1; j++)       //and next candidate j
        {
            if(preferences[i][j] > preferences[j][i])
            {
                pairs[i].winner = preferences[i][j];
                pairs[i].loser = preferences[j][i];
            }
        }
    }


    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    int s; //swap placeholder
    int swap_count = -1;
    int pair_diff[pair_count];

    for (int i = 0; i < pair_count; i++)
    {
        pair_diff[i] = pairs[i].winner - pairs[i].loser;
    }

    do
    {
        swap_count = 0;

        for(int q = 0; q < pair_count - 1; q++)
        {
            if(pair_diff[q] > pair_diff[q + 1])
            {
                s = pair_diff[q];
                pair_diff[q] = pair_diff[q + 1];
                pair_diff[q + 1] = s;

                swap_count++;
            }

        }
    }
    while (swap_count != 0);

    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // TODO
    return;
}

// Print the winner of the election
void print_winner(void)
{
    // TODO
    return;
}

