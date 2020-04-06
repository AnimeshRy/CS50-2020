#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    do {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);

    if (height > 0 || height < 9) {
        int counter = 0;
        for (int row=0; row<height; row++) {
            if (counter != height) {
                for (int spaces = (height-1) - counter; spaces > 0; spaces--) {
                    printf(" ");
                }
                for (int hashes = 0; hashes <= counter; hashes++) {
                    printf("#");
                }

                printf("  ");

                for (int hashes = 0; hashes <= counter; hashes++) {
                    printf("#");
                }

                printf("\n");
                counter++;
            }
        }     
    }       
}