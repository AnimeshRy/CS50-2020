#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int letter;
int word;
int sentence;


int main(void)
{

// prompt the user with the question

    string article = get_string("What's the article?: ");

// set the length of article

    int n = strlen(article);

// add +1 if the article starts with alphanumeric letter

    if (isalnum(article[0]))
    {
        word += 1;
    }

// count words

    for (int i = 0; i < n;  i++)
    {
        // count letters

        if (isalnum(article[i]))
        {
            letter++;
        }

        // count words

        if (isspace(article[i]) && (isalnum(article[i + 1]) || article[i + 1] == '"'))
        {
            word++;
        }

        // count sentences

        if ((article[i] == '!' || article[i] == '?' || article[i] == '.') && isalnum(article[i - 1]))
        {
            sentence++;
        }

    }

// calculate Coleman-Liau index

    double grade = 0.0588 * (100.0 * (double)letter / word) - 0.296 * (100.0 * (double)sentence / word) - 15.8;

// debugger
    int brad = (int) round(grade);
    //  printf("Letters: %lf\n Words: %i\n Sentences: %lf\n", (double)letter, word, (double)sentence);

// print result
    if (brad <= 1)
    {
        printf("Before Grade 1\n");
    }
    else if (brad < 16)
    {
        printf("Grade %d\n", brad);
    }
    else
    {
        printf("Grade 16+\n");
    }
}