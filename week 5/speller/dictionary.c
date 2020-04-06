// Implements a dictionary's functionality


#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

unsigned long words = 0;
// Number of buckets in hash table
const unsigned int N = 65536;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Converts string to its lowercase representation
    char copy[strlen(word) + 1];
    strcpy(copy, word);
    char *p = copy;
    for (; *p; ++p)
    {
        *p = tolower(*p);
    }
    unsigned long h = hash(copy);
    node *cursor = table[h];

    while (cursor != NULL)
    {
        if (strcmp(cursor->word, copy) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
//https://old.reddit.com/r/cs50/comments/1x6vc8/pset6_trie_vs_hashtable/cf9gxh1/
unsigned int hash(const char *word)
{ 
    // TODO
    unsigned int hash = 0;
    int n = strlen(word);
    for (int i = 0; i < n; i++)
    {
        hash = (hash << 2) ^ word[i];
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialising the array to NULL
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
    //opening the file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        return false;
    }
    char wordlen[LENGTH + 1];
    //scaning the current buffer
    while (fscanf(file, "%s", wordlen) != EOF)
    {
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
        {
            return false;
        } 
        //storing the word in the node 
        strcpy(new_node->word, wordlen);
        new_node->next = NULL;

        //some hash function which gives out value 
        unsigned long index = hash(wordlen);

        if (table[index] != NULL)
        {
            //the new node's next is pointing to the element node present in on the hash
            new_node->next = table[index];
        }
        //the new starting element on the hash table is the new node
        table[index] = new_node;
        words++;
    }
    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return words;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);

        }
    }
    return true;
}


