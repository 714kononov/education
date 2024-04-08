#ifndef STACK_H
#define STACK_H

typedef enum {
    X_VALUE,
    VALUE,
    FUNCTION
} Type;

typedef struct{
    Type type;
    void* data;
    void* next;
} Node;

#endif
