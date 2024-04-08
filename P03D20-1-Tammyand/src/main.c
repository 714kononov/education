#include "stack.h"


int main() {
    Node* root = NULL;
    int error = 0;
    root = init_stack(&root);
    error = (root == NULL);
    if(!error) error = get_data(root);
    if(!error) output(root);
    if(error) output_error();
    destroy(root);
    return 0;
}

