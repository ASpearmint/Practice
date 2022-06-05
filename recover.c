#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
 
int main(int argc, char *argv[]) {//if you use sprintf, do sizeof"string"+1 for the /0 char
    if (argc != 2) {
        printf("Usage: ./recover filename.raw");
        return 3; 
    }
    //WHEN YOU PULL FROM FREAD, YOU'RE PUTTING THEM INTO AN INDEXED ARRAY, IF YOU PULL 512 ITEMS OF 1 BYTE SIZE YOU NEED TO HAVE AN ITERABLE VARIABLE AKA BUFFER[I]
    //filenames
    
    typedef uint8_t BYTE;
    int BLOCK = 512 * sizeof(BYTE);
    BYTE buffer[BLOCK * sizeof(BYTE)];
    int tens, ones;
    char *file_name = malloc(sizeof(BYTE)*8);
    //image stored in blocks of 512
    FILE *inptr = fopen(argv[1], "r");

    if (inptr == NULL) {
        printf("File could not be opened");
        return 1;
    }

    //check to see if file is jpeg
    for (int i = 0; i <= 3; i++) {
        fread(&buffer, sizeof(BYTE), 1, inptr); 
    }
  
   
    if (buffer[0] != 0xff && buffer[1] != 0xd8 && buffer[2] != 0xff) {
        printf("File could not be read\n");
        
        return 1; 
    }
    FILE *outptr = fopen(file_name, "w");
        if (outptr == NULL) {
            printf("File could not be written to");
            return 1;
        }
    

    //func to change output name
    
        //open file and store information in variable
        //fread file with those until start of next and then fwrite to file  -> later read next one and write to separate filename 000.jpg

    fseek(inptr, 0, SEEK_SET);
    while (fread(&buffer, BLOCK, 1, inptr) == 0) { 
        //8 bytes in the string
        while (buffer[0] != 0xff && buffer[1] != 0xd8 && buffer[2] != 0xff) { 
            tens = 0, ones = 0;

            if (ones == 10) {
                tens = 1; 
                ones = 0;
            }

            sprintf(file_name, "0%i%i.jpg", tens, ones);
            //set up error statements, not 2 argc, not opened for reading (not 0xff, 0xd8, 0xff)
            
            fwrite(buffer, sizeof(BYTE), BLOCK, outptr);

    }
    
    
        fclose(outptr);
        free(file_name); 
        free(buffer);
        ones++;
        

    }
    
//close file
fclose(inptr);
free(buffer);
}