#include <iostream>

extern "C" int printOneOneZero(int param);

int main() {
//    std::cout << "Hello, World!" << std::endl;
//    std::cout << printOneOneZero() << std::endl;
//    return 1;
    char input[256];

    // 无限循环，直到接收到用户输入的终止命令
    while (1) {
        printf("请输入命令：");
        fgets(input, sizeof(input), stdin);

        // 如果用户输入的是终止命令，则退出循环
        if (strcmp(input, "quit\n") == 0) {
            break;
        }

        // 处理用户输入的命令
        std::cout << printOneOneZero(200) << std::endl;
    }

    printf("程序已退出\n");
    return 0;
}

int printOneOneZero(int param) {
    return 110;
}
