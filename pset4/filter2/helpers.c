#include "helpers.h"
#include <math.h>
#include <stdlib.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float average;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //calculate average RGB of pixel [i][j] and round it up
            average = (image[i][j].rgbtRed + image[i][j].rgbtBlue + image[i][j].rgbtGreen) / 3.0;
            average = (int)round(average);
            //set RGB value of that pixel to the average value of RGB in original pixel
            image[i][j].rgbtRed = average;
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //create buffer pixel
    RGBTRIPLE buffer;
    //iterate through original image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < round(width / 2); j++) //for each pixel in the left half
        {
            //swap it with the pixel on the opposite side
            buffer = image[i][j];
            image[i][j] = image[i][width - 1 - j];
            image[i][width - 1 - j] = buffer;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE b_image[height][width];   //create buffer image
    float averageRed;                   //create buffer RGB values
    float averageGreen;
    float averageBlue;
    int count;

    for (int i = 0; i < height; i++)        //for each row
    {
        for (int j = 0; j < width; j++)     //and each column
        {
            //reset RGB and average counter values
            averageRed = 0.0;
            averageGreen = 0.0;
            averageBlue = 0.0;
            count = 0;

            //iterate through pixels in 3x3 square around [i][j] pixel
            for (int ii = 0; ii < 3; ii++)
            {
                for (int jj = 0; jj < 3; jj++)
                {
                    //check if that pixel inside of image border
                    if (0 <= (i - 1 + ii) && (i - 1 + ii) < height && 0 <= (j - 1 + jj) && (j - 1 + jj) < width)
                    {
                        //add that pixel to average count
                        averageRed += image[i - 1 + ii][j - 1 + jj].rgbtRed;
                        averageGreen += image[i - 1 + ii][j - 1 + jj].rgbtGreen;
                        averageBlue += image[i - 1 + ii][j - 1 + jj].rgbtBlue;
                        //and count how many pixels added to average
                        count++;
                    }

                }
            }

            //calculate the average
            averageRed = averageRed  / count;
            averageGreen = averageGreen / count;
            averageBlue = averageBlue / count;

            //and set buffer image pixel RGB, to rounded up average RGB
            b_image[i][j].rgbtRed = (int)round(averageRed);
            b_image[i][j].rgbtGreen = (int)round(averageGreen);
            b_image[i][j].rgbtBlue = (int)round(averageBlue);
        }
    }
    //copy buffer image to image out
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = b_image[i][j];
        }
    }


    return;
}

int cap(int x);

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE g_image[height][width];       //create buffer image
    int red, green, blue;

    float GxRed, GxGreen, GxBlue;             //create Gx matrix
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};


    float GyRed, GyGreen, GyBlue;             //create Gy matrix
    int Gy[3][3] = {{-1, -2, -1}, { 0,  0,  0}, { 1,  2,  1}};


    for (int i = 0; i < height; i++)        //for each row
    {
        for (int j = 0; j < width; j++)     //and each column
        {
            red = green = blue = 0;
            //reset Gx value for pixel
            GxRed = 0;
            GxGreen = 0;
            GxBlue = 0;
            //reset Gy value for pixel
            GyRed = 0;
            GyGreen = 0;
            GyBlue = 0;

            //itterate 3x3 square around pixel
            for (int ii = 0; ii < 3; ii++)
            {
                for (int jj = 0; jj < 3; jj++)
                {
                    //check if pixel exists
                    if (0 <= (i - 1 + ii) && (i - 1 + ii) < height && 0 <= (j - 1 + jj) && (j - 1 + jj) < width)
                    {
                        //calculate Gx value for RGB
                        GxRed += image[i - 1 + ii][j - 1 + jj].rgbtRed * Gx[ii][jj];
                        GxGreen += image[i - 1 + ii][j - 1 + jj].rgbtGreen * Gx[ii][jj];
                        GxBlue += image[i - 1 + ii][j - 1 + jj].rgbtBlue * Gx[ii][jj];

                        //calculate Gy value for RGB
                        GyRed += image[i - 1 + ii][j - 1 + jj].rgbtRed * Gy[ii][jj];
                        GyGreen += image[i - 1 + ii][j - 1 + jj].rgbtGreen * Gy[ii][jj];
                        GyBlue += image[i - 1 + ii][j - 1 + jj].rgbtBlue * Gy[ii][jj];
                    }
                }
            }
            //determine new value Gx^2 + Gy^2 of a pixel, and round it up
            red = (int)round(sqrt(pow(GxRed, 2) + pow(GyRed, 2)));
            green = (int)round(sqrt(pow(GxGreen, 2) + pow(GyGreen, 2)));
            blue = (int)round(sqrt(pow(GxBlue, 2) + pow(GyBlue, 2)));


            //new value is capped at 255
            g_image[i][j].rgbtRed   = cap(red);
            g_image[i][j].rgbtGreen = cap(green);
            g_image[i][j].rgbtBlue  = cap(blue);

        }
    }
    //copy buffer image to image out
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = g_image[i][j];
        }
    }

    return;
}

int cap(int x)
{
    if (x > 255)
    {
        return 255;
    }

    return x;
}