#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

// Max voters and candidates
#define MAX_VOTERS 100
#define MAX_CANDIDATES 9

// preferences[i][j][k] is the rank and choice of voters. I is the rank, j is the candidates position in array, k is the candidate characters
char pref[10][1000][1000]; //rank choice

// Candidates have name, vote count, eliminated status
typedef struct
{
    char name[1000];
    int votes;
    int eliminated; //bool return 0 if false 1 if true
}
candidate;

// Array of candidates
candidate candidates[MAX_CANDIDATES];

// Numbers of voters and candidates
int the_bar = 0, candidate_count = 0, rank = 0, voter_count, cycle = 0, voter_number = 0;
char name[1000], k[1000], *ptr; //!!!! may change to input_string for clarity

// Function prototypes
int vote(int , int , char*, int candidate); //bool 0 if false 1 if true.  Voter rank name
void tabulate(int, int, int);
int print_winner(int, int, int); //bool
int find_min(int);
int is_tie(int, int ); //bool. min
void eliminate(int, int);

int main(int argc, char *argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: runoff [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX_CANDIDATES)
    {
        printf("Maximum number of candidates is %i\n", MAX_CANDIDATES);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        strcpy(candidates[i].name, argv[i + 1]);
        candidates[i].votes = 0;
        candidates[i].eliminated = 0; // 0 for false
    }

    printf("Number of voters: ");
    voter_count = strtol(fgets(k, 1000, stdin), &ptr, 10);
    



    if (voter_count > MAX_VOTERS)
    {
        printf("Maximum number of voters is %i\n", MAX_VOTERS);
        return 3;
    }

    // Keep querying for votes
    for (int i = 0; i < voter_count; i++ )
    {

        // Query for each rankf
        for (int j = 0, rank = 0; j < candidate_count; j++, rank++) //For each candidate prompt for each candidate per rank until done, then again for next voter
        {
            
            printf("Rank %i: ", j + 1);
            fgets(name, 1000, stdin);
            name[strcspn(name, "\n")] = '\0';
            
            
            
            // Record vote, unless it's invalid
            if (vote(candidate_count, rank, name, voter_number) == 1 || name == "" || name[0] == '\0')
            {
                printf("Invalid vote.\n");
                j--;
                rank--;
            }

            
        }
        voter_number++;
            //if vote? ? ? ?

        printf("\n");
    }

    // Keep holding runoffs until winner exists
    for (cycle = 0; cycle < candidate_count; cycle++) {
        // Calculate votes given remaining candidates
        
        tabulate(candidate_count, cycle, voter_count);
        // Check if election has been won
        int won = print_winner(candidate_count, cycle, voter_count); // bool, return true .. .. . . find way to make rank global either through pointers or otherwise
        if (won == 1)
        {
            break;
        }

        // Eliminate last-place candidates
        int min = find_min(candidate_count);
        int tie = is_tie(min, candidate_count); //bool

        // If tie, everyone wins
        if (tie == 1)
        {
            for (int i = 0; i < candidate_count; i++)
            {
                if (candidates[i].eliminated != 1)
                {
                    printf("%s\n has tied!", candidates[i].name);
                }
            }
            break;
        }

        // Eliminate anyone with minimum number of votes
        eliminate(min, candidate_count);
        

        // Reset vote counts back to zero
        //this function is redundant, if you're eliminated other votes still matter, just don't allow the final candidate to be picked from candidates[i].eliminate = 1
    }
}  
//Taking first rank and evaluate ties, eliminate last person, then revoting on 2nd vote and so on
// Record preference if vote is valid
int vote(int candidate_count, int rank, char name[], int voter_number) //bool
{
    
    //Each rank stored to different array in an array use preferences
    //needs to reset after voter is done to accomodate next voter
    // TODO
    for (int h = 0; h < candidate_count + 2; h++) {
        int result = strcmp(candidates[h].name, name);
        
        if (result == 0) { //!!!!
                strcpy(pref[rank][voter_number], name);
                
                //check and see if votes are being stored properly in pref and being tabulated correctly
                return 0;
            }
        if (h == candidate_count + 1) {
            return 1;
        }
    }
}
//at end of vote do print(winner), send rank
    

   


// Tabulate votes for non-eliminated candidates
void tabulate(int candidate_count, int cycle, int voter_count)
{   
    
    //needs to check for 1st set, then second set, then third set. Should store votes in rank 1, 2, ... 9
    for (int o = 0; o < candidate_count; o++) {
        for (int i = 0; i < voter_count; i++) {
            if (candidates[o].eliminated != 1 && strcmp(candidates[o].name, pref[cycle][i]) == 0 ) {
                candidates[o].votes += 1;
            }
        }
    }
    return;
}

// Print the winner of the election, if there is one
int print_winner(int candidate_count, int cycle, int voter_count) // bool
{   
    
    //First check to see if someone has won majority vote
    //cycle + 1 because cycle starts at 0
    
    float majority = 0;
    majority = (((double) voter_count)/2);
    
    
    for (int i = 0; i < candidate_count; i++) {
        if (candidates[i].votes >= majority || candidate_count == 1 || voter_count == 1) {
            printf("%s, has Won!\n", candidates[i].name);
            return 1;
        }
    }
    
    return 0;
}

// Return the minimum number of votes any remaining candidate has
int find_min(int candidate_count)
{
     
    // find lowest total votes and if is_tie not true send to eliminate
    int min = 901;
    for (int l = 0; l < candidate_count; l++) {
        
        if (candidates[l].votes < min && candidates[l].eliminated == 0) {
            min = candidates[l].votes;
        }

    }
    
    return min; //get minimum to eliminated
}

// Return true if the election is tied between all candidates, false otherwise
int is_tie(int min, int candidate_count) // bool
{
    //!!! when candidate removed, wont proc tie because candidate 3 total 4 
    int total = candidates[0].votes;
    
    for (int i = 0; i < candidate_count + 1; i++) {
        if (candidates[i].eliminated == 0) {
            total =  candidates[i].votes ;
                if (total == candidates[0].votes && i >= candidate_count) {
                    return 1;
                }
        }
        
        
    }
    return 0;
}

// Eliminate the candidate (or candidates) in last place
void eliminate(int min, int candidate_count)
{
    for (int i = 0; i < candidate_count + 1; i++) {
        
        if (candidates[i].votes == min && candidates[i].eliminated == 0) {
            candidates[i].eliminated = 1;
            printf("Candidate %s 's votes: %d\n", candidates[i].name, candidates[i].votes);
            printf("candidates eliminated is %s\n", candidates[i].name);
        }

    }   
    //based on criteria turn candidate[i].eliminated = 1

}
