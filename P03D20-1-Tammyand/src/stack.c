#include "stack.h"

#include <stdlib.h>

Node* init() {
    Node* node = (Node*)malloc(sizeof(Node));
    if (node != NULL) {
        node->next = NULL;
    }
    return node;
}


Node* push(void* data, Node* head, Type type) {
    Node* point = NULL;
    if (head != NULL) {
        point = init();
        point->type = type;
        point->next = head->next;
        head->next = point;
    }
    return point;
}

int pop(Node* head) {
    Node* prev = NULL;
    int data = 0;
    if (head != NULL && head->next != NULL) {
        prev = head->next;
        head->next = prev->next;
        data = prev->data;
        free(prev);
    }
    return data;
}

void destroy(Node* head) {
    Node* p = head;
    while (head != NULL) {
        p = head;
        head = head->next;
        free(p);
    }
}
