#include "parse.h"

void input(char *string) {
    char sin[4] = {'s', 'i', 'n', '\0'};
    char cos[4] = {'c', 'o', 's', '\0'};
    char tan[4] = {'t', 'a', 'n', '\0'};
    char ctg[4] = {'c', 't', 'g', '\0'};
    char sqrt[5] = {'s', 'q', 'r', 't', '\0'};
    char ln[3] = {'l', 'n', '\0'};

    char num[10] = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0'};
    char symb[6] = {'+', '*', '/', '(', ')', '-'};

    int check = 0;
    int i = 0;
    while (string[i] != '\0') {
        if ((string[i] == cos[0] && string[i + 1] == cos[1] && string[i + 2] == cos[2]) ||
            (string[i] == sin[0] && string[i + 1] == sin[1] && string[i + 2] == sin[2]) ||
            (string[i] == tan[0] && string[i + 1] == tan[1] && string[i + 2] == tan[2]) ||
            (string[i] == ctg[0] && string[i + 1] == ctg[1] && string[i + 2] == ctg[2]) ||
            (string[i] == sqrt[0] && string[i + 1] == sqrt[1] && string[i + 2] == sqrt[2] && string[i + 3] == sqrt[3]) ||
            (string[i] == ln[0] && string[i + 1] == ln[1])) {
            i += 3; 
        }else if((int)string[i]> 48 && (int)string[i]<57)
        {
            i++;
        }
        else{
            check = 1; 
            break;
        }
    }
    return check;
}