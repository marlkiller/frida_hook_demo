#include <iostream>
#include <unistd.h>

extern "C" int printOneOneZero(int param);

int main() {
    // std::cout << "Hello, World!" << std::endl;
    // std::cout << printOneOneZero() << std::endl;
    // return 1;
    char input[256];

    // 无限循环，直到接收到用户输入的终止命令
    while (1) {
        // printf("请输入命令：");
        // fgets(input, sizeof(input), stdin);
        // // scanf("%s", input);
        //
        // if (strcmp(input, "quit\n") == 0) {
        //     break;
        // }
        sleep(2);
        printf("%s :%d\n","printOneOneZero",printOneOneZero(200));
    }

    printf("程序已退出\n");
    return 0;
}

int printOneOneZero(int param) {
    return 110;
}
