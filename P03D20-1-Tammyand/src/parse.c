#include "parse.h"


//int get_data(Node* data) {
//    char string[1000] ={0};
//    int error = 0;
//    error = input(string);
//    if(!error)error = validate(string);
//    if(!error)error = parse(data, string);
//    return error;
//}
//
//
//int valid(char* text) {
//    unsigned int brackets = 0;
//    int error = 0;
//    error = valid_first_char(*text);
//    while(*text) {
//        text++;
//    }
//    return error;
//}

int valid_first_char(char c) {
    int error = 0;
    error = (c >= '0' && c <= '9') ? 0 : 1 ;
    error |= (c == '+' || c == '-') ? 0 : 1;
    error |= (c == 's' || c == 'c' || c == 't'|| c == 'l' || c == '(') ? 0 : 1;
    return error;
}


int brackets(char *c) {
    int counter = 0;
    while(*c && counter >= 0) {
        if(*c == '(') {
            counter++;
        }
        if(*c == ')') {
            counter--;
        }
        c++;
    }
    return counter;
}


void space_remove(char *c) {
    unsigned int counter = 0;
    while(*c) {
        if(*c == ' ') counter++;
        else c++;
        *c = *(c + counter);
    }
}

