#include <stdio.h>


int main(void)
{
    int i;
    int j = 0;
    int h = 1;
    int x = 0;
    int y = 0;
    
    
    printf("How many? ");
    scanf("%d", &i);
    char hash[] = "#";
    char dot[] = " ";
    int z = i;

    do {
        //hypothetical i = 3
        //print a dot until y = 2
        if (y < (z - 1)) {
            printf("%s", dot);
            y++;
            
        }
        
        //when y = 2 start printing hashes until y = =3
        if ((y >= (z-1))  && (y != i )) {
           
            printf("%s", hash);
            y++;
        }
        // when y = 3 substract 1 from z and reset y, then increment x and start over 
        if (y == i)  {
            z--;
            printf("\n");
            y = 0;
            x++;
        }
        
    // end the loop after reaching the base of the stairs
      }
    while (i > x);
   

  
    do {
        
        printf("%s", hash);
        j++;
        
            if (j == h) {
            
            printf("\n");
            h++;
            j = 0;
            }
    }
    while (i>j && h < i+1);
   
}


//print until reaches j increment j , subtract from i 
// j 1 i 5 , j = 2