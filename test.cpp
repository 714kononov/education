#include <iostream>
#include <fstream>
#include <string>

int main() {
    std::ifstream file("/Users/admin/Downloads/+C.cs");
    
    if (file.is_open()) {
        char c;
        while (file.get(c)) {
            std::cout << c;
        }
        file.close();
        std::cout << std::endl;
    } else {
        std::cerr << "Unable to open file" << std::endl;
    }
    
    return 0;
}
