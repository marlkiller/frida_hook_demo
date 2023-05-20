## frida + python3 hook demo

doc : https://frida.re/docs/examples/macos/

### 0x0: 准备

写一段c程序, 写一个 printOneOneZero 函数, 返回 110,   
并且导出 extern "C"
编译 运行

### 0x1: 获取进程 ID

```shell
frida-ps | grep main  
11986  main
```

### 0x2: 找到要 hook 的函数 printOneOneZero

```shell

# 设备相关
# -D 连接到指定的设备，多个设备时使用。示例:frida-trace -D 555315d66cac2d5849408f53da9eea514a90547e -F
# -U 连接到USB设备，只有一个设备时使用。示例fria-trace -U -F
# -i 函数过滤
frida-trace -i printOneOneZero -p 11986
# -d, --decorate       将模块名称添加到生成的onEnter
frida-trace --decorate -i "*rintOne*" main

# 遍历所有 module : python3 enumerate_modules.py 
# 遍历所有 class : frida-trace -p 11986 -S ./enumerate_classes.js 
# Trace ObjC method calls 
frida-trace -m "-[NSView drawRect:]" Safari
frida-trace -m "-[NSObject leng*]" main

# Hook 某个动态库
frida-trace -I "libcommonCrypto*" main

```

### 0x3: 编写hook 脚本
```javascript

// 获取被hook的函数指针
var func_ptr = Module.findExportByName(null, 'printOneOneZero');

if (func_ptr !== null) {
    // hook函数
    Interceptor.attach(func_ptr, {
        // 函数入口
        onEnter: function (args) {
            if (args[0].isNull()) {
                console.log("[>>] onEnter args is null");
                return;
            }
            // send 给 python3 回掉信息
            send(args[0])
            console.log("\t[>>] Type of args value: " + typeof args);
            // var argStr = args[0].readUtf8String();
            var argTostring = args[0].toString();
            console.log("\t[>>] Original args Value: " + argTostring);

        },
        // 函数出口
        onLeave: function (retval) {
            send(retval)
            console.log("\t[<<] Type of return value: " + typeof retval);
            console.log("\t[<<] Original Return Value: " + retval);
            retval.replace(0);  //将返回值替换成0
            console.log("\t[<<] New Return Value: " + retval);
        },
    });
} else {
    console.log("[*] Function not found");
}
```
### 0x4: hook

- 基于 JS hook: 
```shell
frida-trace -p 11986 -S ./hook.js
```  
 
- 基于 python+js hook
```shell
python3 hook.py
```