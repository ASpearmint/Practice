#include <stdio.h>
#include <stdlib.h>

//programs do not get compiled and properly run without "running it" so even if you save it wont save, RUN IT
int main(int argc, char *argv[]) {
    int i = 0, x = 0;
    char input_string[2000], *ptr, new_string;
    long k;
    

    k = strtol(argv[1], &ptr, 10 );
    
    if (argc != 2 || argv[1] == "\n") {
        printf("Usage ./caesar key");
        return 1;
    }
    else {

    printf("plaintext: ");
    
    fgets(input_string, 2000, stdin);
    
    
    //printf("Key: %d , Plaintext: %s", k  , input_string);
    
    
    //program works up to here

    while (input_string[i] != '\0') { 
        if (input_string[i] >= 'A' && input_string[i] <= 'Z') {
            input_string[i] =  (((input_string[i] - 'A' + k) % 26 ) + 'A');
               
                }
            

        if (input_string[i] >= 'a' && input_string[i] <= 'z') {
            input_string[i] =  (((input_string[i] -'a' + k) % 26 ) + 'a');
                
        }
        i++;
    }


    printf("ciphertext: %s",  input_string);
    
    
    return 0;

    }
    }

           