#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
char word[1000], word1[1000], word2[1000];
int compute_score();
int i, sum; 


int main(void)
{
    // Get input words from both players
    printf("Player 1: ");
    fgets(word1, 1000, stdin);
    printf("Player 2: ");
    fgets(word2, 1000, stdin); 


    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // TODO: Print the winner
    if (score1 > score2) {
        printf("Player 1 wins");
    }
    else if (score1 == score2) {
        printf("It's a Tie!");
    }
    else { 
        printf("Player 2 wins");
    }

}

int compute_score(char word[]) {
    // TODO: Compute and return score for string
    //if you don't reset sum it keeps the value
    sum = 0;
    for (i = 0; i < strlen(word); i++) {
        if (word[i] > 'a' && word[i] <'z') {
            word[i] = word[i] - 'a';
            word[i] = POINTS[word[i]]; 
        }
        if (word[i] > 'A' && word[i] <'Z') {
            word[i] = word[i] - 'A';
            word[i] = POINTS[word[i]]; 
        }
        //array of letters, both big and small, if input[i] = value then subtract 'a'/'A' and set as x, points[x] will be the value, store value into array add up array
    }
    i = 0;
    while (word[i] != '\0') {
        sum = sum + word[i];
        i++;
    }
    printf("Player %d\n", sum);
    return sum;
}

