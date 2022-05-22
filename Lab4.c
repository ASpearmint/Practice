// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
//Read and Write to File, Write needs to change the value of (something) to 2.0
//uint8_t (8 unsigned) and uint16_t ( 16 signed) as well as size_t (long unsigned) will be used
//Open, read, write, close
//Read the header and write header, uint8_t HEADER_SIZE. READ Data as uint16_t 1 sample at a time, Multiply sample by factor, write sample to output file
// Number of bytes in .wav header
const int HEADER_SIZE = 44;

// Read, store, and write header to output file
// Read data (samples) after the header file and store it
// multiply it by 2.0
// Write changed data to new output file

//To do


int main(int argc, char *argv[])
{


    //Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    //Open (creates) files and determine scaling factor
    FILE *input = fopen(argv[1], "rb");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }
    
    //find end position in file and store to fs
    fseek(input, 0, SEEK_END);
    int fs = ftell(input);
    rewind(input);
    

    //free up some memory for HEADER and data
    uint8_t *headr = malloc(HEADER_SIZE);
    int16_t *bodyr = malloc(fs-HEADER_SIZE);
    
    //Read that data and store in headr and bodyr
    
    fread(headr, sizeof(uint8_t), HEADER_SIZE, input);
    fread(bodyr, sizeof(int16_t), (fs - HEADER_SIZE)/sizeof(int16_t), input);

    float factor = atof(argv[3]);

    
    //change the data by the factor
    for (int x = 0; x < (fs - HEADER_SIZE)/sizeof(int16_t); x++) {
        
        bodyr[x] *= factor;
        
    }
    
    FILE *output = fopen(argv[2], "wb");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    //Find beginning of file and write the header, then find the position after the header and write the data
    //doesnt work
    
    fwrite(headr, sizeof(uint8_t), HEADER_SIZE, output);
    fwrite(bodyr, sizeof(int16_t), (fs - HEADER_SIZE)/ sizeof(int16_t), output);


    

    // TODO: Copy header from input file to output file

    // TODO: Read samples from input file and write updated data to output file

    //Close files
    free(headr);
    free(bodyr);
    fclose(input);
    fclose(output);
}

