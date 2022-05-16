#include <stdio.h>
#include <math.h>
//Take index = 0.0588 * L - 0.296 * S - 15.8, L is for Letters, S is for Sentences
// Iterate through string to find letters, put in list. Find length of list, store to variable L. Ignore " "  and "."
// string length found using /0, count them store to variable str_length
//words through spaces
//periods will tell you how many sentences are in there. Find amount of periods, store to variable S
// output statement is index, printf("Grade level: %s", index)

int main(void)  {
    int i = 0, w = 0, s = 0, l = 0 , x = 0;
    float L, S, index;
    

    
    printf("Input Some text: ");
    // c is stupid and i hate it
    // didn't work without specifically input_string[]. input_string[] = "" did not work surprisingly. Might have to do with DMA maybe idk
    char input_string[2000];
    //fgets also takes /n and must have specified number or it wont work
    fgets(input_string, 2000, stdin);
   
        while (input_string[i] != '\0') {
            i++;
            x++;
            
        }


    for (w = 0, s = 0, l = 0, i = 0; i < x; i++) {
        //there's an easier way using ascii but can't be fucked
        if (input_string[i] >= 'a' && input_string[i] <= 'z' || input_string[i] >= 'A' && input_string[i] <='Z') {
            l++;
            
        }
        if (input_string[i] == ' ') {
            w++;
        }
        if (input_string[i] == '.' || input_string[i] == '!' || input_string[i] == '?') {
            s++;
        }
    
        
        

    }
    printf("Letters: %d, Words: %d, Sentences: %d", l , w = w +1 , s);
    L = (100/(float)w) * (float)l;
    S = (100/(float)w) * (float)s;
    index = (0.0588 * L) - (0.296 * S) - 15.8;
    if (index > 16) {
        printf(" Reading level is: Grade 16+");
    }
    else if (index < 1) {
        printf(" Reading level is: Before Grade 1");
    }
    else {
        printf(" Reading level is: Grade %f", round(index));
    }
    
}
   



