#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>



typedef uint8_t  BYTE;

int main(int argc, char *argv[])
{
    //check arguments
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    //open file, continue if it exists
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open.\n");
        return 1;
    }

    //create buffer, output file placeholder
    BYTE buffer[512];
    FILE *output = NULL;
    //create string filename for name of the file, bool for if writing of the photos started or not and photo count
    char *filename = malloc(10);
    bool writing = false;
    int count = 0;

    //read file in chunks of 512 bytes
    while (fread(&buffer, sizeof(BYTE), 512, file))
    {
        //HEADER: 0xff, 0xd8, 0xff, 0xe..
        //if first 4 bytes of the chunk == header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //create first photo file, if found file is the first one
            if (count == 0)
            {
                sprintf(filename, "%03i.jpg", count);
                output = fopen(filename, "w");
                writing = true;
                count++;
            }
            //else close previous file, modify name and create new photo file
            else
            {
                fclose(output);
                sprintf(filename, "%03i.jpg", count);
                output = fopen(filename, "w");
                count++;
            }
        }
        //if writing started (file created), write buffer to opened file
        if (writing == true)
        {
            fwrite(&buffer, sizeof(BYTE), 512, output);
        }


    }
    free(filename);
    fclose(output);
    fclose(file);
}