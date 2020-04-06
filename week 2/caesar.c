#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <cs50.h>

int main(int argc, string args[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar k");
        return 1;
    }

    int k = atoi(args[1]) % 26; // if k is > 26, store the division remainder instead
    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");

    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (!isalpha(plaintext[i]))
        {
            printf("%c", plaintext[i]);
            continue;
        }

        int ascii_set = isupper(plaintext[i]) ? 65 : 97;

        int pt = plaintext[i] - ascii_set;
        int ct = (pt + k) % 26;

        printf("%c", ct + ascii_set);
    }

    printf("\n");
    return 0;
}