#include <stdio.h>
#include <string.h>
#include <stdlib.h>


// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    char name[1000];
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count = 0, the_bar = 0, i, h, j, l, m, x, voter_count = 0, input_int, result;

char input_string[1000], *ptr, k[1000];

// Function prototypes
int vote(char * , int );
void print_winner(int);


int main(int argc, char *argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (j = 0; j < candidate_count; j++)
    {   
        strcpy(candidates[j].name, argv[j+1]);  
        candidates[j].votes = 0;
       
    }

    printf("Number of voters: ");
    
    input_int = strtol(fgets(k, 1000, stdin), &ptr, 10);
    
    // Loop over all voters
    while (i < input_int) {
        printf("Vote: ");
        fgets(input_string, sizeof(input_string), stdin);
        // gets rid of /n from previous fgets
        input_string[strcspn(input_string, "\n")] = '\0';
        
        
        // Check for invalid vote
        
        if (vote(input_string, input_int) == 1 || input_string == "" || input_string == "\n")
        {
            printf("Invalid vote.\n");
        }
        if (vote(input_string, input_int) == 0)
        {
            i++;
        }
        
        
    }

    // Display winner of election
    print_winner(candidate_count);
}

// Update vote totals given a new vote
int vote(char a[1000], int b)
{ 
    for (h = 0; h < b + 1; h++) {

        result = strcmp(candidates[h].name, a);
        

        if (result == 0) { //!!!!
            candidates[h].votes += 1;
            return result;
            
        }
        if (h == b + 1) {
            return 1;
        }
        
    }

      
    return 1;
    
}

// Print the winner (or winners) of the election
void print_winner(int c)
{
    // TODOnah
    for (l = 0; l < c; l++) {
        if (candidates[l].votes > the_bar) {
            the_bar = candidates[l].votes;
        }
    }
    for (m = 0; m < c; m++) {
        if (the_bar == candidates[m].votes) {
            printf("%s, has Won!\n", candidates[m].name);
        }
    }
    
    return;
}