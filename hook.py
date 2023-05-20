import sys

import frida


# hook回调函数
def on_message(message, data):
    if message['type'] == 'send':
        print("[*] Hooked function:", message['payload'])
    else:
        print("[-] Error:", message['description'])


script_code = '''
// frida-trace -p 11986 -S ./hook.js

// 获取被hook的函数指针
var func_ptr = Module.findExportByName(null, 'printOneOneZero');

if (func_ptr !== null) {
    // hook函数
    Interceptor.attach(func_ptr, {
        onEnter: function (args) {
            
            if (args[0].isNull()) {
                console.log("[>>] onEnter args is null");
                return;
            }
            send(args[0])
            console.log("\t[>>] Type of args value: " + typeof args);
            // var argStr = args[0].readUtf8String();
            var argTostring = args[0].toString();
            console.log("\t[>>] Original args Value: " + argTostring);

        },
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
'''

# 加载JavaScript脚本
# with open('hook.js', 'r') as f:
#     script_code = f.read()

# 连接到目标进程,attach传入进程名称（字符串）或者进程号（整数）
session = frida.attach("main")
# 创建并注入JavaScript脚本
script = session.create_script(script_code)
script.on('message', on_message)
script.load()
sys.stdin.read()

# python3 hook.py
