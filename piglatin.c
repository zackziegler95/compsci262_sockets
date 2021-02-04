// modified from https://stackoverflow.com/questions/37176442/translating-a-sentence-to-pig-latin-in-c
char* to_piglatin(char* input)
{
    int index = 0;
    char* output = {0};

    for (int i = 0, start = 0 , locateSpace = 0; input[i] != '\0'; i++, locateSpace++)
    {
        char temp = input[i];

        for (;input[i] != ' ' && input != '\0' && input[i + 1] != '\0';) {
            locateSpace++;
            i++;
        }

        for (; start < locateSpace ; start++ , index++) {
            strncat(output, input+start+1, 1);
        }
        
        strncat(output, &temp, 1);
        char* ay = "ay ";
        strncat(output, ay, 3);
        piglatin[index - 1] = temp; 
        piglatin[index] = 'a'; 
        piglatin[index + 1] = 'y';
        piglatin[index + 2] = ' ';

        index += 3;
        start = locateSpace + 1;
    }
    piglatin[index] = '\0';//close the end of string 
}

void piglatin (char *english)
{
    char piglatin[MAXC] = "";
    char *e = english, *p = piglatin;
    int c = 0, first = 1;

    /* for each char in english and len < MAXC - 2 */
    for (; *e && e - english + 2 < MAXC; e++) {
        if (('A' <= *e && *e < 'Z') || ('a' <= *e && *e < 'z')) {
            if (first == 1) {       /* if first char in word */
                c = *e, first = 0;  /* save, unset flag      */
                continue;           /* get next char         */
            }
            else 
                *p++ = *e;          /* save char in piglatin */
        }
        else if (*e == ' ') {       /* if space, add c+'ay ' */
            *p++ = c, *p++ = 'a', *p++ = 'y', *p++ = *e;
            first = 1;              /* reset first flag  */
        }
    }   /*  add c+'ay ' for last word and print both */
    *p++ = c, *p++ = 'a', *p++ = 'y', *p++ = *e, *p = 0;
    printf (" english  : %s\n piglatin : %s\n", english, piglatin);
}
